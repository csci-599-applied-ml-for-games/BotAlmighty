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

imglines = imglines[::-1]

def adjacent(data, x, y):
    above     = data[y-1][x  ] if 0 < y < height-1 else None
    left      = data[y  ][x-1] if 0 < x            else None
    leftleft  = data[y  ][x-2] if 1 < x            else None
    aboveleft = data[y-1][x-1] if above and left   else None
    return above, left, leftleft, aboveleft
table = {}

for y, line in enumerate(imglines):
    for x, pixel in enumerate(line):
        key = (y,) + adjacent(imglines, x, y)
        table.setdefault(key, []).append(pixel)

output = []

for y in range(height):
    output.append([])
    for x in range(width):
        key = (y,) + adjacent(output, x, y)
        output[-1].append(random.choice(table.get(key, bgpixel)))

output = output[::-1]
print("output")
print(output)


output_file = '../Output/Markov/output_markov.txt'
ofile = open(output_file,'w')
for line in output:
    for element in line:
        ofile.write(element)
    ofile.write("\n")



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
