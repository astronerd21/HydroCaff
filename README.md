# HydroCaff

A modern desktop application to track your daily water and coffee intake. Built with Python and CustomTkinter.

## Features
* **Track Hydration & Caffeine:** Easily log water (in ml) and coffee (in cups) with a single click.
* **Automatic Daily Reset:** The tracker detects a new day and resets your counts to zero automatically.
* **Persistent Window Position:** The app remembers its last window position on your screen after closing.
* **Modern UI:** Clean interface with rounded buttons and system-matching Dark/Light mode support.
* **Data Persistence:** Saves your daily progress locally in a JSON file.

## Prerequisites
- Python 3.8 or newer

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/astronerd21/HydroCaff.git
   cd HydroCaff
   ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the App

Start the tracker with:
```bash
python main.py
```

## Building a Standalone Executable (Windows)
To build a standalone `.exe` that runs without a Python installation, use PyInstaller.

1. Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```
2. Run the build command in your project directory:
    ```bash
    python -m PyInstaller --noconsole --onefile --collect-all customtkinter main.py
    ```
    Note: If your terminal doesn't find the `pyinstaller` module because of PATH issues, run the absolute path to your Python executable, for example `C:\path\to\python.exe -m PyInstaller ...`.
3. The compiled `main.exe` will be in the `dist` folder. Rename it to `HydroCaff.exe` if you like and move it to your preferred program folder.

## Data Storage
Data is stored outside the project folder for robustness.

- Windows: `C:\Users\<YourUsername>\AppData\Local\HydroCaff\data.json`
- On other OSes the application uses the platform-specific user data directory.