import customtkinter as ctk
import json 

DATA_FILE = "data.json"
water_level = 0
coffee_cups = 0
pos_x = 200
pos_y = 200

try:
    with open(DATA_FILE, "r") as file:
        data = json.load(file)
        water_level = data.get("water", 0)
        coffee_cups = data.get("coffee", 0)
        pos_x = data.get("x", 200)
        pos_y = data.get("y", 200)
except FileNotFoundError:
    pass

def save_data():

    window.update_idletasks()

    data = {
        "water": water_level,
        "coffee": coffee_cups,
        "x": window.winfo_x(),
        "y":window.winfo_y()
    }
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

def on_closing():
    save_data()
    window.destroy()

def add_water():
    global water_level
    water_level += 250  
    lbl_water.configure(text=f"Water: {water_level} ml")
    save_data() 

def add_coffee():
    global coffee_cups
    coffee_cups += 1  
    lbl_coffee.configure(text=f"Coffee: {coffee_cups} Cups")
    save_data() 

def reset_data():
    global water_level, coffee_cups
    water_level = 0
    coffee_cups = 0
    lbl_water.configure(text=f"Water: {water_level} ml")
    lbl_coffee.configure(text=f"Coffee: {coffee_cups} Cups")
    save_data() 

ctk.set_appearance_mode("System")
window = ctk.CTk()
window.title("HydroCaff")
window.geometry(f"300x420+{pos_x}+{pos_y}")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", on_closing)

lbl_title = ctk.CTkLabel(window, text="My Daily Tracker", font=("Arial", 16, "bold"))
lbl_title.pack(pady=20)

lbl_water = ctk.CTkLabel(window, text=f"Water: {water_level} ml", font=("Arial", 14))
lbl_water.pack(pady=5)

btn_water = ctk.CTkButton(window, text="+ 1 Glass of Water (250ml)", font=("Arial", 12),fg_color="#048ac9", hover_color="#044869", command=add_water)
btn_water.pack(pady=5)

spacer = ctk.CTkLabel(window, text="")
spacer.pack(pady=5)

lbl_coffee = ctk.CTkLabel(window, text=f"Coffee: {coffee_cups} Cups", font=("Arial", 14))
lbl_coffee.pack(pady=5)

btn_coffee = ctk.CTkButton(window, text="+ 1 Cup of Coffee", font=("Arial", 12), fg_color="#8b5a2b", hover_color="#6b4226", command=add_coffee)
btn_coffee.pack(pady=5)

spacer_bottom = ctk.CTkLabel(window, text="")
spacer_bottom.pack(pady=5)

btn_reset = ctk.CTkButton(window, text="Reset Today", font=("Arial", 12), 
                          fg_color="#cf0808", border_width=2, text_color=("gray10", "#DCE4EE"), 
                          hover_color="#650505", command=reset_data)
btn_reset.pack(pady=10)

window.mainloop()