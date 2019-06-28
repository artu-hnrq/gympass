
Gympass Interview Challenge
==

This program was developed in Python 3.7 by [Arthur Henrique](https://www.linkedin.com/in/arthur-henrique-della-fraga/) in response to the [Gympass interview challenge](https://github.com/Gympass/interview-test).

### Running

To execute it run the 'src/main.py' archive, from the root folder, like this:
```
$ python3.7 -Bm src.main
```

The algorithm will look for the _'io/race.log'_ archive,
loading it's content as described in challenge's statement.
After this, it will calculate all required items and the description of the race result will be printed, as well as registered in _'io/result.txt'_ archive.

### Presumption

**1.** As the example log file didn't bring units for all values, *average speed* was assumed as in *km/h* and time values in *h:min:s:ms*.

**2.** I also observed a questionable data in the log file provided in the problem statement. In its 17th line there is the record of a pilot, still unregistered, realizing its 4th lap. So, this algorithm will assume each pair (code, name) as a different runner.

A correction suggestion was opened through [this pull request](https://github.com/Gympass/interview-test/pull/2).

### Tests

To execute project's unit tests run the following command from the root folder:
```
$ python3.7 -Bm unittest test
```
