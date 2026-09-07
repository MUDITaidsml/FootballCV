"""
Test script — exercises the exact same pipeline as app.py
but from the command line (no Streamlit needed).
"""
import cv2
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trackers import Tracker
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistance_Estimator
from utils.video_utils import downscale_frame, should_process_frame, save_video_mp4

if len(sys.argv) > 1:
    VIDEO_PATH = sys.argv[1]
else:
    VIDEO_PATH = os.path.join("input_videos", "12819155_640_360_30fps.mp4")
MODEL = "yolov8x.pt"
WIDTH, HEIGHT = 640, 360
MAX_FRAMES = 40       # Fast end-to-end verification
SKIP_INTERVAL = 1      # Process every frame

def main():
    t0 = time.time()

    # ── Step 1: Read frames ──────────────────────────────
    print(f"[1/9] Reading video: {VIDEO_PATH}")
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("ERROR: Cannot open video file")
        return
    frames = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            break
        if should_process_frame(idx, SKIP_INTERVAL):
            frames.append(downscale_frame(frame, WIDTH, HEIGHT))
        del frame
        idx += 1
        if len(frames) >= MAX_FRAMES:
            break
    cap.release()
    print(f"      Read {len(frames)} frames in {time.time()-t0:.1f}s")

    if not frames:
        print("ERROR: No frames read")
        return

    # ── Step 2: Detection & Tracking ─────────────────────
    print("[2/9] Running YOLO detection + ByteTrack …")
    tracker = Tracker(MODEL)
    print(f"      Model classes: {tracker.model.names}")
    tracks = tracker.get_object_tracks(frames, read_from_stub=False, stub_path=None)

    ball_det = sum(1 for f in tracks.get('ball', []) if f)
    player_det = sum(1 for f in tracks.get('players', []) if f)
    ref_det = sum(1 for f in tracks.get('referees', []) if f)
    n = len(frames)
    print(f"      Players in {player_det}/{n} frames, ball in {ball_det}/{n}, referees in {ref_det}/{n}")

    # ── Step 3: Camera Movement ──────────────────────────
    print("[3/9] Estimating camera movement …")
    cam_est = CameraMovementEstimator(frames[0])
    cam_movement = cam_est.get_camera_movement(frames, read_from_stub=False, stub_path=None)
    print(f"      Done ({len(cam_movement)} entries)")

    # ── Step 4: Positions ────────────────────────────────
    print("[4/9] Computing positions …")
    tracker.add_position_to_tracks(tracks)
    cam_est.add_adjust_positions_to_tracks(tracks, cam_movement)
    vt = ViewTransformer()
    vt.add_transformed_position_to_tracks(tracks)
    print("      Done")

    # ── Step 5: Ball Interpolation ───────────────────────
    print("[5/9] Interpolating ball …")
    if tracks.get('ball') and any(tracks['ball']):
        try:
            tracks['ball'] = tracker.interpolate_ball_positions(tracks['ball'])
            print("      Interpolated OK")
        except Exception as e:
            print(f"      WARNING: {e}")
    else:
        print("      No ball detections — skipped")

    # ── Step 6: Speed & Distance ─────────────────────────
    print("[6/9] Speed & distance …")
    sde = SpeedAndDistance_Estimator()
    sde.add_speed_and_distance_to_tracks(tracks)
    print("      Done")

    # ── Step 7: Team Assignment ──────────────────────────
    print("[7/9] Team assignment …")
    ta = TeamAssigner()
    if tracks.get('players') and tracks['players'][0]:
        ta.assign_team_color(frames[0], tracks['players'][0])
    for fnum, pt in enumerate(tracks.get('players', [])):
        for pid, t in pt.items():
            team = ta.get_player_team(frames[fnum], t['bbox'], pid)
            tracks['players'][fnum][pid]['team'] = team
            tracks['players'][fnum][pid]['team_color'] = ta.team_colors[team]
    print("      Done")

    # ── Step 8: Ball Possession ──────────────────────────
    print("[8/9] Ball possession …")
    pba = PlayerBallAssigner()
    tbc = []
    pf = tracks.get('players', [])
    bf = tracks.get('ball', [])
    for fnum, pt in enumerate(pf):
        be = bf[fnum] if fnum < len(bf) else {}
        bb = be.get(1, {}).get('bbox')
        if bb is None:
            tbc.append(tbc[-1] if tbc else 1)
            continue
        ap = pba.assign_ball_to_player(pt, bb)
        if ap != -1 and ap in pt:
            tracks['players'][fnum][ap]['has_ball'] = True
            tbc.append(tracks['players'][fnum][ap].get('team', 1))
        else:
            tbc.append(tbc[-1] if tbc else 1)
    tbc = np.array(tbc)
    t1 = int((tbc == 1).sum())
    t2 = int((tbc == 2).sum())
    total = t1 + t2
    if total:
        print(f"      Team 1: {t1/total*100:.1f}%  |  Team 2: {t2/total*100:.1f}%")
    else:
        print("      No possession data")

    # ── Step 9: Draw & Save ──────────────────────────────
    print("[9/9] Drawing annotations & saving MP4 …")
    out_frames = tracker.draw_annotations(frames, tracks, tbc)
    out_frames = cam_est.draw_camera_movement(out_frames, cam_movement)
    sde.draw_speed_and_distance(out_frames, tracks)

    os.makedirs("output_videos", exist_ok=True)
    out_path = os.path.join("output_videos", "test_output.mp4")
    save_video_mp4(out_frames, out_path)

    fsize = os.path.getsize(out_path) / (1024*1024)
    elapsed = time.time() - t0
    print(f"\n{'='*50}")
    print(f"  DONE in {elapsed:.1f}s")
    print(f"  Output: {out_path} ({fsize:.1f} MB)")
    print(f"  Frames: {len(out_frames)}")
    print(f"  Resolution: {out_frames[0].shape[1]}x{out_frames[0].shape[0]}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
