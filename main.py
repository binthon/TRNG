import RPi.GPIO as GPIO
import spidev
import time
import numpy as np

# Ustawienie trybu numeracji pinów na BCM (numeracja GPIO)
GPIO.setmode(GPIO.BCM)

# Inicjalizacja SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # (bus, device)
spi.max_speed_hz = 1350000

# Funkcja do odczytu kanału z MCP3008
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Funkcja do przeliczania wartości ADC na napięcie
def convert_to_voltage(adc_value):
    return (adc_value * 3.3) / 1023  # 3.3V to napięcie referencyjne

# Odczyt napięcia z kanału 0 (CH0 MCP3008) przez 10 sekund
channel = 0
duration = 10  # czas w sekundach
samples = []

for i in range(duration):
    adc_value = read_channel(channel)
    voltage = convert_to_voltage(adc_value)
    samples.append(voltage)
    print(f"Czas: {i + 1}s, Odczytana wartość ADC: {adc_value}, Napięcie: {voltage:.6f} V")
    time.sleep(1)

# Zamknięcie SPI
spi.close()
# Czyszczenie ustawień GPIO
GPIO.cleanup()

# Obliczanie szumu cieplnego
samples = np.array(samples)
mean_voltage = np.mean(samples)
rms_voltage = np.sqrt(np.mean(np.square(samples - mean_voltage)))

print(f"Średnie napięcie: {mean_voltage:.6f} V")
print(f"RMS napięcie: {rms_voltage:.6f} V")

# Teoretyczne napięcie szumu cieplnego
k_B = 1.38e-23  # Stała Boltzmanna w J/K
T = 298  # Temperatura w kelwinach (przyjmując 25°C)
R = 10e3  # Rezystancja w ohmach (10kΩ)
delta_f = 0.5  # Szerokość pasma w Hz (przy odczytach co 1 sekundę pasmo Nyquista to 0.5 Hz)

theoretical_rms_voltage = np.sqrt(4 * k_B * T * R * delta_f)
print(f"Teoretyczne RMS napięcie szumu cieplnego: {theoretical_rms_voltage:.6f} V")
