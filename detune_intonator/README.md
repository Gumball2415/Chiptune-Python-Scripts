# Detune Intonator

it's just an intonation

---

## About

This generates various intonation detune tables in the 12-tone scale for 0CC-FamiTracker.

## Example

```batch
detune_intonator.py detune.csv --intonation 7_limit --key a
```

spits out [detune.csv](detune.csv)

## Usage

```
usage: detune_intonator.py [-h] [-d] [--intonation {12tet,3_limit,5_limit,7_limit}] [--key {c,c#,d,d#,e,f,f#,g,g#,a,a#,b}] [--reference REFERENCE]
                           [-nchan N163_CHANNELS]
                           output

Intonation detune table generator for 0CC-FamiTracker

positional arguments:
  output                output .csv

options:
  -h, --help            show this help message and exit
  -d, --debug           print debug messages
  --intonation {12tet,3_limit,5_limit,7_limit}
                        intonation type. default = "12tet"
  --key {c,c#,d,d#,e,f,f#,g,g#,a,a#,b}
                        note to be designated as unison. default = "c"
  --reference REFERENCE
                        reference pitch for A. default = 440.0
  -nchan N163_CHANNELS, --n163-channels N163_CHANNELS
                        N163 channel count. default = 0

version 0.1.0
```

## License

Licensed under the MIT-0 license.
Copyright 2021-2025 Persune.
