import customtkinter as ctk
from tkinter import messagebox
import json
from pathlib import Path
from datetime import date

class HydroCaffApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HydroCaff")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        ctk.set_appearance_mode("System")

        self.data_dir = Path.home() / "AppData" / "Local" / "HydroCaff"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.data_dir / "data.json"

        self.water_level = 0
        self.coffee_cups = 0
        self.today = str(date.today())
        
        self.load_data()
        self.setup_ui()

    def load_data(self):
        pos_x, pos_y = 200, 200
        try:
            with open(self.data_file, "r", encoding = "utf-8") as file:
                data = json.load(file)
                pos_x = max(0, int(data.get("x", 200)))
                pos_y = max(0, int(data.get("y", 200)))
                
                if data.get("last_date", "") == self.today:
                    self.water_level = max(0, int(data.get("water", 0)))
                    self.coffee_cups = max(0, int(data.get("coffee", 0)))
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            pass
        
        self.geometry(f"300x420+{pos_x}+{pos_y}")

    def save_data(self):
        try:
            self.update_idletasks()
            data = {
                "water": self.water_level,
                "coffee": self.coffee_cups,
                "x": self.winfo_x(),
                "y": self.winfo_y(),
                "last_date": self.today
            }
            with open(self.data_file, "w", encoding = "utf-8") as file:
                json.dump(data, file, indent = 2)
        except OSError as e:
            print(f"Error saving data: {e}")

    def on_closing(self):
        self.save_data()
        self.destroy()

    def update_labels(self):
        self.lbl_water.configure(text=f"Water: {self.water_level} ml")
        self.lbl_coffee.configure(text=f"Coffee: {self.coffee_cups} Cups")

    def add_water(self):
        self.water_level += 250  
        self.update_labels()
        self.save_data() 

    def add_coffee(self):
        self.coffee_cups += 1  
        self.update_labels()
        self.save_data() 

    def reset_data(self):
        answer = messagebox.askyesno("Reset Data", "Are you sure you want to reset today's data?")
        if answer:
            self.water_level = 0
            self.coffee_cups = 0
            self.update_labels()
            self.save_data() 

    def setup_ui(self):
        self.lbl_title = ctk.CTkLabel(self, text="My Daily Tracker", font=("Arial", 16, "bold"))
        self.lbl_title.pack(pady=20)

        self.lbl_water = ctk.CTkLabel(self, text=f"Water: {self.water_level} ml", font=("Arial", 14))
        self.lbl_water.pack(pady=5)

        self.btn_water = ctk.CTkButton(self, text="+ 1 Glass of Water (250ml)", font=("Arial", 12),
                                       fg_color="#048ac9", hover_color="#044869", command=self.add_water)
        self.btn_water.pack(pady=5)

        self.spacer = ctk.CTkLabel(self, text="")
        self.spacer.pack(pady=5)

        self.lbl_coffee = ctk.CTkLabel(self, text=f"Coffee: {self.coffee_cups} Cups", font=("Arial", 14))
        self.lbl_coffee.pack(pady=5)

        self.btn_coffee = ctk.CTkButton(self, text="+ 1 Cup of Coffee", font=("Arial", 12), 
                                        fg_color="#8b5a2b", hover_color="#6b4226", command=self.add_coffee)
        self.btn_coffee.pack(pady=5)

        self.spacer_bottom = ctk.CTkLabel(self, text="")
        self.spacer_bottom.pack(pady=5)

        self.btn_reset = ctk.CTkButton(self, text="Reset Today", font=("Arial", 12), 
                                       fg_color="#cf0808", hover_color="#9D0606", command=self.reset_data)
        self.btn_reset.pack(pady=10)

if __name__ == "__main__":
    app = HydroCaffApp()
    app.mainloop()