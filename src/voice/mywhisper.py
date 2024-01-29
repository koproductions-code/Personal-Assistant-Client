#https://github.com/davabase/whisper_real_time

import pyaudio
import struct
import whisper
import time
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

SILENCE_THRESHOLD = 0.02
SILENCE_DURATION = 1

model = whisper.load_model("medium", device="cuda")

def is_silent(data_chunk):
    """Check if the given audio chunk is silent."""
    as_ints = struct.unpack("%ih" % (len(data_chunk) // 2), data_chunk)
    max_amplitude = max(as_ints)
    return max_amplitude < (32767 * SILENCE_THRESHOLD)

def record_audio(audio_stream):
    frames = []
    
    silence_start_time = None
    while True:
        data = audio_stream.read(CHUNK)
        frames.append(data)

        if is_silent(data):
            if silence_start_time is None:
                silence_start_time = time.time()
            elif time.time() - silence_start_time > SILENCE_DURATION:
                break
        else:
            silence_start_time = None

    output_filename = "tmp/output.wav"
    SAMPLE_WIDTH = pyaudio.PyAudio().get_sample_size(FORMAT)

    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(SAMPLE_WIDTH)
    wf.setframerate(RATE)

    for frame in frames:
        wf.writeframes(frame)

    wf.close()

    with open(output_filename, "r") as file:
        audio_data = whisper.load_audio(output_filename)
        result = model.transcribe(audio_data)
        return result["text"]