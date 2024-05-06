import re
import numpy as np
import tkinter as tk
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import os
import sys

Tk().withdraw()
window = tk.Tk()
window.geometry("380x470")
window.resizable(width=False, height=False)
window.title("gcode straightener")
window.configure(bg="white")

mod_text = " "

def window_destroy():

    sys.exit()

window.protocol("WM_DELETE_WINDOW", window_destroy)

def ask_fn():
    global input_file, base_name
    input_file = askopenfilename(title='Select file to calibrate')
    base_name = os.path.basename(input_file)
    fn_label.config(text=base_name)


def ask_dir():
    global base_name, output_file
    path = askdirectory(title='Select output destination')
    os.chdir(path)
    output_file = f"calib_{base_name}"
    dir_label.config(text=path)


def save_mline(x,y):
    global input_file, output_file
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            modified_line = modify_gcode_line(line,x,y)
            outfile.write(modified_line)

# x_tgAlfa = (np.tan(np.deg2rad(0.4)))
# y_tgAlfa = (np.tan(np.deg2rad(0.2)))

nx = 0.0
ny = 0.0
x = 0.0
y = 0.0

def modify_gcode_line(line, x_value, y_value):
    #print(x_value, y_value)
    global nx, ny, x, y
    global mod_text
    #nx, ny = 0, 0
    x = float(x_value)
    y = float(y_value)
    x_tgAlfa = (np.tan(np.deg2rad(x)))
    y_tgAlfa = (np.tan(np.deg2rad(y)))

    if line.startswith(";Z:"):
        match = re.match(r';Z:([\d.]+)', line)
        if match:
            z = float(match.group(1))
            nx = x_tgAlfa * z
            ny = y_tgAlfa * z
        # -------------------------
    if line.startswith("G1"):
        match2 = re.match(r'G1\s+X([\d.]+)\s+Y([\d.]+)\s+E([\d.]+)', line)
        if match2:
            x = float(match2.group(1))
            y = float(match2.group(2))
            e = float(match2.group(3))
            x = x + nx
            y = y + ny
            return f"G1 X{x:.6f} Y{y:.6f} E{e:.6f}\n"
        # -------------------------------
    if line.startswith("G1"):
        match3 = re.match(r'G1\s+X([\d.]+)\s+Y([\d.]+)\s+E-([\d.]+)', line)
        if match3:
            x = float(match3.group(1))
            y = float(match3.group(2))
            e = float(match3.group(3))

            x = x + nx
            y = y + ny
            return f"G1 X{x:.6f} Y{y:.6f} E-{e:.6f}\n"

    if line.startswith("G1"):
        match4 = re.match(r'G1\s+X([\d.]+)\s+Y([\d.]+)', line)
        if match4:
            x = float(match4.group(1))
            y = float(match4.group(2))

            x = x + nx
            y = y + ny
            return f"G1 X{x:.6f} Y{y:.6f}\n"

    if line.startswith("G1"):
        match5 = re.match(r'G1\s+X([\d.]+)\s+F([\d.]+)', line)
        if match5:
            x = float(match5.group(1))
            f = float(match5.group(2))

            x = x + nx
            return f"G1 X{x:.6f} F{f:.6f}\n"

    if line.startswith("G1"):
        match6 = re.match(r'G1\s+Y([\d.]+)\s+E([\d.]+)\s+F([\d.]+)', line)
        if match6:
            x = float(match6.group(1))
            e = float(match6.group(2))
            f = float(match6.group(3))

            x = x + nx
            return f"G1 Y{x:.4f} E{e:.6f} F{f:.6f}\n"

    if line.startswith("G1"):
        match7 = re.match(r'G1\s+Y([\d.]+)\s+E-([\d.]+)\s+F([\d.]+)', line)
        if match7:
            x = float(match7.group(1))
            e = float(match7.group(2))
            f = float(match7.group(3))

            x = x + nx
            return f"G1 Y{x:.6f} E-{e:.6f} F{f:.6f}\n"
    mod_label.configure(text="calibrated")
    return line

# input_file, base_name =  ask_fn()
# output_file = ask_dir(base_name)
# save_mline(input_file, output_file)

# print(f"Plik G-code został zmodyfikowany i zapisany jako {output_file}.")
input_file, base_name, output_file = "","select input file", "select output directory"

window_frame = tk.LabelFrame(window, text="parameters", bg="white")


axis_frame = tk.LabelFrame(window_frame, text="angle values", bg="white")
input_frame = tk.LabelFrame(window_frame, text="input file", bg="white")
output_frame = tk.LabelFrame(window_frame, text="output directory", bg="white")

window_frame.grid(row = 0, column= 0, padx=10, pady=10, columnspan=2)


axis_frame.grid(row=0, column=0, padx=10, pady=10)
input_frame.grid(row=1, column=0, padx=10, pady=10)
output_frame.grid(row=2, column=0, padx=10, pady=10)

x_value = tk.Entry(axis_frame)

y_value = tk.Entry(axis_frame)
x = x_value
y = y_value


browse_button = tk.Button(input_frame, text="input file", command=lambda:ask_fn(),width=15)
dir_button =    tk.Button(output_frame, text="output directory", command=lambda: ask_dir(),width=15)
modify_button = tk.Button(window, text="compute", command=lambda: save_mline(x_value.get(), y_value.get()), width = 15)
exit_button =   tk.Button(window, text="exit", command=lambda:window_destroy(),width=15)

x_label = tk.Label(axis_frame, text="x axis:", bg = "white", anchor="w")
y_label = tk.Label(axis_frame, text="y axis:", bg = "white")
fn_label = tk.Label(input_frame, text=base_name,bg = "white", width = 20, anchor="e")
dir_label = tk.Label(output_frame, text=output_file,bg = "white", width = 20, anchor="e")
mod_label = tk.Label(window, text = mod_text, bg="white" )

x_value.grid(row = 0, column = 1, padx = 10, pady = 10)
y_value.grid(row = 1, column = 1, padx = 10, pady = 10)
browse_button.grid(row = 2, column = 0, padx = 10, pady = 10)
dir_button.grid(row = 3, column = 0, padx = 10, pady = 10)
modify_button.grid(row = 4, column = 0, padx = 10, pady = 10)
exit_button.grid(row = 5, column = 0, padx = 10, pady = 10)

x_label.grid(row=0, column=0, sticky="w")
y_label.grid(row=1, column=0, sticky = "w")
fn_label.grid(row=2, column=1, sticky="e")
dir_label.grid(row=3, column=1, sticky="e")
mod_label.grid(row=4, column = 1, sticky = "w")

window.mainloop()