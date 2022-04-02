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
	def __init__(self,code,font_base,num_chars,font_width):
		self.code=code
		self.font_base=font_base
		self.num_chars=num_chars
		self.font_width=font_width
		self.offsets=[]
	def add(self,palbase,portbase):
		self.offsets.append((palbase,portbase))
	def base(self, i):
		return self.offsets[i]


USROM=ROM('AU2E',0x928e9c,89,8)
USROM.add(0xC22858,0xC1E858)
USROM.add(0xC26A58,0xC22A58)
USROM.add(0xc972f8,0xC932F8)

JPROM=ROM('AU2J',0x8D94E8,1791,16)
JPROM.add(0xBFAEA4,0xBF6EA4)
JPROM.add(0xBFF0A4,0xbfb0a4)
JPROM.add(0xC6F944,0xC6B944)


EUROM=ROM('AU2P',0x92C028,153,8)
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

def loadLetter(f,offset,font_width):
	letter=Image.new('RGBA',(font_width,16))
	f.seek(offset)
	# this could be done smarter. I'm not smart enough to do it right now
	if font_width==8:
		letter.paste(readTile(f),(0,0))
		letter.paste(readTile(f),(0,8))
	if font_width==16:
		letter.paste(readTile(f),(0,0))
		letter.paste(readTile(f),(8,0))
		letter.paste(readTile(f),(0,8))
		letter.paste(readTile(f),(8,8))

	return letter

def loadFontPalette():
	global palette
	palette=Image.new('RGBA',(16,1))
	COLORS=[
		(  0,156,165),
		(255,255,230),
		( 49, 57, 57),
		(  8, 16, 25),
		( 16,255,222),
		(107,231,247),
		( 66,189,214),
		(239,148, 33),
		(255,198, 99),
		(214,222,198),
		(255,115,  0),
		(255,222,  0),
		(107,123,148),
		( 90,148,156),
		(  0, 82, 82),
		(123,255,  0)
	]
	for i in range(16):
		palette.putpixel((i,0),COLORS[i])

def loadFont(f,base_offset,num_letters,font_width):
	loadFontPalette()
	out=Image.new('RGBA',(num_letters*font_width,16))
	for i in range(num_letters):
		im=loadLetter(f,base_offset+i*128,font_width)
		out.paste(im,(i*font_width,0))
	return out

if __name__=='__main__':
	if len(sys.argv)<2:
		print 'Usage: extract_ss2.py <foobar.gba>'
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

		im=loadFont(f,rom.font_base,rom.num_chars,rom.font_width)
		im.save('font.png')