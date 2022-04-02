# ShiningSoul2Extractor
A tool for pulling portraits out of Shining Soul II for the GBA

This decodes the Dialogue portraits from the ROM into sensible images, attaching the proper palettes. It's slightly a mess because it was developed in a very iterative experimental way, but I'm committing it in case anyone else finds it useful. 

The RGB555-to-RGB888 code was borrowed from [the mGBA emulator](https://github.com/mgba-emu/mgba), under the MPL 2.0 license. 


# Target ROM:
A US ROM for Shining Soul II by Nextech and Grasshopper Manufacture, published by Sega/THQ/Atlus, named "1460 - Shining Soul II (U).gba", md5sum F4A655E23638E79EACF44A456FAEE6A4. 

# Requirements
* Python 2.7
* [Pillow](https://pillow.readthedocs.io/en/stable/)
 
