import csv
import numpy as np
from . CB_inference import InferenceEngine, PreComputation
from . CBR import retrieval, adaptation


distances_def = [retrieval.dist2, retrieval.dist3, retrieval.dist5]


def load_CB(filename):
    X_CB = []
    Y_CB = []
    
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            X_CB.append(row[0])
            Y_CB.append(row[1])
    return X_CB, Y_CB


class AI_Teacher:
    
    def __init__(self,
                 CB_path,
                 questions):
        self.X_CB, self.Y_CB = load_CB(CB_path)
        self.precomputation = PreComputation(self.X_CB, self.Y_CB, questions, distances_def)
        
        # Initialization of the priors
        prior_cb = .5 * np.ones(len(self.X_CB))
        prior_dist = np.ones(len(distances_def)) / len(distances_def)
        prior_harmony = .5
        
        self.inference = InferenceEngine(prior_cb, prior_dist, prior_harmony)
        self.dict_X = { questions[i]: i for i in range(len(questions)) }
        
        
        
    def analyze_results(self, results):
        n_results = len(results['X'])
        
        for i in range(n_results):
            self.inference.update_probas(self.precomputation, 
                                         self.dict_X[results['X'][i]], 
                                         results['Y'][i])


    def predict_CB(self, n_data):
        return np.argpartition(self.inference.probas_cb, -n_data)
    
    def give_recommendations(self, n_recommendations):
        return list(range(n_recommendations))