import moviepy.editor as mpe 
import moviepy.video.fx.all as vfx
import os
import random
import datetime
from pathlib import Path

import time

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
	videoLength = random.randrange(2, 8)

	return mpe.VideoFileClip(pathToVideo).subclip(t_start=startVideo, t_end=(startVideo + videoLength))


def speedEffectGenerate(video):
	return speedEffect(video, random.uniform(0.4, 1.3))

def speedEffect(video, speed):
	return video.fx(vfx.speedx, speed)

def playBackwardsEffect(video):
	return video.fx(vfx.time_mirror)

def flipClipHorizontallyEffect(video):
	return vfx.mirror_x(video)

def flipClipVerticallyEffect(video):
	return vfx.mirror_y(video)

def blackAndWhiteEffect(video):
	return vfx.blackwhite(video)

def contrastLuminosityGenerate(video):
	return contrastLuminosityEffect(video, getRandomNumber(200), getRandomNumber(30))

def contrastLuminosityEffect(video, luminosity, contrast):
	return vfx.lum_contrast(video, luminosity, contrast)

def gammaCorrectionGenerate(video):
	return gammaCorrectionEffect(video, random.randint(1, 6))

def gammaCorrectionEffect(video, correction):
	return vfx.gamma_corr(video, correction)

def fadeInGenerate(video):
	return fadeInEffect(video, random.randint(1, 2))

def fadeInEffect(video, duration):
	return vfx.fadein(video, duration)

def fadeOutGenerate(video):
	return fadeOutEffect(video, random.randint(1, 2))

def fadeOutEffect(video, duration):
	return vfx.fadeout(video, duration)

def applyVideoEffect(video):
	index = getRandomNumber(len(videoEffects)-1)
	return videoEffects[index](video)

def getRandomNumber(num):
	return random.randint(0, num)


videoEffects = [
				speedEffectGenerate, playBackwardsEffect, flipClipHorizontallyEffect,
 				flipClipVerticallyEffect,blackAndWhiteEffect, contrastLuminosityGenerate,
 				gammaCorrectionGenerate, fadeInGenerate, fadeOutGenerate
 			   ]

def createRandomVideo(amountOfClips, index):
	videoPath = Path("../Videos/")

	count = 0
	videos = []
	while count != amountOfClips:
		print('loop')
		videos.append(getVideoFromClip(videoPath))
		count += 1
	# Splice clips together
	videoClips = mpe.concatenate_videoclips(videos, method="compose")
	videoClips.write_videofile("videoMash" + str(index) + ".mp4", threads=100)


	# Add video effects 
	numOfEffects = videoClips.end
	count = 0
	while count != numOfEffects:
		# grab part of video
		randomStart = random.randint(0, int(videoClips.end))
		randomEnd = random.randint(randomStart, int(videoClips.end))
		print('loop2', randomStart, randomEnd)
		videoClip = videoClips.subclip(t_start=randomStart, t_end=randomEnd)
		# apply effect to video
		modifiedClip = applyVideoEffect(videoClip)
		# re-create the video
		videoClips = mpe.concatenate_videoclips([videoClips.subclip(t_start=videoClips.start, t_end=randomStart), modifiedClip, videoClips.subclip(t_start=randomEnd, t_end=videoClips.end)], method="compose")


		count += 1
	videoClips.write_videofile("videoMashed" + str(index) + ".mp4", threads=100)
	# videoClips.close()gi


count=0
createRandomVideo(1, count)

