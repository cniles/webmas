from flask import Flask,redirect,request
import wiringpi
import json
from random import shuffle
from time import sleep

from tinydb import TinyDB, Query

# Creates our backend flask application. Set the static url path to
# root, so that index.html can fall at /index.html
app = Flask(__name__, static_url_path='')

db = TinyDB('db.json')

timers = db.table('timers')
Timers = Query()

# Maps light number to gpio pin (wiringpi2 mapping)

pins = [ 22, 21, 3, 2, 0, 7, 9, 8, 5, 6, 26, 27 ]

valid_lights = range(len(pins))

gpio_map = dict(zip(valid_lights, pins))
    
# maps light number to a description

# maps pin write status to a string
status_map = {
    0: 'Off',
    1: 'On' }

# Gets a light current status
def getLightStatus(num):
    return wiringpi.digitalRead(gpio_map[num])

# Sets a light on or off
def setLightStatus(num, val):
    wiringpi.digitalWrite(gpio_map[num], val)

# Creates a new dict that describes the current state of a light,
# which can then be encoded into JSON
def makeLight(num):
    status = getLightStatus(num);
    return {
        "description": "na",
        "on": bool(status),
        "status": status_map[status],
        "name": "Light " + str(num+1),
        "num": num }

# Redirect root to index.html
@app.route('/')
def index():
    return redirect("/index.html", code=302)

# Toggles a light's status.  The response body is ignored
@app.route('/light/<int:num>', methods=['POST'])
def toggle_light(num):
    if num in valid_lights:
        status = getLightStatus(num)
        status = status ^ 1
        setLightStatus(num, status)
        return json.dumps(makeLight(num))
    return json.dumps({"success":False,"error":"Not a valid pin"})

# Gets the status of all the lights
@app.route('/lights', methods=['GET'])
def get_lights():
    return json.dumps([ makeLight(num) for num in valid_lights ])

# sets the status of all the lights
@app.route('/lights', methods=['POST'])
def set_lights():
    print "Setting lights"
    data = request.get_json()
    print "Got ", data
    for light in valid_lights:
        val = 1 if data['on'] else 0
        setLightStatus(light, val)
    return get_lights()

@app.route('/timer/<int:num>', methods=['DELETE'])
def delete_timer(num):
    timers.remove(Timers.num == num)
    return json.dumps({'success':True})

@app.route('/timers', methods=['GET'])
def get_timers():
    return json.dumps(timers.all())

@app.route('/timers', methods=['POST'])
def add_timer():
    timer = request.get_json()
    print "Adding timer: ", timer
    timers.insert(timer)
    return json.dumps({'success': True})


@app.route('/twinkle', methods=['POST'])
def random_twinkle():
    
    def lighttree():
        interval_show(30, 0.2, [4, 3, 2])

    def realtrees():
        interval_show(30, 0.1, [0, 6])

    def aroundthehouse():
        lights = valid_lights[:]
        shuffle(lights)
        interval_show(60, 0.33, lights, invert=True)

    shows = [lighttree, realtrees, aroundthehouse]
    shuffle(shows)
    shows[0]()
    
    return json.dumps({'result':'ok'})


def looping_generator(l):
    while True:
        for i in l:
            (yield i)
    

def interval_show(duration, interval, lights, invert=False):
    base = 1 if invert else 0
    select = 0 if invert else 1
    
    prev_states = dict([(light, getLightStatus(light)) for light in lights])

    for light in lights:
        setLightStatus(light, base)

    dt = 0
    light_gen = looping_generator(lights)

    while dt < duration:
        light = next(light_gen)
        setLightStatus(light, select)
        sleep(interval)
        setLightStatus(light, base)
        dt += interval

    for (light, state) in prev_states.items():
        setLightStatus(light, state)


if __name__ == '__main__':

    # initialize wiringpi services
    wiringpi.wiringPiSetup()

    # set gpio to output (if not already)
    for light in valid_lights:
        wiringpi.pinMode(gpio_map[light], 1)

    # start the web services
    # host="0.0.0.0" allows external access
    app.run(port=80, host="0.0.0.0")
