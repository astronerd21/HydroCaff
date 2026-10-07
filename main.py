import customtkinter as ctk
from tkinter import messagebox
import json
from pathlib import Path
from datetime import date, timedelta

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class HydroCaffApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HydroCaff")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.configure(fg_color="#121417")

        self.data_dir = Path.home() / "AppData" / "Local" / "HydroCaff"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data_file = self.data_dir / "data.json"

        self.water_goal = 2000
        self.coffee_guide = 4
        self.coffee_cup_ml = 180

        self.history = {}
        self.current_date_str = str(date.today())

        self.load_data()
        self.setup_ui()
        self.update_ui_state()

    @property
    def today_water(self):
        return self.history.get(self.current_date_str, {}).get("water", 0)

    @property
    def today_coffee(self):
        return self.history.get(self.current_date_str, {}).get("coffee", 0)

    def load_data(self):
        pos_x, pos_y = 200, 200
        try:
            if self.data_file.exists():
                with open(self.data_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    pos_x = int(data.get("x", 200))
                    pos_y = int(data.get("y", 200))
                    self.history = data.get("history", {})

                    if not self.history and "last_date" in data:
                        last_d = data.get("last_date", self.current_date_str)
                        self.history[last_d] = {
                            "water": max(0, int(data.get("water", 0))),
                            "coffee": max(0, int(data.get("coffee", 0))),
                        }
        except (OSError, json.JSONDecodeError, ValueError):
            self.history = {}

        if self.current_date_str not in self.history:
            self.history[self.current_date_str] = {"water": 0, "coffee": 0}

        x_str = f"+{pos_x}" if pos_x >= 0 else str(pos_x)
        y_str = f"+{pos_y}" if pos_y >= 0 else str(pos_y)
        self.geometry(f"340x670{x_str}{y_str}")

    def save_data(self):
        try:
            self.update_idletasks()

            if len(self.history) > 365:
                sorted_dates = sorted(self.history.keys())[-365:]
                self.history = {d: self.history[d] for d in sorted_dates}

            data = {"x": self.winfo_x(), "y": self.winfo_y(), "history": self.history}

            temp_file = self.data_file.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2)
            temp_file.replace(self.data_file)
        except OSError as e:
            print(f"Fehler beim Speichern: {e}")

    def on_closing(self):
        self.save_data()
        self.destroy()

    def add_water(self, amount):
        current = self.today_water
        self.history[self.current_date_str]["water"] = max(0, current + amount)
        self.update_ui_state()
        self.save_data()

    def add_coffee(self, amount):
        current = self.today_coffee
        self.history[self.current_date_str]["coffee"] = max(0, current + amount)
        self.update_ui_state()
        self.save_data()

    def reset_data(self):
        if messagebox.askyesno(
            "Reset Today", "Wasser- und Kaffeezähler für heute zurücksetzen?"
        ):
            self.history[self.current_date_str] = {"water": 0, "coffee": 0}
            self.update_ui_state()
            self.save_data()

    def update_ui_state(self):
        water = self.today_water
        coffee = self.today_coffee

        glasses = water / 250.0
        glass_str = f"{int(glasses)}" if glasses.is_integer() else f"{glasses:.1f}"
        self.lbl_water_sub.configure(text=f"• {glass_str} glasses")
        self.lbl_water_val.configure(text=f"{water:,}".replace(",", "."))

        water_progress = min(1.0, water / self.water_goal)
        self.bar_water.set(water_progress)
        self.lbl_water_status.configure(
            text="✓ Goal reached" if water >= self.water_goal else ""
        )

        coffee_ml = coffee * self.coffee_cup_ml
        self.lbl_coffee_sub.configure(text=f"• {coffee_ml} ml total")
        self.lbl_coffee_val.configure(text=str(coffee))

        dot_count = min(coffee, 6)
        extra = coffee - 6
        dots_text = "● " * dot_count + (f"+{extra}" if extra > 0 else "")
        self.lbl_coffee_dots.configure(text=dots_text.strip() or " ")

        coffee_progress = min(1.0, coffee / self.coffee_guide)
        self.bar_coffee.set(coffee_progress)

        if coffee > self.coffee_guide:
            self.lbl_coffee_val.configure(text_color="#e06c53")
            self.bar_coffee.configure(progress_color="#c94949")
        else:
            self.lbl_coffee_val.configure(text_color="#f0f3f6")
            self.bar_coffee.configure(progress_color="#a8622c")

        self.update_week_bars()

    def update_week_bars(self):
        today_date = date.today()
        for i in range(7):
            d = today_date - timedelta(days=(6 - i))
            d_str = str(d)
            day_label = d.strftime("%a")

            data_entry = self.history.get(d_str, {})
            water_val = data_entry.get("water", 0)
            coffee_val = data_entry.get("coffee", 0)

            ratio = min(1.0, water_val / self.water_goal)
            self.day_bars[i].set(ratio)
            self.day_labels[i].configure(
                text=day_label, text_color="#1496a6" if i == 6 else "#78828f"
            )
            dots = min(coffee_val, 4)
            self.day_dots[i].configure(text="•" * dots if dots > 0 else " ")

    def setup_ui(self):
        f_head = ctk.CTkFrame(self, fg_color="transparent")
        f_head.pack(fill="x", padx=16, pady=(16, 12))

        ctk.CTkLabel(
            f_head, text="HydroCaff", font=("Georgia", 19, "bold"), text_color="#f0f3f6"
        ).pack(side="left")

        ctk.CTkLabel(
            f_head,
            text=date.today().strftime("%a, %b %d"),
            font=("Arial", 11, "bold"),
            fg_color="#1e2229",
            text_color="#9da7b3",
            corner_radius=12,
            padx=10,
            pady=3,
        ).pack(side="right")

        f_w = ctk.CTkFrame(self, fg_color="#181b20", corner_radius=12)
        f_w.pack(fill="x", padx=14, pady=6)

        f_w_top = ctk.CTkFrame(f_w, fg_color="transparent")
        f_w_top.pack(fill="x", padx=14, pady=(12, 0))

        ctk.CTkLabel(
            f_w_top, text="Water", font=("Arial", 13, "bold"), text_color="#1eb4c6"
        ).pack(side="left")
        self.lbl_water_sub = ctk.CTkLabel(
            f_w_top, text="• 0 glasses", font=("Arial", 11), text_color="#6e7887"
        )
        self.lbl_water_sub.pack(side="left", padx=5)
        ctk.CTkLabel(
            f_w_top,
            text=f"Goal {self.water_goal:,} ml".replace(",", "."),
            font=("Arial", 11),
            text_color="#6e7887",
        ).pack(side="right")

        f_w_val = ctk.CTkFrame(f_w, fg_color="transparent")
        f_w_val.pack(fill="x", padx=14, pady=(4, 6))

        self.lbl_water_val = ctk.CTkLabel(
            f_w_val, text="0", font=("Georgia", 28, "bold"), text_color="#f0f3f6"
        )
        self.lbl_water_val.pack(side="left")
        ctk.CTkLabel(
            f_w_val, text=" ml", font=("Georgia", 14), text_color="#9da7b3"
        ).pack(side="left", pady=(10, 0))

        self.lbl_water_status = ctk.CTkLabel(
            f_w_val, text="", font=("Arial", 11, "bold"), text_color="#1496a6"
        )
        self.lbl_water_status.pack(side="right", pady=(10, 0))

        self.bar_water = ctk.CTkProgressBar(
            f_w, progress_color="#1496a6", fg_color="#242a33", height=7, corner_radius=4
        )
        self.bar_water.pack(fill="x", padx=14, pady=(0, 10))

        f_w_btn = ctk.CTkFrame(f_w, fg_color="transparent")
        f_w_btn.pack(fill="x", padx=14, pady=(0, 12))

        ctk.CTkButton(
            f_w_btn,
            text="—",
            width=42,
            height=38,
            font=("Arial", 15, "bold"),
            fg_color="#21252d",
            hover_color="#2c323d",
            text_color="#f0f3f6",
            corner_radius=8,
            command=lambda: self.add_water(-250),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            f_w_btn,
            text="+ Add a glass • 250 ml",
            height=38,
            font=("Arial", 12, "bold"),
            fg_color="#1496a6",
            hover_color="#0f7785",
            text_color="#ffffff",
            corner_radius=8,
            command=lambda: self.add_water(250),
        ).pack(side="left", fill="x", expand=True)

        f_c = ctk.CTkFrame(self, fg_color="#181b20", corner_radius=12)
        f_c.pack(fill="x", padx=14, pady=6)

        f_c_top = ctk.CTkFrame(f_c, fg_color="transparent")
        f_c_top.pack(fill="x", padx=14, pady=(12, 0))

        ctk.CTkLabel(
            f_c_top, text="Coffee", font=("Arial", 13, "bold"), text_color="#c88242"
        ).pack(side="left")
        self.lbl_coffee_sub = ctk.CTkLabel(
            f_c_top, text="• 0 ml total", font=("Arial", 11), text_color="#6e7887"
        )
        self.lbl_coffee_sub.pack(side="left", padx=5)
        ctk.CTkLabel(
            f_c_top,
            text=f"Guide {self.coffee_guide} cups",
            font=("Arial", 11),
            text_color="#6e7887",
        ).pack(side="right")

        f_c_val = ctk.CTkFrame(f_c, fg_color="transparent")
        f_c_val.pack(fill="x", padx=14, pady=(4, 6))

        self.lbl_coffee_val = ctk.CTkLabel(
            f_c_val, text="0", font=("Georgia", 28, "bold"), text_color="#f0f3f6"
        )
        self.lbl_coffee_val.pack(side="left")
        ctk.CTkLabel(
            f_c_val, text=" cups", font=("Georgia", 14), text_color="#9da7b3"
        ).pack(side="left", pady=(10, 0))

        self.lbl_coffee_dots = ctk.CTkLabel(
            f_c, text="", font=("Arial", 13), text_color="#a8622c"
        )
        self.lbl_coffee_dots.pack(anchor="w", padx=14, pady=(0, 4))

        self.bar_coffee = ctk.CTkProgressBar(
            f_c, progress_color="#a8622c", fg_color="#242a33", height=7, corner_radius=4
        )
        self.bar_coffee.pack(fill="x", padx=14, pady=(0, 10))

        f_c_btn = ctk.CTkFrame(f_c, fg_color="transparent")
        f_c_btn.pack(fill="x", padx=14, pady=(0, 12))

        ctk.CTkButton(
            f_c_btn,
            text="—",
            width=42,
            height=38,
            font=("Arial", 15, "bold"),
            fg_color="#21252d",
            hover_color="#2c323d",
            text_color="#f0f3f6",
            corner_radius=8,
            command=lambda: self.add_coffee(-1),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            f_c_btn,
            text="+ Add a cup • 180 ml",
            height=38,
            font=("Arial", 12, "bold"),
            fg_color="#915222",
            hover_color="#733f18",
            text_color="#ffffff",
            corner_radius=8,
            command=lambda: self.add_coffee(1),
        ).pack(side="left", fill="x", expand=True)

        f_hist = ctk.CTkFrame(self, fg_color="#181b20", corner_radius=12)
        f_hist.pack(fill="x", padx=14, pady=6)

        f_hist_top = ctk.CTkFrame(f_hist, fg_color="transparent")
        f_hist_top.pack(fill="x", padx=14, pady=(10, 8))

        ctk.CTkLabel(
            f_hist_top,
            text="LAST 7 DAYS",
            font=("Arial", 10, "bold"),
            text_color="#78828f",
        ).pack(side="left")
        ctk.CTkLabel(
            f_hist_top, text="● Coffee", font=("Arial", 9, "bold"), text_color="#a8622c"
        ).pack(side="right", padx=(4, 0))
        ctk.CTkLabel(
            f_hist_top, text="● Water", font=("Arial", 9, "bold"), text_color="#1496a6"
        ).pack(side="right")

        f_bars = ctk.CTkFrame(f_hist, fg_color="transparent")
        f_bars.pack(fill="x", padx=10, pady=(0, 10))

        self.day_bars = []
        self.day_labels = []
        self.day_dots = []

        for i in range(7):
            col = ctk.CTkFrame(f_bars, fg_color="transparent")
            col.pack(side="left", expand=True, fill="both")

            p_bar = ctk.CTkProgressBar(
                col,
                orientation="vertical",
                width=12,
                height=48,
                progress_color="#1496a6",
                fg_color="#242a33",
                corner_radius=4,
            )
            p_bar.pack(pady=(4, 4))
            p_bar.set(0)
            self.day_bars.append(p_bar)

            lbl_d = ctk.CTkLabel(col, text="", font=("Arial", 9), text_color="#78828f")
            lbl_d.pack()
            self.day_labels.append(lbl_d)

            lbl_dot = ctk.CTkLabel(
                col, text=" ", font=("Arial", 8), text_color="#a8622c"
            )
            lbl_dot.pack(pady=(0, 2))
            self.day_dots.append(lbl_dot)

        ctk.CTkButton(
            self,
            text="↺  Reset today",
            height=32,
            font=("Arial", 11),
            fg_color="transparent",
            hover_color="#261b1d",
            text_color="#c94949",
            border_width=1,
            border_color="#382124",
            corner_radius=8,
            command=self.reset_data,
        ).pack(fill="x", padx=14, pady=(8, 14))


if __name__ == "__main__":
    app = HydroCaffApp()
    app.mainloop()
