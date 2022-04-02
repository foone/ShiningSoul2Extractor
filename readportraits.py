from PIL import Image
import struct
def read4(f):
	x=ord(f.read(1))
	a=(x>>4)&0x0F
	b=x&0x0F
	return b,a
def readN(f,n):
	out=[]
	for i in range(n//2):
		out.extend(list(read4(f)))
	return out
def readTile(f):
	lines=[]
	for y in range(8):
		lines.extend(readN(f,8))
	tile = Image.new('RGBA',(8,8))
	for i,x in enumerate(lines):
		color=palette.getpixel((x,0))

		tile.putpixel((i%8,i//8),color)
	return tile 

def loadPortrait(f):
	port=Image.new('RGBA',(32,64))
	for yline in range(8):
		a,b,c,d=readTile(f),readTile(f),readTile(f),readTile(f)
		port.paste(a,(0,yline*8))
		port.paste(b,(8,yline*8))
		port.paste(c,(16,yline*8))
		port.paste(d,(24,yline*8))
	return port	

def RGBA555(X):
	# stolen from mgba: https://github.com/mgba-emu/mgba/blob/26aea8544fc46c87b28541de4df744ef0ec4c518/include/mgba/core/interface.h
	COLOR=((((X) & 0x1F) << 3) | ( (((X) >> 5) & 0x1F) << 11) | ((((X) >> 10) & 0x1F) << 19))
	COLOR |= COLOR>>5 & 0x070707

	r=COLOR&0xFF
	g=(COLOR>>8)&0xFF
	b=(COLOR>>16)&0xFF
	return r,g,b,255


def loadPalette(f,offset):
	f.seek(offset)
	colors=struct.unpack('16H',f.read(32))
	colors = [RGBA555(color) for color in colors]
	colors[0]=(255,0,255,0)
	palette = Image.new('RGBA',(16,1))
	for i,color in enumerate(colors):
		palette.putpixel((i,0),color)
	
	return palette

palette_offset = 0xC97438


ports=[]
def loadNPortraits(f,offset,n):
	f.seek(offset)
	for porti in range(n):
		ports.append(loadPortrait(f))


def loadIndexedPortrait(f,i,palbase,portbase):
	global palette
	palette=loadPalette(f,palbase+i*32)
	loadNPortraits(f,portbase+1024*i,1)

with open('1460 - Shining Soul II (U).gba','rb') as f:
	for i in range(9):
		loadIndexedPortrait(f,i,0xC22858,0xC1E858)
	for i in range(16):
		loadIndexedPortrait(f,i,0xC26A58,0xc22A58)
	for i in range(16):
		loadIndexedPortrait(f,i,0xc972f8,0xC932F8)
	

	out=Image.new('RGBA',(32*16,64*3))
	for porti,port in enumerate(ports):
		out.paste(port,(32*(porti%16),64*(porti//16)))
	out.save('out.png')
