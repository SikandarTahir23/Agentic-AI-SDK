import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# --- Load API Key (Optional for future AI integration) ---
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# --- Page Config ---
st.set_page_config(page_title="📚 Smart Study Scheduler", page_icon="📘", layout="centered")

# --- Custom CSS (Modern UI + Glassmorphism) ---
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #2b5876, #4e4376);
    font-family: 'Segoe UI', sans-serif;
    color: #f0f0f0;
}
.main {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    border-radius: 16px;
    padding: 2rem;
    margin-top: 40px;
}
.stTextInput > div > input,
.stNumberInput > div > input,
.stDateInput input {
    background-color: #1f2937;
    color: white;
    border: 1px solid #3b82f6;
    border-radius: 12px;
    padding: 10px;
}
.stButton button {
    background: linear-gradient(to right, #06b6d4, #3b82f6);
    border: none;
    color: white;
    font-size: 16px;
    padding: 12px 28px;
    border-radius: 30px;
    transition: all 0.3s ease;
    box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
}
.stButton button:hover {
    background: linear-gradient(to right, #3b82f6, #06b6d4);
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
with st.container():
    st.markdown("""
    <div class='main'>
        <h1 style='text-align:center; color:#ffffff; font-size:2.8em;'>📘 Smart Study Scheduler</h1>
        <p style='text-align:center; font-size:1.1em; color:#cbd5e1;'>
        Plan your perfect study routine with smart logic — based on your subjects, difficulty, study time, and exam date.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- Input Section ---
subjects = st.text_input("📚 Enter subjects (comma-separated)", placeholder="e.g., Math, Physics, English")
difficulties = st.text_input("⚖️ Enter difficulty levels (in order: Easy, Medium, Hard)", placeholder="e.g., Hard, Medium, Easy")
hours_per_day = st.number_input("⏱️ Available study hours per day", min_value=1, max_value=24, value=4)
exam_date = st.date_input("🗓️ Exam date")

# --- Schedule Generator Logic ---
def generate_schedule(subjects_list, diff_list, hours_per_day, exam_date):
    total_days = (exam_date - datetime.today().date()).days
    schedule = []

    if total_days <= 0:
        return ["⛔ Exam date must be in the future."]

    weights = {"Easy": 1, "Medium": 2, "Hard": 3}
    weight_list = [weights.get(d.strip().capitalize(), 2) for d in diff_list]
    total_weight = sum(weight_list)
    total_hours = hours_per_day * total_days

    subject_hours = [(subjects_list[i], round((weight_list[i]/total_weight) * total_hours, 1)) for i in range(len(subjects_list))]

    for day in range(1, total_days + 1):
        today = datetime.today().date() + timedelta(days=day)
        day_plan = {
            "day": day,
            "date": today,
            "tasks": [],
            "breaks": "🧘 Breaks every 45 mins"
        }
        for subject, hrs in subject_hours:
            per_day = round(hrs / total_days, 2)
            if per_day > 0:
                day_plan["tasks"].append(f"{subject}: {per_day} hrs")
        schedule.append(day_plan)

    return schedule

# --- Generate Button and Output ---
if st.button("📅 Generate Study Plan") and subjects.strip() and difficulties.strip():
    with st.spinner("🛠️ Creating your smart study schedule..."):
        subject_list = [s.strip() for s in subjects.split(",")]
        diff_list = [d.strip() for d in difficulties.split(",")]

        if len(subject_list) != len(diff_list):
            st.error("❌ Number of subjects and difficulty levels must match.")
        else:
            output = generate_schedule(subject_list, diff_list, hours_per_day, exam_date)

            if isinstance(output, str):
                st.error(output)
            else:
                st.markdown("### ✅ Your Smart Study Plan")
                for day in output:
                    with st.expander(f"📆 Day {day['day']} – {day['date']}"):
                        for task in day["tasks"]:
                            st.markdown(f"- {task}")
                        st.markdown(f"🧘 {day['breaks']}")

# --- Footer ---
st.markdown("---")
st.markdown("<div style='text-align:center;'>Made with ❤️ by <b>Sikandar Tahir</b> | Powered by <b>Python + Streamlit</b></div>", unsafe_allow_html=True)
