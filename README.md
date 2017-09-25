
Type 'python conways_GOL.py -h' to see the following screen.

usage: conways_GOL.py [-h] [-c CYCLES] [-f INPUTFILE] [-s INPUTSTR] [-d DELAY]

optional arguments:
  -h, --help            show this help message and exit
  -c CYCLES, --cycles CYCLES
                        Number of iterations to execute. Default is infinite.
			Press ctrl+c or equivalent keyboard interrupt to stop.
  -f INPUTFILE, --inputfile INPUTFILE
                        Local file to pull initial configuration.
  -s INPUTSTR, --inputstr INPUTSTR
                        User input initial state. Please use '\n' to separate
                        rows.
  -d DELAY, --delay DELAY
                        Delay between updated states.

INSTRUCTIONS:
The easiest way to run this program is to type in a pattern into a file (file_name).
Afterwards, run the following command:
python conways_GOL.py -f file_name -c 1 -d .1

Some files have been provided for viewing:
To see the glider gun on wikipedia: python conways_GOL.py -f input_file_4.txt -c 200 -d .1

To run tests:
python conways_test.py


FEATURES AVAILABLE:
1. dynamic grid
2. dynamic cycles
3. performance considerations
4. considerations for extensibility