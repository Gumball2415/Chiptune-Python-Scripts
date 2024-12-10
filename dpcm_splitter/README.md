# dpcm_splitter

the NES can't stream more than 4081 bytes of DPCM data, skill issue

---

## About

Splits a given input DPCM binary into chunks of specified chunk size.

## Usage

extremely crusty. **DO NOT USE THIS. I DON'T EVEN USE THIS ANYMORE EITHER.**

1. drag n drop a .dmc or dpcm-encoded file
2. enter chunk (partition)
3. the program will generate `n` amounts of full-size chunks, with the final chunk containing less than or equal to specified chunk size.
4. press enter to exit

## License

Licensed under the MIT-0 license.
Copyright 2021-2024 Persune.
