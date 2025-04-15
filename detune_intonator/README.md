# Detune Intonator

it's just an intonation

---

## About

This generates various intonation detune tables in the 12-tone scale for 0CC-FamiTracker.

## Example

```batch
detune_intonator.py detune.csv --intonation 7_limit --key a --reference 440.0
```

spits out [detune.csv](detune.csv)

## Usage

```
usage: detune_intonator.py [-h] [-d] [--intonation {12tet,3_limit,5_limit,7_limit}]
                           [--intervals n_0 d_0 n_1 d_1 n_2 d_2 n_3 d_3 n_4 d_4 n_5 d_5 n_6 d_6 n_7 d_7 n_8 d_8 n_9 d_9 n_10 d_10 n_11 d_11]
                           [--key {c,c#,d,d#,e,f,f#,g,g#,a,a#,b}] [--reference REFERENCE] [-nchan N163_CHANNELS]
                           output

Intonation detune table generator for 0CC-FamiTracker

positional arguments:
  output                output .csv

options:
  -h, --help            show this help message and exit
  -d, --debug           print debug messages
  --intonation {12tet,3_limit,5_limit,7_limit}
                        intonation type. default = "12tet"
  --intervals n_0 d_0 n_1 d_1 n_2 d_2 n_3 d_3 n_4 d_4 n_5 d_5 n_6 d_6 n_7 d_7 n_8 d_8 n_9 d_9 n_10 d_10 n_11 d_11
                        custom 12 tone interval ratio list, overrides default intonation settings.
  --key {c,c#,d,d#,e,f,f#,g,g#,a,a#,b}
                        note to be designated as unison. default = "a"
  --reference REFERENCE
                        reference pitch for unison note. default = 440.0
  -nchan N163_CHANNELS, --n163-channels N163_CHANNELS
                        N163 channel count. default = 0

version 0.2.0
```

## License

Licensed under the MIT-0 license.
Copyright 2021-2025 Persune.
