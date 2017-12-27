# GAonline
A flask, clifford and threejs/javascript visualiser for 4,1 CGA.

An Azure deployment of this project can be found here:
http://gaonline.azurewebsites.net/

The project is intentionally fairly barebones, although help on improving the interface would be very appreciated.

# The flask server can be started by running
python main.py

# NB.
This is a very 'lazy' implementation in that it falls back on Clifford to do all the heavy lifting, this would not be a good way of doing things for a real production site as it will be bandwidth and sever side heavy.
