import tkinter as tk
from tkinter import ttk

def get_selected_value():
    selected_value = combo_box.get()
    print("Selected value:", selected_value)

# Create a tkinter window
root = tk.Tk()
root.title("ComboBox Example")

# Create a Combobox
combo_box = ttk.Combobox(root)
combo_box['values'] = ("Option 1", "Option 2", "Option 3", "Option 4")
combo_box.pack()

# Create a button to get the selected value
get_value_button = tk.Button(root, text="Get Selected Value", command=get_selected_value)
get_value_button.pack()

root.mainloop()
