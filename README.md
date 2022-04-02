# ShiningSoul2Extractor
A tool for pulling portraits and fonts out of Shining Soul II for the GBA

This decodes the Dialogue portraits & fonts from the ROM into sensible images, attaching the proper palettes. It's slightly a mess because it was developed in a very iterative experimental way, but I'm committing it in case anyone else finds it useful. 

The RGB555-to-RGB888 code was borrowed from [the mGBA emulator](https://github.com/mgba-emu/mgba), under the MPL 2.0 license. 

# Usage:

Just run `python extract_ss2.py <ROMNAME.gba>` and it'll generate out.png & font.png file in the current directory.

# Target ROM:
It supports 3 different roms, but the output should be identical no matter the ROM:
* JP ROM (1113), md5sum 3BAE05647BBEE8565E3993FADE2CA5BA. 
* EU ROM (1407), md5sum 49AA688745111AAA51076A345F8F18C3. 
* US ROM (1460), md5sum F4A655E23638E79EACF44A456FAEE6A4. 

# Requirements
* Python 2.7
* [Pillow](https://pillow.readthedocs.io/en/stable/)
 
