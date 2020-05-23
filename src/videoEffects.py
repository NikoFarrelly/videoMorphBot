import moviepy.editor as mpe 
import moviepy.video.fx.all as vfx
from moviepy.editor import * 
import random

def applyVideoEffect(video):
	rarityOfEffect = getRandomNumber(10)
	videoEffectToUse = ''
	if (rarityOfEffect >= 9):
		videoEffectToUse = RARE_VIDEO_EFFECTS[getRandomNumber(len(RARE_VIDEO_EFFECTS)-1)]
	elif (rarityOfEffect >= 7):
		videoEffectToUse = UNCOMMON_VIDEO_EFFECTS[getRandomNumber(len(UNCOMMON_VIDEO_EFFECTS)-1)]
	else:
		videoEffectToUse = COMMON_VIDEO_EFFECTS[getRandomNumber(len(COMMON_VIDEO_EFFECTS)-1)]
	return videoEffectToUse(video)

# Utility
def getRandomNumber(num):
	return random.randint(0, num)

# Generation
def fadeInGenerate(video):
	return fadeInEffect(video, random.randint(1, 2))

def speedEffectGenerate(video):
	return speedEffect(video, random.uniform(0.4, 1.3))

def contrastLuminosityGenerate(video):
	return contrastLuminosityEffect(video, getRandomNumber(200), getRandomNumber(30))

def gammaCorrectionGenerate(video):
	return gammaCorrectionEffect(video, random.randint(1, 6))

def fadeOutGenerate(video):
	return fadeOutEffect(video, random.randint(1, 2))

def fadeInGenerate(video):
	return fadeInEffect(video, random.randint(1, 2))

# Effects
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

def contrastLuminosityEffect(video, luminosity, contrast):
	return vfx.lum_contrast(video, luminosity, contrast)

def gammaCorrectionEffect(video, correction):
	return vfx.gamma_corr(video, correction)

def fadeInEffect(video, duration):
	return vfx.fadein(video, duration)

def fadeOutEffect(video, duration):
	return vfx.fadeout(video, duration)

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


ALL_VIDEO_EFFECTS = [
			speedEffectGenerate, playBackwardsEffect, flipClipHorizontallyEffect,
			flipClipVerticallyEffect,blackAndWhiteEffect, 
			# contrastLuminosityGenerate,	gammaCorrectionGenerate, fadeInGenerate, fadeOutGenerate
			deepFryEffect, loopClipEffect
			]

RARE_VIDEO_EFFECTS = [	deepFryEffect	]
UNCOMMON_VIDEO_EFFECTS = [	loopClipEffect	]
COMMON_VIDEO_EFFECTS = 	[	
	speedEffectGenerate, playBackwardsEffect, flipClipHorizontallyEffect,
	flipClipVerticallyEffect,	blackAndWhiteEffect
	]