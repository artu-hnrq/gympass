import random
from src.time import *
from src.race import *

# ------------------------------------------
def createDriver():
    return (
        str(random.randint(0, 33)),
        'Driver' + str(random.randint(0, 33))
    )

def createLaps(lap_distance):
    laps = []

    for i in range(random.randint(2, 4)):
        lap_duration = createDuration()

        laps.append((
            i+1,
            lap_duration,
            lap_distance / lap_duration.to_milliseconds() / MILLISECONDS_PER_HOUR
        ))

    return laps

def createDuration():
    args = {
        'minutes':          random.randint(0, 10),
        'seconds':          random.randint(0, 59),
        'milliseconds':     random.randint(0, 999)
    }

    return Duration(args)
