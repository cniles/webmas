from flask import Flask,redirect
import wiringpi2
import json

# Creates our backend flask application. Set the static url path to
# root, so that index.html can fall at /index.html
app = Flask(__name__, static_url_path='')

# valid light numbers
valid_lights = [0, 1, 2, 3]

# Maps light number to gpio pin (wiringpi2 mapping)
gpio_map = { 0: 7,
             1: 0,
             2: 1,
             3: 4 }

# maps light nmber to a description
descriptions = {
    0: "Stairs/balcony",
    1: "Plants/Shrubs",
    2: "Roof",
    3: "Windows/Garage"
}

# maps pin write status to a string
status_map = {
    0: 'Off',
    1: 'On'
}

# Gets a light current status
def getLightStatus(num):
    return wiringpi2.digitalRead(gpio_map[num])

# Sets a light on or off
def setLightStatus(num, val):
    wiringpi2.digitalWrite(gpio_map[num], val)

# Creates a new dict that describes the current state of a light,
# which can then be encoded into JSON
def makeLight(num):
    status = getLightStatus(num);
    return {
        "description": descriptions[num],
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
    if light in valid_lights:
        status = getLightStatus(num)
        status = status ^ 1
        setLightStatus(num, status)
        return json.dumps(makeLight(num))
    return json.dumps({"error":"Not a valid pin"})

# Gets the status of all the lights
@app.route('/lights', methods=['GET'])
def get_lights():
    return json.dumps([ makeLight(num) for num in valid_lights ])

# Fire it up
if __name__ == '__main__':

    # initialize wiringpi2 services
    wiringpi2.wiringPiSetup()

    # set gpio to output (if not already)
    for light in valid_lights:
        wiringpi2.pinMode(gpio_map[light], 1)

    # start the web services
    # host="0.0.0.0" allows external access
    app.run(port=80, host="0.0.0.0")
