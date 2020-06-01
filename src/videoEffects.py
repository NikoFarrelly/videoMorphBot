import moviepy.editor as mpe 
import moviepy.video.fx.all as vfx
from moviepy.editor import * 
import random
from videoRetrieval import get_video_from_clip
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

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

def repeat_sample_effect(video):
	return vfx.supersample(video, video.end, random.randint(5,20))

def two_clips_at_once_effect(video):
	return vfx.mask_or(video, get_video_from_clip())

def zoom_center_effect(video):
	focused_height = video.h // 3
	focused_width = video.w // 3
	return zoom(video, focused_width, focused_height, focused_width * 2, focused_height * 2)

def zoom(video, x1, y1, x2, y2):
    return vfx.crop(video, x1=x1, y1=y1, x2=x2, y2=y2).resize(video.size)

def be_right_back_effect(video):
	meme_length = 3 # what has my life come to
	start_effect_at = video.end - meme_length if video.end - meme_length >= 0 else 1
	text = "We'll be right back"
	filename = "be_right_back_effect.png"
	pre_effect_clip = video.subclip(t_start=0, t_end=start_effect_at)
	clip_to_save = video.subclip(t_start=start_effect_at)
	clip_to_save.save_frame(filename)
	text_clip = add_text_to_image((175,video.h/2 - 60), filename, text).set_duration(meme_length)
	concatenated_clips = mpe.concatenate_videoclips([text_clip], method="compose")

	audio_clip = mpe.AudioFileClip("../Audio/We'll be right back Sound Effect meme.mp3")
	clip_with_audio = concatenated_clips.subclip(t_start=0, t_end=meme_length).set_audio(audio_clip)

	re_concatenation = mpe.concatenate_videoclips([pre_effect_clip, clip_with_audio], method="compose")
	return re_concatenation

def add_text_to_image(coords, image_filename, text):
	image_file = Image.open(image_filename)
	draw = ImageDraw.Draw(image_file)
	font = ImageFont.truetype("impact.ttf", 120)
	draw.text(coords, text, (255, 255, 255), font=font)
	image_file.save(image_filename)
	return mpe.ImageClip(image_filename)


# def slow_rotate(video):
# 	### UNFINISHED
# 	count = 0
# 	sub_clip_count = 0
# 	step = 0
# 	video_array = []
# 	degrees_to_spin = 180
# 	sub_clip_length = video.end / degrees_to_spin
# 	print('video len:', video.end)
# 	while count != degrees_to_spin:
# 		count += 1
# 		step += 1 / (degrees_to_spin)
# 		video_clip = video.subclip(t_start=sub_clip_count, t_end=sub_clip_count + sub_clip_length)
# 		video_clip = vfx.rotate(video_clip, step, 'rad')
# 		video_array.append(video_clip)
# 		print('accessing', sub_clip_count, 'to', sub_clip_count+sub_clip_length, 'and applying', step, 'rad degrees')
# 		sub_clip_count += sub_clip_length

# 	concatenated_video = mpe.concatenate_videoclips(video_array, method="compose")
# 	return concatenated_video

def loop_clip_effect(video):
	video_length = video.end
	if (video.end == 0):
		return video
	index = random.randrange(0, video_length)
	index_step = random.uniform(0.5, 1)
	count = 0
	clipped_video = []
	while int(count) != video_length:
		clipped_video.append(video.subclip(index, index + index_step))
		count += index_step
	merged_clips = mpe.concatenate_videoclips(clipped_video, method="compose")
	return merged_clips


ALL_VIDEO_EFFECTS = [
			speed_effect_generate, play_backwards_effect, flip_clip_horizontally_effect,
			flip_clip_vertically_effect,black_and_white_effect, 
			# contrast_luminosity_generate,	gamma_correction_generate, fade_in_generate, fade_out_generate
			deep_fry_effect, loop_clip_effect
		]

RARE_VIDEO_EFFECTS = [	deep_fry_effect, zoom_center_effect, be_right_back_effect	]
UNCOMMON_VIDEO_EFFECTS = [	loop_clip_effect, repeat_sample_effect, two_clips_at_once_effect	]
COMMON_VIDEO_EFFECTS = 	[	
	speed_effect_generate, play_backwards_effect, flip_clip_horizontally_effect,
	flip_clip_vertically_effect,	black_and_white_effect
]