Dantien - OpenGL brainwave visualizer
=====================================

Demo call (show random sinoids and their spectrogram/scaleogram):

    $ ./dantien.py


OpenEEG
-------

Example modEEG call:

    $ cat recorded_eeg.dat | ./dantien.py --modeeg

Example live modEEG call:

    $ ./utils/rec-modeeg | ./dantien.py --modeeg

Of course, it can be routed over the network (for example, if you want to read the data on a portable computer that is not connected to the mains supply):

    visualizer$ nc -l -p 12000 | ./dantien.py --modeeg
    collector$ ./utils/rec-modeeg | nc visualizer 12000


Requirements
------------

 * numpy
 * scipy
 * pywt
 * pyopengl
 * glumpy (included)
 * pytfd (included)
 * modEEG hardware if you want to visualize or collect live data

