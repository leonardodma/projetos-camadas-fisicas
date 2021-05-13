import sounddevice as sd
from scipy.io.wavfile import write


fs = 44100 

def record_to_file(file_name):
    print('Gravação iniciada')
    seconds = 3  # Duration of recording
    recording = sd.rec(int(seconds * fs), samplerate=fs)
    sd.wait()  # Wait until recording is finished
    write(file_name, fs, recording)  # Save as WAV file
    print('Gravação finalizada')