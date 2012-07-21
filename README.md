Dantien - OpenGL brainwave visualizer
=====================================

Demo call (show random sinoids and their spectrogram/scaleogram):

    $ ./dantien.py


OpenEEG
-------

Example modEEG call:

    $ cat recorded_eeg.dat | ./dantien.py --modeeg

Example live modEEG call (not yet):

    $ ./collect-openeeg.py /dev/ttyUSB0 | ./dantien.py --modeeg

Of course, it can be routed over the network (for example, if you want to read the data on a portable computer that is not connected to the mains supply) (not yet):

    visualizer$ nc -l -p 12000 | ./dantien.py --modeeg
    collector$ ./collect-openeeg.py | nc visualizer 12000


Requirements
------------

 * numpy
 * scipy
 * pywt
 * pyopengl
 * glumpy (included)
 * pytfd (included)
 * modEEG hardware if you want to visualize or collect live data

