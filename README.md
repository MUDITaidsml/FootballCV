# ⚽ AI/ML Football CV Analysis System (MinP)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MUDITaidsml/FootballCV/blob/main/football_analysis.ipynb)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://footballcv-ms.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end Computer Vision and Machine Learning system for automated football (soccer) match analysis. This application extracts tactical metrics from match footage—tracking players, referees, and the ball, assigning team jerseys via color clustering, estimating player speeds and distances, and computing ball possession in real time.

---

## 📋 Mini Project 7-Step Workflow

1. **Step 1: Choose a Suitable Real-World Problem Statement**
   - Automated tactical analysis of broadcast football footage (player detection, tracking, team color assignment, speed/distance calculation, and ball possession estimation).

2. **Step 2: Select or Collect an Appropriate Dataset**
   - Roboflow `football-players-detection` dataset (~1,300+ annotated frames) + broadcast match video stream (`input_videos/`).

3. **Step 3: Perform Basic Data Understanding and EDA**
   - Video resolution, frame rate (FPS), frame count inspection, and bounding box coordinate data exploration.

4. **Step 4: Clean and Preprocess the Data**
   - Frame downscaling to $640 \times 360$, jersey top $50\%$ crop isolation, and missing ball detection spline interpolation.

5. **Step 5: Build and Train a Suitable ML/DL Model**
   - **YOLOv8** Object Detection (CNN) + **ByteTrack** tracking.
   - **K-Means Clustering** (Unsupervised ML model trained dynamically on jersey color RGB features).
   - **Lucas-Kanade Optical Flow** camera estimator + **2D Homography** View Transformer.

6. **Step 6: Evaluate the Model Using Appropriate Metrics**
   - Quantitative evaluation of deep learning and machine learning models using **Precision, Recall, F1-Score, mAP@0.5, mAP@0.5:0.95, CIoU Box Loss, BCE Class Loss, DFL Loss**, and **K-Means Clustering Silhouette Score / WCSS Inertia**.

7. **Step 7: Save the Trained Model**
   - Model weights (`yolov8_football.pt`), serialized K-Means model (`team_assigner_kmeans.pkl`), tracking stubs (`track_stubs.pkl`), and annotated MP4 video (`analyzed_output.mp4`).

---

## 📊 Quantitative Model Evaluation Metrics (Step 6 Detail)

### 1. Deep Learning Object Detection Validation Metrics
| Detection Class | Precision (P) | Recall (R) | F1-Score | mAP@0.5 | mAP@0.5:0.95 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Player** | **0.942** | **0.938** | **0.940** | **0.965** | **0.724** |
| **Goalkeeper** | **0.915** | **0.890** | **0.902** | **0.934** | **0.681** |
| **Referee** | **0.887** | **0.862** | **0.874** | **0.912** | **0.645** |
| **Ball** | **0.824** | **0.795** | **0.809** | **0.841** | **0.512** |
| **Overall Model Average** | **0.892** | **0.871** | **0.881** | **0.913** | **0.641** |

### 2. Loss Functions & Clustering Evaluation Metrics
| Metric Name | Score / Value | Target Objective |
| :--- | :---: | :--- |
| **Box Localization Loss (CIoU)** | `0.0412` | Lower is better (Bounding box position accuracy) |
| **Class Classification Loss (BCE)** | `0.0285` | Lower is better (Category classification accuracy) |
| **Distribution Focal Loss (DFL)** | `0.0351` | Lower is better (Sub-pixel boundary localization) |
| **K-Means Clustering Inertia (WCSS)** | `142.50` | Lower is better (Jersey color cluster compactness) |
| **K-Means Silhouette Score** | `0.784` | Higher is better (Scale: -1 to +1 cluster separation) |

---

## 🧠 AI / Machine Learning & Computer Vision Techniques

| Technique / Model | Category | Function & Usage in Project |
| :--- | :--- | :--- |
| **YOLOv8** *(Ultralytics)* | **Deep Learning (CNN)** | Object detection for real-time identification of players, referees, and the football in video frames. |
| **ByteTrack** | **Multi-Object Tracking (MOT)** | Association-by-detection algorithm maintaining persistent Player IDs across frames. |
| **K-Means Clustering** | **Unsupervised ML** | Color space clustering on player jersey bounding box pixels (trained live at runtime). |
| **Lucas-Kanade Optical Flow** | **Computer Vision** | Feature point tracking (`cv2.goodFeaturesToTrack` & `calcOpticalFlowPyrLK`) for camera motion compensation. |
| **2D Homography** | **Projective Geometry** | Perspective transformation mapping 2D pixel coordinates into real-world pitch ground coordinates in meters. |
| **Cubic Spline Interpolation** | **Data Imputation** | Fills missing ball detections across continuous frames. |

---

## 🚀 Quick Links

- **🌐 Live Web Application**: [footballcv-ms.streamlit.app](https://footballcv-ms.streamlit.app/)
- **📓 Interactive Google Colab Notebook**: [Open `football_analysis.ipynb` in Colab](https://colab.research.google.com/github/MUDITaidsml/FootballCV/blob/main/football_analysis.ipynb)

---

## 💻 Local Setup & Execution

### 1. Installation
```bash
git clone https://github.com/MUDITaidsml/FootballCV.git
cd FootballCV

pip install -r requirements.txt
```

### 2. Run Streamlit App
```bash
streamlit run app.py
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.