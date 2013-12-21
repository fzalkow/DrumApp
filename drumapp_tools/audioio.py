import pyaudio
import wave

def record(seconds=3.0, rate=44100, channels=2, format=pyaudio.paInt16, chunk=1024):
    """ record audio from mic """
    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("> start recording...")

    frames = []

    for i in range(0, int(rate / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("> done recording...")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames

def play(frames, rate=44100, channels=2, format=pyaudio.paInt16, chunk=1024):
    """ play audio by your speakers """

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    output=True)

    for frame in frames:
        stream.write(frame)

    stream.stop_stream()
    stream.close()

    p.terminate()

def write_chunks(path, frames, rate=44100, channels=2, format=pyaudio.paInt16):
    """ write audio to hard disk """
    
    wf = wave.open(path, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()
