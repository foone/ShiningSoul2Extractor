from PIL import Image
import struct,sys
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

class ROM(object):
	def __init__(self,code):
		self.code=code
		self.offsets=[]
	def add(self,palbase,portbase):
		self.offsets.append((palbase,portbase))
	def base(self, i):
		return self.offsets[i]

USROM=ROM('AU2E')
USROM.add(0xC22858,0xC1E858)
USROM.add(0xC26A58,0xC22A58)
USROM.add(0xc972f8,0xC932F8)

JPROM=ROM('AU2J')
JPROM.add(0xBFAEA4,0xBF6EA4)
JPROM.add(0xBFF0A4,0xbfb0a4)
JPROM.add(0xC6F944,0xC6B944)


EUROM=ROM('AU2P')
EUROM.add(0xC30014,0xC2C014)
EUROM.add(0xC34214,0xC30214)
EUROM.add(0xCA4AB4,0xCA0AB4)

ROMS=[USROM,JPROM,EUROM]
ports=[]
def loadNPortraits(f,offset,n):
	f.seek(offset)
	for porti in range(n):
		ports.append(loadPortrait(f))

def loadIndexedPortrait(f,i,palbase,portbase):
	global palette
	palette=loadPalette(f,palbase+i*32)
	loadNPortraits(f,portbase+1024*i,1)

def findROM(f):
	f.seek(0xAC)
	code=f.read(4)
	for rom in ROMS:
		if rom.code==code:
			return rom
	print("Couldn't find a matching ROM for {}".format(code))
	sys.exit(1)
if __name__=='__main__':
	if len(sys.argv)<2:
		print 'Usage: readportraits.py <foobar.gba>'
		sys.exit(1)
	with open(sys.argv[1],'rb') as f:
		rom=findROM(f)
		for i in range(9):
			loadIndexedPortrait(f,i,*rom.base(0))
		for i in range(16):
			loadIndexedPortrait(f,i,*rom.base(1))
		for i in range(16):
			loadIndexedPortrait(f,i,*rom.base(2))
		

		out=Image.new('RGBA',(32*16,64*3))
		for porti,port in enumerate(ports):
			out.paste(port,(32*(porti%16),64*(porti//16)))
		out.save('out.png')