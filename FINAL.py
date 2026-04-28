import RS485CombinedFINAL as com
import serial
import tkinter as tk
from tkinter import ttk
import time
import threading
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

arduino_port = '/dev/ttyACM0'

ser = serial.Serial(arduino_port, 9600, timeout=1)

csv_lock = threading.Lock()

# Initial CSV file setup

fileName = "Dixie05 Data" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
programStart = time.time()
csv_file = None
csv_writer = None

def make_csv(fileName):
    global csv_file, csv_writer # makes changes to the global variables. Needed to write to a new CSV file

    if csv_file:
        csv_file.close() # Closes an open CSV file if one is open

    # CSV writer
    csv_file = open(fileName, mode = "w", newline = "")
    csv_writer = csv.writer(csv_file)

    # Header of the CSV file
    csv_writer.writerow(["Timestamp", "Voltage A (V)", "Voltage B (V)","Voltage C (V)", "Current A (A)", "Current B (A)", "Current C (A)", "Temperature (\u00B0F)", "Airflow (CFM)", "Power (W)", "Power Factor"])

make_csv(fileName)

# GUI Window setup

root = tk.Tk()
root.title("Motor Control Dashboard")
root.geometry("1000x1000")

label_frame = tk.Frame(root)
label_frame.pack(side = tk.TOP, fill=tk.X)

# Setup of output data

voltage_labelA = ttk.Label(root, text = "Voltage A values: ---", font = ("Arial", 16))
voltage_labelB = ttk.Label(root, text = "Voltage B values: ---", font = ("Arial", 16))
voltage_labelC = ttk.Label(root, text = "Voltage C values: ---", font = ("Arial", 16))
voltage_labelA.pack(pady=5)
voltage_labelB.pack(pady=5)
voltage_labelC.pack(pady=5)

temp_label = ttk.Label(root, text = "Temperature values: ---", font = ("Arial", 16))
temp_label.pack(pady=5)

current_labelA = ttk.Label(root, text = "Current A values: ---", font = ("Arial", 16))
current_labelB = ttk.Label(root, text = "Current B values: ---", font = ("Arial", 16))
current_labelC = ttk.Label(root, text = "Current C values: ---", font = ("Arial", 16))
current_labelA.pack(pady=5)
current_labelB.pack(pady=5)
current_labelC.pack(pady=5)

airflow_label = ttk.Label(root, text = "Airflow values: ---", font = ("Arial", 16))
airflow_label.pack(pady=5)

power_label = ttk.Label(root, text = "Power values: ---", font = ("Arial", 16))
power_label.pack(pady=5)

powerF_label = ttk.Label(root, text = "PF values: ---", font = ("Arial", 16))
powerF_label.pack(pady=5)


# GUI Graph setup

window_size = 50  # number of samples shown in graph
voltage_dataA = deque([0.0]*window_size, maxlen=window_size)
voltage_dataB = deque([0.0]*window_size, maxlen=window_size)
voltage_dataC = deque([0.0]*window_size, maxlen=window_size)
temp_data = deque([0.0]*window_size, maxlen=window_size)
current_dataA = deque([0.0]*window_size, maxlen=window_size)
current_dataB = deque([0.0]*window_size, maxlen=window_size)
current_dataC = deque([0.0]*window_size, maxlen=window_size)
airflow_data = deque([0.0]*window_size, maxlen=window_size)
power_data = deque([0.0]*window_size, maxlen=window_size)
powerF_data = deque([0.0]*window_size, maxlen=window_size)

# Makes the graphs sit in a 3x3 plot, with the graphs being of size 12x10
fig, axes = plt.subplots(3,3,figsize=(12, 10), sharex=True)
axes = axes.flatten()

# Individual Graph initialization

voltage_lineA, = axes[0].plot(voltage_dataA, color="mediumslateblue", linewidth=2, label = "Voltage A") # Says what graph each data point is on, and formats the line
axes[0].set_ylim(0, 150) # Sets the y-axis
axes[0].set_xlim(0, window_size) # Sets the x-axis
axes[0].set_xlabel("Samples") # Label for the x-axis, can be changed as needed
axes[0].set_ylabel("Voltage A (V)") # Label for the y-axis
axes[0].grid(True, linestyle="--", alpha=0.6)
axes[0].legend()

