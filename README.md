# Simple Project: Drum learning app

This a project for making a learning app for drum students.

**Heads up!** This project is folded here and is being continued on [bitbucket](https://bitbucket.org/voocoder/drumapp)!

## C/C++

At the moment there are the functions `play_from_file` (which plays an existing WAVE file) and `record_to_file` (which records from Default Audio Input and writes it to Disk as WAVE file). It can be compiled with `gcc -o test main.c -lsndfile -lportaudio -include audioio.c`.

### Dependencies
You need
- portaudio (http://www.portaudio.com/)
- libsndfile (http://www.mega-nerd.com/libsndfile/)

## Prototypes in Python

At the moment you can load the Python script `interactive.py` and you'll get in a loop where you can
- record audio (via PortAudio)
- play this back (via PortAudio)
- real-time spectogram plotting
- time-stretch it (simple, pitch-changing, by just interpolating the audio signal)
- writing it to hard disk

### Dependencies
At the moment you need
- Python (http://www.python.org/)
- PyAudio (http://people.csail.mit.edu/hubert/pyaudio/)
- NumPy/SciPy (http://www.scipy.org/)
- PyQtGraph (http://www.pyqtgraph.org/)

## Time Stretch Tests
In the folder `time_stretch_tests` there are tests for time stretching. The original file `ionisation_orig.mp3` is a small excerpt from Edgar Varèses *Ionisation*. The stretched files are twice as long, i.e. half tempo. (The files have been converted to mp3 afterwards via `lame infile.wav outfile.mp3 -V2`.)
- `ionisation_dirac3le.mp3` used DIRAC3 LE (http://dirac.dspdimension.com/)
- `ionisation_interpolated.mp3` is just an interpolation the signal with `drumapp_tools.timestretch`, so the pitch is an octave higher
- `ionisation_soundtouch.mp3` used SoundTouch (http://www.surina.net/soundtouch/)
