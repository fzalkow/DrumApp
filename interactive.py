#!/usr/bin/env python

import drumapp_tools.audioio as audioio
import drumapp_tools.utils as utils
import drumapp_tools.timestretch as timestretch
import drumapp_tools.realtimestft as realtimestft

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
        
    # time-stretch
    elif myinput == "t":
        fac = utils.ask_for_number("Factor for stretching (0.5 = double speed, 2.0 = halfe speed): ")
        AUDIO = timestretch.simple_stretcher(utils.chunks_to_numpy(AUDIO), float(fac))
        return 1
        
    # save to disk
    elif myinput == "s":
        path = raw_input("Give path for wav file: ")
        audioio.write_chunks(path, AUDIO)
        return 1
    
    # quit loop
    elif myinput == "q":
        return 0
        
    # typed non-sense
    else:
        print "You have not typed something correct..."
        return 1


def options ():
    """ record or quit """
    global AUDIO
    print "Type R to record audio."
    print "Type S for a real time spectogram."
    print "Type Q to quit this loop."
    myinput = raw_input().lower()

    # record something
    if myinput == "r":
        secs = utils.ask_for_number("How many seconds? ")
        AUDIO = audioio.record(float(secs))

        record_loop = 1
        while (record_loop == 1):
            record_loop = record_interactive()
        return 1
        
    # real time stft
    elif myinput == "s":
    		realtimestft.real_time_spectogram()
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
