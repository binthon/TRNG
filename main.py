import spidev
import time
import hashlib
import matplotlib.pyplot as plt
from collections import Counter

# Inicjalizacja SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Funkcja do odczytu z MCP3008
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Funkcja do generowania losowej liczby na podstawie szumu cieplnego
def generate_random_number(min_val, max_val):
    samples = []
    
    # Pobierz 20 próbek z CH0
    for _ in range(20):
        value = read_channel(0)
        samples.append(value)
        time.sleep(0.5)  # Mała przerwa między próbkami

    # Suma próbek
    total = sum(samples)
    
    # Użyj funkcji hashującej do dodatkowego mieszania danych
    hash_object = hashlib.sha256(str(total).encode())
    hash_hex = hash_object.hexdigest()
    hash_int = int(hash_hex, 16)
    
    # Użyj zahashowanej wartości do generowania losowej liczby
    random_value = hash_int % (max_val - min_val + 1) + min_val
    
    return samples, random_value

try:
    min_val = int(input("Podaj minimalną wartość: "))
    max_val = int(input("Podaj maksymalną wartość: "))
    num_samples = int(input("Podaj liczbę próbek: "))
    
    random_numbers = []
    all_samples = []
    
    for _ in range(num_samples):
        samples, random_number = generate_random_number(min_val, max_val)
        random_numbers.append(random_number)
        all_samples.append(samples)
        print(f"Próbki napięć: {samples}")
        print(f"Losowa liczba: {random_number}")
        time.sleep(0.5)  # Przerwa między generowaniem kolejnej liczby
    
    # Zliczanie liczby wystąpień każdej liczby
    counter = Counter(random_numbers)
    
    # Tworzenie listy wszystkich możliwych wartości w zadanym zakresie
    all_values = list(range(min_val, max_val + 1))
    occurrences = [counter.get(i, 0) for i in all_values]
    
    # Wykres liczby wystąpień
    plt.bar(all_values, occurrences)
    plt.xlabel('Liczba')
    plt.ylabel('Liczba wystąpień')
    plt.title('Histogram losowych liczb')
    plt.xticks(all_values, rotation=90)  # Ustawienie wszystkich wartości na osi X i ich obrót
    plt.tight_layout()  # Automatyczne dopasowanie układu, aby uniknąć nachodzenia się etykiet
    plt.show()

except KeyboardInterrupt:
    spi.close()
