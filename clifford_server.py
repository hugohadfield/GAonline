from flask import Flask, jsonify, json, request, render_template
import clifford as cf
app = Flask(__name__)


def dict_to_multivector(dict_in):
    return cf.MultiVector(layout,)


@app.route("/")
def render_main():
    return render_template('main.html')

@app.route("/to_sphere/",methods=['POST'])
def to_sphere():
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print(present_blades_dict)
    return jsonify(centre=[1.0,1.0,2.0]) 