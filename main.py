import tkinter as tk

water_level = 0
coffee_cups = 0

def add_water():
    global water_level
    water_level += 250  
    lbl_water.config(text=f"Water: {water_level} ml")

def add_coffee():
    global coffee_cups
    coffee_cups += 1  
    lbl_coffee.config(text=f"Coffee: {coffee_cups} Cups")

window = tk.Tk()
window.title("HydroCaff")
window.geometry("300x350")

lbl_title = tk.Label(window, text="My Daily Tracker", font=("Arial", 16, "bold"))
lbl_title.pack(pady=20)

lbl_water = tk.Label(window, text="Water: 0 ml", font=("Arial", 14))
lbl_water.pack(pady=5)

btn_water = tk.Button(window, text="+ 1 Glass of Water (250ml)", font=("Arial", 12), command=add_water)
btn_water.pack(pady=5)

spacer = tk.Label(window, text="")
spacer.pack(pady=10)

lbl_coffee = tk.Label(window, text="Coffee: 0 Cups", font=("Arial", 14))
lbl_coffee.pack(pady=5)

btn_coffee = tk.Button(window, text="+ 1 Cup of Coffee", font=("Arial", 12), command=add_coffee)
btn_coffee.pack(pady=5)

window.mainloop()