# NSFPlay Multichannel Exporter

A quick and dirty multichannel exporter for NSFPlay, built on version 2.5, compatible with version 2.4.
Place the script in the NSFPlay folder, making sure it's next to `nsfplay.exe` and the `plugins` folder.

![](nsfplay_folder.png)

Note that this will generate tracks with nonlinear distortion, so make sure your configurations are set to deterministic settings (i.e. no random triangle phase, random noise phase, etc.)

![](commandline.png)

[Example oscilloscope video using the output files](https://youtu.be/71gAf07z7e4)

```
usage: nsfplay_multiexporter.py [-h] [-i INPUTNSF] [-o OUTPUTWAV] [-t NSFTRACK] [-l WAVLENGTH] [-v]

NSFPlay Channel Exporter by Persune

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTNSF, --inputnsf INPUTNSF
                        NSF file input
  -o OUTPUTWAV, --outputwav OUTPUTWAV
                        WAV Export name
  -t NSFTRACK, --nsftrack NSFTRACK
                        Track of .nsf
  -l WAVLENGTH, --wavlength WAVLENGTH
                        Length of .wav export in milliseconds
  -v, --verbose         Enable output verbosity

version beta 0.2
```

