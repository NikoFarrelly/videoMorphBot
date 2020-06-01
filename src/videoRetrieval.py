import os
from pathlib import Path
import moviepy.editor as mpe 
import random

REL_VIDEO_PATH = Path("../Videos/")

def get_video_from_clip(video_path = REL_VIDEO_PATH):
	video_array = os.listdir(video_path)
	video_index = random.randint(0, len(video_array) - 1)
	path_to_video = str(video_path) + '/' + str(video_array[video_index])

	# create video object to grab stats
	video = mpe.VideoFileClip(path_to_video)

	# avoid intro & credits
	skip_start = 0;
	skip_end = 0;
	# video frame retrieval range
	video_start = int(video.start + skip_start)
	video_end = int(video.end - skip_end)

	# video no longer needed
	video.close()

	start_video = random.randrange(video_start, video_end)
	video_length = random.randrange(2, 6)

	return mpe.VideoFileClip(path_to_video).subclip(t_start=start_video, t_end=(start_video + video_length))