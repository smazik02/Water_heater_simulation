from random import randrange

VOLT_MIN = 0
VOLT_MAX = 10
HEATER_POWER = 18000
TEMP_IN = 10  # Temperatura zimnej wody w kranie
CV = 4180  # ciepło właściwe wody, J * 1/kg * 1/K
RHO = 1000  # gęstość wody 1000 kg/m^3

VOLUME = 1/1000  # Pojemność [m^3]
TOTAL_TIME = 240

integer = 0  # Dla skrócenia obliczeń całkowania


# Wersja stała:
def genOutFlowConst(n: int) -> tuple[list[float], list[float]]:
    outFlow = [0.0000333333 for _ in range(n)]
    return outFlow, [x*60000 for x in outFlow]


# Wersja ze stopniem:
def genOutFlowStep2(n: int) -> tuple[list[float], list[float]]:
    outFlow = [0.0000333333 for _ in range(n//2+1)] + \
        [0.0001 for _ in range(n//2+1, n)]
    return outFlow, [x*60000 for x in outFlow]


# Wersja ze stopniem:
def genOutFlowStep3(n: int) -> tuple[list[float], list[float]]:
    outFlow = [0.0000333333 for _ in range(n//3+1)] + \
        [0.0001 for _ in range(n//3+1, 2*n//3+1)] + \
        [0.0000333333 for _ in range(2*n//3+1, n)]
    return outFlow, [x*60000 for x in outFlow]


# Wersja ze stopniem:
def genOutFlowStep4(n: int) -> tuple[list[float], list[float]]:
    outFlow = [0.0000333333 for _ in range(n//4+1)] + \
        [0.0001 for _ in range(n//4+1, n//2+1)] + \
        [0.0000333333 for _ in range(n//2+1, 3*n//4+1)] + \
        [0.0001 for _ in range(3*n//4+1, n)]
    return outFlow, [x*60000 for x in outFlow]

# Wersja losowa:
def genOutFlowStepRand(n: int) -> tuple[list[float], list[float]]:
    rand1, rand2, rand3, rand4 = randrange(
        1, 13)/2, randrange(1, 13)/2, randrange(1, 13)/2, randrange(1, 13)/2
    outFlow = [rand1/60000 for _ in range(n//4+1)] + \
        [rand2/60000 for _ in range(n//4+1, n//2+1)] + \
        [rand3/60000 for _ in range(n//2+1, 3*n//4+1)] + \
        [rand4/60000 for _ in range(3*n//4+1, n)]
    return outFlow, [x*60000 for x in outFlow]


def PI(en: float, kp: float, ti: float, timeProbe: float) -> float:
    global integer
    integer += en
    return kp * (en + (timeProbe*integer)/(ti))


async def main(tempSet: float, timeProbe: float, gain: float, integral: float):
    global time, e, temp, volt, waterFlow, waterFlowLitres, heaterPower, integer
    integer = 0
    n = int(TOTAL_TIME/timeProbe) + 1

    time = [0.0]  # Czas
    e = [0.0]  # Uchyb
    temp = [10.0]  # Temperatura wody
    volt = [0.0]  # Napięcie sterujące
    heaterPower = [0.0]  # Moc grzałki wody

    # waterFlow, waterFlowLitres = genOutFlowConst(n)  # Przepływ wody m^3/s
    waterFlow, waterFlowLitres = genOutFlowStep4(n)  # Przepływ wody m^3/s
    # waterFlow, waterFlowLitres = genOutFlowStepRand(n)  # Przepływ wody m^3/s

    for i in range(n):
        time.append(time[-1] + timeProbe)
        e.append(tempSet - temp[-1])
        volt.append(
            min(VOLT_MAX, max(VOLT_MIN, PI(e[-1], gain, integral, timeProbe))))
        heaterPower.append(
            HEATER_POWER * (volt[-1]-VOLT_MIN)/(VOLT_MAX-VOLT_MIN))
        temp.append(temp[-1] + timeProbe * (waterFlow[i] * RHO*CV *
                    (TEMP_IN-temp[-1]) + heaterPower[-1]) / (VOLUME*RHO*CV))


if __name__ == "__main__":
    main()