voltage_lineB, = axes[1].plot(voltage_dataB, color="chartreuse", linewidth=2, label = "Voltage B") # Says what graph each data point is on, and formats the line
axes[1].set_ylim(0, 150) # Sets the y-axis
axes[1].set_xlim(0, window_size) # Sets the x-axis
axes[1].set_xlabel("Samples") # Label for the x-axis, can be changed as needed
axes[1].set_ylabel("Voltage B (V)") # Label for the y-axis
axes[1].grid(True, linestyle="--", alpha=0.6)
axes[1].legend()

voltage_lineC, = axes[2].plot(voltage_dataC, color="fuchsia", linewidth=2, label = "Voltage C") # Says what graph each data point is on, and formats the line
axes[2].set_ylim(0, 150) # Sets the y-axis
axes[2].set_xlim(0, window_size) # Sets the x-axis
axes[2].set_xlabel("Samples") # Label for the x-axis, can be changed as needed
axes[2].set_ylabel("Voltage C (V)") # Label for the y-axis
axes[2].grid(True, linestyle="--", alpha=0.6)
axes[2].legend()

temp_line, = axes[6].plot(temp_data, color="teal", linewidth=2, label = "Temperature") # Says what graph each data point is on, and formats the line
axes[6].set_ylim(0, 150) # Sets the y-axis
axes[6].set_xlim(0, window_size) # Sets the x-axis
axes[6].set_xlabel("Samples") # Label for the x-axis, can be changed as needed
axes[6].set_ylabel("Temperature (\u00B0F)") # Label for the y-axis
axes[6].grid(True, linestyle="--", alpha=0.6)
axes[6].legend()

current_lineA, = axes[3].plot(current_dataA, color="mediumslateblue", linewidth=2, label = "Current A") # Says what graph each data point is on, and formats the line
axes[3].set_ylim(0, 2) # Sets the y-axis
axes[3].set_xlim(0, window_size) # Sets the x-axis
axes[3].set_xlabel("Samples") # Label for the x-axis, can be changed as needed
axes[3].set_ylabel("Current (mA)") # Label for the y-axis
axes[3].grid(True, linestyle="--", alpha=0.6)
axes[3].legend()

current_lineB, = axes[4].plot(current_dataB, color="chartreuse", linewidth=2, label = "Current B") # Says what graph each data point is on, and formats the line
axes[4].set_ylim(0, 2) # Sets the y-axis
axes[4].set_xlim(0, window_size) # Sets the x-axis
axes[4].set_xlabel("Samples") # Label for the x-axis, can be changed as needed
axes[4].set_ylabel("Current B (mA)") # Label for the y-axis
axes[4].grid(True, linestyle="--", alpha=0.6)
axes[4].legend()

current_lineC, = axes[5].plot(current_dataC, color="fuchsia", linewidth=2, label = "Current C") # Says what graph each data point is on, and formats the line
axes[5].set_ylim(0, 2) # Sets the y-axis
axes[5].set_xlim(0, window_size) # Sets the x-axis
axes[5].set_xlabel("Samples") # Label for the x-axis, can be changed as needed
axes[5].set_ylabel("Current C (mA)") # Label for the y-axis
axes[5].grid(True, linestyle="--", alpha=0.6)
axes[5].legend()

airflow_line, = axes[7].plot(airflow_data, color="cyan", linewidth=2, label = "Airflow") # Says what graph each data point is on, and formats the line
axes[7].set_ylim(0, 5000) # Sets the y-axis
axes[7].set_xlim(0, window_size) # Sets the x-axis
axes[7].set_xlabel("Samples") # Label for the x-axis, can be changed as needed
axes[7].set_ylabel("Airflow (CFM)") # Label for the y-axis
axes[7].grid(True, linestyle="--", alpha=0.6)
axes[7].legend()

power_line, = axes[8].plot(power_data, color="tomato", linewidth=2, label = "Power") # Says what graph each data point is on, and formats the line
axes[8].set_ylim(0, 100) # Sets the y-axis
axes[8].set_xlim(0, window_size) # Sets the x-axis
axes[8].set_xlabel("Samples") # Label for the x-axis, can be changed as needed
axes[8].set_ylabel("Power (W)") # Label for the y-axis
axes[8].grid(True, linestyle="--", alpha=0.6)
axes[8].legend()

fig.tight_layout()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(pady=10)


# Uses a serial connecction to read the temperature values through the Arduino
def getTemp():

    try:
        raw = ser.readline().decode('utf-8', errors = 'ignore').strip()
        if raw:
            try:
                return float(raw)
            except ValueError:
                pass

    except Exception as e:
        print("Serial error:", e)


