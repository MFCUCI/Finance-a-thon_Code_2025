import numpy as np
import sympy
import PIL
import matplotlib.pyplot as plt
import random
import numpy_financial as npf
from scipy.optimize import fsolve
import scipy.stats as stats
import math


class MarkovChain:
   def __init__(self, states, transition_matrix):
       self.states = states
       self.transition_matrix = np.array(transition_matrix)
       self.state_index = {state: i for i, state in enumerate(states)}


   def next_state(self, current_state):
       current_idx = self.state_index[current_state]
       next_state_idx = np.random.choice(
           range(len(self.states)),
           p=self.transition_matrix[current_idx]
       )
       return self.states[next_state_idx]


   def generate_sequence(self, start_state, length):
       sequence = [start_state]
       current_state = start_state
       for _ in range(length - 1):
           current_state = self.next_state(current_state)
           sequence.append(current_state)
       return sequence


# Example usage

states = ['No Crash', 'Minor Crash', 'Major Crash']
transition_matrix = [
   [],  # Given No Crash last year -> probabilities of No Crash, Minor Crash, Major Crash in the next 10 years
   [],    # Given Minor Crash last year -> ...
   [], # Given Major Crash last year -> ...
]


markov = MarkovChain(states, transition_matrix)
sequence = markov.generate_sequence('No Crash', 10)

print("Example Sequence:") # Not needed, just to show how the chain works for one iterations $
print(sequence)

# Initialize Markov Chain
markov = MarkovChain(states, transition_matrix)

# Simulation parameters
num_simulations = 100000 # VERY IMPORTANT this will be used for ALL models. Adjust according to your desired accuracy, as more simulations are more accurate but take longer. #
sequence_length = 11
start_state = 'No Crash'


crash_occurrences = 0




# Run simulations

crash_count_minor = 0

for _ in range(num_simulations):
   sequence = markov.generate_sequence(start_state, sequence_length)
   new_array1 = sequence[1:]
   crash_count_minor += sum(1 for state in new_array1 if state != 'No Crash' and state != 'Major Crash')

crash_count_major = 0

for _ in range(num_simulations):
   sequence = markov.generate_sequence(start_state, sequence_length)
   new_array1 = sequence[1:]
   crash_count_major += sum(1 for state in new_array1 if state != 'No Crash' and state != 'Minor Crash')

# Calculate and print the probability

print(f"For every {num_simulations} Low Risk Clients, we expect {crash_count_minor} total Minor crashes over 10 years")
print(f"For every {num_simulations} Low Risk Clients, we expect {crash_count_major} total Major crashes over 10 years")





# Simulation parameters given Minor Crash this year #

sequence_length = 11
start_state = 'Minor Crash'
crash_occurrences = 0

crash_count_minor = 0

for _ in range(num_simulations):
   sequence = markov.generate_sequence(start_state, sequence_length)
   new_array1 = sequence[1:]
   crash_count_minor += sum(1 for state in new_array1 if state != 'No Crash' and state != 'Major Crash')

crash_count_major = 0

for _ in range(num_simulations):
   sequence = markov.generate_sequence(start_state, sequence_length)
   new_array1 = sequence[1:]
   crash_count_major += sum(1 for state in new_array1 if state != 'No Crash' and state != 'Minor Crash')


# Calculate and print the probability
crash_probability = crash_occurrences / num_simulations
print(f"For every {num_simulations} Mid Risk Clients, we expect {crash_count_minor} total Minor crashes over 10 years")
print(f"For every {num_simulations} Mid Risk Clients, we expect {crash_count_major} total Major crashes over 10 years")








# Simulation parameters given that the client has been in a major crash this year #

sequence_length = 11
start_state = 'Major Crash'

# Run simulations

crash_count_minor = 0

for _ in range(num_simulations):
   sequence = markov.generate_sequence(start_state, sequence_length)
   new_array1 = sequence[1:]
   crash_count_minor += sum(1 for state in new_array1 if state != 'No Crash' and state != 'Major Crash')

crash_count_major = 0

for _ in range(num_simulations):
   sequence = markov.generate_sequence(start_state, sequence_length)
   new_array1 = sequence[1:]
   crash_count_major += sum(1 for state in new_array1 if state != 'No Crash' and state != 'Minor Crash')

# Calculate and print the probability

print(f"For every {num_simulations} High Risk Clients, we expect {crash_count_minor} total Minor crashes over 10 years")
print(f"For every {num_simulations} High Risk Clients, we expect {crash_count_major} total Major crashes over 10 years")




