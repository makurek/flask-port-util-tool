import os
import re
import ipaddress
import requests as req
from flask import Flask
from flask_wtf import FlaskForm
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap
from wtforms import StringField
from wtforms.validators import InputRequired
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.tasks.networking import napalm_cli
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command


nr = InitNornir(config_file="config.yaml")

app = Flask(__name__)
app.config['SECRET_KEY'] = '443436456542'
Bootstrap(app)
  
def initCheck():
  ge_pattern1 = re.compile("^GigabitEthernet[0-9]/[0-9]/[0-9]/[0-9]$")
  ge_pattern2 = re.compile("^ge-[0-9]/[0-9]/[0-9]$")
  ge_pattern3 = re.compile("^GigabitEthernet[0-9]$")
  result = {}
  basic_facts = nr.run(name="Get interfaces", task=napalm_get, getters=["interfaces"])
  for k,v in basic_facts.items():
     d = {}
     d['gig_up'] = 0
     d['gig_down'] = 0
     print(k)
     for iface, b in v[0].result['interfaces'].items():
       if re.match(r"^GigabitEthernet[0-9]/[0-9]/[0-9]/[0-9]$", iface) or re.match(r"^ge-[0-9]/[0-9]/[0-9]$", iface) or re.match("^GigabitEthernet[0-9]$", iface):
         if(b['is_enabled']):
           d['gig_up'] = d['gig_up'] + 1
         else:
           d['gig_down'] = d['gig_down'] + 1
     result[k] = d 
         
  print(result)
  return result


@app.route("/", methods=["GET", "POST"])

def index():
        
        result = initCheck()
        return render_template("home.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
