from .in_out import *
from .race import *

# ------------------------------------------

if __name__ == '__main__':

    io = IoManager()

    try:
        race = Race(io.load('race.log'))
    except Exception as e:
        print(str(e))
    else:
        print(race)
        io.save(race.__str__())
