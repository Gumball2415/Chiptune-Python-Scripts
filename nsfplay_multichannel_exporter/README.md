# NSFPlay Multichannel Exporter

automatic stem extract?

---

## About

A quick and dirty multichannel exporter for NSFPlay, built on version 2.6, compatible with version 2.7.

## Example

See `export_example.bat`.

Note that this python script will generate tracks with nonlinear distortion, so make sure your configurations are set to deterministic settings (i.e. no random triangle phase, no random noise phase, etc.)

![Windows commandline executing export_example.bat](commandline.png)

[Example oscilloscope video using the output files](https://youtu.be/71gAf07z7e4)

## Usage

```
usage: nsfplay_multiexporter.py [-h] [-v] [-nch N163CHANNELS] nsfplay_path inputnsf nsftrack wavlength outputwav

NSFPlay Channel Exporter by Persune

positional arguments:
  nsfplay_path          path to NSFPlay folder
  inputnsf              NSF file input
  nsftrack              Track of .nsf
  wavlength             Length of .wav export in seconds
  outputwav             WAV Export name

options:
  -h, --help            show this help message and exit
  -v, --verbose         Enable output verbosity
  -nch N163CHANNELS, --n163channels N163CHANNELS
                        Specify number of N163 channels. Default is 0

version beta 0.6
```

## License

Licensed under the MIT-0 license.
Copyright 2021-2024 Persune.
