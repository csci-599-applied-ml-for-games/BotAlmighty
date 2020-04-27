import argparse
import sys
import base_model
import numpy as np
import os


class MarkovMarioGeneration:
    def __init__(self):
        pass

    def get_params(self):
        args = argparse.ArgumentParser(
            description="Input map path and required parameters"
        )
        args.add_argument(
            "-ns",
            "--num-states",
            help="Enter number of hidden states",
            type=int,
            required=True
        )

        args.add_argument(
            "-rm",
            "--req-maps",
            help="Enter number of samples",
            type=int,
            required=True
        )

        args.add_argument(
            "in_map",
            type=argparse.FileType("r"),
            help="Enter the input file path",
            default=sys.stdin
        )

        args = args.parse_args()
        return args.num_states, args.req_maps, args.in_map

    def parse_input_map(self, input_map):
        # Parse map line by line
        map_l = []
        for item in input_map:
            map_l.append(item.split())

        all_lengths = [len(item) for item in map_l]

        # Convert to normalized form
        map_e = [ele.lower() for item in map_l for ele in item]

        # Get horizontal transpose of the map
        map_h = ["".join([map_e[j][i] for j in range(len(map_e))]) for i in range(len(map_e[0]))]

        return map_h, all_lengths

    def write_output(self, rm, hmm_model, label_encoder):
        for _ in range(rm):
            map_length = 200
            entities, states = hmm_model.sample(map_length)
            comp_entities = np.squeeze(entities)

            new_state = label_encoder.inverse_transform(comp_entities)

            line_by_line = ([''.join(item) for item in zip(*new_state)])

            # Initialize file object
            output_file_path = os.path.join('output_level', 'output_markov.txt')
            file_obj = open(output_file_path, 'w')
            for index in range(len(line_by_line)):
                file_obj.write(line_by_line[index])
                if index != len(line_by_line)-1:
                    file_obj.write('\n')
                print(line_by_line[index])
            print()

    def model_transform(self, label_encoder, final_parsed_map):
        sequence = label_encoder.transform(final_parsed_map)

        # Get map features
        map_features = np.fromiter(sequence, np.int64)
        map_features = np.atleast_2d(map_features).T

        return map_features


# main()
mario_obj = MarkovMarioGeneration()

# Get user input
ns, rm, input_map = mario_obj.get_params()
final_parsed_map, all_lengths = mario_obj.parse_input_map(input_map)

# Get BaseModel object
bm_obj = base_model.BaseModel()

# Get Label Encoder
items = set(final_parsed_map)
label_encoder = bm_obj.get_label_encoder(items)
map_features = mario_obj.model_transform(label_encoder, final_parsed_map)

# Get HMM Model
hmm_model = bm_obj.get_hmm_model(ns)
hmm_model = hmm_model.fit(map_features)

# Write output map
mario_obj.write_output(rm, hmm_model, label_encoder)
print("New map written location: ./output_level/")