def read_serial():

    # Declares this as global variable so that the global instance is changed
    global programStart
    while True:
        try:
            # These call the asynchronous functions from the RS485CombinedFINAL file
            voltageA = com.asyncio.run_coroutine_threadsafe(com.async_rtu_voltageA(), loop).result()
            voltageB = com.asyncio.run_coroutine_threadsafe(com.async_rtu_voltageB(), loop).result()
            voltageC = com.asyncio.run_coroutine_threadsafe(com.async_rtu_voltageC(), loop).result()

            currA = com.asyncio.run_coroutine_threadsafe(com.async_rtu_currentA(), loop).result()
            currB = com.asyncio.run_coroutine_threadsafe(com.async_rtu_currentB(), loop).result()
            currC = com.asyncio.run_coroutine_threadsafe(com.async_rtu_currentC(), loop).result()

            temp = getTemp()

            air = com.asyncio.run_coroutine_threadsafe(com.async_rtu_air(), loop).result()
            powerA = com.asyncio.run_coroutine_threadsafe(com.async_rtu_powerA(), loop).result()
            powerB = com.asyncio.run_coroutine_threadsafe(com.async_rtu_powerB(), loop).result()
            powerC = com.asyncio.run_coroutine_threadsafe(com.async_rtu_powerC(), loop).result()
            
            powerF = com.asyncio.run_coroutine_threadsafe(com.powerFactor(), loop).result()

            # Calculates the average power over the three phases
            power = (powerA + powerB + powerC) / 3
            
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            currentTime = time.time()
            
            if (currentTime - programStart >= 300): # How often a new file is created
                # Same code as the instantiations above
                with csv_lock:
                    name = "Dixie05 Data"
                    fileName = name + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
                    make_csv(fileName)

                    # Resets the programStart to "0"
                    programStart = time.time()

            # Ensures that the csv files are always in sync
            # Essentially acts as a mutex lock -> one csv file can be open at any given time
            with csv_lock:
                csv_writer.writerow([timestamp, voltageA, voltageB, voltageC , currA, currB, currC, temp, air, power, powerF])
                csv_file.flush()

            # Calls the update GUI function with the values that are read
            root.after(0, update_gui, voltageA, voltageB, voltageC , currA, currB, currC, temp, air, power, powerF)

        except Exception as e:
            print("ERROR:", e)
        
        time.sleep(0.1)


def update_gui(voltageA, voltageB, voltageC, currentA, currentB, currentC, temperature, airflow, power, powerF):
     
     # Sets the values at the top of the GUI
     voltage_labelA.config(text=f"Voltage A: {voltageA:.2f} V")
     voltage_labelB.config(text=f"Voltage B: {voltageB:.2f} V")
     voltage_labelC.config(text=f"Voltage C: {voltageC:.2f} V")

     current_labelA.config(text=f"Current A: {currentA:.2f} mA")
     current_labelB.config(text=f"Current B: {currentB:.2f} mA")
     current_labelC.config(text=f"Current C: {currentC:.2f} mA")

     temp_label.config(text=f"Temperature: {temperature:.2f} \u00B0F")
     airflow_label.config(text=f"Airflow: {airflow:.2f} CFM")
     power_label.config(text=f"Power: {power:.2f} W")
     powerF_label.config(text=f"PowerF: {powerF:.2f}")

     # Formats the data to the formatting above

     voltage_dataA.append(voltageA)
     voltage_dataB.append(voltageB)
     voltage_dataC.append(voltageC)

     current_dataA.append(currentA)
     current_dataB.append(currentB)
     current_dataC.append(currentC)

     temp_data.append(temperature)

     airflow_data.append(airflow)
     power_data.append(power)
     powerF_data.append(powerF)

     # Creates the graph lines based on the data 

     voltage_lineA.set_ydata(voltage_dataA)
     voltage_lineB.set_ydata(voltage_dataB)
     voltage_lineC.set_ydata(voltage_dataC)
     current_lineA.set_ydata(current_dataA)
     current_lineB.set_ydata(current_dataB)
     current_lineC.set_ydata(current_dataC)
     temp_line.set_ydata(temp_data)

     airflow_line.set_ydata(airflow_data)
     power_line.set_ydata(power_data)

     canvas.draw_idle()


# Start and End

loop = com.asyncio.new_event_loop()
threading.Thread(target=loop.run_forever, daemon=True).start()
future = com.asyncio.run_coroutine_threadsafe(com.create_client(), loop)
future.result()
threading.Thread(target=read_serial, daemon = True).start()

def close():
    with csv_lock:
        if csv_file:
            csv_file.close()

    if com.client:
        loop.call_soon_threadsafe(loop.stop)
    
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close)

root.mainloop()