# CansatRover
----
The project is created for the initial purpose of entering a tournament named CanSat Competition. With this code we will be controlling a rocket that will launch a can filled with a little rover, after a certain altitude a parachute will be displayed, in the air it will try to fall intothe launching position and if it doesn't land in the launching position, it will return to the launching position with a pair of motors. This specific repository will be runed in the controller (Rashberry PI) wth the task of managing all the stages of the Rover.

## QUICK START
---
1. The initial step for working with the repository is to have a 3.6 or further Python version installed.
2. AVOID THIS STEP IF YOU ARE USING THIS CODE ON THE CONTROLLER. The code should be developed and run by a virtual enviroment created with the above mentioned python version, to know the steps on how to set up the virtual env follow the instructions on **Tutorials/virtual_env**.
3. A requirements.txt will be included in order to download all the necessary libraries for succesfully running the code. To install the required libraries follow the instructions on **Tutorials/requirements.txt**

## Tutorials

### * Commiting to the project

Every development to the project must be dealt in a new branch created by the author for development, such branch can be worked only in the local repo, or if a long feature is being developed, then pushed to the repo. When the development is finished then a merge request will be issued and the contributors will accept such change if correct.

Commit message convention is:

type(scope): subject

body
footer
            
* Type:
            * feat : new feature
            * fix : bug fix
            * docs : changes in documentation
            * style : formating and style changes
            * refactor : code changes for refactoring 
            * perf : performance increase implementation
            * test : testing capabilities change (unit testing)
* Scope: a phrase describing parts of the code being affected by the commit (modules affected)
* Subject: short description
* Body (optional): further information of the change 
* Footer: to reference issues marked in ClickUp (tickets and/or tasks)

Example of a good commit message:


feat(RoverMain): new method to connect with roverData


### * Virtual Enviroment

1. in a Terminal instal the package for python virtual enviroment using pip
```js
python -m pip install virtualenv
```
*the above command depends on the enviroment
2. set up the virtual enviroment in the folder named **pyvirtual**
```js
python -m virtualenv venv
```
3. Activate the virtual env in the terminal to be used for execution
*For Linux
```js
source venv/bin/activate
```
*For windows
```js
venv/bin/activate
```

### * Requierements.txt
pip offers a way to automatically instal all the dependencies used in an enviroment by a requirements.txt.
Since a virtual enviroment is used then only requiered libraries will be isntalled. Before the installation the virtual enviroment must be activated, otherwise the requirements will be installed in your default python path.
To instal the requirements follow:
```js
python -m pip install -r requirements.txt
```

If a new dependency is added to the code the an update to the requirements is required. To do so follow:
```js
python -m pip freeze > requirements.txt
```
