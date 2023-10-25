# import librosa
# import numpy as np
# from transformers import pipeline
#
# # Replace 'audio_file.wav' with the path to your audio file
# audio_file = r"C:\Users\Dell\Downloads\file_23.oga"
#
# # Load the audio file using librosa
# audio, sample_rate = librosa.load(audio_file, sr=None)
#
# # Convert the audio data to a NumPy array
# audio_array = np.array(audio)
#
# # Print the shape of the audio array
# print("Shape of the audio array:", audio_array.shape)
# # Use a pipeline as a high-level helper
#
# pipe = pipeline("automatic-speech-recognition", model="openai/whisper-base")
# print(pipe(audio_array))
# import soundfile as sf
# import soundfile as sf
# import sounddevice as sd
#
# # Read the .npy file
# # audio_data = soundfile.read(r'C:\Users\Dell\Desktop\PROJECT\HTM\audio_array.npy')
# data, sample_rate = sf.read(r'C:\Users\Dell\Desktop\PROJECT\HTM\audio_array.npy')
#
# # Play the audio
# sd.play(data, sample_rate)
# sd.wait()
# import soundfile as sf

###To play the audio
# # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@22
import sounddevice as sd
import numpy as np

# Replace 'audio_data.npy' with the path to your .npy file
audio_file = r'C:\Users\Dell\Desktop\PROJECT\HTM\audio_array.npy'

# Load the audio data from the .npy file
audio_data = np.load(audio_file)

# Play the audio using sounddevice
sd.play(audio_data, samplerate=44100)  # Replace 44100 with the appropriate sample rate

# Wait for the audio to finish playing
sd.wait()

# import librosa
#
#
# mp3_file_1 = r'C:\Users\Dell\Desktop\PROJECT\HTM\temp_audio.mp3'
# mp3_file_2=r"C:\Users\Dell\Downloads\ElevenLabs_2023-10-25T08_07_23_Gigi_pre_s50_sb63_m1.mp3"
#
# # Load the MP3 file using librosa
# audio_data, sample_rate = librosa.load(mp3_file_1, sr=None)
# print(audio_data.shape)
#
# # Replace 'input.mp3' with the path to your input MP3 file



