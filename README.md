# nuvox-mobile
***

Table of Contents
=================


  * [What is nuvox?](#what-is-nuvox)
  * [What is nuvox-mobile?](#what-is-nuvox-mobile)
  * [Project Structure](#project-structure)
  * [Development Guide](#development-guide)
     * [Requirements](#requirements)
     * [Installation](#installation)
     * [Local Django Setup](#local-django-setup)
  * [Trace Algorithm Competition](#trace-algorithm-competition)
     * [What is a 'trace algorithm'?](#what-is-a-trace-algorithm)
     * [What's the challenge?](#whats-the-challenge)
     * [Algorithm Implementation](#algorithm-implementation)
     * [Dataset](#dataset)
     * [Evaluation on Training Set](#evaluation-on-training-set)
     * [Entering the Competition](#entering-the-competition)


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

## Project Structure
The project is divided into two parts:
- `/nuvox_algorithm` contains everything related to the predictive text algorithms.
- `/nuvox_app` contains a Django project which I've been using to collect training data, host the
trace algorithm competition etc.

***

## Development Guide

### Requirements
You'll probably need Python 3.6+.

### Installation
1. Clone the repo: `https://github.com/lukasmyth96/nuvox-mobile.git`.
2. Install dependencies: `pip install -r requirements.txt`

### Local Django Setup
_Note this is only required to access or work on the Django app - you don't need
to do this if you're just working on the trace algorithm._
1. Change directory to `nuvox_app`
2. Run `python manage.py migrate` - this will create a db.sqlite3 file.
3. Run `python manage.py createsuperuser` to create an admin account for yourself.
4. Run `python manage.py runserver` to run the development server.
5. Visit http://localhost:8000 to view the development server.

If you wish to access the development server on a mobile device then run `./runserver_mobile.sh`
and click on the link in the output. Note this script will only work on Linux and you will only
be able to access the server using a device on the same network.

***
## Trace Algorithm Competition


### What is a 'trace algorithm'?
The 'trace algorithm' is the first of two algorithms required by nuvox
in order to predict which word a user wants to write. At a high level, its goal is to
take the path traced by a users eye/finger/cursor in a single swipe and predict the sequence of keys that the user
intended to swipe.

Consider the swipe shown below for example where a user swipes the word 'hello'. The trace algorithm would receive the sequence of (x, y, time) coordinates
for each point in the path and predict the sequence of intended keys. In this case a reasonable algorithm may predict 3-2-1-4-5-6 or
3-2-4-6.

![Alt text](readme_assets/example_swipe.png?raw=true "Example swipe for the word 'hello'.")

### What's the challenge?
The challenge is simply to develop the best performing trace algorithm you can! The algorithm can
work in any way you like and may or may not use a machine learning model.

### Algorithm Implementation
- You should implement your algorithm by 'filling in' the `TraceAlgorithm` class in `nuvox_algorithm.trace_algorith.trace_algorithm.py`.
- The only requirement on your class is that it implements the `predict_intended_kis` method correctly.
- This is necessary for the evaluation and competition entry scripts to work. 
- Please read the docstring of this method for an explanation of its expected output.
- As a demo I have implemented a very simple baseline algorithm - feel free to delete this when you get started.


### Dataset
- To help you develop and evaluate your algorithm there is a training set provided in JSON format.
- To load the dataset import the `load_train_set` function from `nuvox_algorithm.trace_algorithm.utils`.
- This function downloads the data from GDrive and parses it into a list of convenient 'Swipe' objects.
- Each Swipe object in the dataset has the following attributes:
   - `trace: List[TracePoint]` is a list of each point in the trace. Each `TracePoint` object stores
   the x, y and time (s) coordinates of that point as well as the ID of the key which that point belongs to.
   - `target_word: str` is the word that the user intended to write.
   - `target_kis: str` is the intended key-id-sequence - e.g. if the target_word was 'hello' then the target_kis would
   be '3246'. Note this sequence is a string rather than list so that it's hashable and can be used as key of dictionary.
     

### Evaluation on Training Set
- Whilst developing your trace algorithm you may want to evaluate its performance on the training set.
- To do this run the script `nuvox_algorithm/trace_algorith/evaluate_trace_algorithm.py`.
- The script will print the accuracy of your algorithm on the train set.


### Entering the Competition
_Once you've implemented your algorithm follow these steps to enter the competition:_
1. Run the script `nuvox_algorithm/trace_algorithm/generate_compeition_submission.py`.
This will generate a `submission.json` file which contains the predictions of your algorithm
   on a separate test set where the labels have been removed.
2. Go to [http://nuvox-mobile-prod.eu-west-2.elasticbeanstalk.com/competition/](http://nuvox-mobile-prod.eu-west-2.elasticbeanstalk.com/competition/).
3. Click the link to enter the competition - sign up if you haven't already.
4. Copy and paste the entire contents of your `submission.json` file into the text box and submit.

### Useful Functions
- I have include a script `nuvox_algorithm/trace_algorithm/utils/visualizations/visualise_swipe.py` which
you can run to produce an animation of a single swipe. Note you may need to install: `sudo apt-get install python3-tk` for
this to work depending on your Python installation.  


***