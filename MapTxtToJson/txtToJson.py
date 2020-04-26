import json
from os import listdir

output_folder = '../Output'
output_files = [ifile for ifile in listdir(output_folder)]

level_count = 1

for folder in listdir(output_folder):
    if folder!='.DS_Store':
        for ifile in listdir(output_folder + '/' + folder):
            if ifile!='.DS_Store':

                model = folder

                # Produce the generic maps
                if model == 'RNN':
                    symbol_map = { "sky":["-"] , "coins":["?"] , "ground":["B","#"] , "pipe":["pP"], "koopa" : ["e"], "goomba":[] }    
                elif model == 'Markov':
                    symbol_map = { "sky":[" "] , "coins":["+","."] , "ground":["@"] , "pipe":["$","%"] , "koopa":["&"], "goomba":[] }
                elif model == 'PCG':
                    symbol_map = { "sky":["-"] , "coins":["o"] , "ground":["X","S"] , "pipe":["t","T"] , "koopa":["k","K","r"], "goomba":["g","G"] }

                # Perform the conversion
                input_file_path = output_folder + '/' + folder + '/' + ifile
                text_file = open(input_file_path,'r').read()
                text_file = text_file.split("\n")

                level = {}
                level["id"] = 100

                level_file = [string for string in text_file if string != ""]

                level["length"] = len(level_file[0])
                length = level["length"]
                width = len(level_file)

#                print("length:",length)
#                print("width:",width)


                # Adding pip coordinates
                pipes = []
                pipe_points = {}

                for i in range(len(level_file[0])):
                    for j in range(len(level_file)):
                        for element in symbol_map['pipe']:
                            if level_file[j][i]==element:
                                if(i in pipe_points):
                                    pipe_points[i][1] = pipe_points[i][1]+1
                                else:
                                    pipe_points[i]=[j,1]

                for k,v in pipe_points.items():
                    pipes.append([k,v[0],v[1]])    


                # Adding coin coordinates
                coins = []
                for i in range(len(level_file[0])):
                    for j in range(len(level_file)):
                        for element in symbol_map['coins']:
                            if level_file[j][i] == element:
                                coins.append([j,i])      


                # Adding ground coordinates                
                ground = []
                for i in range(len(level_file[0])):
                    for j in range(len(level_file)):
                        for element in symbol_map['ground']:            
                            if level_file[j][i] == element:
                                ground.append([i,j])   


                # Adding Goomba coordinates
                goomba = []
                for i in range(len(level_file[0])):
                    for j in range(len(level_file)):
                        for element in symbol_map['goomba']:            
                            if level_file[j][i] == element:
                                goomba.append([j,i])         


                # Adding Koopa coordinates
                koopa = []
                for i in range(len(level_file[0])):
                    for j in range(len(level_file)):
                        for element in symbol_map['koopa']:            
                            if level_file[j][i] == element:
                                koopa.append([j,i])         


                level["level"]={"objects": {"bush":[[10,12]], "sky":[[5,5]], "cloud":[[5,5]], "coin":coins, "pipe":pipes, "ground":ground}}
                level["level"]["layers"]={"sky":{"x":[0,length] , "y":[0,width-3]},  "ground":{"x":[0,length] , "y":[width-2,width]}   }
                level["level"]["entities"] = {"coin":coins,"randomBox":[[4,8]], "Goomba":goomba , "Koopa":koopa}
                
#                print(level_count)
                output_file_name = '../convertedJSONFiles/' + model + '/' + 'Level' + str(level_count) + '-1.json'
                with open(output_file_name, 'w') as outfile:
                    json.dump(level, outfile,indent = 3)

                level_count = level_count + 1







