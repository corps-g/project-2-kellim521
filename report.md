# ME 701 - Project 2 Report
#### DMX Data in Standard Binary Format<br />Kelli Ward

The majority of this project is similar to my project 1, and builds off the same concepts. This version of my project now works with DMX data created automatically from a .wav file, and the binary file it outputs works with the DMX light.

`binarytodmx.py`
Running this file will prompt the user to enter the name of the wav file they wish to convert, start and end times for when they want frames generated, the time interval for the frames to be generated, and the name to save the ouput file. It then calls `DMXMusic.py` for each time step the user wants a frame generated, and writes each frame to the binary file specified by the user. It includes the standard header information. `RGB.bin` is the output file created using `increasing.wav` as the input, when starting at 0 seconds, ending at 30 seconds, with 0.5 s intervals.
