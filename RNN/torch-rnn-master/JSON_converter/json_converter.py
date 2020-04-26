# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 23:53:56 2020

@author: pritishrawal
"""
import json

#for now the boxes are ground
#there is no cloud or grass
map_dic = {"-":"sky", "?":"coins", "B":"ground", "#": "ground","pP":"pipe"} 
           
#aim is to convert text to json

"""
1. convert sky and ground
2. include entitites and objects
3. add clouds and grass

camera doesnt pan after 60, fix that, cant find root cause"
must configure ground
put objects accordingly

"""
#level_read = open("seq_linear_output.txt").read()
level_read = open("enemies_mario_2.txt").read()
#level_read = open("mario_1.txt").read()
#below line is for hardcoding only 60 as x axis limit
#level_read = level_read.split("\n")[:][:60]
#will demp this in json
level = {}
level["id"] = 100

level_parse_with_empty_strings = level_read.split("\n")
level_parse = [string for string in level_parse_with_empty_strings if string != ""]
level["length"] = len(level_parse[0])
#hard coding as 60
#level["length"] = 60`

length = level["length"]
#uncomment below line to read from text file 
width = len(level_parse)
#setting width by hard coding, and we already split level_read above
#width = 16

"""
check length and width
"""
#print("length:",length)
#print("width:",width)
#####################################
#pipewa
############################
pipes = []
pipe_points = {}
#get all points for pipe location
for i in range(len(level_parse[0])):
    for j in range(len(level_parse)):
        #print(j,i)
        if(level_parse[j][i]=="p"):
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
        if(level_parse[j][i]=="?"):
            coins.append([i,j])         


######################
#bricks above ground
#######################
ground = []

#get all points for pipe location
for i in range(len(level_parse[0])):
    for j in range(len(level_parse)):
        #print(j,i)
        if(level_parse[j][i]=="B"):
            ground.append([i,j])   

######################
#goomba -  e
#######################

goomba = []
for i in range(len(level_parse[0])):
    for j in range(len(level_parse)):
        #print(j,i)
        if(level_parse[j][i]=="e" and i+1<len(level_parse[0]) and level_parse[j][i+1]!="e" and level_parse[j][i-1]!="e"):
            goomba.append([i,8])             
######################
#koompa -  ee
#######################

koopa =[]
for i in range(len(level_parse[0])):
    for j in range(len(level_parse)):
        #print(j,i)
        if(level_parse[j][i]=="e" and i+1<len(level_parse[0]) and level_parse[j][i+1]=="e"):
            koopa.append([i,8])             

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
level["level"]["layers"]={"sky":{"x":[0,length] , "y":[0,width-3]},  "ground":{"x":[0,length] , "y":[width-2,width]}   }

"""
level["level"] = {}
level["level"]["layers"] = {"sky","ground"}
level["level"]["layers"]["sky"]["x"] = [0,length] 
level["level"]["layers"]["sky"]["y"] = [0,width]
"""
####################
#entities
#####################
level["level"]["entities"] = {"coin":coins,"randomBox":[[4,8]], "Goomba":goomba , "Koopa":koopa}

#level_op = json.dumps(level,indent = 3)
#naming is imp
with open(r'G:\Study\USC\ML for games\super-mario-python-master\levels\Level69-1.json', 'w') as outfile:
#with open(r'temp1.json', 'w') as outfile:
    json.dump(level, outfile,indent = 3)