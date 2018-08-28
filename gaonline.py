
import hashlib
import os
import time
from main import app
from multiprocessing import Process
from cef_gui import *


def generate_template(script_string):
    s_start = """{% extends 'base.html' %}

    {% block user_script %}
    `"""
    s_end = """
    `
    {% endblock %}
    """
    return s_start + script_string + s_end


def generate_and_save_template(script_string):
    template_string = generate_template(script_string)
    endpointname = hashlib.sha224(template_string.encode('utf-8')).hexdigest()
    filename = endpointname + ".html"
    dir_name = os.path.dirname(os.path.abspath(__file__))
    fullname = dir_name + '/templates/' + filename
    with open(fullname,'w') as f_obj:
        print(template_string, file=f_obj)
    return fullname, filename, endpointname


def render_script(script_string):
    # First save the script string as a template
    fullname, filename, endpointname = generate_and_save_template(script_string)

    def run_cef_process():
        run_cef_gui("localhost:5000/" + endpointname, "GAOnline")

    try:
        # Now run the flask server
        server = Process(target=app.run)
        cef_gui = Process(target=run_cef_process)
        server.start()
        # Wait a little to warm up
        time.sleep(1)
        cef_gui.start()
        # Clean up our mess
        cef_gui.join()
        server.terminate()
        server.join()

        if os.path.isfile(fullname):
            os.remove(fullname)
    except:
        if os.path.isfile(fullname):
            os.remove(fullname)

