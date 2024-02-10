import pyaudio
import wave

class AudioRecorder:
    def __init__(self, filename="output.wav", chunk=1024, format=pyaudio.paInt16, channels=2, rate=44100):
        self.filename = filename
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.frames = []

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=format,
                                      channels=channels,
                                      rate=rate,
                                      input=True,
                                      frames_per_buffer=chunk)

    def record(self, seconds):
        print("Recording...")
        for _ in range(0, int(self.rate / self.chunk * seconds)):
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        print("Finished recording.")

    def save(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print("Audio saved as", self.filename)

def main():
    recorder = AudioRecorder()
    recorder.record(5)  # Record for 5 seconds
    recorder.save()

if __name__ == "__main__":
    main()