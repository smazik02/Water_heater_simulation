from math import sqrt
import random
from time import sleep


VOLT_MIN = 0
VOLT_MAX = 10
CV = 4180  # ciepło właściwe wody, J * 1/kg * 1/K
RHO = 1000  # gęstość wody 1000 kg/m^3

KP = 0.00005  # Wzmocnienie regulatora
TI = 2.5  # Czas zdwojenia
TD = 0  # Czas wyprzedzenia

timeProbe = 0.1  # Okres czasu próbkowania [s]

integer = 0  # Dla skrócenia obliczeń całkowania


# def genOutFlow(n, totalTime):
#     outFlow = [0.0 for _ in range(n+1)]
#     for i in range(x := int(1000 * (totalTime/3600) / timeProbe), x + 5*60*10):
#         outFlow[i] = 3.33e-5
#     for i in range(x := int(1500 * (totalTime/3600) / timeProbe), x + 60*10):
#         outFlow[i] = 3.33e-5/2
#     return outFlow

def genOutFlow(n, totalTime):
    outFlow = [3.33e-5 for _ in range(n+1)]
    return outFlow


def P(en, kp):
    return kp*en


def PI(en, kp, ti):
    global integer
    integer += en
    return kp * (en + (timeProbe)/(TI) * integer)


def PD(en, kp, td):
    if len(volt) < 2:
        return kp * (en + (td)/(timeProbe) * volt[-1])
    return kp * (en + (td)/(timeProbe) * (volt[-1] - volt[-2]))


def PID(en, kp, ti, td):
    global integer
    integer += en
    if len(volt) < 2:
        return kp * (en + (timeProbe)/(ti) * integer + (td)/(timeProbe) * volt[-1])
    return kp * (en + (timeProbe)/(ti) * integer + (td)/(timeProbe) * (volt[-1] - volt[-2]))


async def main(totalTime=3600, powerMax=1500, litreVolume=50, tempSet=45):
    global time, e, temp, volt, waterFlow, heaterPower

    TEMP_IN = 15  # Temperatura zimnej wody w kranie
    volume = litreVolume/1000  # Pojemność z litrów na m^3

    time = [0.0]  # Czas
    e = [0.0]  # Uchyb
    temp = [15.0]  # Temperatura wody
    volt = [0.0]  # Napięcie sterujące
    heaterPower = [0.0]  # Moc grzałki wody

    N = int(totalTime/timeProbe) + 1

    waterFlow = genOutFlow(N, totalTime)  # Przepływ wody m^3/s

    for i in range(N):
        time.append(time[-1] + timeProbe)
        e.append(tempSet - temp[-1])
        volt.append(min(VOLT_MAX, max(VOLT_MIN, PID(e[-1], KP, TI, TD))))
        heaterPower.append(powerMax * (volt[-1]-VOLT_MIN)/(VOLT_MAX-VOLT_MIN))
        temp.append(temp[-1] + timeProbe * (waterFlow[i] * RHO*CV *
                    (TEMP_IN-temp[-1]) + heaterPower[-1]) / (volume*RHO*CV))


if __name__ == "__main__":
    main()
