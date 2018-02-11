# PiFlow

## Installation
Just copy the files to your Raspberry Pi. All the required libraries should already be installed.

## Usage
*Pump_Functions.py* has two functions that you can call:
* __Constant_Flow(Q1, Q2, T)__ where Q1 and Q2 are the flow rates for pumps 1 and 2 respectively, and T is the duration in seconds.
* __Dynamic_Flow(csv_path)__ where you can specify the path to a csv file with three columns. The first column should contain the sampling interval and the next two columns the flow rate for pumps 1 and 2. See Example_Profile.csv.

*PiFlow_Program.py* is the main program to run. In it you can call the two functions in *Pump_Functions.py*. Additionally you can configure your Raspberry Pi to load a script on boot if you want to run PiFlow on booting up without user intervention.

## Contributing
If you have any improvements in mind please feel free to contribute to the project via GitHub. If you encounter any issue running the above code please raise the issue here.
