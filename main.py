import tkinter as tk
from tkinter import ttk
from datetime import datetime

# ================== SETTINGS ==================
BG = "#F3F6FC"
WHITE = "#FFFFFF"
BLUE = "#2563EB"
DARK = "#172B4D"
GREEN = "#16A34A"
RED = "#DC2626"
GRAY = "#64748B"
PURPLE = "#7C3AED"

root = tk.Tk()
root.title("Smart Home Expert System")
root.geometry("1100x720")
root.minsize(900, 620)
root.configure(bg=BG)

devices = {
    "Lights": True,
    "Air Conditioner": False,
    "Door Lock": True,
    "Alarm": True,
    "Smart Fan": False
}

temperature = 24
energy_saving = False
activity_log = []
diagnosis_history = []

# Expert system rules: IF problem THEN cause and solution
rules = {
    "Lights not working": {
        "cause": "Possible power, bulb, or switch problem.",
        "solution": "Check the power supply, bulb, and light switch."
    },
    "Room is too hot": {
        "cause": "The room temperature may be too high.",
        "solution": "Turn on the AC, set a suitable temperature, and check ventilation."
    },
    "Wi-Fi disconnected": {
        "cause": "The router or network connection may be interrupted.",
        "solution": "Restart the router and check the network connection."
    },
    "Door lock problem": {
        "cause": "The smart lock may have a power or connection problem.",
        "solution": "Check the lock battery, connection, and locking mechanism."
    },
    "Alarm not working": {
        "cause": "The alarm may have no power or a sensor issue.",
        "solution": "Check the alarm power supply and sensor connections."
    },
    "High energy consumption": {
        "cause": "Devices may be running when they are not needed.",
        "solution": "Enable Energy Saving and switch off unused devices."
    },
    "Fan not working": {
        "cause": "The fan may be switched off or have a power issue.",
        "solution": "Check the power supply and fan settings."
    }
}

# ================== HELPER FUNCTIONS ==================
def log_action(message):
    time_now = datetime.now().strftime("%H:%M:%S")
    activity_log.insert(0, f"{time_now}  |  {message}")
    refresh_status()

def clear_main():
    for widget in main.winfo_children():
        widget.destroy()

def make_label(parent, text, size=12, color=DARK,
               bold=False, bg=None):
    return tk.Label(
        parent, text=text,
        font=("Segoe UI", size, "bold" if bold else "normal"),
        fg=color, bg=bg or parent["bg"],
        anchor="w", justify="left",
        wraplength=650
    )

def heading(title, subtitle=""):
    clear_main()
    make_label(main, title, 23, BLUE, True).pack(anchor="w", pady=(0, 5))
    if subtitle:
        make_label(main, subtitle, 10, GRAY).pack(anchor="w", pady=(0, 18))

def make_button(parent, text, command, color=BLUE):
    return tk.Button(
        parent, text=text, command=command,
        bg=color, fg=WHITE, activebackground=color,
        activeforeground=WHITE,
        font=("Segoe UI", 10, "bold"),
        relief="flat", bd=0, cursor="hand2",
        padx=12, pady=9
    )

def card(parent, title, value, color=BLUE):
    frame = tk.Frame(parent, bg=WHITE, highlightbackground="#E2E8F0",
                     highlightthickness=1, padx=15, pady=13)
    tk.Label(frame, text=title, bg=WHITE, fg=GRAY,
             font=("Segoe UI", 10)).pack(anchor="w")
    tk.Label(frame, text=value, bg=WHITE, fg=color,
             font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(7, 0))
    return frame

def refresh_status():
    if "status_label" in globals() and status_label.winfo_exists():
        active = sum(devices.values())
        status_label.config(
            text=f"Devices ON: {active}/{len(devices)}   |   "
                 f"Energy Saving: {'ON' if energy_saving else 'OFF'}"
        )

# ================== MAIN LAYOUT ==================
sidebar = tk.Frame(root, bg=DARK, width=205)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

topbar = tk.Frame(root, bg=WHITE, height=58)
topbar.pack(side="top", fill="x")
topbar.pack_propagate(False)

tk.Label(
    topbar, text="  SMART HOME  /  CONTROL CENTER",
    bg=WHITE, fg=DARK, font=("Segoe UI", 13, "bold")
).pack(side="left", padx=12, pady=15)

status_label = tk.Label(
    topbar, text="", bg=WHITE, fg=GREEN,
    font=("Segoe UI", 9, "bold")
)
status_label.pack(side="right", padx=15)

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=25, pady=22)

tk.Label(
    sidebar, text="SMART\nHOME", bg=DARK, fg="#93C5FD",
    font=("Segoe UI", 22, "bold"), justify="left"
).pack(anchor="w", padx=22, pady=(28, 30))

