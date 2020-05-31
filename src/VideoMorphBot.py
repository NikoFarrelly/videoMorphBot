import os
import random
from pathlib import Path
import json
from videoEffects import apply_video_effect
import moviepy.editor as mpe 
from twitterHandler import update_status_with_video

REL_VIDEO_PATH = Path("../Videos/")
OUTPUT_VIDEO_RESOLUTION = (1280,720)

def get_video_from_clip(video_path):
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


def add_video_effects(video_clips, num_of_vfx): 
	count = 0
	while count != num_of_vfx:
		# grab part of video
		random_start = random.randint(0, int(video_clips.end))
		random_end = random.randint(random_start, int(video_clips.end))

		video_clip = video_clips.subclip(t_start=random_start, t_end=random_end)
		# apply effect to video
		modified_clip = apply_video_effect(video_clip)
		# re-create the video
		video_clips = mpe.concatenate_videoclips(
			[
				video_clips.subclip(t_start=video_clips.start, t_end=random_start),
				modified_clip, video_clips.subclip(t_start=random_end, t_end=video_clips.end)
			],
			method="compose"
		)

		count += 1
	return video_clips


# def add_audio_effects(videoClips, index, numOfEffects):
# 	count = 0
# 	while count != numOfEffects:
# 		# grab part of video
# 		randomStart = random.randint(0, int(videoClips.end))
# 		randomEnd = random.randint(randomStart, int(videoClips.end))
# 		videoClip = videoClips.subclip(t_start=randomStart, t_end=randomEnd)
# 		# apply effect to video
# 		modifiedClip = applyAudioEffect(videoClip)
# 		# re-create the video
# 		videoClips = mpe.concatenate_videoclips([videoClips.subclip(t_start=videoClips.start, t_end=randomStart), modifiedClip, videoClips.subclip(t_start=randomEnd, t_end=videoClips.end)], method="compose")
# 		count += 1

# 	return videoClips


def create_random_video(num_clips_to_get):
	count = 0
	videos = []
	while count != num_clips_to_get:
		videos.append(get_video_from_clip(REL_VIDEO_PATH).resize(OUTPUT_VIDEO_RESOLUTION))
		count += 1
	video_clips = mpe.concatenate_videoclips(videos, method="compose")
	video_clips.write_videofile("videoMash.mp4", threads=100, audio_codec="aac")

	# audio effects should rarely be added
	# checkadd_audio_effects = getRandomNumber(10)
	# if (checkadd_audio_effects > 8):
	# 	numOfAudioEffects = videoClips.end // 5
	# 	if (numOfAudioEffects == 0):
	# 		numOfAudioEffects = 1
	# 	videoClips = add_audio_effects(videoClips, index, numOfAudioEffects)

	num_of_vfx = video_clips.end // 3
	video = add_video_effects(video_clips, num_of_vfx)
	
	video_name = "videoMashed.mp4"
	video.write_videofile(video_name, threads=1000, audio_codec="aac")
	video.close()
	return video_name

def post_to_twitter(tweet, filename):
	update_status_with_video(tweet, filename)


filename = create_random_video(3)
tweet = ""
post_to_twitter(tweet, filename)
