# webmas
Christmas Light Controller

This is a small web application that can control Christmas lights.  It utilizes Angular JS to produce the client and Python Flask for backend services.

## setup
Setup your raspberry pi with raspbian (haven't tested any other linux distributions, but they could work equally well I suppose). Search around on their website for instructions on how to do this.

Next, install pip:
`sudo apt-get install python-pip`

Using pip, install Flask: `sudo pip install flask`

Then, go get wiringPi and follow the instructions there:

http://wiringpi.com/download-and-install/

Awesome, now you need to install the python bindings from Philip Howard.  But first, its needs some dependencies:
`sudo apt-get install python-dev python-setuptools`

You could clone the the git repo and install that way...but I just used pip:
`sudo pip install wiringpi2`

If you have problems with your debian packages (old image maybe, or haven't run updates in a while?), try running update:
`sudo apt-get update`

## running
Pretty simple, just run the start script (note: it eats up port 80 by default, so you'll need to run it as sudo):

`sudo ./start` starts the backend

`sudo ./stop` stops it

`sudo ./restart` well...you get it...

## some details
Its configured by default to control *wiringPi pins* 7, 0, 1, 4 which are mapped to light strands 0, 1, 2, 3 respectively.  Don't get these confused with the GPIO name, or the header number!

See here for more information: http://wiringpi.com/pins/

# Main hardware used
- RaspberryPi Model B
- SainSmart 5V 4-Channel Solid State Relay Board 
