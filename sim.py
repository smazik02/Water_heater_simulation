from math import sqrt
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

KP = 0.025  # Wzmocnienie regulatora
TI = 2.5  # Czas zdwojenia
TD = 3.0  # Czas wyprzedzenia

timeProbe = 0.1  # Okres czasu próbkowania [s]
totalTime = 3600  # Czas symulacji [s]

time = [0.0]  # Czas
e = [0.0]  # Uchyb
temp = [15.0]  # Temperatura wody
volt = [0.0]  # Napięcie sterujące
outFlow = [0.0]  # Dopływ wody
inFlow = [0.0]  # Odpływ wody
energy = [0.0]  # Energia rozgrzewania wody
heaterPower = [0.0]  # Moc grzałki wody

N = int(totalTime/timeProbe) + 1


def genOutFlow():
    global outFlow
    outFlow = [0.0 for _ in range(N)]
    # print(outFlow)


def voltage(en):
    if len(volt) < 2:
        return KP * (en + (timeProbe)/(TI) * sum(e) + (TD)/(timeProbe) * volt[-1])
    return KP * (en + (timeProbe)/(TI) * sum(e) + (TD)/(timeProbe) * (volt[-1] - volt[-2]))


def heatEnergy(un):
    return ((ENERGY_MAX-ENERGY_MIN)*(un-VOLT_MIN))/(VOLT_MAX-VOLT_MIN) + ENERGY_MIN


genOutFlow()

for i in range(N):
    time.append(time[-1] + timeProbe)
    e.append(TEMP_SET - temp[-1])
    volt.append(min(VOLT_MAX, max(VOLT_MIN, voltage(e[-1]))))
    energy.append(min(ENERGY_MAX, max(ENERGY_MIN, heatEnergy(volt[-1]))))
    # print(energy[-1])
    heaterPower.append(energy[-1]/timeProbe)
    inFlow.append(outFlow[i])
    temp.append(temp[-1]*((1-outFlow[-1])/CAPACITY) +
                TEMP_IN * (inFlow[-1]/CAPACITY) +
                (energy[-1]/10)/(CV*CAPACITY))
    print(temp[-1]*((1-outFlow[-1])/CAPACITY) +
          TEMP_IN * (inFlow[-1]/CAPACITY))
    print((heaterPower[-1]/10)/(CV*CAPACITY))
    sleep(1)
