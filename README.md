python-network-games
====================

A framework to create simulations for strategic agents on a dynamic network <br />

To run on a linux based machine: <br />
1) Download the entire directory from GitHub. <br />
2) Check if pip is installed on the machine (type "which pip" into terminal. If a directory shows up, proceed to step 4.) <br />
3) Install pip. To do so, run the command: "sudo easy_install pip". <br />
4) Download the requirements (the ones included in requirements.txt). To do so, run the command "pip install -r <br /> requirements.txt". This may take some time, matplotlib has a lot of functionality and is a moderately large dependency. <br />
5) Run the simulation by typing python main.py <br />
<br />
Or, just type these next few lines into terminal: <br />
git clone git@github.com:sjerome/python-network-games.git <br />
cd python-network-games <br />
sudo easy_install pip <br />
pip install -r requirements.txt <br />
python main.py <br />

To build a simulation:
Choose some agents. The agents currently available can be found in Agents.py. Add to the list!
Go to Simulations.py, and create a simulation. A simulation generally takes in as parameters and updating function,
and an initial configuration. 

If there are any questions, please feel free to email me at sjerome@princeton.edu.
