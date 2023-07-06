# %%
import vosk
import pyaudio
import keyboard as kb
import wave
import whisper
import time
import win32com.client
import pythoncom
WAVE_OUTPUT_FILENAME = "temp.wav"
#_recording = False
label = lambda x: print('-=-=-=-=-=-=-=-=-=-=- ' + str(x) + ' -=-=-=-=-=-=-=-=-=-=-\n')

# %%
audioSetup = {
    'format': pyaudio.paInt16,
    'channels':1,
    'rate':16000,
    'input':True,
    'framesPerBuffer': 8192
}

HOTKEY = 'alt+1'

# %%
# label('loading English model')
# modelEN = vosk.Model('model/en')
# recognizerEN = vosk.KaldiRecognizer(modelEN,16000)
# print('ready')
# label('loading Polish model')
# modelPL = vosk.Model('model/pl')
# recognizerPL = vosk.KaldiRecognizer(modelPL,16000)
# print('ready')
label("Loading whisper model")
model = whisper.load_model("base")
print("done")

tts = win32com.client.Dispatch("SAPI.SpVoice")
# %%
def recordAudio():
    rec = pyaudio.PyAudio()
    stream = rec.open(format=audioSetup['format'], channels=audioSetup['channels'],rate=audioSetup['rate'],input=audioSetup['input'],frames_per_buffer=audioSetup['framesPerBuffer'])
    stream.start_stream()
    print('recording . . .')
    #tts.Speak("recording")
    #_recording = True
    frames = []
    while kb.is_pressed(HOTKEY):
        data = stream.read(audioSetup['framesPerBuffer'])
        frames.append(data)
    stream.stop_stream()
    stream.close()
    rec.terminate()
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(audioSetup['channels'])
    waveFile.setsampwidth(rec.get_sample_size(audioSetup['format']))
    waveFile.setframerate(audioSetup['rate'])
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    print('audio recorded')
    tts.Speak("audio recorded, please wait")


def textFromAudio():
    print("Transcribing audio")
    timeStart = time.time()
    result = model.transcribe(WAVE_OUTPUT_FILENAME)
    timeEnd = time.time()
    print('Time taken to transcribe:',timeEnd - timeStart)

    return result['text']

def startProcess():
    pythoncom.CoInitialize()
    recordAudio()
    text = textFromAudio()
    print(text)
    tts.Speak("Transcribed text: ..." + str(text) + "... did i understand correctly? press 2 to proceed, or 3 to cancel")
    print("Press 2 to confirm, or 3 to cancel")
    while True:
        if kb.is_pressed('2'):
            tts.Speak("proceeding")
            break
        if kb.is_pressed('3'):
            tts.Speak("Canceling")
            label("Canceled")
            label("Waiting for new request")
            return
    
    


# %%
print(tts.GetVoices())
kb.add_hotkey(HOTKEY,startProcess)

#kb.add_hotkey('alt+2',startProcess,args=(recognizerPL,))
label('waiting for input')
kb.wait('alt+ctrl+shift+1+2+3')


