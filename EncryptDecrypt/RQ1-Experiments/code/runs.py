import pandas as pd
import numpy as np

path = 'EncryptDecrypt/RQ1-Experiments/data/win64_2.csv'
data = pd.read_csv(path)

# parameters that are adjusted
lower = 0
upper = 99
values = 1000

# do not change values beyond this point
mean_of_uniform_dist = (upper + lower) / 2

above_the_mean = 0
below_the_mean = 0

for value in data['Value']:
    if value > mean_of_uniform_dist:
        above_the_mean += 1
    elif value < mean_of_uniform_dist:
        below_the_mean += 1

# runs are defined as: length of sequence of numbers that are above (below) the mean before a value below (above) the mean is generate
current_run_length = 0
total_runs = 0
prev_value = None

for value in data['Value']:
    if prev_value is None:
        prev_value = value
        continue
    
    if value > mean_of_uniform_dist and prev_value <= mean_of_uniform_dist:
        total_runs += 1
    elif value < mean_of_uniform_dist and prev_value >= mean_of_uniform_dist:
        total_runs += 1
    
    prev_value = value

if prev_value is not None and prev_value != mean_of_uniform_dist:
    total_runs += 1

print("Total number of runs:", total_runs)

final_mean = ((2 * (above_the_mean) * (below_the_mean)) / values ) + 0.5 # i put 0.5 because that is what we used in SSA, even though online it says 1
final_variance = (2 * (above_the_mean) * (below_the_mean) * (2 * (above_the_mean) * (below_the_mean) - values)) / ((values * values)*(values - 1))

test_statistic = (total_runs - final_mean) / np.sqrt(final_variance)

print("Final mean:", final_mean)
print("Final variance", final_variance)
print("Test statistic:", test_statistic)

z_alpha_half = 1.96

if test_statistic >= (-z_alpha_half) and test_statistic <= z_alpha_half:
    print("No reason to reject the null hypothesis. The data does not show non-random patterns.")
else:
    print("Reject null hypothesis. The data may not be random.")
