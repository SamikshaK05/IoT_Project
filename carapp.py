import streamlit as st
import requests

# -------- CONFIG (IMPORTANT FIX: http:// added) --------
ESP32_URL = "http://10.70.241.202"   # 🔴 Change this if IP changes

st.set_page_config(layout="wide")

# -------- STYLING --------
st.markdown("""
<style>
body {
    background-color: #020617;
}
.title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #38bdf8;
}
.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}
.card {
    background: #020617;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}
button {
    width: 90px !important;
    height: 90px !important;
    border-radius: 50% !important;
    border: 3px solid #38bdf8 !important;
    background: transparent !important;
    color: #38bdf8 !important;
    font-size: 30px !important;
}
button:hover {
    background: #38bdf8 !important;
    color: #020617 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🚗 ESP32 RC Car Controller</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Move on Press | Stop on Release</div>", unsafe_allow_html=True)

# -------- SEND FUNCTION --------
def send(cmd):
    try:
        r = requests.get(f"{ESP32_URL}/{cmd}", timeout=0.5)
        print(r.status_code)
    except Exception as e:
        st.warning("⚠ ESP32 not reachable")
        print(e)


# -------- DIRECTION UI --------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🎮 Direction Control")

outer1, outer2, outer3 = st.columns([1,2,1])
with outer2:
    r1 = st.columns([1,1,1])
    with r1[1]:
        up = st.button("⬆️")

    r2 = st.columns([1,1,1])
    with r2[0]:
        left_btn = st.button("⬅️")
    with r2[1]:
        stop_btn = st.button("⏹️")
    with r2[2]:
        right_btn = st.button("➡️")

    r3 = st.columns([1,1,1])
    with r3[1]:
        down = st.button("⬇️")

st.markdown("</div>", unsafe_allow_html=True)

# -------- SMART CONTROL LOGIC --------
if "last_cmd" not in st.session_state:
    st.session_state.last_cmd = "stop"

cmd = "stop"
if up:
    cmd = "forward"
elif down:
    cmd = "backward"
elif left_btn:
    cmd = "left"
elif right_btn:
    cmd = "right"
elif stop_btn:
    cmd = "stop"

if cmd != st.session_state.last_cmd:
    send(cmd)
    st.session_state.last_cmd = cmd