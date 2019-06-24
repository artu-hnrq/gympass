from util import *
from in_out import *
from race import *

# ------------------------------------------

if __name__ == '__main__':
    io = IoManager()
    race = io.load('race.log')
    print(race)
    io.save(race.__str__())
