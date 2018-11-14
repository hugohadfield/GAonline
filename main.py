#!/usr/bin/python3

from flask import Flask, jsonify, json, request, render_template
import clifford as cf
from clifford.g3c import *
from clifford.tools.g3c import *
import numpy as np
import math

ninf = einf
no = -eo

I3 = e123
I5 = e12345


app = Flask(__name__)


def as_3D_list(mv_3d):
    return  [mv_3d[1],mv_3d[2],mv_3d[3]]


@app.route("/")
def render_main():
    return render_template('default.html', show_help = True, show_tools=True)


@app.route('/<page>')
def show(page):
    show_tools_string = request.args.get('show_tools')
    if show_tools_string == 'True':
        show_tools = True
    else:
        show_tools = False
    return render_template('%s.html' % page, show_help = False, show_tools=show_tools)


@app.route("/to_interpretted/", methods=['POST'])
def to_interpretted():
    print('RECIEVING UNKNOWN MULTIVECTOR')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    mv = layout.dict_to_multivector(present_blades_dict)
    # Interpret the multivector as an object
    return_val = interpret_multivector_as_object(mv)
    if return_val > 0:
        if return_val == 1:
            print('Euc Point: ',mv)
            p = as_3D_list(mv)
            print('p: ',p)
            return jsonify(obj_flag=1,p=p)
        elif return_val == 2:
            print('Conf Point: ',mv)
            p = as_3D_list(down(mv))
            print('p: ',p)
            return jsonify(obj_flag=2,p=p)
        elif return_val == 3:
            print('Point pair: ',mv)
            A,B = point_pair_to_end_points(mv)
            a = as_3D_list(down(A))
            b = as_3D_list(down(B))
            print('a: ',a)
            print('b: ',b)
            return jsonify(obj_flag=3,a=a,b=b)
        elif return_val == 4:
            print('Circle: ',mv)
            GAcentre,GAnormal,radius = get_circle_in_euc(mv);
            centre = as_3D_list(GAcentre)
            normal = as_3D_list(GAnormal)
            print('Radius: ', radius)
            print('Centre: ', centre)
            print('Normal: ', normal)
            return jsonify(obj_flag=4,centre=centre,normal=normal,radius=radius) 
        elif return_val == 5:
            print('Line: ',mv)
            GApoint,GAdirection = line_to_point_and_direction(mv)
            point = as_3D_list(GApoint)
            direction = as_3D_list(GAdirection)
            print('Point: ', point)
            print('Direction: ', direction)
            return jsonify(obj_flag=5,point=point,direction=direction) 
        elif return_val == 6:
            print('Sphere: ',mv)
            GAcentre = down(get_center_from_sphere(mv))
            centre = as_3D_list(GAcentre)
            radius = get_radius_from_sphere(mv)
            print('Centre: ',centre)
            print('Radius: ',radius)
            return jsonify(obj_flag=6,centre=centre,radius=radius)
        elif return_val == 7:
            print('Plane: ',mv)
            normalGA = get_plane_normal(mv)
            normal = as_3D_list(normalGA)
            distance = get_plane_origin_distance(mv)
            print('Distance: ', distance)
            print('Normal: ', normal)
            return jsonify(obj_flag=7,distance=distance,normal=normal) 
    else:
        print('ERROR MULIVECTOR IS NOT INTERPRETTABLE')


@app.route("/to_conformal_point/", methods=['POST'])
def to_conformal_point():
    print('RECIEVING CONFORMAL POINT')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    point = layout.dict_to_multivector(present_blades_dict)
    print('Point: ',point)
    p = as_3D_list(down(point))
    print('p: ',p)
    return jsonify(p=p)


@app.route("/to_point_pair/", methods=['POST'])
def to_point_pair():
    print('RECIEVING POINT PAIR')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    point_pair = layout.dict_to_multivector(present_blades_dict)
    print('Point pair: ',point_pair)
    A,B = point_pair_to_end_points(point_pair)
    a = as_3D_list(down(A))
    b = as_3D_list(down(B))
    print('a: ',a)
    print('b: ',b)
    return jsonify(a=a,b=b)


@app.route("/to_sphere/",methods=['POST'])
def to_sphere():
    print('RECIEVING SPHERE')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    sphere = layout.dict_to_multivector(present_blades_dict)
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
    plane = layout.dict_to_multivector(present_blades_dict)
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
    line = layout.dict_to_multivector(present_blades_dict)
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
    circle = layout.dict_to_multivector(present_blades_dict)
    print('Circle: ',circle)

    GAcentre,GAnormal,radius = get_circle_in_euc(circle);

    centre = as_3D_list(GAcentre)
    normal = as_3D_list(GAnormal)
    print('Radius: ', radius)
    print('Centre: ', centre)
    print('Normal: ', normal)
    return jsonify(centre=centre,normal=normal,radius=radius) 


def run_app():
    app.run()


if __name__ == '__main__':
  app.run()
