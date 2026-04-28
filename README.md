# Final-Motor-Monitoring

This is written in the assumption that the setup used is similar to ours.

The folder consists of five other files: a datasheet for the voltage and current sensors,
a datasheet for the airflow sensor, the python files to run the code, and an Arduino file containing
the code to read from the temperature sensor.

For our project, we used and Arduino UNO R3, a Polaris 3000 meter, a Temco Controls AFS-150 airflow
sensor, a Raspberry Pi IV, and various power connections. We used the Raspberry Pi OS, but there is
no reason that a different OS can't be used.


1.  The required libraries are all imported at the top of the FINAL. py file,
	but some will need to be directly installed onto your machine before using
	
	a. The latest version of Python must also be installed on your machine.
	
	b. The GUI requires the matplotlib, tkinter, and collections libraries
	
	c. The serial library is only required if using an Arduino
	
	d. The time and csv libraries are used in the csv file creation

2.  The Arduino file needs to be uploaded to the Arduino once, and all serial
	monitors need to be closed
	
	a. Having a serial monitor open makes the UART busy, not allowing the project
	   to work
	   
3.  All of the sensor code is written in the RS485CombinedFINAL.py file. The registers
	are specified in the provided data sheets.
	
	a. If you want to ping a register specifically, you can run print(asyncio.run(async_rtu_powerA)), for example.
	
4.  The python files must be in the same directory to run properly.

5.  If a graph needs to be changed to show a different value, both the read_serial function and the 
	update_gui functions need to be updated to show the proper values. 
	
	a. A separate com.asyncio call must be made to an async function pulling in the desired reading.
	   On top of that, the variable will need to be passed into the update_gui function, where it
	   will need it's own set of .config, .append, and .set_ydata.
	   
	   i. The existing lines can be updated in place of writing new lines.
	
Comments are provided in each file to explain the reasoning behind the lines of code.

CSV file creation is automated to every 5 minutes (written as 300 seconds in the code), but that number
can easily be changed to however long is needed. 