# ================== DASHBOARD ==================
def dashboard():
    heading("Smart Home Dashboard",
            "Monitor your smart devices and manage your home.")

    row = tk.Frame(main, bg=BG)
    row.pack(fill="x", pady=(0, 18))

    active = sum(devices.values())
    card(row, "TOTAL DEVICES", str(len(devices)), BLUE).pack(
        side="left", fill="x", expand=True, padx=(0, 8))
    card(row, "DEVICES ON", str(active), GREEN).pack(
        side="left", fill="x", expand=True, padx=8)
    card(row, "ROOM TEMPERATURE", f"{temperature}°C", PURPLE).pack(
        side="left", fill="x", expand=True, padx=8)
    card(row, "ENERGY SAVING",
         "ON" if energy_saving else "OFF",
         GREEN if energy_saving else RED).pack(
        side="left", fill="x", expand=True, padx=(8, 0))

    make_label(main, "Device Status", 15, DARK, True).pack(
        anchor="w", pady=(5, 10))

    device_box = tk.Frame(main, bg=WHITE, padx=18, pady=10)
    device_box.pack(fill="x", pady=(0, 18))

    for name, state in devices.items():
        line = tk.Frame(device_box, bg=WHITE)
        line.pack(fill="x", pady=5)
        make_label(line, name, 11, DARK, True, WHITE).pack(
            side="left")
        tk.Label(
            line, text="●  ON" if state else "●  OFF",
            bg=WHITE, fg=GREEN if state else RED,
            font=("Segoe UI", 10, "bold")
        ).pack(side="right")

    make_label(main, "Quick Actions", 15, DARK, True).pack(
        anchor="w", pady=(0, 8))

    quick = tk.Frame(main, bg=BG)
    quick.pack(fill="x")
    make_button(quick, "Device Controls", controls).pack(
        side="left", padx=(0, 8))
    make_button(quick, "Diagnose Problem", diagnosis, PURPLE).pack(
        side="left", padx=8)
    make_button(quick, "Energy Saving", energy_page, GREEN).pack(
        side="left", padx=8)

# ================== DEVICE CONTROLS ==================
def controls():
    heading("Smart Device Controls",
            "Switch devices ON or OFF and adjust room temperature.")

    for name, state in devices.items():
        row = tk.Frame(main, bg=WHITE, padx=15, pady=10)
        row.pack(fill="x", pady=5)

        tk.Label(row, text=name, bg=WHITE, fg=DARK,
                 font=("Segoe UI", 11, "bold")).pack(side="left")

        make_button(
            row, "Turn OFF" if state else "Turn ON",
            lambda n=name: toggle_device(n),
            RED if state else GREEN
        ).pack(side="right")

        tk.Label(
            row, text="ON" if state else "OFF",
            bg=WHITE, fg=GREEN if state else GRAY,
            font=("Segoe UI", 10, "bold")
        ).pack(side="right", padx=18)

    make_label(main, f"Room Temperature: {temperature}°C",
               13, DARK, True).pack(anchor="w", pady=(18, 4))

    temp_var = tk.IntVar(value=temperature)

    def update_temperature(value):
        global temperature
        temperature = int(float(value))
        temp_text.config(text=f"{temperature}°C")

    scale = tk.Scale(
        main, from_=16, to=32, orient="horizontal",
        variable=temp_var, command=update_temperature,
        bg=BG, fg=DARK, troughcolor="#BFDBFE",
        highlightthickness=0, length=450
    )
    scale.pack(anchor="w")

    temp_text = make_label(main, f"{temperature}°C", 11, BLUE, True)
    temp_text.pack(anchor="w")

    make_button(main, "Save Temperature Setting",
                lambda: log_action(
                    f"Temperature set to {temperature}°C"
                ), GREEN).pack(anchor="w", pady=12)

def toggle_device(name):
    devices[name] = not devices[name]
    log_action(f"{name} turned {'ON' if devices[name] else 'OFF'}")
    controls()

# ================== EXPERT DIAGNOSIS ==================
def diagnosis():
    heading("Expert Diagnosis",
            "Choose a problem. The rule-based system will suggest a cause and solution.")

    tk.Label(main, text="Select the problem:",
             bg=BG, fg=DARK, font=("Segoe UI", 11, "bold")).pack(
        anchor="w", pady=(5, 7))

    problem_var = tk.StringVar(value=list(rules.keys())[0])
    combo = ttk.Combobox(
        main, textvariable=problem_var,
        values=list(rules.keys()), state="readonly", width=42
    )
    combo.pack(anchor="w", ipady=5)

    result = tk.Frame(main, bg=WHITE, padx=18, pady=18)
    result.pack(fill="x", pady=18)

    result_title = tk.Label(
        result, text="Diagnosis result will appear here.",
        bg=WHITE, fg=BLUE, font=("Segoe UI", 13, "bold"),
        wraplength=650, justify="left"
    )
    result_title.pack(anchor="w")

    cause_text = tk.Label(
        result, text="", bg=WHITE, fg=DARK,
        font=("Segoe UI", 10), wraplength=650,
        justify="left"
    )
    cause_text.pack(anchor="w", pady=10)

    solution_text = tk.Label(
        result, text="", bg=WHITE, fg=GREEN,
        font=("Segoe UI", 10, "bold"),
        wraplength=650, justify="left"
    )
    solution_text.pack(anchor="w")

    def solve():
        problem = problem_var.get()
        rule = rules[problem]
        result_title.config(text=f"Problem: {problem}")
        cause_text.config(text=f"Possible cause: {rule['cause']}")
        solution_text.config(text=f"Recommended solution: {rule['solution']}")
        diagnosis_history.insert(
            0, f"{datetime.now().strftime('%H:%M:%S')} | {problem}"
        )
        log_action(f"Diagnosed: {problem}")

    make_button(main, "DIAGNOSE PROBLEM", solve, PURPLE).pack(
        anchor="w", pady=5)

