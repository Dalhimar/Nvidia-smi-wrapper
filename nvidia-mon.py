import tkinter as tk
import subprocess

#Nvidia-smi query
def get_nvidia_smi_output(gpu_id):
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=index,name,utilization.gpu,memory.total,memory.used,temperature.gpu,power.draw,power.limit', '--format=csv,noheader,nounits', '--id=' + str(gpu_id)], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip().split('\n')[0].split(',')
    except:
        return []

#function to start polling
def start_polling():
    global polling
    polling = True
    gpu_id = gpu_id_input.get()
    update_output(gpu_id)

#function to stop polling
def stop_polling():
    global polling
    polling = False

#function to set the interval
def set_polling_interval(value):
    global polling_interval
    polling_interval = int(value)
    polling_interval_label.config(text=f"{value} ms")  # Update label with current interval

#Update gpu data in the GUI
def update_output(gpu_id):
    if polling:
        data = get_nvidia_smi_output(gpu_id)
        if data:
           index_value_label.config(text=data[0])
           name_value_label.config(text=data[1])
           utilization_canvas.itemconfig(utilization_text, text="Utilization: " + data[2] + "%")
           utilization_canvas.coords(utilization_bar, 0, 0, float(data[2]) * 4, 20)
           used_memory = float(data[4])
           total_memory = float(data[3])
           memory_canvas.itemconfig(memory_text, text=f"{used_memory} MB / {total_memory} MB")
           memory_canvas.coords(memory_bar, 0, 0, (used_memory / total_memory) * 400, 20)
           temperature_value_label.config(text=data[5] + "°C", justify=tk.CENTER,)
           current_wattage = float(data[6])
           max_wattage = float(data[7])
           power_canvas.itemconfig(power_text, text=f"{current_wattage}w / {max_wattage}w")
           power_canvas.coords(power_bar, 0, 0, (current_wattage / max_wattage) * 400, 20)

        root.after(polling_interval, lambda: update_output(gpu_id))  # Use the polling_interval variable

#set up the main window
root = tk.Tk()
root.title("NVIDIA SMI Monitor")
root.geometry("400x230")
root.resizable(width=False, height=False)

#Interval menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

polling_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Polling Interval", menu=polling_menu)

polling_interval = 1000  # Default polling interval in milliseconds
polling_interval_var = tk.IntVar(value=polling_interval) # Declare the variable here

polling_menu.add_radiobutton(label="1000 ms", value=1000, variable=polling_interval_var, command=lambda: set_polling_interval(1000))
polling_menu.add_radiobutton(label="500 ms", value=500, variable=polling_interval_var, command=lambda: set_polling_interval(500))
polling_menu.add_radiobutton(label="250 ms", value=250, variable=polling_interval_var, command=lambda: set_polling_interval(250))
polling_menu.add_radiobutton(label="100 ms", value=100, variable=polling_interval_var, command=lambda: set_polling_interval(100))


#current interval
polling_label = tk.Label(menu_bar, text=f"Current: {polling_interval} ms", relief=tk.SUNKEN, anchor=tk.W)
polling_label.pack(side=tk.RIGHT)

#create GUI frames to contain the GPU data
def create_frame(root, title, justify=tk.W, create_bar=False):
    frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
    frame.pack(fill=tk.X, padx=5, pady=2)
    if create_bar:
        canvas = tk.Canvas(frame, height=20, width=400, bg='white')
        canvas.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=2)
        bar = canvas.create_rectangle(0, 0, 0, 20, fill='green')
        text = canvas.create_text(200, 10, text='', anchor=justify)
        tk.Label(frame, text=title, anchor=tk.W).pack(side=tk.LEFT, padx=5, pady=2)
        return text, canvas, bar
    else:
        tk.Label(frame, text=title, anchor=tk.W).pack(side=tk.LEFT, padx=5, pady=2)
        value_label = tk.Label(frame, anchor=justify)
        value_label.pack(side=tk.RIGHT, padx=5, pady=2)
        return value_label

index_value_label = create_frame(root, "Index:")
name_value_label = create_frame(root, "Name:")
utilization_text, utilization_canvas, utilization_bar = create_frame(root, "GPU Utilization:", justify=tk.CENTER, create_bar=True)
memory_text, memory_canvas, memory_bar = create_frame(root, "Memory Usage:", justify=tk.CENTER, create_bar=True)

power_text, power_canvas, power_bar = create_frame(root, "Power Consumption:", justify=tk.CENTER, create_bar=True)
temperature_value_label = create_frame(root, "Temperature:")

# New frame for the GPU selection, start, and stop buttons.
selection_frame = tk.Frame(root, bd=2, relief=tk.GROOVE)
selection_frame.pack(fill=tk.X, padx=5, pady=2)

tk.Label(selection_frame, text="GPU ID:").pack(side=tk.LEFT, padx=5, pady=2)
gpu_id_input = tk.Entry(selection_frame, width=5)
gpu_id_input.pack(side=tk.LEFT, padx=5, pady=2)

# Create a label to display the polling interval
polling_interval_label = tk.Label(selection_frame, text=f"{polling_interval} ms")
polling_interval_label.pack(side=tk.LEFT, padx=5, pady=2)

start_button = tk.Button(selection_frame, text="Start", command=start_polling)
start_button.pack(side=tk.LEFT, padx=5, pady=2)

stop_button = tk.Button(selection_frame, text="Stop", command=stop_polling)
stop_button.pack(side=tk.LEFT, padx=5, pady=2)

polling = False  # Variable to control the polling state.

# Comment out the existing update_output call.

root.mainloop()
