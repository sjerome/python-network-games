python-network-games
====================

A framework to create simulations for strategic agents on a dynamic network

To run on a mac or linux based machine:

The harder way:  
1) Download the entire directory from GitHub.  
2) Check if pip is installed on the machine (type "which pip" into terminal. If a directory shows up, proceed to step 4.)  
3) Install pip. To do so, run the command: "sudo easy_install pip".  
4) Download the requirements (the ones included in requirements.txt). To do so, run the command "pip install -r requirements.txt". This may take some time, matplotlib has a lot of functionality and is a moderately large dependency.  
5) Run the simulation by typing python main.py  


The easier way: 
Open up terminal, and copy and paste these lines:  
git clone git@github.com:sjerome/python-network-games.git   
cd python-network-games  
sudo easy_install pip  
pip install -r requirements.txt   
python main.py  

To build a simulation:  
Choose some agents. The agents currently available can be found in Agents.py. Add to the list!  
Go to Simulations.py, and create a simulation. A simulation generally takes in as parameters and updating function,
and an initial configuration.  

If there are any questions, please feel free to email me at sjerome@princeton.edu.
