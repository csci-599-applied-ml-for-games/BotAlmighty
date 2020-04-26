import numpy as np


with open('../output_level.txt', 'r') as file_obj:
    level_str = file_obj.read()

mod_13 = len(level_str) % 13
input_test = level_str[:-mod_13]
num_cols = len(input_test) // 13

input_list = list(input_test)
input_len = len(input_list)


target = np.zeros([13, 1])

for index in range(num_cols):
    new_column = list(input_test[(index*13) : (index*13)+13])
    col_add = list(map(list, new_column))
    target = np.append(target, col_add, axis = 1)

target = np.delete(target, 0, 1)

level_out = []
for index in range(13):
    line = "".join(target[index])
    level_out.append(line)

g1, g2 = level_out[0], level_out[1]
level_out.pop(0)
level_out.pop(0)
level_out.append(g1)
level_out.append(g2)

for index in range(13):
    print(level_out[index])

with open('../Output/output_rnn.txt', 'w') as file_obj:
    for index in range(13):
        file_obj.write(level_out[index])
        if index < 12:
            file_obj.write('\n')
