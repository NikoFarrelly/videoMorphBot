import moviepy.editor as mpe 
import moviepy.video.fx.all as vfx
from moviepy.editor import * 
import random

def apply_video_effect(video):
	rarityOfEffect = get_random_number(100)
	videoEffectToUse = ''
	if (rarityOfEffect >= 95):
		videoEffectToUse = RARE_VIDEO_EFFECTS[get_random_number(len(RARE_VIDEO_EFFECTS)-1)]
	elif (rarityOfEffect >= 90):
		videoEffectToUse = UNCOMMON_VIDEO_EFFECTS[get_random_number(len(UNCOMMON_VIDEO_EFFECTS)-1)]
	else:
		videoEffectToUse = COMMON_VIDEO_EFFECTS[get_random_number(len(COMMON_VIDEO_EFFECTS)-1)]
	return videoEffectToUse(video)

# Utility
def get_random_number(num):
	return random.randint(0, num)

# Generation
def fade_in_generate(video):
	return fade_in_effect(video, random.randint(1, 2))

def speed_effect_generate(video):
	return speed_effect(video, random.uniform(0.4, 1.3))

def contrast_luminosity_generate(video):
	return contrast_luminosity_effect(video, get_random_number(200), get_random_number(30))

def gamma_correction_generate(video):
	return gamma_correction_effect(video, random.randint(1, 6))

def fade_out_generate(video):
	return fade_out_effect(video, random.randint(1, 2))

def fade_in_generate(video):
	return fade_in_effect(video, random.randint(1, 2))

# Effects
def speed_effect(video, speed):
	return video.fx(vfx.speedx, speed)

def play_backwards_effect(video):
	return video.fx(vfx.time_mirror)

def flip_clip_horizontally_effect(video):
	return vfx.mirror_x(video)

def flip_clip_vertically_effect(video):
	return vfx.mirror_y(video)

def black_and_white_effect(video):
	return vfx.blackwhite(video)

def contrast_luminosity_effect(video, luminosity, contrast):
	return vfx.lum_contrast(video, luminosity, contrast)

def gamma_correction_effect(video, correction):
	return vfx.gamma_corr(video, correction)

def fade_in_effect(video, duration):
	return vfx.fadein(video, duration)

def fade_out_effect(video, duration):
	return vfx.fadeout(video, duration)

def deep_fry_effect(video):
	return vfx.lum_contrast(video.volumex(2000), 50, 10)

def loop_clip_effect(video):
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
			speed_effect_generate, play_backwards_effect, flip_clip_horizontally_effect,
			flip_clip_vertically_effect,black_and_white_effect, 
			# contrast_luminosity_generate,	gamma_correction_generate, fade_in_generate, fade_out_generate
			deep_fry_effect, loop_clip_effect
		]

RARE_VIDEO_EFFECTS = [	deep_fry_effect	]
UNCOMMON_VIDEO_EFFECTS = [	loop_clip_effect	]
COMMON_VIDEO_EFFECTS = 	[	
	speed_effect_generate, play_backwards_effect, flip_clip_horizontally_effect,
	flip_clip_vertically_effect,	black_and_white_effect
]