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

I5 = e12345



app = Flask(__name__)

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
    return math.sqrt( abs(dual_sphere*dual_sphere) )

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
    GAcentre = get_center_from_sphere(sphere)
    print(GAcentre)
    centre = [GAcentre[1],GAcentre[2],GAcentre[3]]
    radius = get_radius_from_sphere(sphere)
    print('Centre: ',centre)
    print('Radius: ',radius)
    return jsonify(centre=centre,radius=radius) 