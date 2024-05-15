from . CB_inference import Evaluation, InferenceEngine
import random
from typing import Tuple, List, Set
import copy
import numpy as np
from itertools import combinations

class SimulatedAnnealing:
    
    def __init__(self, n_reco: int, max_step: int, temperature: int, possible_actions: Set[int]):
        self.max_step = max_step
        self.n_reco = n_reco
        self.temperature = temperature
        self.possible_actions = possible_actions
        self.solution = random.sample(list(possible_actions), n_reco)
        
        
    def neighbors(self):
        current_solution = copy.copy(self.solution)
        actions = self.possible_actions.difference(set(current_solution))
        
        return



def evaluate_action(evaluation: Evaluation,
                    action: Tuple[int], 
                    inference: InferenceEngine):
    new_inference = copy.deepcopy(inference)
    new_inference.probas_cb[list(action)] = 1
    return evaluation.evaluate(new_inference)
        
    
    

def get_actions(n_cards: int, predicted_cards: List[int]) -> Set[int]:
    return set(range(n_cards)).difference(set(predicted_cards))



def recommendation_bruteforce(inference: InferenceEngine,
                              evaluation: Evaluation,
                              n_reco: int, 
                              possible_cards: Set[int]):
    
    recos_by_n = []
    scores_by_n = []
    
    for n in range(1, n_reco+1):
        actions = list(combinations(possible_cards, n))
        scores = [evaluate_action(evaluation, action, inference) for action in actions]
        
        argmax = np.argmax(scores)
        recos_by_n.append(actions[argmax])
        scores_by_n.append(scores[argmax])
    
    return recos_by_n[np.argmax(scores_by_n)]
    
    
    
def recommendation_greedy(inference: InferenceEngine,
                              evaluation: Evaluation,
                              n_reco: int, 
                              possible_cards: Set[int],
                              current_score=0):
    if n_reco == 0: return []
    actions = []
    scores = []
    for card in possible_cards:
        actions.append(card)
        scores.append(evaluate_action(evaluation, (card,), inference))
    
    idx_action = np.argmax(scores)
    if scores[idx_action] == current_score: return []
    
    
    new_inference = copy.deepcopy(inference)
    new_inference.probas_cb[idx_action] = 1
    
    new_possible_cards = copy.deepcopy(possible_cards)
    new_possible_cards.remove(actions[idx_action])
    
    return [actions[idx_action]] + recommendation_greedy(new_inference, 
                                                         evaluation, 
                                                         n_reco-1,
                                                         new_possible_cards, 
                                                         scores[idx_action])



def make_recommendations(inference: InferenceEngine,
                         evaluation: Evaluation,
                         n_reco: int, 
                         max_step: int, 
                         initial_temperature: int, 
                         n_cards: int, 
                         predicted_cards: List[int]):
    
    possible_cards = get_actions(n_cards, predicted_cards)
    return recommendation_bruteforce(inference, evaluation, n_reco, possible_cards)

