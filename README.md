# Simple Project: Drum learning app

This a project for making a learning app for drum students. It is situated in its very beginnings.

At the moment you can load the Python script *interactive.py* and you'll get in a loop where you can
- record audio (via PortAudio)
- play this back (via PortAudio)
- time-stretch it (simple, pitch-changing, by just interpolating the audio signal)
- writing it to hard disk

## Dependencies
At the moment you need
- Python (http://www.python.org/)
- PyAudio (http://people.csail.mit.edu/hubert/pyaudio/)
- NumPy/SciPy (http://www.scipy.org/)

## Time Stretch Tests
In the folder `time_stretch_tests` there are tests for time stretching. The original file is a small excerpt from Edgar Varèses *Ionisation*. The stretched files are twice as long, i.e. half tempo.
- `ionisation_dirac3le.mp3` used DIRAC3 LE (http://dirac.dspdimension.com/)
- `ionisation_interpolated.mp3` just interpolated the signal with `drumapp_tools.timestretch`, so the pitch is an octave higher
- `ionisation_soundtouch.mp3` used SoundTouch (http://www.surina.net/soundtouch/)
(The files have been converted to mp3 afterwards via `lame infile.wav outfile.mp3 -V2`.)
