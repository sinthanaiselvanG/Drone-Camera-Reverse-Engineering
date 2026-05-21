import socket
import cv2
import numpy as np
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
import time
import os

CAMERA_IP = "192.168.4.153"
CAMERA_PORT = 8080

latest_status = {
    "connected": False,
    "message": "Not started"
}

streaming = False
recording = False
video_writer = None
latest_frame = None

camera_sock = None
socket_initialized = False


def init_socket():
    global camera_sock, socket_initialized

    if socket_initialized:
        return

    camera_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    camera_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8 * 1024 * 1024)
    camera_sock.bind(("0.0.0.0", 0))
    camera_sock.settimeout(2)

    print("STREAM PORT:", camera_sock.getsockname()[1])

    socket_initialized = True


def gen_frames():
    global latest_status, streaming, recording, video_writer, latest_frame, camera_sock

    init_socket()

    sock = camera_sock

    current_frame_id = None
    frame_buffer = bytearray()

    last_packet_time = time.time()

    while True:

        if not streaming:
            time.sleep(0.05)
            continue

        try:
            data, addr = sock.recvfrom(65535)

            if addr[0] != CAMERA_IP:
                continue

            latest_status["connected"] = True
            latest_status["message"] = "Receiving stream"
            last_packet_time = time.time()

            if len(data) < 8:
                continue

            frame_id = data[0]
            payload = data[8:]

            if current_frame_id is None:
                current_frame_id = frame_id

            # Encoder restart protection
            if frame_id < current_frame_id:
                frame_buffer = bytearray()

            if frame_id != current_frame_id:

                if len(frame_buffer) > 1000:

                    frame = cv2.imdecode(
                        np.frombuffer(frame_buffer, dtype=np.uint8),
                        cv2.IMREAD_COLOR
                    )

                    if frame is not None:

                        latest_frame = frame.copy()

                        if recording and video_writer:
                            video_writer.write(frame)

                        ret, jpeg = cv2.imencode('.jpg', frame)

                        if ret:
                            yield (
                                b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' +
                                jpeg.tobytes() +
                                b'\r\n\r\n'
                            )

                frame_buffer = bytearray()
                current_frame_id = frame_id

            frame_buffer.extend(payload)

        except socket.timeout:

            if time.time() - last_packet_time > 5:
                latest_status["connected"] = False
                latest_status["message"] = "Waiting for stream"

            continue

        except Exception as e:
            print("Stream error:", e)
            latest_status["connected"] = False
            latest_status["message"] = "Error receiving stream"
            time.sleep(0.1)


# ======================
# CONTROL FUNCTIONS
# ======================

def start_stream(request):
    global streaming

    init_socket()

    streaming = True

    camera_sock.sendto(b'\x42\x76', (CAMERA_IP, CAMERA_PORT))

    latest_status["message"] = "Streaming started"

    return JsonResponse({"status": "started"})


def stop_stream(request):
    global streaming, recording, video_writer

    streaming = False
    recording = False

    if video_writer:
        video_writer.release()
        video_writer = None

    latest_status["message"] = "Stream stopped"

    return JsonResponse({"status": "stopped"})


def capture_image(request):
    global latest_frame

    if latest_frame is None:
        return JsonResponse({"status": "error", "message": "No frame available"})

    os.makedirs("captures", exist_ok=True)

    filename = f"captures/image_{int(time.time())}.jpg"

    cv2.imwrite(filename, latest_frame)

    return JsonResponse({
        "status": "saved",
        "message": f"Saved: {filename}"
    })


def record_video(request):
    global recording, video_writer, latest_frame

    if latest_frame is None:
        return JsonResponse({"status": "error", "message": "No frame available"})

    if not recording:

        os.makedirs("recordings", exist_ok=True)

        h, w, _ = latest_frame.shape
        filename = f"recordings/video_{int(time.time())}.avi"

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (w, h))

        recording = True

        return JsonResponse({
            "status": "recording_started"
        })

    else:

        recording = False

        if video_writer:
            video_writer.release()
            video_writer = None

        return JsonResponse({
            "status": "recording_stopped"
        })


def video_feed(request):
    return StreamingHttpResponse(
        gen_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def switch_camera(request):
    global camera_sock

    if camera_sock is None:
        return JsonResponse({"status": "error", "message": "Stream not started"})

    try:
        print("SWITCH PORT:", camera_sock.getsockname()[1])

        camera_sock.sendto(b'\x42\x79', (CAMERA_IP, CAMERA_PORT))

        time.sleep(0.2)

        latest_status["message"] = "Camera switched"

    except Exception as e:
        print(e)
        return JsonResponse({"status": "error"})

    return JsonResponse({"status": "camera_switched"})


def index(request):
    return render(request, 'index.html')


def get_status(request):
    return JsonResponse(latest_status)