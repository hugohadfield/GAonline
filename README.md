# GAonline
A [flask](http://flask.pocoo.org/), [clifford](https://github.com/pygae/clifford) and [threejs/javascript](https://threejs.org/) visualiser for (4,1) [Conformal Geometric Algebra (CGA)](http://www2.montgomerycollege.edu/departments/planet/planet/Numerical_Relativity/GA-SIG/Conformal%20Geometry%20Papers/Cambridge/Covarient%20Approach%20to%20Geometry%20Using%20Geometric%20Algebra.pdf) .

Created by [Hugo Hadfield](https://github.com/hugohadfield)

# Use it now
An Azure deployment of this project can be found here:
http://gaonline.azurewebsites.net/

A tutorial coving basic usage can be found here:
https://hugohadfield.github.io/GAonline/index.html


The project is intentionally fairly barebones, although help on improving the interface would be very appreciated! 

The key goal of this project is to be able to visualise conformal objects that are very hard to think about otherwise. With this visualiser there is minimal installation (none if you use a web deployed version!) and the code is incredibly simple.

# Setting up and running the server
First clone this repository and ensure you have the required packages on your machine
Flask>=0.12.1
clifford>=0.81

The flask server can be started by running:
python main.py

It works very well when run locally, I find an especially useful combination is to use [embedded chrome](https://github.com/cztomczak/cefpython) with a flask server as shown here:
https://github.com/hugohadfield/cefFlask

# A note on performance
This is a very 'lazy' implementation in that it falls back on server side clifford to do all the heavy lifting, this would not be a good way of doing things for a real production site as it will be bandwidth and sever side heavy.

