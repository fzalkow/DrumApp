import numpy
import math

def is_number(s):
    """ check if s is a number """
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False

def ask_for_number(str=""):
    """ loop for asking the user until he gives a number """
    n = None
    while (not(is_number(n))):
        n = raw_input(str)
    return n

def chunks_to_numpy(chunks, dtype="int16"):
    """ convert list of binary strings to numpy array """
    return numpy.concatenate(
        map(lambda (chunk): numpy.fromstring(chunk, dtype=dtype), chunks))

def numpy_to_chunks(array, chunklen=1024):
    """ convert numpy array to list of binary strings """
    l = len(array)
    chunks = numpy.array_split(array, int(math.ceil(l/float(chunklen))))
    #chunks[-1] = numpy.append(chunks[-1], numpy.zeros(chunklen-len(chunks[-1])))
    return map(lambda (chunk): chunk.tostring(), chunks)
