from hmmlearn import hmm
from sklearn.preprocessing import LabelEncoder


class BaseModel:
    def __init__(self):
        pass

    def get_hmm_model(self, n_states):
        model = hmm.MultinomialHMM(
            n_components=n_states,
            n_iter=40,
            init_params='ste',
            verbose=True)

        return model

    def get_label_encoder(self, input):
        label_encoder = LabelEncoder()
        input_list = list(input)
        label_encoder.fit(input_list)

        return label_encoder
