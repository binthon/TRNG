import spidev
import time
import hashlib
import matplotlib.pyplot as plt
from collections import Counter

# SPI initialization
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# read data form spi
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# count value from ADC to voltage
def convert_to_voltage(adc_value):
    return (adc_value * 3.3) / 1023  # 3.3V benchmark voltage

# generate a random number based on voltage
def generate_random_number(min_val, max_val):
    samples = []
    voltages = []
    
    # default 100 samples from CH0, can change
    for _ in range(100):
        value = read_channel(0)
        voltage = convert_to_voltage(value)
        samples.append(value)
        voltages.append(voltage)
        time.sleep(0.01)  # #Default value, can change

    # download every third value
    selected_samples = samples[::3]

    # Sum of selected samples
    total = sum(selected_samples)
    
    # hashing for better randomness
    hash_object = hashlib.sha256(str(total).encode())
    hash_hex = hash_object.hexdigest()
    hash_int = int(hash_hex, 16)
    
    # use hash to generate random number
    random_value = hash_int % (max_val - min_val + 1) + min_val
    
    return samples, voltages, random_value

try:
    min_val = int(input("Enter min range value: "))
    max_val = int(input("Enter max range value: "))
    num_samples = int(input("Enter number of samples: "))
    
    random_numbers = []
    all_samples = []
    all_voltages = []
    
    for _ in range(num_samples):
        samples, voltages, random_number = generate_random_number(min_val, max_val)
        random_numbers.append(random_number)
        all_samples.append(samples)
        all_voltages.append(voltages)
        print(f"Voltage of sample (V): {voltages}")
        print(f"Random number: {random_number}")
        time.sleep(0.5)  # interval between drawn numbers, can change
    
    # count appearances of every number
    counter = Counter(random_numbers)
    
    # create list for chart
    all_values = list(range(min_val, max_val + 1))
    occurrences = [counter.get(i, 0) for i in all_values]
    
    # chart creation
    plt.bar(all_values, occurrences)
    plt.xlabel('Number')
    plt.ylabel('Number appearances')
    plt.title('Histogram of the random numbers')
    plt.xticks(all_values, rotation=90) 
    plt.tight_layout() 
    plt.show()

except KeyboardInterrupt:
    spi.close()
