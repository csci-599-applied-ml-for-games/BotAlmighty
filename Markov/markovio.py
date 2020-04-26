#!/usr/bin/env python

import subprocess, sys, re, random, getopt
import json

usage = """\
usage: %s [options] [inputfile]

options:
    -h,   --help:           this help.
    -b x, --bg-pixel=x:     background pixel character of x.  default is space.
    -s x, --output-scale=x: how large to magnify output png.  default is 8.

input file defaults to "./input.xpm".  it must be an xpm in a similar format to
the ones made by the gimp.""" % sys.argv[0]


opts, args = getopt.getopt(sys.argv[1:], "hb:s:", ["help", "bg-pixel=", "output-scale="])

#except getopt.GetoptError, e:
#    print str(e)
#    print
#    print usage
#    sys.exit(2)

bgpixel = ' '
outputscale = 8
infile = open(args[0] if args else 'input.xpm')

for o, a in opts:
    if o in ('-b', '--bg-pixel'):
        assert len(a) == 1
        bgpixel = a
    elif o in ('-s', '--output-scale'):
        outputscale = int(a)
    elif o in ('-h', '--help'):
        print(usage)
        sys.exit(0)

def raw_line_data(line):
    return line.lstrip('"').rstrip('"},;\n')

lines = [ line for line in infile.readlines() if line.strip() ]
width = len(raw_line_data(lines[-1]))
imglines = [ raw_line_data(line) for line in lines if len(line) > width ]
height = len(imglines)
header = lines[:-height]

# reversed because building from bottom to top and right to left works better
imglines = imglines[::-1]

def adjacent(data, x, y):
    above     = data[y-1][x  ] if 0 < y < height-1 else None
    left      = data[y  ][x-1] if 0 < x            else None
    leftleft  = data[y  ][x-2] if 1 < x            else None
    aboveleft = data[y-1][x-1] if above and left   else None
    return above, left, leftleft, aboveleft

# build markov chains

table = {}

for y, line in enumerate(imglines):
    for x, pixel in enumerate(line):
        key = (y,) + adjacent(imglines, x, y)
        table.setdefault(key, []).append(pixel)

# generate output

output = []

for y in range(height):
    output.append([])
    for x in range(width):
        key = (y,) + adjacent(output, x, y)
        output[-1].append(random.choice(table.get(key, bgpixel)))

# un-reverse only vertically -- but leave horizontal alone.  why does this work
# best?  who the hell knows?

output = output[::-1]
print("output")
print(output)
# write


####################### CONVER TO DICTIONARY #############################
map_dic = {" ":"sky", ".":"coins", "+":"coins", "@":"ground", "$":"pipe", "%":"pipe" } 

level = {}
level["id"] = 100

#level_parse_with_empty_strings = level_read.split("\n")
#level_parse = [string for string in level_parse_with_empty_strings if string != ""]
level_parse = output
level["length"] = len(level_parse[0])
#hard coding as 60
#level["length"] = 60

length = level["length"]
#uncomment below line to read from text file 
width_mario = len(level_parse)
#setting width by hard coding, and we already split level_read above
#width = 16
"""
check length and width
"""
print("length:",length)
print("width:",width_mario)
#####################################
#pipewa
############################
pipes = []
pipe_points = {}
#get all points for pipe location
for i in range(len(level_parse[0])):
    for j in range(len(level_parse)):
        #print(j,i)
        if level_parse[j][i]=="$" or level_parse[j][i]=="%" :
            if(i in pipe_points):
                pipe_points[i][1] = pipe_points[i][1]+1
                
            else:
                pipe_points[i]=[j,1]




for k,v in pipe_points.items():
    pipes.append([k,v[0],v[1]])    



######################
#coints
#######################
coins = []

#get all points for pipe location
for i in range(len(level_parse[0])):
    for j in range(len(level_parse)):
        #print(j,i)
        if level_parse[j][i]=="." or level_parse[j][i]=="+":
            coins.append([i,j])         


######################
#bricks above ground
#######################
ground = []

#get all points for pipe location
for i in range(len(level_parse[0])):
    for j in range(len(level_parse)):
        if(level_parse[j][i]=="@"):
            ground.append([i,j]) 

"""
part 2
level["level"]["objects"] ----> bush, sky, cloud, pipe, ground
"""
##################
#### Part 2 #####
#################

#hard coding for now
level["level"]={"objects": {"bush":[[10,12]] ,  "sky":[[48,11]] , "cloud":[[5,5]]  ,   "pipe":pipes , "ground":ground}}


#print(level)
################
####  Part 1 ##
###############
#level["level"]={"layers":{"sky":{"x":[0,length] , "y":[0,width-2]},  "ground":{"x":[0,length] , "y":[width-1,width]}   }}
level["level"]["layers"]={"sky":{"x":[0,length+1] , "y":[0,width_mario-3+1]},  "ground":{"x":[0,length+1] , "y":[width_mario-2+1,width_mario+1]}   }

"""
level["level"] = {}
level["level"]["layers"] = {"sky","ground"}
level["level"]["layers"]["sky"]["x"] = [0,length] 
level["level"]["layers"]["sky"]["y"] = [0,width]
"""
####################
#entities
#####################
level["level"]["entities"] = {"coin":coins,"randomBox":[[4,8]], "Goomba":[[9,12]] , "Koopa":[[9,25]]}

#level_op = json.dumps(level,indent = 3)
#naming is imp
with open('Level1-1.json', 'w') as outfile:
    json.dump(level, outfile,indent = 3)



#########################################################################




#prefix = '/tmp/markovio1.out'
prefix = 'here'
xpm = prefix+'.xpm'
png = prefix+'.png'

f = open(xpm, 'w')
f.write(''.join(header))

for y in range(height):
    f.write('"')
    for x in range(width):
        f.write(output[y][x])
    f.write('"')

    if y < height-1:
        f.write(',\n')
    else:
        f.write('};')

f.close()

print(open(xpm, 'r').read())
print(sys.stdout.write("the above xpm image was written to %s" % xpm))

try:
    subprocess.Popen([
        "convert", '-scale',
        "%dx%d" % (width*outputscale, height*outputscale),
        xpm, png
    ]).wait()
except OSError:
    print(",\nalthough conversion from xpm to png didn't work.")
    print("do you have the 'convert' utility installed (from imagemagick)?")
else:
    print(" and\nalso converted to %s, scaled up %d times" % (png, outputscale))


