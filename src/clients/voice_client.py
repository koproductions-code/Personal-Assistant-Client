import voice.mywhisper as mywhisper
import struct
import pvporcupine
import requests
import pyttsx3

from playsound import playsound
from pyaudio import PyAudio, paInt16
from functions.utils import *
from time import sleep

tts = pyttsx3.init()
tts.setProperty("rate", 130)

def handle_response(response: str):
    if "<functioncall>" in response:
        split = response.split("<functioncall>")[1]
        newprompt = "<functioncall>" + split
        print("Calling function: {}".format(newprompt))
        result : FunctionResponse = call_function(newprompt)
        if result.return_to_assistant == False:
            playsound("tones/chime.mp3", True)
        else:
            newresult = request(str(result.result), True)
            handle_response(newresult)
    elif "ASSISTANT: " in response:
        split = response.split("ASSISTANT: ")[1]
        tts.say(split)
        tts.runAndWait()
    else:
        tts.say("There was an error.")
        tts.runAndWait()

def request(prompt, first):
    body = {}

    if first:
        system = generate_system_prompt()
        functions = generate_functions()
        body["system"] = system
        body["functions"] = functions

def do(config_folder, model):
    while True:
        text = input("Prompt: ")

        system = model.generate_system()
        functions = model.generate_functions(config_folder)
        prompt = model.generate_prompt(text)

        result = request(system, functions, prompt)
    return result.json()["response"]


access_key = "O6AJWTE5FIeAGUfjSxNGTzYNgVvdv+Vm8ccCzccfWrym61l7nA2rMQ=="

audio_stream = PyAudio()
porcupine = pvporcupine.create(access_key, keyword_paths=["wakewords/jarvis.ppn"])

buffer_size = porcupine.frame_length
sample_rate = porcupine.sample_rate

stream = audio_stream.open(
    format=paInt16,
    channels=1,
    rate=sample_rate,
    input=True,
    frames_per_buffer=buffer_size
)


while True:
    pcm = stream.read(buffer_size)
    pcm = struct.unpack_from("h" * buffer_size, pcm)

    keyword_index = porcupine.process(pcm)

    if keyword_index == 0:
        sleep(0.2)
        playsound('tones/chime.mp3', True)

        mystream = PyAudio().open(format=paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        audio = mywhisper.record_audio(mystream)
        result = request(audio, True)
        handle_response(result)

audio_stream.stop_stream()
audio_stream.close()
audio_stream.terminate()

"""
while True:
    result = request(input("Prompt: "), True)
    handle_response(result)

"""