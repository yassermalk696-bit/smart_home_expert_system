import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Smart Home Expert System",
    page_icon="🏠",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #F3F6FC;
}
[data-testid="stSidebar"] {
    background-color: #172B4D;
}
[data-testid="stSidebar"] * {
    color: white;
}
h1, h2, h3 {
    color: #2563EB;
}
div.stButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🏠 Smart Home Expert System")
st.caption("SMART HOME / CONTROL CENTER")
st.divider()

if "devices" not in st.session_state:
    st.session_state.devices = {
        "Lights": True,
        "Air Conditioner": False,
        "Door Lock": True,
        "Alarm": True,
        "Smart Fan": False
    }

if "temperature" not in st.session_state:
    st.session_state.temperature = 24

if "energy_saving" not in st.session_state:
    st.session_state.energy_saving = False

if "activity_log" not in st.session_state:
    st.session_state.activity_log = []

if "diagnosis_history" not in st.session_state:
    st.session_state.diagnosis_history = []

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

def log_action(message):
    now = datetime.now().strftime("%H:%M:%S")
    st.session_state.activity_log.insert(
        0, f"{now} | {message}"
    )

page = st.sidebar.radio(
    "🏠 SMART HOME",
    [
        "Dashboard",
        "Smart Controls",
        "Expert Diagnosis",
        "Energy Saving",
        "Activity Log",
        "About Project"
    ]
)

st.sidebar.divider()
st.sidebar.caption("PYTHON PROJECT | VERSION 2.0")

if page == "Dashboard":
    st.header("Smart Home Dashboard")
    st.write("Monitor your smart devices and manage your home.")

    active = sum(st.session_state.devices.values())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Devices", len(st.session_state.devices))
    c2.metric("Devices ON", active)
    c3.metric("Room Temperature", f"{st.session_state.temperature}°C")
    c4.metric(
        "Energy Saving",
        "ON" if st.session_state.energy_saving else "OFF"
    )

    st.subheader("Device Status")
    for name, state in st.session_state.devices.items():
        st.write(f"{'🟢' if state else '🔴'} **{name}:** {'ON' if state else 'OFF'}")

    st.subheader("Quick Actions")
    st.info("Use the menu on the left to control devices, diagnose problems, and manage energy.")

elif page == "Smart Controls":
    st.header("Smart Device Controls")
    st.write("Switch devices ON or OFF and adjust room temperature.")

    for name, state in list(st.session_state.devices.items()):
        col1, col2 = st.columns([3, 1])
        col1.write(f"**{name}** — {'🟢 ON' if state else '🔴 OFF'}")
        if col2.button(
            "Turn OFF" if state else "Turn ON",
            key=f"device_{name}"
        ):
            st.session_state.devices[name] = not state
            log_action(
                f"{name} turned {'ON' if not state else 'OFF'}"
            )
            st.rerun()

    st.divider()
    new_temp = st.slider(
        "Room Temperature (°C)", 16, 32,
        st.session_state.temperature
    )
    if new_temp != st.session_state.temperature:
        st.session_state.temperature = new_temp

    if st.button("Save Temperature Setting"):
        log_action(
            f"Temperature set to {st.session_state.temperature}°C"
        )
        st.success("Temperature setting saved!")

elif page == "Expert Diagnosis":
    st.header("Expert Diagnosis")
    st.write(
        "Choose a problem. The rule-based system will suggest "
        "a possible cause and solution."
    )

    problem = st.selectbox("Select the problem:", list(rules.keys()))

    if st.button("🔍 Diagnose Problem", type="primary"):
        result = rules[problem]
        st.subheader(f"Problem: {problem}")
        st.warning(f"Possible cause: {result['cause']}")
        st.success(f"Recommended solution: {result['solution']}")

        st.session_state.diagnosis_history.insert(
            0, f"{datetime.now().strftime('%H:%M:%S')} | {problem}"
        )
        log_action(f"Diagnosed: {problem}")

elif page == "Energy Saving":
    st.header("Energy Management")
    st.write("Reduce unnecessary energy use with one simple setting.")

    st.metric(
        "Energy Saving Mode",
        "ON" if st.session_state.energy_saving else "OFF"
    )

    st.subheader("Energy-saving tips")
    st.write("- Turn off lights when leaving a room.")
    st.write("- Use the AC only when necessary.")
    st.write("- Switch off unused smart devices.")
    st.write("- Choose a comfortable temperature.")

    if st.button(
        "Turn OFF Energy Saving"
        if st.session_state.energy_saving
        else "Turn ON Energy Saving"
    ):
        st.session_state.energy_saving = not st.session_state.energy_saving

        if st.session_state.energy_saving:
            for name in ("Lights", "Air Conditioner", "Smart Fan"):
                st.session_state.devices[name] = False

        log_action(
            "Energy Saving turned "
            + ("ON" if st.session_state.energy_saving else "OFF")
        )
        st.rerun()

elif page == "Activity Log":
    st.header("Activity Log")
    st.write("Recent actions performed in this application.")

    if st.session_state.activity_log:
        for item in st.session_state.activity_log[:30]:
            st.write(f"🕒 {item}")
    else:
        st.info("No activities recorded yet.")

    if st.button("Clear Activity Log"):
        st.session_state.activity_log.clear()
        st.rerun()

    if st.session_state.diagnosis_history:
        st.subheader("Diagnosis History")
        for item in st.session_state.diagnosis_history[:20]:
            st.write(f"🔎 {item}")

elif page == "About Project":
    st.header("About the Project")
    st.write(
        "A Python-based educational Expert System "
        "for Smart Home management."
    )

    st.subheader("Project Information")
    st.write("**Project:** Smart Home Expert System")
    st.write("**Programming Language:** Python")
    st.write("**Interface Library:** Streamlit")
    st.write("**AI Method:** Rule-Based Expert System (IF-THEN)")
    st.write(
        "**Main Features:** Device controls, expert diagnosis, "
        "energy saving, and activity log."
    )

    st.info(
        "This is a simulation for educational purposes. "
        "It does not control real smart-home hardware."
    )

st.divider()
st.caption("Smart Home Expert System | Educational Project")
