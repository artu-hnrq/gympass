import random
from src.time import *
from src.race import *

# Create a Driver with random code and name
def createDriver():
    return (
        str(random.randint(0, 33)),
        'Driver' + str(random.randint(0, 33))
    )

# Create a random number of laps,
# with duration and runner's average speed varying
# based on lap_distance
def createLaps(lap_distance):
    laps = []

    for i in range(random.randint(2, 4)):
        lap_duration = createDuration()

        laps.append((
            i+1,
            lap_duration,
            lap_distance / lap_duration.to_milliseconds() * MILLISECONDS_PER_HOUR
        ))

    return laps

# Create a ramdom Duration between 0ms and 9min 59s 999ms
def createDuration():
    args = {
        'minutes':          random.randint(0, 9),
        'seconds':          random.randint(0, 59),
        'milliseconds':     random.randint(0, 999)
    }

    return Duration(args)
