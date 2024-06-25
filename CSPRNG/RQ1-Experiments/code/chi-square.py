import pandas as pd
from scipy.stats import chisquare
import numpy as np

path = 'array2.csv'
data = pd.read_csv(path)

# change this to change number of bins 
bins = np.arange(0, 101, 5) # create 20 bins of 5 numbers (explained why in the report)
bin_labels = [f"{i}-{i+4}" for i in range(0, 100, 5)]
alpha = 0.05

# do not change any values beyond this point
data['Binned'] = pd.cut(data['Value'], bins=bins, labels=bin_labels, right=False)
observed_frequencies = data['Binned'].value_counts().sort_index()

total_numbers = len(data)
num_bins = len(bin_labels)
expected_frequency = total_numbers / num_bins

expected_frequencies = [expected_frequency] * num_bins

chi_square_stat, p_value = chisquare(f_obs=observed_frequencies, f_exp=expected_frequencies)

print(f"Chi-square statistic: {chi_square_stat}")
print(f"P-value: {p_value}")

if p_value < alpha:
    print("Reject the null hypothesis: Numbers are not uniformly distributed.")
else:
    print("No reason to reject: Numbers seem to be uniformly distributed")
