import RPi.GPIO as GPIO
import time
import spidev

# Ustawienie trybu numeracji pinów na BCM (numeracja GPIO)
GPIO.setmode(GPIO.BCM)

# Ustawienie GPIO23 jako wyjście
GPIO.setup(23, GPIO.OUT)

# Ustawienie stanu wysokiego na GPIO23
GPIO.output(23, GPIO.HIGH)

# Inicjalizacja SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Funkcja do odczytu kanału z MCP3008
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Odczyt napięcia z kanału 0 (R1 podłączony do CH0 MCP3008) przez 10 sekund
channel = 0
for i in range(10):
    adc_value = read_channel(channel)
    voltage = (adc_value * 3.3) / 1023  # Przeskalowanie wartości ADC do napięcia
    print(f"Czas: {i + 1}s, Odczytana wartość ADC: {adc_value}, Napięcie na R1: {voltage:.2f} V")
    time.sleep(1)

# Wyłączenie diody (ustawienie stanu niskiego na GPIO23)
GPIO.output(23, GPIO.LOW)

# Wyłączenie trybu pull-up na GPIO23 (jeśli jest ustawiony)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

# Czyszczenie ustawień GPIO
GPIO.cleanup()

# Zamknięcie SPI
spi.close()
