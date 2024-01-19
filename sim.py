VOLT_MIN = 0
VOLT_MAX = 10
CV = 4180  # ciepło właściwe wody, J * 1/kg * 1/K
RHO = 1000  # gęstość wody 1000 kg/m^3

KP = 0.9  # Wzmocnienie regulatora
TI = 50  # Czas zdwojenia

timeProbe = 0.1  # Okres czasu próbkowania [s]

integer = 0  # Dla skrócenia obliczeń całkowania


def genOutFlowConst(n, totalTime):  # Wersja stała:
    outFlow = [0.0000333333 for _ in range(n)]
    return outFlow


def genOutFlowStep2(n, totalTime):  # Wersja ze stopniem:
    outFlow = [0.0000333333 for _ in range(n//2+1)] + \
        [0.0001 for _ in range(n//2+1, n)]
    return outFlow


def genOutFlowStep3(n, totalTime):  # Wersja ze stopniem:
    outFlow = [0.0000333333 for _ in range(n//3+1)] + \
        [0.0001 for _ in range(n//3+1, 2*n//3+1)] + \
        [0.0000333333 for _ in range(2*n//3+1, n)]
    return outFlow


def genOutFlowStep4(n, totalTime):  # Wersja ze stopniem:
    outFlow = [0.0000333333 for _ in range(n//4+1)] + \
        [0.0001 for _ in range(n//4+1, n//2+1)] + \
        [0.0000333333 for _ in range(n//2+1, 3*n//4+1)] + \
        [0.0001 for _ in range(3*n//4+1, n)]
    return outFlow


def P(en, kp):
    return kp*en


def PI(en, kp, ti):
    global integer
    integer += en
    return kp * (en + (timeProbe*integer)/(ti))


# def PID(en, kp, ti, td):
#     global integer
#     integer += en
#     if len(volt) < 2:
#         return kp * (en + (timeProbe)/(ti) * integer + (td)/(timeProbe) * volt[-1])
#     return kp * (en + (timeProbe)/(ti) * integer + (td)/(timeProbe) * (volt[-1] - volt[-2]))


async def main(powerMax, tempSet):
    global time, e, temp, volt, waterFlow, heaterPower, integer
    integer = 0

    TEMP_IN = 10  # Temperatura zimnej wody w kranie
    VOLUME = 1/1000  # Pojemność z litrów na m^3
    TOTAL_TIME = 240

    time = [0.0]  # Czas
    e = [0.0]  # Uchyb
    temp = [10.0]  # Temperatura wody
    volt = [0.0]  # Napięcie sterujące
    heaterPower = [0.0]  # Moc grzałki wody

    N = int(TOTAL_TIME/timeProbe) + 1

    # waterFlow = genOutFlowConst(N, TOTAL_TIME)  # Przepływ wody m^3/s
    waterFlow = genOutFlowStep4(N, TOTAL_TIME)  # Przepływ wody m^3/s

    for i in range(N):
        time.append(time[-1] + timeProbe)
        e.append(tempSet - temp[-1])
        # volt.append(min(VOLT_MAX, max(VOLT_MIN, P(e[-1], KP))))
        volt.append(min(VOLT_MAX, max(VOLT_MIN, PI(e[-1], KP, TI))))
        heaterPower.append(powerMax * (volt[-1]-VOLT_MIN)/(VOLT_MAX-VOLT_MIN))
        temp.append(temp[-1] + timeProbe * (waterFlow[i] * RHO*CV *
                    (TEMP_IN-temp[-1]) + heaterPower[-1]) / (VOLUME*RHO*CV))


if __name__ == "__main__":
    main()
