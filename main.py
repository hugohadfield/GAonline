from flask import Flask, jsonify, json, request, render_template
import clifford as cf
from clifford import g3c
from clifford_tools.common.g3c.core import *
import numpy as np
import math

layout = g3c.layout
locals().update(g3c.blades)

ep, en, up, down, homo, E0, ninf, no = (g3c.stuff["ep"], g3c.stuff["en"], 
                                        g3c.stuff["up"], g3c.stuff["down"], g3c.stuff["homo"], 
                                        g3c.stuff["E0"], g3c.stuff["einf"], -g3c.stuff["eo"])

I3 = e123
I5 = e12345


app = Flask(__name__)


def as_3D_list(mv_3d):
    return  [mv_3d[1],mv_3d[2],mv_3d[3]]

@app.route("/")
def render_main():
    return render_template('main.html')

@app.route("/to_sphere/",methods=['POST'])
def to_sphere():
    print('RECIEVING SPHERE')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    sphere = dict_to_multivector(present_blades_dict)
    print('Sphere: ',sphere)
    GAcentre = down(get_center_from_sphere(sphere))
    centre = as_3D_list(GAcentre)
    radius = get_radius_from_sphere(sphere)
    print('Centre: ',centre)
    print('Radius: ',radius)
    return jsonify(centre=centre,radius=radius) 

@app.route("/to_plane/",methods=['POST'])
def to_plane():
    print('RECIEVING PLANE')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    plane = dict_to_multivector(present_blades_dict)
    print('Plane: ',plane)
    normalGA = get_plane_normal(plane)
    normal = as_3D_list(normalGA)
    distance = get_plane_origin_distance(plane)
    print('Distance: ', distance)
    print('Normal: ', normal)
    return jsonify(distance=distance,normal=normal) 

@app.route("/to_line/",methods=['POST'])
def to_line():
    print('RECIEVING LINE')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    line = dict_to_multivector(present_blades_dict)
    print('Line: ',line)
    GApoint,GAdirection = line_to_point_and_direction(line)
    point = as_3D_list(GApoint)
    direction = as_3D_list(GAdirection)
    print('Point: ', point)
    print('Direction: ', direction)
    return jsonify(point=point,direction=direction) 

@app.route("/to_circle/",methods=['POST'])
def to_circle():
    print('RECIEVING CIRCLE')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    circle = dict_to_multivector(present_blades_dict)
    print('Circle: ',circle)

    GAcentre,GAnormal,radius = get_circle_in_euc(circle);

    centre = as_3D_list(GAcentre)
    normal = as_3D_list(GAnormal)
    print('Radius: ', radius)
    print('Centre: ', centre)
    print('Normal: ', normal)
    return jsonify(centre=centre,normal=normal,) 


if __name__ == '__main__':
  app.run()
