import streamlit as st

st.set_page_config(
    page_title="AI Football Analysis",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS for modern dark UI ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global ─────────────────────────────────────────── */
html, body, .stApp {
    font-family: 'Inter', sans-serif;
}

/* Hide default Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ── Sidebar ────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1923 0%, #1a2736 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e2e8f0;
}
section[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
    font-weight: 500;
    font-size: 0.85rem;
    letter-spacing: 0.02em;
}

/* ── Hero Header ────────────────────────────────────── */
.hero-container {
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 40%, rgba(16,185,129,0.08) 0%, transparent 60%),
                radial-gradient(circle at 70% 80%, rgba(59,130,246,0.06) 0%, transparent 50%);
    animation: shimmer 8s ease-in-out infinite alternate;
}
@keyframes shimmer {
    0% { transform: translate(0, 0); }
    100% { transform: translate(-5%, 5%); }
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #10b981, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem 0;
    position: relative;
    z-index: 1;
}
.hero-subtitle {
    color: #94a3b8;
    font-size: 1.05rem;
    font-weight: 400;
    line-height: 1.5;
    position: relative;
    z-index: 1;
}

/* ── Glass Card ─────────────────────────────────────── */
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.15);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
    border-color: rgba(16,185,129,0.2);
    box-shadow: 0 8px 32px rgba(16,185,129,0.08);
}
.glass-card h3 {
    margin: 0 0 0.8rem 0;
    color: #e2e8f0;
    font-weight: 600;
    font-size: 1.1rem;
}

/* ── Metric Cards ───────────────────────────────────── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}
.metric-card {
    background: linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(59,130,246,0.06) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #10b981, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
}
.metric-label {
    color: #94a3b8;
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Pipeline Step Badges ───────────────────────────── */
.step-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 8px;
    padding: 0.3rem 0.8rem;
    color: #10b981;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 0.15rem;
}

/* ── Upload Area ────────────────────────────────────── */
section[data-testid="stFileUploader"] {
    border-radius: 14px;
}
section[data-testid="stFileUploader"] > div {
    border-radius: 14px;
}

/* ── Tabs ────────────────────────────────────────────── */
button[data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
}

/* ── Streamlit button override ──────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.7rem 2rem;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: 0.02em;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px rgba(16,185,129,0.3);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    box-shadow: 0 6px 24px rgba(16,185,129,0.4);
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0);
}

/* ── Progress bar tint ──────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #10b981, #3b82f6);
}

/* ── Divider ────────────────────────────────────────── */
.section-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)

import cv2
import tempfile
import os
import sys
import time
import numpy as np

# Add the current directory to sys.path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ultralytics import YOLO
from trackers import Tracker
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistance_Estimator
from utils.video_utils import downscale_frame, should_process_frame, save_video_mp4

# ── Sidebar: Settings ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Analysis Settings")
    st.markdown("---")

    st.markdown("##### 🤖 Model")
    model_files = [f for f in os.listdir('.') if f.endswith('.pt')]
    if not model_files:
        st.error("No `.pt` model files found in project root.")
        st.stop()
    default_idx = model_files.index('yolov8x.pt') if 'yolov8x.pt' in model_files else 0
    selected_model = st.selectbox(
        "YOLO model weights",
        options=model_files,
        index=default_idx,
        help="Select the YOLO model file to use for detection."
    )

    st.markdown("---")
    st.markdown("##### 🖼️ Frame Processing")
    width = st.slider("Frame width (px)", 320, 1280, 640, 32,
                       help="Width to downscale each frame to before processing.")
    height = st.slider("Frame height (px)", 180, 720, 360, 18,
                        help="Height to downscale each frame to before processing.")
    max_frames = st.slider("Max frames to process", 10, 2000, 300, 10,
                            help="Maximum number of frames to read from the video.")
    skip_interval = st.slider("Process every Nth frame", 1, 5, 1,
                               help="Skip frames to speed up processing. 1 = every frame.")

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#64748b; font-size:0.75rem; margin-top:1rem;'>"
        "AI Football Analysis v2.0</div>",
        unsafe_allow_html=True
    )

# ── Cached tracker ───────────────────────────────────────────────────────────
@st.cache_resource
def get_tracker(model_name):
    return Tracker(model_name)

# ── Hero Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">⚽ AI Football Analysis</div>
    <div class="hero-subtitle">
        Upload a football match clip and let our ML pipeline track players, assign teams,
        estimate speed &amp; distance, and compute ball possession — all in real time.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Pipeline overview badges ─────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; flex-wrap:wrap; gap:0.3rem; margin-bottom:1.2rem;">
    <span class="step-badge">🔍 YOLO Detection</span>
    <span class="step-badge">📷 Camera Estimation</span>
    <span class="step-badge">👕 Team Assignment</span>
    <span class="step-badge">⚽ Ball Tracking</span>
    <span class="step-badge">🏃 Speed &amp; Distance</span>
    <span class="step-badge">🎯 Possession Analysis</span>
