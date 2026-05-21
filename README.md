# 🚁 Reverse Engineered UDP Drone Camera Streaming System

A real-time video streaming system built by reverse engineering a discarded drone camera’s proprietary UDP communication protocol using Wireshark.

This project reconstructs fragmented UDP image packets, decodes live camera frames using OpenCV, and streams the feed through a Django web application.

The main objective of this project was to understand how embedded wireless video transmission works internally and reuse discarded hardware for learning and experimentation.

---

# 📌 Features

- Reverse engineered proprietary drone camera protocol
- UDP packet capture and frame reconstruction
- Fragmented frame joining and ordered packet assembly
- Real-time MJPEG browser streaming
- Camera switching support
- Live stream start/stop controls
- Image capture support
- Video recording support
- Browser-based dashboard using Django
- Low-cost wireless streaming experimentation
- E-waste hardware reuse
- Tested YOLO object detection using the live camera stream with a laptop as the main processing unit

---

# 🧠 Project Objective

The primary goal of this project was to understand how embedded wireless video transmission systems work internally.

Instead of using official SDKs or APIs, the communication protocol of a discarded drone camera was analyzed manually using packet inspection and reverse engineering techniques.

This project focuses on:
- UDP-based wireless communication
- proprietary protocol analysis
- fragmented frame reconstruction
- real-time browser streaming
- low-cost hardware experimentation

---

# 🔄 System Architecture

```text
Drone Camera
     ↓
UDP Packet Stream
     ↓
Packet Capture & Analysis
     ↓
Reverse Engineering
     ↓
Frame Chunk Ordering
     ↓
JPEG Frame Reconstruction
     ↓
OpenCV Decode
     ↓
Django Streaming Server
     ↓
Browser Live Feed
```

---

# 📡 Reverse Engineering Process

The drone camera was recovered from discarded hardware.

Using Wireshark, network traffic between the original drone application and the camera was analyzed to identify:

- stream initialization packets
- camera switch commands
- UDP packet structure
- frame identifiers
- payload positions
- fragmented image transmission behavior

Important discoveries included:
- proprietary command bytes
- packet ordering logic
- frame reconstruction patterns
- JPEG payload fragmentation

Example discovered command packets:

```python
b'\x42\x76'   # Start stream
b'\x42\x79'   # Switch camera
```

---

# 🧩 Frame Reconstruction Logic

One of the most important parts of this project is the frame reconstruction system.

The drone camera does not transmit a complete image in a single UDP packet.

Instead:
- each camera frame is divided into multiple smaller UDP chunks
- every packet contains:
  - frame identifier
  - payload data
  - packet metadata

The application continuously listens for incoming UDP packets and reconstructs the original image frame in real time.

---

# ⚙️ How Frame Formation Works

## Step 1 — Receive UDP Packet

The application listens for UDP packets from the camera:

```python
data, addr = sock.recvfrom(65535)
```

Each packet contains:
- frame metadata
- frame ID
- partial JPEG image data

---

## Step 2 — Extract Frame Identifier

The first byte is used as a frame identifier:

```python
frame_id = data[0]
```

This helps determine which packets belong to the same image frame.

---

## Step 3 — Extract JPEG Payload

The actual JPEG image chunk starts after packet headers:

```python
payload = data[8:]
```

The payload data is appended into a temporary frame buffer.

---

## Step 4 — Buffer Fragmented Chunks

Since a single image arrives as many UDP packets, all payload chunks are buffered together:

```python
frame_buffer.extend(payload)
```

This gradually reconstructs the original JPEG image data.

---

## Step 5 — Detect Frame Boundary

When a new frame ID appears:

```python
if frame_id != current_frame_id:
```

the application understands that:
- the previous image frame is complete
- a new image frame has started

---

## Step 6 — Reconstruct Complete JPEG Frame

The buffered payload is converted into a NumPy array:

```python
np.frombuffer(frame_buffer, dtype=np.uint8)
```

Then decoded using OpenCV:

```python
cv2.imdecode(..., cv2.IMREAD_COLOR)
```

This recreates the original camera frame.

---

## Step 7 — Stream to Browser

The decoded frame is:
- streamed through Django
- optionally recorded
- optionally saved as image

The stream is served as MJPEG for real-time browser viewing.

---

# 🧠 Why Frame Reconstruction Was Important

UDP is connectionless and does not guarantee:
- packet ordering
- packet delivery
- frame integrity

Because of this:
- packets may arrive fragmented
- frames may be incomplete
- ordering becomes important

The reconstruction logic ensures:
- correct frame assembly
- stable video streaming
- proper JPEG decoding
- smooth browser playback

This was one of the core technical challenges of the project.

---

# 🛠️ Technologies Used

- Python
- Django
- OpenCV
- Socket Programming
- UDP Networking
- Wireshark
- NumPy

---

# 📂 Project Structure

```text
Camera_udp_reverse_engineering/
│
├── camstream/
│   ├── stream/
│   │   ├── templates/
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── captures/
│   ├── recordings/
│   └── manage.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Installation & Django Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/sinthanaiselvanG/Drone-Camera-Reverse-Engineering.git
cd Drone-Camera-Reverse-Engineering
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv jango
```

Activate virtual environment:

```bash
.\jango\Scripts\activate
```

---

### Linux / Mac

```bash
python3 -m venv jango
source jango/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Verify Django Installation

```bash
python -m django --version
```

---

# ▶️ Running the Project

Move into Django project folder:

```bash
cd camstream
```

Start Django development server:

```bash
python manage.py runserver
```

Open browser:

```text
http://127.0.0.1:8000
```

---

# 📷 Features Available in Web Interface

- Start Live Stream
- Stop Stream
- Switch Camera
- Capture Images
- Record Video
- Live MJPEG Feed

---

# 🎯 Learning Outcomes

This project helped in understanding:

- UDP communication
- proprietary protocol analysis
- packet reconstruction
- fragmented frame assembly
- embedded streaming systems
- real-time video processing
- Django streaming responses
- socket programming
- reverse engineering workflows

---

# ♻️ Motivation

Instead of discarding damaged hardware, this project explores how low-cost embedded devices can be reused for research and experimentation.

The primary goal was educational:
- understanding wireless camera communication
- learning reverse engineering concepts
- experimenting with UDP-based video streaming

---

# 🚀 Future Improvements

- RTP stream decoding
- GStreamer integration
- Raspberry Pi deployment
- WebRTC streaming
- Latency optimization
- Multi-camera support
- Custom protocol documentation

---

# 📜 Disclaimer

This project was developed purely for educational and research purposes using personally owned discarded hardware.

No unauthorized access or exploitation of third-party systems was performed.

---

# 👨‍💻 Author

SINTHANAISELVAN G

Developed as a reverse engineering and networking learning project using discarded drone hardware and UDP-based wireless video streaming experimentation.
