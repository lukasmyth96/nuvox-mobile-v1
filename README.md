# nuvox-mobile
***

## What is nuvox?

nuvox is an intelligent, on-screen keyboard that allows people to type with their
eyes using commercial eye-tracking hardware. The goal of the nuvox project is to 
leverage machine learning to maximise the speed at which people can communicate
in this manner and improve peoples quality of life as a result.

You can see the first prototype of nuvox [here](https://github.com/lukasmyth96/nuvox).

***
## What is nuvox-mobile?

The nuvox-mobile project aims to build the worlds fastest and smartest keyboard for mobile.
Building a mobile version will allow us to develop and test the core nuvox algorithm on anyone with
a phone, removing the requirement for users to own eye-tracking hardware. The goal is to then transfer
the algorithm back to eye-tracking once perfected.

***

## Development Guide

### Installation
1. Clone the repo: `https://github.com/lukasmyth96/nuvox-mobile.git`.
2. Install dependencies: `pip install -r requirements.txt`

### Local Django Setup
_Note this is only required to access or work on the Django app._
1. Change directory to `nuvox_app`
2. Run `python manage.py migrate` - this will create a db.sqlite3 file.
3. Run `python manage.py createsuperuser` to create an admin account for yourself.
4. Run `python manage.py runserver` to run the development server.
5. Visit http://localhost:8000 to view the development server.

If you wish to access the development server on a mobile device then run `./runserver_mobile.sh`
and click on the link in the output. Note this script will only work on Linux and you will only
be able to access the server using a device on the same network.

***
## Trace Algorithm Challenge


### What is the 'trace algorithm'?
The trace algorithm is the first of two algorithms required by nuvox
in order to predict which word a user intended to swipe. At a high level, its goal is to
take the path traced by a users eye/finger/cursor in a single swipe and predict the sequence of keys that the user
intended to swipe.

For example consider the keyboard layout shown below. 

![Alt text](nuvox_app/keyboard/static/keyboard/assets/nuvox_keyboard_img.png?raw=true "Test")

### What's the challenge?
There are

The algorithm receives as input a trace (sequence of
(x, y, t) triples) which describes the path that was traced by the users eyes/finger/mouse.
For each point in the trace x∈(0, 1) and y∈(0, 1) gives the location relative to the top-left
corner of the key-pad and t gives the time in seconds that has elapsed between the start of the
swipe and this point being recorded.