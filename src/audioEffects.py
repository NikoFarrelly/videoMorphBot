import moviepy.editor as mpe 

AUDIO_PATH = Path("../Audio/")

def get_audio_clip():
	audioArray = os.listdir(AUDIO_PATH)
	audioIndex = random.randint(0, len(audioArray) - 1)
	pathToAudio = str(AUDIO_PATH) + '/' + str(audioArray[audioIndex])
	return mpe.AudioFileClip(pathToAudio)

def apply_audio_effect(videoClip):
	audioClip = getAudioClip().subclip(t_start=videoClip.start, t_end=videoClip.end)
	AUDIO_EFFECTS_USED.append(audioClip.filename)
	return videoClip.set_audio(audioClip)