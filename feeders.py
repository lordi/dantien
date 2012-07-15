import sys
import os
import fcntl
import numpy as np
from operator import itemgetter
from struct import unpack
import io

def random_sinoids():
    return np.sin(np.arange(100)*np.random.random(1)*5.0)

def random_positive_sinoids():
    return np.sin(np.arange(100)*np.random.random(1)*5.0) / 2.0 + 0.5

def _set_non_blocking(output):
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

def stdin():
    _set_non_blocking(sys.stdin)
    def stdin_read():
        x = []
        try:
            x = map(ord, sys.stdin.read()[:100])
        except IOError, e:
            print e
            pass
        print x
        return x
    return stdin_read

MODEEG_PKTLEN = 17
MODEEG_SYNC = (0xa5, 0x5a, 0x02)

def modeeg():
    """
    Read raw ModEEG data from stdin
    """
    f = sys.stdin
    _set_non_blocking(f)
    inbuf = io.open(f.fileno(), mode='rb', closefd=False)
    def stdin_read():
        x = []
        leftover = None
        for i in range(30): # Limit to 30 frames per call, FIXME
            data = inbuf.read(MODEEG_PKTLEN)
            if data is None or len(data) < MODEEG_PKTLEN:
                leftover = data
                break
            info = unpack('>BBBBHHHHHHB', data)
            if info[:3] != MODEEG_SYNC:
                inbuf.read(1)
                continue
            x.append(info)
        print len(x), leftover
        # TODO: BufferedReader what?! make use of leftover!
        return [(info[4] - 512) / 1024.0 for info in x[:300]]
    return stdin_read

