from ultralytics import YOLO
import supervision as sv
import pickle
import os
import numpy as np
import pandas as pd
import cv2
import sys 
sys.path.append('../')
from utils import get_center_of_bbox, get_bbox_width, get_foot_position

class Tracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path) 
        self.tracker = sv.ByteTrack()

    def add_position_to_tracks(sekf,tracks):
        for object, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    bbox = track_info['bbox']
                    if object == 'ball':
                        position= get_center_of_bbox(bbox)
                    else:
                        position = get_foot_position(bbox)
                    tracks[object][frame_num][track_id]['position'] = position

    def interpolate_ball_positions(self,ball_positions):
        ball_positions = [x.get(1,{}).get('bbox',[]) for x in ball_positions]
        df_ball_positions = pd.DataFrame(ball_positions,columns=['x1','y1','x2','y2'])

        # Interpolate missing values
        df_ball_positions = df_ball_positions.interpolate()
        df_ball_positions = df_ball_positions.bfill()

        ball_positions = [{1: {"bbox":x}} for x in df_ball_positions.to_numpy().tolist()]

        return ball_positions

    def detect_frames(self, frames):
        batch_size=20 
        detections = [] 
        for i in range(0,len(frames),batch_size):
            detections_batch = self.model.predict(frames[i:i+batch_size],conf=0.01)
            detections += detections_batch
        return detections

    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            with open(stub_path,'rb') as f:
                tracks = pickle.load(f)
            return tracks

        detections = self.detect_frames(frames)

        tracks={
            "players":[],
            "referees":[],
            "ball":[]
        }

        for frame_num, detection in enumerate(detections):
            cls_names = detection.names
            cls_names_inv = {v:k for k,v in cls_names.items()}

            # Covert to supervision Detection format
            detection_supervision = sv.Detections.from_ultralytics(detection)

            # Convert GoalKeeper to player object
            for object_ind, class_id in enumerate(detection_supervision.class_id):
                if cls_names[class_id] == "goalkeeper":
                    # Safely replace goalkeeper with player if player class exists
                    player_cls_id = cls_names_inv.get('player')
                    if player_cls_id is not None:
                        detection_supervision.class_id[object_ind] = player_cls_id

            # Track Objects
            detection_with_tracks = self.tracker.update_with_detections(detection_supervision)

            tracks["players"].append({})
            tracks["referees"].append({})
            tracks["ball"].append({})

            for frame_detection in detection_with_tracks:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]
                track_id = frame_detection[4]

                # Safely handle player class; fall back to 'person' for standard COCO YOLO models
                player_cls_id = cls_names_inv.get('player')
                if player_cls_id is None:
                    player_cls_id = cls_names_inv.get('person')
                if player_cls_id is not None and cls_id == player_cls_id:
                    tracks["players"][frame_num][track_id] = {"bbox":bbox}
                
                # Safely handle referee class; some models may not have a 'referee' class name
                referee_cls_id = cls_names_inv.get('referee')
                if referee_cls_id is not None and cls_id == referee_cls_id:
                    tracks["referees"][frame_num][track_id] = {"bbox":bbox}
            
            for frame_detection in detection_supervision:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]

                # Detect ball by class name containing "ball" (covers variations like "sports ball", "ball", etc.)
                class_name = cls_names.get(cls_id, "").lower()
                if "ball" in class_name:
                    tracks["ball"][frame_num][1] = {"bbox": bbox}
                else:
                    # Preserve previous ball detection fallback (if any)
                    ball_cls_id = cls_names_inv.get('ball')
                    if ball_cls_id is None:
                        ball_cls_id = cls_names_inv.get('sports ball')
                    if ball_cls_id is not None and cls_id == ball_cls_id:
                        tracks["ball"][frame_num][1] = {"bbox": bbox}

        if stub_path is not None:
            with open(stub_path,'wb') as f:
                pickle.dump(tracks,f)

        return tracks
    
    def draw_ellipse(self,frame,bbox,color,track_id=None):
        y2 = int(bbox[3])
        x_center, _ = get_center_of_bbox(bbox)
        width = get_bbox_width(bbox)

        cv2.ellipse(
            frame,
            center=(x_center,y2),
            axes=(int(width), int(0.35*width)),
            angle=0.0,
            startAngle=-45,
            endAngle=235,
            color = color,
            thickness=2,
            lineType=cv2.LINE_4
        )

        rectangle_width = 40
        rectangle_height=20
        x1_rect = x_center - rectangle_width//2
        x2_rect = x_center + rectangle_width//2
        y1_rect = (y2- rectangle_height//2) +15
        y2_rect = (y2+ rectangle_height//2) +15

        if track_id is not None:
            cv2.rectangle(frame,
                          (int(x1_rect),int(y1_rect) ),
                          (int(x2_rect),int(y2_rect)),
                          color,
                          cv2.FILLED)
            
            x1_text = x1_rect+12
            if track_id > 99:
                x1_text -=10
            
            cv2.putText(
                frame,
                f"{track_id}",
                (int(x1_text),int(y1_rect+15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,0,0),
                2
            )

        return frame

    def draw_traingle(self,frame,bbox,color):
        y= int(bbox[1])
        x,_ = get_center_of_bbox(bbox)

        triangle_points = np.array([
            [x,y],
            [x-10,y-20],
            [x+10,y-20],
        ])
        cv2.drawContours(frame, [triangle_points],0,color, cv2.FILLED)
        cv2.drawContours(frame, [triangle_points],0,(0,0,0), 2)

        return frame

    def draw_team_ball_control(self,frame,frame_num,team_ball_control):
        # Draw a semi-transparent rectangle — position relative to frame size
        h, w = frame.shape[:2]
        overlay = frame.copy()

        # Scale font and padding relative to frame width (reference: 1920px)
        scale = w / 1920.0
        font_scale = max(0.35, 0.9 * scale)
        thickness = max(1, int(2.5 * scale))
        pad = int(10 * scale)
        line_h = int(35 * scale)
        box_w = int(480 * scale)
        box_h = int(line_h * 2 + pad * 3)

        x1 = w - box_w - pad
        y1 = h - box_h - pad
        x2 = w - pad
        y2 = h - pad

        cv2.rectangle(overlay, (x1, y1), (x2, y2), (255,255,255), -1)
        alpha = 0.4
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        team_ball_control_till_frame = team_ball_control[:frame_num+1]
        # Get the number of time each team had ball control
        team_1_num_frames = team_ball_control_till_frame[team_ball_control_till_frame==1].shape[0]
        team_2_num_frames = team_ball_control_till_frame[team_ball_control_till_frame==2].shape[0]
        total = team_1_num_frames + team_2_num_frames
        if total == 0:
            team_1, team_2 = 0.5, 0.5
        else:
            team_1 = team_1_num_frames / total
            team_2 = team_2_num_frames / total

        text_x = x1 + pad
        cv2.putText(frame, f"Team 1 Ball Control: {team_1*100:.2f}%",
                    (text_x, y1 + pad + line_h), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0), thickness)
        cv2.putText(frame, f"Team 2 Ball Control: {team_2*100:.2f}%",
                    (text_x, y1 + pad * 2 + line_h * 2), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0), thickness)

        return frame

    def draw_annotations(self,video_frames, tracks,team_ball_control):
        # Identify top 22 most persistent player IDs (max 22 players on pitch)
        player_counts = {}
        for f_dict in tracks.get('players', []):
            for pid in f_dict.keys():
                player_counts[pid] = player_counts.get(pid, 0) + 1
        
        top_player_ids = set(
            pid for pid, _ in sorted(player_counts.items(), key=lambda x: x[1], reverse=True)[:22]
        )

        output_video_frames= []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            # Safely retrieve dictionaries for the current frame, handling missing keys or out-of-range indices
            players_list = tracks.get('players', [])
            ball_list = tracks.get('ball', [])
            referees_list = tracks.get('referees', [])
            player_dict = players_list[frame_num] if frame_num < len(players_list) else {}
            ball_dict = ball_list[frame_num] if frame_num < len(ball_list) else {}
            referee_dict = referees_list[frame_num] if frame_num < len(referees_list) else {}

            # Draw Players (only top 22 pitch players)
            for track_id, player in player_dict.items():
                if track_id not in top_player_ids:
                    continue
                color = player.get("team_color",(0,0,255))
                frame = self.draw_ellipse(frame, player["bbox"],color, track_id)

                if player.get('has_ball',False):
                    frame = self.draw_traingle(frame, player["bbox"],(0,0,255))

            # Draw Referee
            for _, referee in referee_dict.items():
                frame = self.draw_ellipse(frame, referee["bbox"],(0,255,255))
            
            # Draw ball 
            for track_id, ball in ball_dict.items():
                frame = self.draw_traingle(frame, ball["bbox"],(0,255,0))


            # Draw Team Ball Control
            frame = self.draw_team_ball_control(frame, frame_num, team_ball_control)

            output_video_frames.append(frame)

        return output_video_frames