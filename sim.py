from math import sqrt
import random
from time import sleep


VOLT_MIN = 0
VOLT_MAX = 10
CV = 4180  # ciepło właściwe wody, J * 1/kg * 1/K

KP = 3  # Wzmocnienie regulatora
TD = 0.005  # Czas wyprzedzenia

timeProbe = 0.1  # Okres czasu próbkowania [s]


def genOutFlow(n, totalTime):
    outFlow = [0.0 for _ in range(n+1)]
    for i in range(x := int(1000 * (totalTime/3600) / timeProbe), x + 5*60*10):
        outFlow[i] = 0.131666
    for i in range(x := int(1500 * (totalTime/3600) / timeProbe), x + 60*10):
        outFlow[i] = 0.131666/2
    return outFlow


def voltage(en):
    if len(volt) < 2:
        return KP * (en + TD/timeProbe * volt[-1])
    return KP * (en + TD/timeProbe * (volt[-1] - volt[-2]))


async def main(totalTime=3600, energyMax=150, capacity=50, tempSet=45):
    global time, e, temp, volt, outFlow, energy, heaterPower

    TEMP_IN = 15  # Temperatura zimnej wody w kranie

    MAX_POWER = int(energyMax/10)

    time = [0.0]  # Czas
    e = [0.0]  # Uchyb
    temp = [15.0]  # Temperatura wody
    volt = [0.0]  # Napięcie sterujące
    inFlow = [0.0]  # Odpływ wody m^s/s
    energy = [0.0]  # Energia rozgrzewania wody
    heaterPower = [0.0]  # Moc grzałki wody

    N = int(totalTime/timeProbe) + 1

    outFlow = genOutFlow(N, totalTime)

    for i in range(N):
        time.append(time[-1] + timeProbe)
        inFlow.append(outFlow[i])
        e.append(tempSet - temp[-1])
        volt.append(min(VOLT_MAX, max(VOLT_MIN, voltage(e[-1]))))
        energy.append(MAX_POWER * (volt[-1]-VOLT_MIN)/(VOLT_MAX-VOLT_MIN))
        heaterPower.append(energy[-1]/timeProbe)
        temp.append(temp[-1] * ((capacity-outFlow[i]*timeProbe)/capacity) +
                    TEMP_IN * (inFlow[-1]*timeProbe/capacity) +
                    (energy[-1])/(CV*capacity))


if __name__ == "__main__":
    main()