# ================== ENERGY SAVING ==================
def energy_page():
    heading("Energy Management",
            "Reduce unnecessary energy use with one simple setting.")

    state = "ON" if energy_saving else "OFF"
    color = GREEN if energy_saving else RED
    card(main, "ENERGY SAVING MODE", state, color).pack(
        fill="x", pady=(0, 15))

    make_label(main, "Energy-saving tips", 14, DARK, True).pack(
        anchor="w", pady=(5, 8))

    tips = [
        "Turn off lights when leaving a room.",
        "Use the AC only when necessary.",
        "Switch off unused smart devices.",
        "Choose a comfortable temperature instead of extreme cooling."
    ]

    for tip in tips:
        tk.Label(main, text="•  " + tip, bg=WHITE, fg=DARK,
                 font=("Segoe UI", 10), padx=14, pady=9,
                 anchor="w").pack(fill="x", pady=3)

    make_button(
        main,
        "Turn OFF Energy Saving" if energy_saving
        else "Turn ON Energy Saving",
        toggle_energy, GREEN if not energy_saving else RED
    ).pack(anchor="w", pady=16)

def toggle_energy():
    global energy_saving
    energy_saving = not energy_saving

    if energy_saving:
        for name in ("Lights", "Air Conditioner", "Smart Fan"):
            devices[name] = False

    log_action(
        f"Energy Saving turned {'ON' if energy_saving else 'OFF'}"
    )
    energy_page()

# ================== ACTIVITY LOG ==================
def activity_page():
    heading("Activity Log",
            "Recent actions performed in this application.")

    if not activity_log:
        make_label(main, "No activities recorded yet.", 12, GRAY).pack(
            anchor="w", pady=10)
    else:
        for item in activity_log[:30]:
            tk.Label(
                main, text=item, bg=WHITE, fg=DARK,
                font=("Consolas", 10), anchor="w",
                padx=12, pady=8
            ).pack(fill="x", pady=3)

    make_button(main, "Clear Activity Log", clear_log, RED).pack(
        anchor="w", pady=12)

def clear_log():
    activity_log.clear()
    dashboard()

# ================== ABOUT ==================
def about():
    heading("About the Project",
            "A Python-based educational Expert System for Smart Homes.")

    details = [
        ("Project", "Smart Home Expert System"),
        ("Programming Language", "Python"),
        ("GUI Library", "Tkinter"),
        ("AI Method", "Rule-Based Expert System (IF-THEN)"),
        ("Main Features", "Device control, diagnosis, energy saving, activity log"),
        ("Device Connection", "Simulated devices; no physical hardware is connected.")
    ]

    for title, value in details:
        box = tk.Frame(main, bg=WHITE, padx=15, pady=12)
        box.pack(fill="x", pady=5)
        tk.Label(box, text=title, bg=WHITE, fg=BLUE,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(box, text=value, bg=WHITE, fg=DARK,
                 font=("Segoe UI", 10), wraplength=650,
                 justify="left").pack(anchor="w", pady=(4, 0))

# ================== NAVIGATION ==================
def nav_button(text, action):
    button = tk.Button(
        sidebar, text="   " + text, command=action,
        bg=DARK, fg=WHITE, activebackground=BLUE,
        activeforeground=WHITE, relief="flat", bd=0,
        font=("Segoe UI", 11), anchor="w",
        padx=12, pady=12, cursor="hand2"
    )
    button.pack(fill="x", padx=10, pady=3)

nav_button("Dashboard", dashboard)
nav_button("Smart Controls", controls)
nav_button("Expert Diagnosis", diagnosis)
nav_button("Energy Saving", energy_page)
nav_button("Activity Log", activity_page)
nav_button("About Project", about)

tk.Label(
    sidebar, text="PYTHON PROJECT\nVersion 2.0",
    bg=DARK, fg="#94A3B8",
    font=("Segoe UI", 9), justify="left"
).pack(side="bottom", anchor="w", padx=22, pady=22)

dashboard()
refresh_status()
root.mainloop()