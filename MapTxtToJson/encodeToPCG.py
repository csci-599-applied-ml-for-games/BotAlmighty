import json
from os import listdir

output_folder = '../Output'
output_files = [ifile for ifile in listdir(output_folder)]

level_count = 16


for ifile in output_files:
	if ifile!='.DS_Store':
		output_file_path = '../PCG/src/levels/original/lvl-' + str(level_count) + '.txt'
		output_file = open(output_file_path,'w')

		text_file = open(output_folder+'/'+ifile,'r').read()
		text_file = text_file.split("\n")

		level_file = [string for string in text_file if string != ""]

		pcg_line = ""
		length = len(level_file[0])
		width = len(level_file)
		print("Length ", length)
		print("Width ", width)

		#F coordinate
		#width - 3 
		#length - 2 

		l = 0
		w = 0
		for line in level_file:	
			l = 0
			for element in line:
				print(l)
				print(w)
				# Introduce the Final Coordinate
				if (l == (length - 2)) and (w == (width - 3)):
					pcg_line += "F"
					print(pcg_line)

				else:
					if element == " " or element == "-":
						pcg_line += "-"

					elif element == "+" or element == "." or element == "?" or element == 'o':
						pcg_line += "o"

					elif element == "@" or element == "B" or element == "#" or element == 'X' or element == 'S':
						pcg_line += "X"

					elif element == "$" or element == "%" or element == "P" or element == "p" or element == "t" or element == "T":
						pcg_line += "t"

					elif element == "&" or element == "e" or element == "k" or element == "K" or element == "r":
						pcg_line += "k"
					else:
						pcg_line += '-'

				l = l + 1
			
			pcg_line += "\n"
			w = w + 1

		output_file.write(pcg_line)
		output_file.close()

		level_count += 1 

