import os
import random
from pathlib import Path
import json
from videoEffects import applyVideoEffect
import moviepy.editor as mpe 
from twitterHandler import update_status_with_video

CURRENT_DIR = os.path.dirname(__file__)
VIDEO_PATH = Path("../Videos/")

def getVideoFromClip(videoPath):
	videoArray = os.listdir(videoPath)
	videoIndex = random.randint(0, len(videoArray) - 1)
	pathToVideo = str(videoPath) + '/' + str(videoArray[videoIndex])

	# create video object to grab stats
	video = mpe.VideoFileClip(pathToVideo)

	# avoid intro & credits
	skipStart = 0;
	skipEnd = 0;
	# video frame retrieval range
	videoStart = int(video.start + skipStart)
	videoEnd = int(video.end - skipEnd)

	# video no longer needed
	video.close()

	startVideo = random.randrange(videoStart, videoEnd)
	videoLength = random.randrange(2, 6)

	return mpe.VideoFileClip(pathToVideo).subclip(t_start=startVideo, t_end=(startVideo + videoLength))


def addVideoEffects(videoClips, index, numOfEffects): 
	count = 0
	while count != numOfEffects:
		# grab part of video
		randomStart = random.randint(0, int(videoClips.end))
		randomEnd = random.randint(randomStart, int(videoClips.end))

		videoClip = videoClips.subclip(t_start=randomStart, t_end=randomEnd)
		# apply effect to video
		modifiedClip = applyVideoEffect(videoClip)
		# re-create the video
		videoClips = mpe.concatenate_videoclips([videoClips.subclip(t_start=videoClips.start, t_end=randomStart), modifiedClip, videoClips.subclip(t_start=randomEnd, t_end=videoClips.end)], method="compose")

		count += 1
	return videoClips


# def addAudioEffects(videoClips, index, numOfEffects):
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


def createRandomVideo(amountOfClips, index):
	count = 0
	videos = []
	while count != amountOfClips:
		videos.append(getVideoFromClip(VIDEO_PATH))
		count += 1
	# Splice clips together
	videoClips = mpe.concatenate_videoclips(videos, method="compose")
	videoClips.write_videofile("videoMash" + str(index) + ".mp4", threads=100, audio_codec="aac")

	# audio effects should rarely be added
	# checkAddAudioEffects = getRandomNumber(10)
	# if (checkAddAudioEffects > 8):
	# 	numOfAudioEffects = videoClips.end // 5
	# 	if (numOfAudioEffects == 0):
	# 		numOfAudioEffects = 1
	# 	videoClips = addAudioEffects(videoClips, index, numOfAudioEffects)

	numOfVideoEffects = videoClips.end // 3
	videoClips = addVideoEffects(videoClips, index, numOfVideoEffects)
	
	videoName = "videoMashed" + str(index) + ".mp4"
	videoClips.write_videofile(videoName, threads=1000)
	return videoClips

def postToTwitter(tweet, video):
	update_status_with_video(tweet, video)



count = 0
# while count != 10:
video = createRandomVideo(1, count)
tweet = "please work"

postToTwitter(tweet,video)
video.close()


