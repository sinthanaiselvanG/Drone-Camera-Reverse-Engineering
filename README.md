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

# 🧠 How It Works

The drone camera transmits fragmented JPEG frames over UDP packets.

Using Wireshark, the communication packets were analyzed to identify:

- stream initialization commands
- camera switch commands
- packet structure
- frame identifiers
- payload format

The Python application:
1. Receives UDP packets
2. Orders fragmented frame chunks
3. Reconstructs complete image frames
4. Decodes JPEG images using OpenCV
5. Streams frames through Django

---

# 🔄 System Architecture

```text
Drone Camera
     ↓
UDP Packet Stream
     ↓
Packet Reverse Engineering
     ↓
Frame Chunk Ordering
     ↓
Frame Reconstruction
     ↓
OpenCV JPEG Decode
     ↓
Django Streaming Server
     ↓
Browser Live Feed
```

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

# 📡 Reverse Engineering Process

The drone camera was recovered from discarded hardware.

Using Wireshark, network traffic between the drone controller application and the camera was analyzed to identify proprietary control packets.

Important discoveries included:
- stream start command packets
- camera swap commands
- UDP packet format
- fragmented JPEG transmission structure
- frame chunk ordering logic

The camera transmitted image frames as multiple fragmented UDP chunks.

The application reconstructs the original frame by buffering and ordering packets using frame identifiers before decoding the final JPEG image.

Example discovered command packets:

```python
b'\x42\x76'   # Start stream
b'\x42\x79'   # Switch camera
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

# 🧩 Frame Reconstruction Logic

One of the important parts of this project is the frame reconstruction process.

The drone camera does not send a complete image in a single UDP packet.

Instead, each JPEG frame is fragmented into multiple smaller UDP chunks.

The application:
- receives fragmented UDP packets
- identifies frame IDs
- buffers payload chunks
- orders frame packets correctly
- reconstructs the original JPEG frame
- decodes the final image using OpenCV

This process enables stable real-time streaming despite fragmented packet transmission.

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
