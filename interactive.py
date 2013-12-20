#!/usr/bin/env python

import drumapp_tools.audioio as audioio
import drumapp_tools.utils as utils
import drumapp_tools.timestretch as timestretch

def record_interactive():
    """ interactive loop to do something with the audio recording:
        play, time-stretch, writing to disk """
    global AUDIO
    print "Type P to play the recording."
    print "Type T to time-stretch the recording."
    print "Type S to save the recording to disk."
    print "Type Q to return to top level loop."
    myinput = raw_input().lower()

    #play
    if myinput == "p":
        print "Play..."
        audioio.play(AUDIO)
        return 1
    if myinput == "t":
        print "Factor for stretching (0.5 = double speed, 2.0 = halfe speed)"
        fac = utils.ask_for_number()
        AUDIO = timestretch.simple_stretcher(utils.chunks_to_numpy(AUDIO), float(fac))
        return 1
    if myinput == "s":
        print "Give path for wav file"
        path = raw_input()
        audioio.write_chunks(path, AUDIO)
        return 1
    if myinput == "q":
        return 0
    else:
        print "You have not typed something correct..."
        return 1


def options ():
    """ record or quit """
    global AUDIO
    print "Type R to record audio."
    print "Type Q to quit this loop."
    myinput = raw_input().lower()

    # record something
    if myinput == "r":
        print "How many seconds?"
        secs = utils.ask_for_number()
        AUDIO = audioio.record(float(secs))

        record_loop = 1
        while (record_loop == 1):
            record_loop = record_interactive()
        return 1

    # quit the loop
    elif myinput == "q":
        return 0

    # typed non-sense
    else:
        print "You have not typed something correct..."
        return 1

# main loop
AUDIO = None
print "Hi to the Python test recording environment."
loop = 1
while (loop == 1):
    loop = options()
