from flask import Flask, jsonify, json, request, render_template
import clifford as cf
from clifford import g3c
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


def normalise_n_minus_1(mv):
    scale = (mv|ninf)[0]
    if scale != 0.0:
        return -mv/scale
    else:
        raise ZeroDivisionError('Multivector has 0 ninf component')

def dict_to_multivector(dict_in):
    constructed_values = np.zeros(32)
    for k in list(dict_in.keys()):
        constructed_values[int(k)] = dict_in[k]
    return cf.MultiVector(layout,constructed_values)

def get_center_from_sphere(sphere):
    center = sphere*ninf*sphere
    return center

def get_radius_from_sphere(sphere):
    dual_sphere = sphere*I5
    dual_sphere = dual_sphere/(-dual_sphere|ninf)
    return math.sqrt( abs(dual_sphere*dual_sphere) )

def get_plane_origin_distance(plane):
    return float(((plane*I5)|no)[0])

def get_plane_normal(plane):
    return (plane*I5 - get_plane_origin_distance(plane)*ninf)

def get_nearest_plane_point(plane):
    return get_plane_normal(plane)*get_plane_origin_distance(plane)

def get_circle_in_euc(circle):
    Ic = (circle^ninf).normal()
    GAnormal = get_plane_normal(Ic)
    inPlaneDual = circle*Ic
    mag = float((inPlaneDual|ninf)[0])
    inPlaneDual = -inPlaneDual/mag
    radius = math.sqrt((inPlaneDual*inPlaneDual)[0])
    #GAcentre = down(circle*ninf*circle)
    GAcentre = down(inPlaneDual*(1+0.5*inPlaneDual*ninf))
    return [GAcentre,GAnormal,radius]

def point_pair_to_end_points(T):
    beta = math.sqrt((T*T)[0])
    F = T/beta
    P = 0.5*(1+F)
    P_twiddle = 0.5*(1-F)
    A = normalise_n_minus_1(-P_twiddle*(T|ninf))
    B = normalise_n_minus_1(P*(T|ninf))
    return A,B

def line_to_point_and_direction(line):
    L_star = line*I5
    T = L_star|no
    mhat = -(L_star - T*ninf)*I3
    p = (T^mhat)*I3
    return [p,mhat]

def as_3D_list(mv_3d):
    return  [mv_3d[1],mv_3d[2],mv_3d[3]]

@app.route("/")
def render_main():
    return render_template('main.html')

@app.route("/to_point_pair/",methods=['POST'])
def to_point_pair():
    print('RECIEVING POINT PAIR')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    point_pair = dict_to_multivector(present_blades_dict)
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
    return jsonify(centre=centre,normal=normal,radius=radius) 


if __name__ == '__main__':
  app.run()
