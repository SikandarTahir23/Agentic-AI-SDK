import re
import random
import string
import streamlit as st

def generate_strong_password(length):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choice(characters) for _ in range(length))

def check_password_strength(password):
    score = 0
    common_passwords = ["password123", "12345678", "qwerty", "letmein", "admin", "welcome"]
    
    if password in common_passwords:
        return "❌ Too Common - Try something unique!", "Weak"
    
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("🔹 Minimum 8 characters needed.")
    
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🔹 Mix uppercase and lowercase letters.")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🔹 Add at least one number.")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("🔹 Include a special character (!@#$%^&*).")
    
    if score == 4:
        return "✅ Perfect! Your password is strong.", "Strong"
    elif score == 3:
        return "⚠️ Decent, but could be better.", "Moderate"
    else:
        return "\n".join(feedback), "Weak"

# Streamlit UI with improved design
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")

# Custom CSS for enhanced UI with black text for generated password
st.markdown("""
    <style>
        /* Main background with gradient */
        .main {background: linear-gradient(135deg, #1F2A44 0%, #00A8B5 100%); padding: 40px; border-radius: 20px; box-shadow: 0 6px 25px rgba(0,0,0,0.3);} 
        h1 {color: #FFFFFF; text-align: center; font-family: 'Poppins', sans-serif; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); font-size: 36px;}
        h3 {color: #A3E4D7; font-family: 'Poppins', sans-serif; font-size: 24px;}
        p, label {color: #D5F5E3; font-family: 'Arial', sans-serif; font-size: 16px;}
        
        /* Input styling */
        .stTextInput>div>div>input {background-color: #F7F9F9; color: #1F2A44; border: 2px solid #A3E4D7; border-radius: 12px; text-align: center; font-size: 16px; padding: 12px; box-shadow: 0 3px 6px rgba(0,0,0,0.1);}
        .stNumberInput>div>div>input {background-color: #F7F9F9; color: #1F2A44; border: 2px solid #A3E4D7; border-radius: 12px;}
        
        /* Specific styling for the generated password input (disabled state) */
        .stTextInput input[disabled] {color: #000000 !important; background-color: #F7F9F9 !important;}
        
        /* Button styling with teal-to-emerald gradient */
        .stButton>button {background: linear-gradient(90deg, #00B4A6 0%, #27AE60 100%); color: #FFFFFF; font-weight: bold; border-radius: 12px; padding: 14px; width: 100%; transition: all 0.3s; box-shadow: 0 4px 12px rgba(0,0,0,0.2);}
        .stButton>button:hover {background: linear-gradient(90deg, #27AE60, #00B4A6); transform: scale(1.05); box-shadow: 0 6px 18px rgba(0,0,0,0.3);}
        
        /* Sidebar styling */
        .css-1d391kg {background: linear-gradient(180deg, #00A8B5 0%, #1F2A44 100%); color: #FFFFFF; box-shadow: 2px 0 15px rgba(0,0,0,0.2);}
        .sidebar .sidebar-content {padding: 25px;}
        
        /* Feedback styling */
        .stSuccess {background-color: rgba(39, 174, 96, 0.15) !important; color: #27AE60 !important; border: 1px solid #27AE60; border-radius: 10px; padding: 15px; font-weight: bold;}
        .stWarning {background-color: rgba(241, 196, 15, 0.15) !important; color: #F1C40F !important; border: 1px solid #F1C40F; border-radius: 10px; padding: 15px; font-weight: bold;}
        .stError {background-color: rgba(231, 76, 60, 0.15) !important; color: #E74C3C !important; border: 1px solid #E74C3C; border-radius: 10px; padding: 15px; font-weight: bold;}
        
        /* Divider */
        hr {border: 1px solid #A3E4D7; opacity: 0.6; margin: 30px 0;}
        
        /* Container tweaks */
        .stContainer {margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# Sidebar for Password History
st.sidebar.title("🔑 Password History")
if 'password_history' not in st.session_state:
    st.session_state.password_history = []

for i, past_password in enumerate(st.session_state.password_history[-5:], 1):
    st.sidebar.write(f"{i}. {past_password}")

# Main content
st.title("🔐 Password Strength Meter")
st.write("Test your password or generate a secure one below!")

# Password input and check
with st.container():
    password = st.text_input("Enter your password:", type="password", placeholder="Type your password...")
    if st.button("Check Strength"):
        if password:
            st.session_state.password_history.append(password)
            result, strength = check_password_strength(password)
            if strength == "Strong":
                st.success(result)
                st.balloons()
            elif strength == "Moderate":
                st.warning(result)
            else:
                st.error("Weak Password - Tips to improve:")
                for tip in result.split("\n"):
                    st.write(tip)
        else:
            st.warning("⚠️ Please enter a password!")

# Password generator
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("✨ Generate a Strong Password")
with st.container():
    password_length = st.number_input("Password Length:", min_value=8, max_value=20, value=12, step=1)
    if st.button("Generate Now"):
        strong_password = generate_strong_password(password_length)
        st.text_input("Your Strong Password:", strong_password, disabled=True)
        st.info("Copy this to secure your accounts! 🔒")

# Footer
st.markdown("<p style='text-align: center; color: #D5F5E3; font-size: 14px;'>Built with ❤️ By Sikandar Tahir using Streamlit</p>", unsafe_allow_html=True)