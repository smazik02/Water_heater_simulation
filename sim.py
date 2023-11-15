from math import sqrt

CAPACITY = 50  # Pojemność bojlera [litr]
TEMP_SET = 45  # Ustawiona temperatura wody [*C]
TEMP_MAX = 80
TEMP_IN = 15  # Temperatura zimnej wody w kranie
VOLT_MIN = 0
VOLT_MAX = 10
POWER_MIN = 0
POWER_MAX = 1500

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
heaterPower = [0.0]

N = int(totalTime/timeProbe) + 1


def voltage(en):
    if len(volt) < 2:
        return KP * (en + (timeProbe)/(TI) * sum(e) + (TD)/(timeProbe) * volt[-1])
    return KP * (en + (timeProbe)/(TI) * sum(e) + (TD)/(timeProbe) * (volt[-1] - volt[-2]))


def power(un):
    return ((POWER_MAX-POWER_MIN)*(un-VOLT_MIN))/(VOLT_MAX-VOLT_MIN) + POWER_MIN


for _ in range(N):
    time.append(time[-1] + timeProbe)
    e.append(TEMP_SET - temp[-1])
    volt.append(min(VOLT_MAX, max(VOLT_MIN, voltage(e[-1]))))
    inFlow.append(min(POWER_MAX, max(POWER_MIN, power(volt[-1]))))
    # temp.append(timeProbe)
