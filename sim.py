from math import sqrt
import random
from time import sleep

CAPACITY = 50  # Pojemność bojlera [litr]
TEMP_SET = 45  # Ustawiona temperatura wody [*C]
TEMP_MAX = 80
TEMP_IN = 15  # Temperatura zimnej wody w kranie
VOLT_MIN = 0
VOLT_MAX = 10
ENERGY_MIN = 0
ENERGY_MAX = 1500
CV = 4180  # ciepło właściwe wody, J * 1/kg * 1/K

KP = 3  # Wzmocnienie regulatora
TD = 0.005  # Czas wyprzedzenia

timeProbe = 0.1  # Okres czasu próbkowania [s]
totalTime = 3600  # Czas symulacji [s]

time = [0.0]  # Czas
e = [0.0]  # Uchyb
temp = [15.0]  # Temperatura wody
volt = [0.0]  # Napięcie sterujące
outFlow = [0.0]  # Dopływ wody m^3/s
inFlow = [0.0]  # Odpływ wody m^s/s
energy = [0.0]  # Energia rozgrzewania wody
heaterPower = [0.0]  # Moc grzałki wody

N = int(totalTime/timeProbe) + 1


def genOutFlow():
    global outFlow
    outFlow = [0.0 for _ in range(N+1)]
    for i in range(10000, 10000 + 5*60*10):
        outFlow[i] = 0.131666
    for i in range(15000, 15000 + 60*10):
        outFlow[i] = 0.131666


def voltage(en):
    if len(volt) < 2:
        return KP * (en + TD/timeProbe * volt[-1])
    return KP * (en + TD/timeProbe * (volt[-1] - volt[-2]))


genOutFlow()

for i in range(N):
    time.append(time[-1] + timeProbe)
    # outFlow.append(0.0)
    inFlow.append(outFlow[i])
    e.append(TEMP_SET - temp[-1])
    volt.append(min(VOLT_MAX, max(VOLT_MIN, voltage(e[-1]))))
    energy.append(ENERGY_MAX * (volt[-1]-VOLT_MIN)/(VOLT_MAX-VOLT_MIN))
    # print(energy[-1])
    heaterPower.append(energy[-1]/timeProbe)
    temp.append(temp[-1] * ((CAPACITY-outFlow[i]*timeProbe)/CAPACITY) +
                TEMP_IN * (inFlow[-1]*timeProbe/CAPACITY) +
                (energy[-1])/(CV*CAPACITY))
    # print(temp[-1]*((CAPACITY-outFlow[-1])/CAPACITY) + TEMP_IN * (inFlow[-1]/CAPACITY))
