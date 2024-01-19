VOLT_MIN = 0
VOLT_MAX = 10
HEATER_POWER = 18000
TEMP_IN = 10  # Temperatura zimnej wody w kranie
CV = 4180  # ciepło właściwe wody, J * 1/kg * 1/K
RHO = 1000  # gęstość wody 1000 kg/m^3

VOLUME = 1/1000  # Pojemność z litrów na m^3
TIME_PROBE = 0.1  # Okres czasu próbkowania [s]
TOTAL_TIME = 240
N = int(TOTAL_TIME/TIME_PROBE) + 1

KP = 0.9  # Wzmocnienie regulatora
TI = 50  # Czas zdwojenia

integer = 0  # Dla skrócenia obliczeń całkowania


def genOutFlowConst(n: int) -> (list[float], list[float]):  # Wersja stała:
    outFlow = [0.0000333333 for _ in range(n)]
    return (outFlow, [x*60000 for x in outFlow])


# Wersja ze stopniem:
def genOutFlowStep2(n: int) -> (list[float], list[float]):
    outFlow = [0.0000333333 for _ in range(n//2+1)] + \
        [0.0001 for _ in range(n//2+1, n)]
    return (outFlow, [x*60000 for x in outFlow])


# Wersja ze stopniem:
def genOutFlowStep3(n: int) -> (list[float], list[float]):
    outFlow = [0.0000333333 for _ in range(n//3+1)] + \
        [0.0001 for _ in range(n//3+1, 2*n//3+1)] + \
        [0.0000333333 for _ in range(2*n//3+1, n)]
    return (outFlow, [x*60000 for x in outFlow])


# Wersja ze stopniem:
def genOutFlowStep4(n: int) -> (list[float], list[float]):
    outFlow = [0.0000333333 for _ in range(n//4+1)] + \
        [0.0001 for _ in range(n//4+1, n//2+1)] + \
        [0.0000333333 for _ in range(n//2+1, 3*n//4+1)] + \
        [0.0001 for _ in range(3*n//4+1, n)]
    return (outFlow, [x*60000 for x in outFlow])


def P(en: float, kp: float) -> float:
    return kp*en


def PI(en: float, kp: float, ti: float) -> float:
    global integer
    integer += en
    return kp * (en + (TIME_PROBE*integer)/(ti))


# def PID(en, kp, ti, td):
#     global integer
#     integer += en
#     if len(volt) < 2:
#         return kp * (en + (TIME_PROBE)/(ti) * integer + (td)/(TIME_PROBE) * volt[-1])
#     return kp * (en + (TIME_PROBE)/(ti) * integer + (td)/(TIME_PROBE) * (volt[-1] - volt[-2]))


async def main(tempSet: float):
    global time, e, temp, volt, waterFlow, waterFlowLitres, heaterPower, integer
    integer = 0

    time = [0.0]  # Czas
    e = [0.0]  # Uchyb
    temp = [10.0]  # Temperatura wody
    volt = [0.0]  # Napięcie sterujące
    heaterPower = [0.0]  # Moc grzałki wody

    # waterFlow = genOutFlowConst(N)  # Przepływ wody m^3/s
    waterFlow, waterFlowLitres = genOutFlowStep4(N)  # Przepływ wody m^3/s

    for i in range(N):
        time.append(time[-1] + TIME_PROBE)
        e.append(tempSet - temp[-1])
        # volt.append(min(VOLT_MAX, max(VOLT_MIN, P(e[-1], KP))))
        volt.append(min(VOLT_MAX, max(VOLT_MIN, PI(e[-1], KP, TI))))
        heaterPower.append(HEATER_POWER * (volt[-1]-VOLT_MIN)/(VOLT_MAX-VOLT_MIN))
        temp.append(temp[-1] + TIME_PROBE * (waterFlow[i] * RHO*CV *
                    (TEMP_IN-temp[-1]) + heaterPower[-1]) / (VOLUME*RHO*CV))


if __name__ == "__main__":
    main()
