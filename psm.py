import re
import random
import string
import streamlit as st

# ✅ Page Configuration
st.set_page_config(page_title="Password Strength Checker", page_icon="🔐", layout="centered")

# ✅ Custom CSS for Gradient Background and Styled Input Label
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #000046, #1cb5e0) !important;
            color: white;
            height: 100vh;
            width: 100vw;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        .stApp {
            background: linear-gradient(135deg, #000046, #1cb5e0) !important;
            color: white;
        }
        h1 {
            color: #ffffff;
            text-align: center;
            font-size: 32px;
        }
        label[data-testid="stWidgetLabel"] {
            color: #ffffff !important;
            font-size: 20px !important;
            font-weight: bold !important;
        }
        .stTextInput > div > div > input {
            text-align: center;
            font-size: 18px;
            padding: 10px;
            border-radius: 10px;
        }
        .stButton button {
            background-color: #3fc495 !important;
            color: white !important;
            font-size: 20px !important;
            width: 60%;
            padding: 10px;
            border-radius: 10px;
            transition: 0.3s;
            border: none;
        }
        .stButton button:hover {
            background-color: #3fc495 !important;
            transform: scale(1.05);
        }
        .weak-password {
            background-color: #ff4d4d !important;
            color: white !important;
            font-weight: bold !important;
            text-align: center;
            padding: 12px;
            border-radius: 10px;
        }
        .moderate-password {
            background-color: #ffcc00 !important;
            color: black !important;
            font-weight: bold !important;
            text-align: center;
            padding: 12px;
            border-radius: 10px;
        }
        .empty-password {
            background-color: #ff4d4d !important;
            color: white !important;
            font-weight: bold !important;
            text-align: center;
            padding: 12px;
            border-radius: 10px;
        }

        .strong-password {
    background-color: #3fc495 !important; /* Green background for strong password */
    color: white !important;
    font-weight: bold !important;
    text-align: center;
    padding: 12px;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(40, 167, 69, 0.5);
}

    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Title
st.markdown("<h1>🔒 Password Strength Checker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Enter your password below to check its security level.</p>", unsafe_allow_html=True)

# ✅ Password Strength Function
def check_password(password):
    score = 0
    feedback = []

    if len(password) < 8:
        feedback.append("❌ Password should be **at least 8 characters long**.")
    elif len(password) > 20:
        feedback.append("❌ Password should **not exceed 20 characters**.")
    else:
        score += 1

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("⚠️ Password should **include both uppercase and lowercase letters**.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("⚠️ Password should **include at least one number**.")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("⚠️ Password should **include at least one special character** (!@#$%^&*).")

    if score == 4:
        st.markdown("<div class='strong-password'> ☑️ Your password is **strong**! 💪</div>", unsafe_allow_html=True)
    elif score == 3:
        st.markdown("<div class='moderate-password'>🔵 Not bad! Your password is moderate. Strengthen it for extra security! 🛠️</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='weak-password'>🟡⚠️ Warning! Your password is too weak. Strengthen it now! 🔐</div>", unsafe_allow_html=True)
        if feedback:
            with st.expander("🔍 How to Improve Your Password?"):
                for item in feedback:
                    st.write(item)

# ✅ Generate Strong Password Function
def generate_password():
    length = random.randint(12, 16)
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))

    while (not any(c.isupper() for c in password) or 
           not any(c.islower() for c in password) or 
           not any(c.isdigit() for c in password) or 
           not any(c in "!@#$%^&*" for c in password)):
        password = ''.join(random.choice(characters) for _ in range(length))

    return password

# ✅ User Input for Password
if "password" not in st.session_state:
    st.session_state["password"] = ""

password = st.text_input("Enter your password:", value=st.session_state["password"], type="password", help="Ensure your password is strong (8-20 characters).")

# ✅ Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🔎 Check Strength"):
        if password:
            check_password(password)
        else:
            st.markdown("<div class='empty-password'>⚠️ A password is required to proceed</div>", unsafe_allow_html=True)

with col2:
    if st.button("⚡ Generate Password"):
        st.session_state["password"] = generate_password()
        st.rerun()

# ✅ Auto-Fill the Generated Password
if st.session_state["password"]:
    st.text_input("Generated Password:", value=st.session_state["password"], type="password", help="Use this strong password!", key="generated_password")
