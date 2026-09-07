# ⚽ AI/ML Football CV Analysis System

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MUDITaidsml/FootballCV/blob/main/football_analysis.ipynb)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://footballcv-ms.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end Computer Vision and Machine Learning system for automated football (soccer) match analysis. This application extracts tactical metrics from match footage—tracking players, referees, and the ball, assigning team jerseys via color clustering, estimating player speeds and distances, and computing ball possession in real time.

---

## 🧠 AI / Machine Learning & Computer Vision Techniques

| Technique / Model | Category | Function & Usage in Project |
| :--- | :--- | :--- |
| **YOLOv8** *(Ultralytics)* | **Deep Learning (CNN)** | Object detection for real-time identification of players, referees, and the football in video frames. Supports `yolov8n`, `yolov8s`, and `yolov8x`. |
| **ByteTrack** | **Multi-Object Tracking (MOT)** | Association-by-detection algorithm maintaining persistent Player IDs and tracking trajectories across frames through occlusions. |
| **K-Means Clustering** | **Unsupervised ML** | Color space clustering on player jersey bounding box pixels to automatically classify players into Team 1 vs. Team 2. |
| **Lucas-Kanade Optical Flow** | **Computer Vision** | Feature point tracking (`cv2.goodFeaturesToTrack` & `calcOpticalFlowPyrLK`) along pitch boundaries to measure camera panning and zooming offsets. |
| **2D Homography** | **Projective Geometry** | Perspective transformation mapping 2D pixel coordinates $(x, y)$ into real-world pitch ground coordinates in meters $(X, Y)$. |
| **Cubic Spline Interpolation** | **Data Imputation** | Fills missing ball detections caused by fast movement or player occlusions across continuous frames. |
| **Euclidean Proximity Analysis** | **Spatial Kinematics** | Measures foot-to-ball distance ($\sqrt{\Delta x^2 + \Delta y^2}$) to determine individual player possession and overall team control ratios. |
| **Kinematic Speed Estimation** | **Motion Metrics** | Computes frame-by-frame velocity in $\text{km/h}$ and total distance covered in meters based on transformed pitch coordinates and frame rates. |

---

## 🛠️ Software Stack & Technologies

- **Deep Learning Framework**: PyTorch, Ultralytics (`ultralytics`).
- **Computer Vision Libraries**: OpenCV (`opencv-python-headless`), Supervision (`supervision`).
- **Machine Learning & Data Science**: Scikit-Learn (`scikit-learn`), NumPy (`numpy`), Pandas (`pandas`), SciPy (`scipy`).
- **Data Visualization**: Matplotlib (`matplotlib`).
- **Video & Media Processing**: ImageIO (`imageio`), ImageIO-FFmpeg (`imageio-ffmpeg`), OpenCV VideoWriter (H.264 MP4).
- **Web App Framework**: Streamlit (`streamlit`).
- **Environment & Hosting**: Python 3.10+, Streamlit Community Cloud, Google Colab (GPU), Git / GitHub.

---

## 🌟 Key Features

1. **🤖 Multi-Object Detection & Tracking**: Powered by **YOLOv8** and **ByteTrack** to persistently track players, referees, and the ball across frames.
2. **📷 Camera Movement Compensation**: Employs **Lucas-Kanade Optical Flow** to separate camera panning/zooming from true player movement on the pitch.
3. **📐 Perspective Transformation (Homography)**: Maps 2D pixel coordinates into real-world pitch ground coordinates (in meters) to compute accurate spatial metrics.
4. **👕 Automatic Team Assignment**: Uses **K-Means Clustering** on player jersey color histograms to classify players into distinct teams automatically.
5. **⚽ Ball Possession Analysis**: Dynamically calculates ball control using spatial proximity and nearest-player tracking algorithms.
6. **🏃 Speed & Distance Metrics**: Computes real-time player velocity ($\text{km/h}$) and total distance covered ($\text{meters}$) throughout the clip.
7. **🎨 Visual Annotations & Web Export**: Draws tactical overlays (player tactical circles, team colors, possession bars, speed tags) and exports web-compatible **H.264 MP4** video.

---

## 🚀 Quick Links

- **🌐 Live Web Application**: [footballcv-ms.streamlit.app](https://footballcv-ms.streamlit.app/)
- **📓 Interactive Google Colab Notebook**: [Open `football_analysis.ipynb` in Colab](https://colab.research.google.com/github/MUDITaidsml/FootballCV/blob/main/football_analysis.ipynb)

---

## 📁 Repository Structure

```text
FootballCV/
├── app.py                         # Streamlit web application dashboard
├── football_analysis.ipynb        # Comprehensive Google Colab notebook
├── packages.txt                   # Linux system dependencies for Streamlit Cloud
├── requirements.txt               # Python package dependencies
├── camera_movement_estimator/     # Lucas-Kanade optical flow camera tracker
├── player_ball_assigner/          # Ball-to-player possession assigner
├── speed_and_distance_estimator/  # Player speed (km/h) & distance (m) estimator
├── team_assigner/                 # K-Means jersey color clustering module
├── trackers/                      # YOLOv8 + ByteTrack object tracking module
├── utils/                         # Video I/O, downscaling, & geometry utilities
└── view_transformer/              # 2D Homography perspective transformer
```

---

## 💻 Local Setup & Execution

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/MUDITaidsml/FootballCV.git
cd FootballCV

pip install -r requirements.txt
```

### 3. Run Streamlit App
Launch the interactive web application locally:
```bash
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

---

## 📓 Running in Google Colab

You can run the full machine learning analysis pipeline in Google Colab with GPU acceleration:

1. Click the **[Open in Colab](https://colab.research.google.com/github/MUDITaidsml/FootballCV/blob/main/football_analysis.ipynb)** badge.
2. Select **Runtime > Change runtime type** and set the accelerator to **GPU**.
3. Run the notebook cells sequentially to execute tracking, camera estimation, team clustering, and export the annotated video.

---

## ☁️ Deployment on Streamlit Community Cloud

This project is optimized for deployment on Streamlit Community Cloud:

- **OS Packages (`packages.txt`)**: Pre-configured with OpenCV dependencies (`libgl1`, `libglib2.0-dev`, `libsm6`, `libice6`, `libxext6`, `libxrender1`).
- **Memory Optimized**: Uses mini-batch streaming predictions and in-place frame drawing to run seamlessly within 1GB RAM limits.
- **Auto Model Fetching**: Automatically downloads light YOLO weights (`yolov8n.pt`) on demand.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.