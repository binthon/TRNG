# TRNG (TRUE RANDOM NUMBER GENERATOR)

# PROJECT GOAL
The goal is to use the mcp3008 a/c converter and to read random voltages from CH0. Then using these voltages to generate a fully random number in the range specified by the user. 
# TECHNOLOGY
The program was written in python along with the libraries spidev (used to communicate with the SPI interface of the Raspberry PI 4), matplotlib, hashlib.
# HOW PROGRAM WORKS
The program reads the compactness every 0.01 seconds a hundred times by default. These values are converted to voltage, and every third sample is selected from these 100 samples. They are then summed. A sha256 hash function is used to improve randomness. In order to get a number in the specified range, I used the variable random_value where the modulo of the hash with the range is counted. 
The results are presented in the form of a graph, where the x-axis is the numbers in the range, and the y-axis is the number of occurrences of a given number in the number of numbers you specify that you want to draw in the range.
# RESULTS
![image](https://github.com/binthon/TRNG/assets/74725795/e9ab3959-d3f4-4ce6-aaae-5d5ed5d084b4)
![image](https://github.com/binthon/TRNG/assets/74725795/b30ae7e5-39fd-489e-b2e0-1289362747f2)
![chart2](https://github.com/binthon/TRNG/assets/74725795/681ca99d-ff04-4097-95f1-09cd4d36b5ed)
# Circuit 
![image](https://github.com/binthon/TRNG/assets/74725795/6c715d7b-7c5c-4fcf-8825-3ec49c6b5cc6)
To connect in RP4 I connected:
1. Power:
   a) Vcc - GPIO 1 (3,3V)
   b) GND - GPIO 6
2. MCP:
   a) SCLK - GPIO 11
   b) MISO - GPIO 9
   c) MOSI - GPIO 10
   d) CSO - GPIO 8
# DOC RP4
Here is GPIO description
<br>
![image](https://github.com/binthon/TRNG/assets/74725795/a994ea1c-8ef1-4d8f-99ec-a3f8a06331ae)

# DOC MCP3008
Here is doc MCP3008
[Data Sheet: MCP3008](https://ww1.microchip.com/downloads/aemDocuments/documents/MSLD/ProductDocuments/DataSheets/MCP3004-MCP3008-Data-Sheet-DS20001295.pdf)

