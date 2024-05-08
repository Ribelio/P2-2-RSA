import platform
import subprocess
import os

try:
    import csprng
except ModuleNotFoundError:
    subprocess.check_call(['pip', 'install', 'csprng'])
    import csprng

try:
    import numpy as np
except ModuleNotFoundError:
    subprocess.check_call(['pip', 'install', 'numpy'])
    import numpy as np

try:
    import pandas as pd
except ModuleNotFoundError:
    subprocess.check_call(['pip', 'install', 'pandas'])
    import pandas as pd

try:
    import cpuinfo
except ModuleNotFoundError:
    subprocess.check_call(['pip', 'install', 'py-cpuinfo'])
    import cpuinfo

csprng = csprng.CSPRNG(32)

# number of RNGs we are going to create as a sample from user X
count_to_generate = 1000 

device_test_numbers = np.empty(count_to_generate, dtype=int)

for i in range(0, count_to_generate):
    device_test_numbers[i] = csprng.rand_int(0, 100)

print(len(device_test_numbers))
print(device_test_numbers)

# generate file 1: array of random numbers 
df = pd.DataFrame(device_test_numbers, columns=['Value'])
df.to_csv('array.csv', index_label='Index')

##################################################################

ops = platform.system()
bits = platform.architecture()

cpu_info = cpuinfo.get_cpu_info()
processor = cpu_info['brand_raw']
arch = cpu_info['arch']
threads = cpu_info['count']

system_info = {
    'OS': ops,
    'Bits': bits,
    'CPU': processor,
    'Architecture': arch,
    'Threads': threads
}

# generate file 2: system information
with open('system_info.txt', 'w') as file:
    for key, value in system_info.items():
        file.write(f"{key}: {value}\n")