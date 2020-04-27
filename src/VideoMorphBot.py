import moviepy.editor as mpe 
import moviepy.video.fx.all as vfx
from moviepy.editor import * 
import os
import random
import datetime
from pathlib import Path

import time

CURRENT_DIR = os.path.dirname(__file__)
AUDIO_PATH = Path("../Audio/")
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
	rarityOfEffect = getRandomNumber(10)
	videoEffectToUse = ''
	if (rarityOfEffect >= 9):
		videoEffectToUse = RARE_VIDEO_EFFECTS[getRandomNumber(len(RARE_VIDEO_EFFECTS)-1)]
	elif (rarityOfEffect >= 7):
		videoEffectToUse = UNCOMMON_VIDEO_EFFECTS[getRandomNumber(len(UNCOMMON_VIDEO_EFFECTS)-1)]
	else:
		videoEffectToUse = COMMON_VIDEO_EFFECTS[getRandomNumber(len(COMMON_VIDEO_EFFECTS)-1)]
	VIDEO_EFFECTS_USED.append(videoEffectToUse.__name__)
	return videoEffectToUse(video)

def getRandomNumber(num):
	return random.randint(0, num)

def deepFryEffect(video):
	return vfx.lum_contrast(video.volumex(2000), 50, 10)

def loopClipEffect(video):
	videoLength = video.end
	if (video.end == 0):
		return video
	index = random.randrange(0, videoLength)
	indexStep = random.uniform(0.5, 1)
	count = 0
	clippedVideo = []
	while int(count) != videoLength:
		clippedVideo.append(video.subclip(index, index + indexStep))
		count += indexStep
	mergedClips = mpe.concatenate_videoclips(clippedVideo, method="compose")
	return mergedClips


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

def getAudioClip():
	audioArray = os.listdir(AUDIO_PATH)
	audioIndex = random.randint(0, len(audioArray) - 1)
	pathToAudio = str(AUDIO_PATH) + '/' + str(audioArray[audioIndex])
	return mpe.AudioFileClip(pathToAudio)


def applyAudioEffect(videoClip):
	audioClip = getAudioClip().subclip(t_start=videoClip.start, t_end=videoClip.end)
	print(dir(audioClip))
	AUDIO_EFFECTS_USED.append(audioClip.filename)
	return videoClip.set_audio(audioClip)



def addAudioEffects(videoClips, index, numOfEffects):
	count = 0
	while count != numOfEffects:
		# grab part of video
		randomStart = random.randint(0, int(videoClips.end))
		randomEnd = random.randint(randomStart, int(videoClips.end))
		videoClip = videoClips.subclip(t_start=randomStart, t_end=randomEnd)
		# apply effect to video
		modifiedClip = applyAudioEffect(videoClip)
		# re-create the video
		videoClips = mpe.concatenate_videoclips([videoClips.subclip(t_start=videoClips.start, t_end=randomStart), modifiedClip, videoClips.subclip(t_start=randomEnd, t_end=videoClips.end)], method="compose")
		count += 1

	return videoClips


def createRandomVideo(amountOfClips, index):
	count = 0
	videos = []
	while count != amountOfClips:
		videos.append(getVideoFromClip(VIDEO_PATH))
		count += 1
	# Splice clips together
	videoClips = mpe.concatenate_videoclips(videos, method="compose")
	videoClips.write_videofile("videoMash" + str(index) + ".mp4", threads=100)

	# audio effects should rarely be added
	checkAddAudioEffects = getRandomNumber(10)
	if (checkAddAudioEffects > 8):
		numOfAudioEffects = videoClips.end // 5
		if (numOfAudioEffects == 0):
			numOfAudioEffects = 1
		videoClips = addAudioEffects(videoClips, index, numOfAudioEffects)
	numOfVideoEffects = videoClips.end // 3
	videoClips = addVideoEffects(videoClips, index, numOfVideoEffects)
	# Write video
	
	return videoClips.write_videofile("videoMashed" + str(index) + ".mp4", threads=1000)

ALL_VIDEO_EFFECTS = [
			speedEffectGenerate, playBackwardsEffect, flipClipHorizontallyEffect,
			flipClipVerticallyEffect,blackAndWhiteEffect, 
			# contrastLuminosityGenerate,	gammaCorrectionGenerate, fadeInGenerate, fadeOutGenerate
			deepFryEffect, loopClipEffect
			]

RARE_VIDEO_EFFECTS = [	deepFryEffect	]
UNCOMMON_VIDEO_EFFECTS = [	loopClipEffect	]
COMMON_VIDEO_EFFECTS = 	[	speedEffectGenerate, playBackwardsEffect, flipClipHorizontallyEffect,
							flipClipVerticallyEffect,	blackAndWhiteEffect
						]

def postToTwitter(video):
	pass

count = 0
while count != 10:
	VIDEO_EFFECTS_USED = []
	AUDIO_EFFECTS_USED = []

	video = createRandomVideo(3, count)
	print(VIDEO_EFFECTS_USED)
	print(AUDIO_EFFECTS_USED)
	count += 1

# videoPath = Path("../Videos/")
# video = getVideoFromClip(videoPath)
# # video = loopClipEffect(video)
# video = addAudioEffects(video, count)
# video.write_videofile("test effect.mp4", threads=100)


