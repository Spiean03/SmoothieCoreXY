'''
Python Laser Module GCode Generator. 

Save the image you want to the same folder as the script and change filename 
according to the file you want to engrave.
'''

from PIL import Image
import string 

'''
Input variables
Change filename according to the file you want to engrave
Change laser speed, width, Power offset
'''

filename="blackandwhite.jpg" #input filename (gray colormode)
laserwidth=0.2 #Laser beam size
dpi=300
speed=7200
minPower=0.0 #minimum power (for white)
maxPower=1.0 #maximum power (for black)
Zoffset=9 #for focal adjustement (z-offset)


'''
Converting the file
'''

im = Image.open(filename) 
name=string.split(filename,".") 
#print name[0]


data = list(im.getdata())
print("The file %s successfully loaded" %filename)
#print im.format, im.size, im.mode

width=round(float(im.size[0])/dpi*25.4,3)
height=round(float(im.size[1])/dpi*25.4,3)
print("Size of Image (width and height in mm): %s x %s" %(width,height))
#print width,height




nlines=int(height/laserwidth)
#nlines=10
nb=im.convert("L")
raster = nb.resize((im.size[0], nlines), Image.ANTIALIAS) 
#raster.show()

#print(nlines)


#gcode="G92 X0 Y0 Z0\n" #set actual position as X=0 and Y=0 
gcode ="G28 X Y\n" #Home the X and Y axes; move to 0,0
gcode +="G0 Z"+str(Zoffset)+"\n" #Rapid move to Z-offset position
#gcode += "M10\n" #Vacuum on (in case you have vacuum/filter to remove smoke)

power=-1
gcodelines=0
direction=1

for y in range(nlines-1):
	if direction==1:
	  startx=0
	else:
	  startx=im.size[0]	
	gcode +="G0 Y"+str(y*laserwidth)+" X"+str(round(float(startx)/dpi*25.4,3))+"\n"
	
	for x in range(im.size[0]):
		#newpower=round(raster.getpixel((x,y))/255,3)
		if direction==1:
		  curx=x
		else:
		  curx=im.size[0]-x-1 
			
		newpower=minPower+((maxPower-minPower)*(1-round(float(raster.getpixel((curx,y)))/255,2)))
		if power!=newpower or x==im.size[0]-1 :
			if x>1:			
				gcode +="G1 X"+str(round(float(curx-(1*direction))/dpi*25.4,3))+" S"+str(power)+" F"+str(speed)+"\n"
				gcodelines+=1
			power=newpower			
	direction=-direction
	
#gcode += "M11\n" #Vacuum off 
#gcode +="G0 XO Y0 Z0\n"
gcode +="G28 X Y\n" #After job completed, move to X,Y home


'''
Print GCode, write and save file
'''
print "The GCode has %s lines" %gcodelines

#witting file
gcodefile = open(name[0]+".gcode", 'w')
gcodefile.write(gcode)
gcodefile.close()
print "File saved as "+name[0]+".gcode"
