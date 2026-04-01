import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from google import genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import time

# ✅ Load environment variables
load_dotenv()

# ✅ Setup client (ONLY new SDK)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Gemini response with retry (handles rate limit)
def get_gemini_response(input_text):
    for _ in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=input_text
            )
            return response.text
        except Exception as e:
            time.sleep(5)
    return "⚠️ API rate limit hit. Please try again."

# ✅ Extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())

    # 🔥 IMPORTANT: limit size (avoid token errors)
    return text[:1500]

# ✅ Prompt template
input_prompt = """
You are an advanced ATS (Application Tracking System).

Evaluate the resume based on the job description.

resume: {text}
job description: {jd}

Return ONLY JSON format:
{{
  "JD Match": "%",
  "MissingKeywords": [],
  "Profile Summary": ""
}}
"""

# ---------------- STREAMLIT UI ---------------- #

with st.sidebar:
    st.title("Smart ATS for Resumes")
    st.subheader("About")
    st.write("AI-powered ATS system using Gemini")

    st.markdown("""
    - Streamlit  
    - Gemini AI  
    - Resume Analyzer  
    """)

    add_vertical_space(2)
    st.write("Made with ❤")

st.title("Smart Application Tracking System")
st.text("Improve Your Resume ATS")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")

submit = st.button("Submit")

# ---------------- MAIN LOGIC ---------------- #

if submit:
    if uploaded_file is not None and jd.strip() != "":
        text = input_pdf_text(uploaded_file)

        final_prompt = input_prompt.format(text=text, jd=jd)

        response = get_gemini_response(final_prompt)

        st.subheader("📊 Analysis Result")
        st.write(response)

    else:
        st.warning("⚠️ Please upload resume and paste job description")
        import time

def get_gemini_response(input_text):
    for _ in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=input_text
            )
            return response.text
        except Exception:
            time.sleep(10)
    return "⚠️ Rate limit hit. Try again in a minute."