</div>
""", unsafe_allow_html=True)

# ── Upload Section ───────────────────────────────────────────────────────────
st.markdown('<div class="glass-card"><h3>📤 Upload Video</h3>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop a football match clip here",
    type=["mp4", "avi"],
    label_visibility="collapsed",
    help="Supported formats: MP4, AVI. Keep clips under 2 minutes for best performance."
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    tfile.flush()
    video_path = tfile.name

    # Preview in an expander
    with st.expander("🎬 Preview uploaded video", expanded=False):
        st.video(video_path)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # ── Analyze Button ───────────────────────────────────────────────────
    col_btn, col_spacer = st.columns([1, 3])
    with col_btn:
        analyze_clicked = st.button("🎯 Run Analysis", use_container_width=True)

    if analyze_clicked:
        # ── Progress container ───────────────────────────────────────
        status = st.empty()
        progress_bar = st.progress(0)

        try:
            # ── Step 1: Read & downscale frames ─────────────────────
            status.info("📹 **Step 1/9** — Reading and downscaling video frames…")
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                st.error("❌ Failed to open video file. The file may be corrupted or in an unsupported codec.")
                st.stop()

            original_fps = cap.get(cv2.CAP_PROP_FPS) or 24
            total_video_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
            processed_frames = []
            frame_idx = 0

            while True:
                ret, frame = cap.read()
                if not ret or frame is None:
                    break
                if should_process_frame(frame_idx, skip_interval):
                    resized = downscale_frame(frame, width, height)
                    processed_frames.append(resized)
                    pct = min(int(len(processed_frames) / max_frames * 100), 100)
                    progress_bar.progress(pct)
                del frame
                frame_idx += 1
                if len(processed_frames) >= max_frames:
                    break
            cap.release()

            if not processed_frames:
                st.error("❌ No frames could be read from the video. Try a different file or format.")
                st.stop()

            progress_bar.progress(100)
            status.success(f"✅ **Step 1/9** — Read {len(processed_frames)} frames successfully.")

            # ── Step 2: Object detection & tracking ─────────────────
            status.info("🔍 **Step 2/9** — Running YOLO object detection & ByteTrack tracking…")
            tracker = get_tracker(selected_model)
            tracks = tracker.get_object_tracks(
                processed_frames,
                read_from_stub=False,
                stub_path=None
            )

            # Count detections for stats
            ball_det_count = sum(1 for f in tracks.get('ball', []) if f)
            player_det_count = sum(1 for f in tracks.get('players', []) if f)
            referee_det_count = sum(1 for f in tracks.get('referees', []) if f)
            total_frames = len(processed_frames)
            status.success(f"✅ **Step 2/9** — Detection complete.")

            # ── Step 3: Camera movement estimation ──────────────────
            status.info("📷 **Step 3/9** — Estimating camera movement (optical flow)…")
            camera_estimator = CameraMovementEstimator(processed_frames[0])
            camera_movement_per_frame = camera_estimator.get_camera_movement(
                processed_frames,
                read_from_stub=False,
                stub_path=None
            )
            status.success("✅ **Step 3/9** — Camera movement estimated.")

            # ── Step 4: Positions ───────────────────────────────────
            status.info("📐 **Step 4/9** — Computing player positions…")
            tracker.add_position_to_tracks(tracks)
            camera_estimator.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)

            view_transformer = ViewTransformer()
            view_transformer.add_transformed_position_to_tracks(tracks)
            status.success("✅ **Step 4/9** — Positions computed.")

            # ── Step 5: Ball interpolation ──────────────────────────
            status.info("⚽ **Step 5/9** — Interpolating ball positions…")
            ball_interpolated = False
            if tracks.get('ball') and any(tracks['ball']):
                try:
                    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])
                    ball_interpolated = True
                except Exception as e:
                    st.warning(f"⚠️ Ball interpolation skipped: {e}")
            else:
                st.warning("⚠️ No ball detections found — ball interpolation skipped.")
            status.success("✅ **Step 5/9** — Ball positions processed.")

            # ── Step 6: Speed & distance ────────────────────────────
            status.info("🏃 **Step 6/9** — Computing player speed & distance…")
            speed_and_distance_estimator = SpeedAndDistance_Estimator()
            speed_and_distance_estimator.add_speed_and_distance_to_tracks(tracks)
            status.success("✅ **Step 6/9** — Speed & distance computed.")

            # ── Step 7: Team assignment ─────────────────────────────
            status.info("👕 **Step 7/9** — Assigning teams via jersey color clustering…")
            team_assigner = TeamAssigner()
            
            # Find the first frame with player detections to fit team colors
            first_p_frame = None
            for f_idx, p_dict in enumerate(tracks.get('players', [])):
                if len(p_dict) >= 2:
                    first_p_frame = (f_idx, p_dict)
                    break
            if first_p_frame is None and tracks.get('players'):
                for f_idx, p_dict in enumerate(tracks.get('players', [])):
                    if len(p_dict) > 0:
                        first_p_frame = (f_idx, p_dict)
                        break

            if first_p_frame is not None:
                f_idx, p_dict = first_p_frame
                team_assigner.assign_team_color(processed_frames[f_idx], p_dict)

            for frame_num, player_track in enumerate(tracks.get('players', [])):
                for player_id, track in player_track.items():
                    team = team_assigner.get_player_team(
                        processed_frames[frame_num], track['bbox'], player_id
                    )
                    tracks['players'][frame_num][player_id]['team'] = team
                    tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors.get(team, (0, 0, 255))
            status.success("✅ **Step 7/9** — Teams assigned.")

            # ── Step 8: Ball possession ─────────────────────────────
            status.info("🎯 **Step 8/9** — Computing ball possession…")
            player_assigner = PlayerBallAssigner()
            team_ball_control = []
            player_frames = tracks.get('players', [])
            ball_frames = tracks.get('ball', [])
            for frame_num, player_track in enumerate(player_frames):
                ball_entry = ball_frames[frame_num] if frame_num < len(ball_frames) else {}
                ball_bbox = ball_entry.get(1, {}).get('bbox')
                if ball_bbox is None:
                    team_ball_control.append(team_ball_control[-1] if team_ball_control else 1)
                    continue
                assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bbox)
                if assigned_player != -1 and assigned_player in player_track:
                    tracks['players'][frame_num][assigned_player]['has_ball'] = True
                    team_ball_control.append(
                        tracks['players'][frame_num][assigned_player].get('team', 1)
                    )
                else:
                    # Find closest player in this frame to determine possession team
                    closest_team = None
                    if player_track:
                        from utils import get_center_of_bbox, measure_distance
                        ball_pos = get_center_of_bbox(ball_bbox)
                        min_dist = 999999
                        for pid, p_info in player_track.items():
                            p_box = p_info.get('bbox')
                            if p_box:
                                p_pos = (p_box[0] + (p_box[2]-p_box[0])/2, p_box[3])
                                dist = measure_distance(p_pos, ball_pos)
                                if dist < min_dist:
                                    min_dist = dist
                                    closest_team = p_info.get('team', 1)
                    if closest_team is not None:
                        team_ball_control.append(closest_team)
                    else:
                        team_ball_control.append(team_ball_control[-1] if team_ball_control else 1)

            team_ball_control = np.array(team_ball_control)
            status.success("✅ **Step 8/9** — Possession computed.")

            # ── Step 9: Draw annotations & save ─────────────────────
            status.info("🎨 **Step 9/9** — Drawing annotations & saving output video…")
            output_video_frames = tracker.draw_annotations(
                processed_frames, tracks, team_ball_control
            )
            output_video_frames = camera_estimator.draw_camera_movement(
                output_video_frames, camera_movement_per_frame
            )
            speed_and_distance_estimator.draw_speed_and_distance(output_video_frames, tracks)

            output_path = os.path.join("output_videos", "analyzed_output.mp4")
            os.makedirs("output_videos", exist_ok=True)
            save_video_mp4(output_video_frames, output_path)

            progress_bar.progress(100)
            status.success("🎉 **Analysis Complete!** Scroll down for results.")

            # ── Compute stats for dashboard ─────────────────────────
            t1_ctrl = int((team_ball_control == 1).sum())
            t2_ctrl = int((team_ball_control == 2).sum())
            total_ctrl = t1_ctrl + t2_ctrl
            t1_pct = round(t1_ctrl / total_ctrl * 100, 1) if total_ctrl else 50.0
            t2_pct = round(t2_ctrl / total_ctrl * 100, 1) if total_ctrl else 50.0
            ball_det_pct = round(ball_det_count / total_frames * 100, 1) if total_frames else 0

            # Filter and rank player tracks to find primary pitch players (max 22 on field)
            player_counts = {}
            for frame_tracks in tracks.get('players', []):
                for pid in frame_tracks.keys():
                    player_counts[pid] = player_counts.get(pid, 0) + 1

            pitch_players = sorted(player_counts.items(), key=lambda x: x[1], reverse=True)[:22]
            num_pitch_players = len(pitch_players)

            # ══════════════════════════════════════════════════════════
            #  RESULTS DASHBOARD
            # ══════════════════════════════════════════════════════════
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown("""
            <div style="margin-bottom: 1rem;">
                <span style="font-size:1.4rem; font-weight:700; color:#e2e8f0;">📊 Results Dashboard</span>
            </div>
            """, unsafe_allow_html=True)

            # ── Metric Cards ────────────────────────────────────────
            st.markdown(f"""
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">{num_pitch_players}</div>
                    <div class="metric-label">Pitch Players (Max 22)</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{total_frames}</div>
                    <div class="metric-label">Frames Processed</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{ball_det_pct}%</div>
                    <div class="metric-label">Ball Detection Rate</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{t1_pct}%</div>
                    <div class="metric-label">Team 1 Possession</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{t2_pct}%</div>
                    <div class="metric-label">Team 2 Possession</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Tabbed Results ──────────────────────────────────────
            tab_video, tab_stats, tab_download = st.tabs([
                "🎬 Analyzed Video", "📈 Statistics", "💾 Download"
            ])

            with tab_video:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    st.video(output_path)
                else:
                    st.warning(
                        "⚠️ The output video file could not be created. "
                        "This usually means your OpenCV installation lacks MP4 codec support. "
                        "Try installing `ffmpeg` and rebuilding `opencv-python`."
                    )
                st.markdown('</div>', unsafe_allow_html=True)

            with tab_stats:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown('<div class="glass-card"><h3>⚽ Ball Possession</h3>', unsafe_allow_html=True)
                    import matplotlib.pyplot as plt
                    import matplotlib
                    matplotlib.use('Agg')

                    fig, ax = plt.subplots(figsize=(4, 4), facecolor='#0e1117')
                    colors = ['#10b981', '#3b82f6']
                    wedges, texts, autotexts = ax.pie(
                        [t1_pct, t2_pct],
                        labels=['Team 1', 'Team 2'],
                        autopct='%1.1f%%',
                        colors=colors,
                        startangle=90,
                        textprops={'color': '#e2e8f0', 'fontsize': 12, 'fontweight': 'bold'},
                        wedgeprops={'edgecolor': '#1e293b', 'linewidth': 2}
                    )
                    for at in autotexts:
                        at.set_color('#ffffff')
                        at.set_fontsize(13)
                        at.set_fontweight('bold')
                    ax.set_title('Ball Possession', color='#e2e8f0', fontsize=14, fontweight='bold', pad=15)
                    st.pyplot(fig)
                    plt.close(fig)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="glass-card"><h3>📋 Detection Summary</h3>', unsafe_allow_html=True)
                    st.markdown(f"""
                    | Metric | Value |
                    |--------|-------|
                    | **Pitch Players (Max 22)** | {num_pitch_players} |
                    | **Frames with Players** | {player_det_count} / {total_frames} |
                    | **Frames with Ball** | {ball_det_count} / {total_frames} |
                    | **Frames with Referees** | {referee_det_count} / {total_frames} |
                    | **Ball Interpolated** | {'✅ Yes' if ball_interpolated else '❌ No'} |
                    | **Input Resolution** | {width} × {height} |
                    | **Original FPS** | {original_fps:.1f} |
                    | **Skip Interval** | {skip_interval} |
                    """)
                    st.markdown('</div>', unsafe_allow_html=True)

            with tab_download:
                st.markdown('<div class="glass-card"><h3>💾 Download Results</h3>', unsafe_allow_html=True)
                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="⬇️  Download Analyzed Video (MP4)",
                            data=f,
                            file_name="football_analysis_output.mp4",
                            mime="video/mp4",
                            use_container_width=True,
                        )
                    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                    st.caption(f"File size: {file_size_mb:.1f} MB")
                else:
                    st.info("No output file available for download.")
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            import traceback
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.error(f"❌ **Analysis failed:** {e}")
            with st.expander("🔍 Show full error traceback", expanded=False):
                st.code(traceback.format_exc(), language="python")

else:
    # ── Empty state ──────────────────────────────────────────────────
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:3rem 2rem;">
        <div style="font-size:3rem; margin-bottom:0.8rem;">🎥</div>
        <h3 style="color:#e2e8f0; margin-bottom:0.5rem;">No video uploaded yet</h3>
        <p style="color:#64748b; font-size:0.95rem;">
            Upload a football match clip using the upload area above to get started.<br>
            The analysis pipeline will automatically detect players, track the ball,
            and compute team statistics.
        </p>
    </div>
    """, unsafe_allow_html=True)
