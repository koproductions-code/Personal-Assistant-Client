import voice.mywhisper as mywhisper
import struct
import pvporcupine
import pyttsx3
from playsound import playsound
from pyaudio import PyAudio, paInt16
from functions.utils import *
from time import sleep
from server.Server import LLMServer
from datetime import datetime

tts = pyttsx3.init()
tts.setProperty("rate", 130)

def say(text):
    tts.say(text)
    tts.runAndWait()

class VoiceClient:

    def __init__(self, host, port, config, model) -> None:
        self.server = LLMServer(str(host), str(port))
        self.config = config
        self.model = model

        self.access_key = "O6AJWTE5FIeAGUfjSxNGTzYNgVvdv+Vm8ccCzccfWrym61l7nA2rMQ=="

        self.audio_stream = PyAudio()
        self.porcupine = pvporcupine.create(self.access_key, keyword_paths=["wakewords/jarvis.ppn"])

        self.BUFFER_SIZE = self.porcupine.frame_length
        self.SAMPLE_RATE = self.porcupine.sample_rate

        self.stream = self.audio_stream.open(
            format=paInt16,
            channels=1,
            rate=self.SAMPLE_RATE,
            input=True,
            frames_per_buffer=self.BUFFER_SIZE
        )

        print("Ready!")

    def request(self, prompt):
        system = self.model.generate_system()
        functions = self.model.generate_functions(self.config)
        prompt = self.model.generate_prompt(prompt)

        result = self.server.request(system, functions, prompt)
        self.model.handle_response(result, prompt, self.server, say)
    
    def main(self):
        while True:
            pcm = self.stream.read(self.BUFFER_SIZE)
            pcm = struct.unpack_from("h" * self.BUFFER_SIZE, pcm)

            keyword_index = self.porcupine.process(pcm)

            if keyword_index == 0:
                sleep(0.2)
                playsound('tones/chime.mp3', True)

                mystream = PyAudio().open(format=paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
                prompt = mywhisper.record_audio(mystream)
                self.request(prompt)
