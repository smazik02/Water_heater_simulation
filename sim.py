VOLT_MIN = 0
VOLT_MAX = 10
CV = 4180  # ciepło właściwe wody, J * 1/kg * 1/K
RHO = 1000  # gęstość wody 1000 kg/m^3

KP = 0.8  # Wzmocnienie regulatora
TI = 1800  # Czas zdwojenia
TD = 0  # Czas wyprzedzenia

timeProbe = 0.1  # Okres czasu próbkowania [s]

integer = 0  # Dla skrócenia obliczeń całkowania


def genOutFlowConst(n, totalTime):  # Wersja stała:
    outFlow = [0.0001083333 for _ in range(n)]
    return outFlow


def genOutFlowStep(n, totalTime):  # Wersja ze stopniem:
    outFlow = [0.0000833333 for _ in range(n//3+1)] + \
        [0.00015 for _ in range(n//3+1, 2*n//3+1)] + \
        [0.0000833333 for _ in range(2*n//3+1, n)]
    return outFlow


# def genOutFlowStep(n, totalTime):  # Wersja ze stopniem:
#     outFlow = [0.00015 for _ in range(n//2+1)] + \
#         [0.0000833333 for _ in range(n//2+1, n)]
#     return outFlow


def P(en, kp):
    return kp*en


def PI(en, kp, ti):
    global integer
    integer += en
    return kp * (en + (timeProbe)/(ti) * integer)


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


async def main(totalTime, powerMax, litreVolume, tempSet):
    global time, e, temp, volt, waterFlow, heaterPower, integer
    integer = 0

    TEMP_IN = 10  # Temperatura zimnej wody w kranie
    volume = litreVolume/1000  # Pojemność z litrów na m^3

    time = [0.0]  # Czas
    e = [0.0]  # Uchyb
    temp = [10.0]  # Temperatura wody
    volt = [0.0]  # Napięcie sterujące
    heaterPower = [0.0]  # Moc grzałki wody

    N = int(totalTime/timeProbe) + 1

    # waterFlow = genOutFlowConst(N, totalTime)  # Przepływ wody m^3/s
    waterFlow = genOutFlowStep(N, totalTime)  # Przepływ wody m^3/s

    for i in range(N):
        time.append(time[-1] + timeProbe)
        e.append(tempSet - temp[-1])
        # volt.append(min(VOLT_MAX, max(VOLT_MIN, P(e[-1], KP))))
        volt.append(min(VOLT_MAX, max(VOLT_MIN, PID(e[-1], KP, TI, TD))))
        heaterPower.append(powerMax * (volt[-1]-VOLT_MIN)/(VOLT_MAX-VOLT_MIN))
        temp.append(temp[-1] + timeProbe * (waterFlow[i] * RHO*CV *
                    (TEMP_IN-temp[-1]) + heaterPower[-1]) / (volume*RHO*CV))


if __name__ == "__main__":
    main()
