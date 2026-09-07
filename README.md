# AI/ML Football Analysis Project

This project builds an end-to-end AI/ML Football Analysis system. Using advanced computer vision techniques (YOLOv8, Optical Flow, K-Means clustering, and Perspective Transformation), this system tracks players, referees, and the ball, assigns players to teams based on jersey colors, and estimates player speed and distance covered.

## Deliverables

1. **Jupyter Notebook (`football_analysis.ipynb`)**: Contains the step-by-step EDA, training steps, and inference code for the ML models.
2. **Streamlit Web Application (`app.py`)**: A web app for users to upload video clips and run the analysis pipeline directly from their browser.
3. **Source Code**: Python modules containing trackers, camera estimators, and speed estimators.

## Getting Started

### Local Setup
1. Clone this repository.
2. Ensure you have Python 3.8+ installed.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. To run the Streamlit App:
   ```bash
   streamlit run app.py
   ```

### Notebook Usage
Open `football_analysis.ipynb` in Jupyter Notebook or VSCode. Make sure to download a sample football video clip and place it in the `input_videos/` directory before running the cells.

## Deployment on Streamlit Community Cloud
1. Push this repository to your GitHub account.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click "New app" and authorize your GitHub account.
4. Select the repository, set the main file path to `app.py`, and click "Deploy".

## Model Weights
For optimal performance, place your fine-tuned YOLOv8 weights (e.g., `best.pt`) in the `models/` directory. If missing, the app will fallback to the standard `yolov8x.pt` model which is downloaded automatically on the first run.