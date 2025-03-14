import subprocess
import cv2

def open_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video file: {video_path}")
    return cap

def get_frame_size(cap):
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return frame_width, frame_height

def get_fps(cap):
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    return fps

def get_frame_count(cap):
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return frame_count

def get_video_writer(output_video_path, fps, frame_width, frame_height, codec="HFYU"):
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
    return out
    
def convert_to_mp4(input_path, output_path):
    try:
        command = [
            'ffmpeg',
            '-y',
            '-i', input_path,
            '-c:v', 'libx264',
            '-crf', '23',
            '-preset', 'medium',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-strict', 'experimental',
            output_path
        ]
        subprocess.run(command, check=True)
        print(f"Video converted successfully: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting video: {e}")
        raise