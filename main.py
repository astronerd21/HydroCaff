import tkinter as tk
import json 

DATA_FILE = "data.json"
water_level = 0
coffee_cups = 0

try:
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
        water_level = data.get("water", 0)
        coffee_cups = data.get("coffee", 0)
except FileNotFoundError:
    pass

def save_data():
    data = {
        "water": water_level,
        "coffee": coffee_cups
    }
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

def add_water():
    global water_level
    water_level += 250  
    lbl_water.config(text=f"Water: {water_level} ml")
    save_data() 

def add_coffee():
    global coffee_cups
    coffee_cups += 1  
    lbl_coffee.config(text=f"Coffee: {coffee_cups} Cups")
    save_data() 

def reset_data():
    global water_level, coffee_cups
    water_level = 0
    coffee_cups = 0
    lbl_water.config(text=f"Water: {water_level} ml")
    lbl_coffee.config(text=f"Coffee: {coffee_cups} Cups")
    save_data() 

window = tk.Tk()
window.title("HydroCaff")
window.geometry("300x420") 

lbl_title = tk.Label(window, text="My Daily Tracker", font=("Arial", 16, "bold"))
lbl_title.pack(pady=20)

lbl_water = tk.Label(window, text=f"Water: {water_level} ml", font=("Arial", 14))
lbl_water.pack(pady=5)

btn_water = tk.Button(window, text="+ 1 Glass of Water (250ml)", font=("Arial", 12), command=add_water)
btn_water.pack(pady=5)

spacer = tk.Label(window, text="")
spacer.pack(pady=5)

lbl_coffee = tk.Label(window, text=f"Coffee: {coffee_cups} Cups", font=("Arial", 14))
lbl_coffee.pack(pady=5)

btn_coffee = tk.Button(window, text="+ 1 Cup of Coffee", font=("Arial", 12), command=add_coffee)
btn_coffee.pack(pady=5)

spacer_bottom = tk.Label(window, text="")
spacer_bottom.pack(pady=5)

btn_reset = tk.Button(window, text="Reset Today", font=("Arial", 10), fg="red", command=reset_data)
btn_reset.pack(pady=10)

window.mainloop()