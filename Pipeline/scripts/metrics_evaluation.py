import json
from os import listdir, path
from random import randint

class ModelEvaluation:
	def __init__(self):
		# Model output files and names
		# self.model_jsons = ['/Users/test/.jenkins/workspace/Mario_DDA_Master/output_json/Markov.json',
		# 					'/Users/test/.jenkins/workspace/Mario_DDA_Master/output_json/RNN.json',
		# 					'/Users/test/.jenkins/workspace/Mario_DDA_Master/output_json/PCG.json']
		# self.model_jsons = ['/Users/test/.jenkins/workspace/Mario_DDA_Master/output_json/output_markov.json',
		# 					'/Users/test/.jenkins/workspace/Mario_DDA_Master/output_json/output_rnn.json',
		# 					'/Users/test/.jenkins/workspace/Mario_DDA_Master/output_json/output_pcg.json']
		self.model_jsons = listdir('output_json/')


	def parse_json(self):
		# Model json dictionaries to store json data		
		markov_dict, rnn_dict, pcg_dict = {}, {}, {}
		model_dicts = [markov_dict, rnn_dict, pcg_dict]
		model_names = ['markov', 'rnn', 'pcg']

		# Parse json files into model json dictionaries
		for index in range(len(model_names)):
			if index == 0:
				file_path = path.join('output_json', 'output_markov.json')
			elif index == 1:
				file_path = path.join('output_json', 'output_rnn.json')
			else:
				file_path = path.join('output_json', 'output_pcg.json')
			
			with open(file_path, 'r') as file_obj:
				model_dicts[index] = json.load(file_obj)
		return model_dicts, model_names

	def calculate_model_params(self, model_dicts, model_names):
		# Model dictionaries to store object parameters
		markov_params, rnn_params, pcg_params = {}, {}, {}
		model_params = [markov_params, rnn_params, pcg_params]

		# Calculate parameters for each model
		for index in range(len(model_names)):

			# Calculate object properties
			# Calculate Map length
			if 'length' in model_dicts[index]:
				model_params[index]['map_length'] = float(model_dicts[index]['length'])
			else:
				model_params[index]['map_length'] = 0

			# Calculate number of pipes
			if 'objects' in model_dicts[index]['level']:
				if 'pipe' in model_dicts[index]['level']['objects']:
					model_params[index]['num_pipes'] = float(len(model_dicts[index]['level']['objects']['pipe']))
			else:
				model_params[index]['num_pipes'] = 0

			# Calculate Ground length
			if 'objects' in model_dicts[index]['level']:
				if 'ground' in model_dicts[index]['level']['objects']:
					model_params[index]['ground_length'] = float(len(model_dicts[index]['level']['objects']['ground']))
			else:
				model_params[index]['ground_length'] = 0

			# Calculate all Obstacles
			# Calculate number of Goombas
			if 'Goomba' in model_dicts[index]['level']['entities']:
				num_goombas = float(len(model_dicts[index]['level']['entities']['Goomba']))
			else:
				num_goombas = float(0)
			
			# Calculate number of Koopas
			if 'Koopa' in model_dicts[index]['level']['entities']:
				num_koopas = float(len(model_dicts[index]['level']['entities']['Koopa']))
			else:
				num_koopas = float(0)

			# Calculate all Rewards
			# Calculate number of coins
			if 'coin' in model_dicts[index]['level']['entities']:
				num_coins = float(len(model_dicts[index]['level']['entities']['coin']))
			else:
				num_coins = float(0)

			# Calculate number of random boxes
			if 'randomBox' in model_dicts[index]['level']['entities']:
				num_randomboxes = float(len(model_dicts[index]['level']['entities']['randomBox']))
			else:
				num_randomboxes = float(0)

			model_params[index]['num_enemies'] = num_goombas + num_koopas
			model_params[index]['num_rewards'] = num_coins + num_randomboxes

		# Identify map with pipe height more than 4 units
		unplayable_levels = {}
		for model_name in model_names:
			unplayable_levels[model_name] = False

		for index in range(len(model_dicts)):
			for pipe_config in model_dicts[index]['level']['objects']['pipe']:
				if pipe_config[2] > 4:
					unplayable_levels[model_names[index]] = True
					break

		# print('model_params: ', model_params)
		return model_params, unplayable_levels

	def calculate_eval_metrics(self, model_params, unplayable_levels, model_names):

		# Calculate difficulty percentages for each model
		# More the difficulty, more difficulty is the level
		# If unplayability for any model is True, then difficulty will be highest

		model_eval = {}
		for index in range(len(model_names)):
			if not unplayable_levels[model_names[index]]:
				if model_params[index]['map_length'] != 0:
					random_range = model_params[index]['map_length'] // 4
					num_pits = randint(0, random_range)
					fall_percentage = num_pits / model_params[index]['map_length']
					rewards_percentage_comp = (model_params[index]['map_length'] - model_params[index]['num_rewards']) / model_params[index]['map_length']
					rewards_percentage_comp = rewards_percentage_comp * 0.15
				else:
					fall_percentage = 1
					rewards_percentage_comp = 1
				
				if model_params[index]['map_length'] != 0:
					pipe_percentage = model_params[index]['num_pipes'] / model_params[index]['map_length']
					enemies_percentage = model_params[index]['num_enemies'] / model_params[index]['map_length']
				else:
					pipe_percentage = 1
					enemies_percentage = 1
				# print('fall_percentage: {}, pipe_percentage: {}, enemies_percentage: {}, rewards_percentage_comp: {}'.format(fall_percentage, pipe_percentage, enemies_percentage, rewards_percentage_comp))
				model_eval[model_names[index]] = ((fall_percentage + pipe_percentage + enemies_percentage + rewards_percentage_comp) / 4) * 100
			else:
				model_eval[model_names[index]] = float('inf')

		# Sort Model evaluation as per increasing difficulty level
		model_eval_out = sorted(model_eval.items(), key=lambda item:item[1])
		# print('model_eval_out: ', model_eval_out)
		return model_eval_out

print('*******************************************************************************************\n')
print('Metrics Evaluation results')
# Initiate evaluation
model_eval_obj = ModelEvaluation()

# Parse JSON files and store in dictionaries
model_dicts, model_names = model_eval_obj.parse_json()

# Calculate object parameters for models and also associate unplayability
model_params, unplayable_levels = model_eval_obj.calculate_model_params(model_dicts, model_names)

# Evalaute model playability
model_evaluation = model_eval_obj.calculate_eval_metrics(model_params, unplayable_levels, model_names)

# Remove levels which are unplayable
for item in model_evaluation:
	if item[1] == float('inf'):
		print('\nLevel found with objects of unstatisfying constraints: Pipe height')
		print('Deleted Unplayable Model level: {}\n'.format(item[0]))
		model_evaluation.remove(item)

# Output individual difficulty model percentages
print('Model level difficulty')
for item in model_evaluation:
	print('{}: {:.2f}%'.format(item[0], item[1]))

# Output level as per the user requirement
user_level = 'Easy'
# user_level = 'Difficult'
if user_level == 'Easy':
	print('\nUser selected level: Easy')
	output_level = model_evaluation[0][0]
else:
	print('\nUser selected level: Difficult')
	output_level = model_evaluation[-1][0]

print('\nOutput level: {}'.format(output_level))

# Output model value
if output_level == 'markov':
	print(0)
elif output_level == 'rnn':
	print(1)
else:
	print(2)
print('*******************************************************************************************\n')
