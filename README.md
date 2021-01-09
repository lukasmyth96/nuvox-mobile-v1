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

## Repo Structure
The repo is divided into two parts
- `/nuvox_algorithm` contains everything related to the predictive text algorithms.
- `/nuvox_app` contains a Django project which I've been using to collect training data!

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


### What is a 'trace algorithm'?
The trace algorithm is the first of two algorithms required by nuvox
in order to predict which word a user intended to swipe. At a high level, its goal is to
take the path traced by a users eye/finger/cursor in a single swipe and predict the sequence of keys that the user
intended to swipe.

Consider the swipe shown below for example. The trace algorithm would receive the sequence of coordinates
in the path traced and predict the sequence of intended keys. In this case a reasonable algorithm may predict 3-2-1-4-5-6 or
3-2-4-6.

![Alt text](readme_assets/example_swipe.png?raw=true "Example swipe for the word 'hello'.")

### What's the challenge?
The challenge is simply to develop the best performing trace algorithm you can! The algorithm can
work in any way you like and may or may not use a machine learning model.

### Dataset
- To help you
develop and evaluate your algorithm there is a dataset provided in JSON format [here](https://drive.google.com/file/d/1xHxEiUHyiAlS-qjYE4J2syPOQVQcr_U5/view?usp=sharing).
- This file is a dump of a Postgres table containing ~1K+ swipes along with their intended word.
- You can use the `create_dataset(...)` function in `nuvox_algorithm/trace_algorithm/create_dataset.py` to 
parse this JSON file into a more convenient list of Python objects.
- See `nuvox_algorithm/trace_algorithm/swipe.py` for details about this `Swipe` class.  
-  NOTE - each swipe contains a boolean field `trace_matches_text` which indicates whether the
trace is a reasonable match for the target text. You can filter out inaccurate traces by passing `remove_inaccurate_swipes=True`
   to the `create_dataset(...)` function.

### Algorithm Implementation
You should implement your algorithm as a Python class. The only requirement of this class is that
it exposes a method called `predict_intended_kis` - see the docstring for this method in `nuvox_algorithm/trace_algorithm/trace_algorithm.py`
for more details.

### Evaluation
- A script is provided in `nuvox_algorithm/trace_algorithm/evaluate_trace_algorithm.py` for evaluating your algorithm.
- You will simply need to set the `DATA_DUMP_JSON_FILE` variable at the top of the script.
- The script will print the top-1 and top-3 accuracy (%) of your algorithm across the entire dataset.
- NOTE - if your algorithm uses a machine learning model make sure you leave a held-out test set for evaluation.

***