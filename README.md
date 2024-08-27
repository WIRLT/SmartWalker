# SmartWalker project, PC GUI and system code.
note: the code in here is used for the specific system for walkers built in tel aviv university.

## The project keep track of certain parameters for the walker and send them via wifi to a PC program (GUI).

### Full description of the project:
* a system that is attached to a normal walker.
* during the use of the walker by patients in a the rehabilitation process, the system provide real time tracking.
* it tracks: speed, distance, step size, grip force on the handles.
* the measured data is sent via wifi to a gui program sitting on PC.
* in the program as well it can save data showen on the screen at anytime.

### Demo
![Screenshot 2024-08-28 005022](https://github.com/user-attachments/assets/6d9dc271-4893-4733-a691-e60580e7c198)

### working with the files
* SmartWalker.py - the main gui file 
* check_run.py - the seconde gui page where data is showen in real time
* database.py - functions for working with database
* server_connection.py - functions to handle connections with the system placed at the walker
* system_code.txt - C++ code for the system uploaded to esp32 board
* users.db - database for patients saved by id (note id 0 is for testing)

#### how to run the GUI
1) clone the repository
```console
git clone https://github.com/WIRLT/SmartWalker.git
```
2) open the folder
```console
cd SmartWalker
```

3) run SmartWalker.py
```console
python3 ./SmartWalker.py
```
