import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Learning Roadmap Generator", page_icon="🗺️")
st.title("🗺️ AI Learning Roadmap Generator")
st.write("Tell me what you want to learn and I'll build a personalized roadmap.")

# Read the API key from Streamlit Secrets
api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else None

field = st.text_input("Field / domain", placeholder="e.g. Data Science, Web Development")
level = st.selectbox("Your skill level", ["Beginner", "Intermediate", "Advanced"])

col1, col2 = st.columns(2)
amount = col1.number_input("Time to learn", min_value=1, max_value=104, value=12)
unit = col2.selectbox("Unit", ["Weeks", "Months"])


def build_prompt(field, level, duration):
    return f"""
You are an expert learning-path designer.

Create a detailed learning roadmap for: {field}
Learner level: {level}
Total time available: {duration}

Requirements:
- Divide the roadmap into phases that fit exactly within {duration}.
- For each phase include: goal, topics to learn, a hands-on practice task, and a milestone.
- Suggest free resources (docs, courses, books) for each phase.
- Skip basics the learner already knows for their level.
- End with a capstone project and tips for staying on track.
- Use clean Markdown with headings and bullet points.
"""


if st.button("Generate Roadmap", type="primary"):
    if not api_key:
        st.error("API key not found. Add GROQ_API_KEY in Streamlit Secrets.")
    elif not field.strip():
        st.warning("Please enter a field.")
    else:
        duration = f"{amount} {unit.lower()}"
        with st.spinner("Building your roadmap..."):
            try:
                client = Groq(api_key=api_key)
                resp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You create realistic, well-paced learning roadmaps."},
                        {"role": "user", "content": build_prompt(field, level, duration)},
                    ],
                    temperature=0.6,
                    max_tokens=3000,
                )
                st.session_state["roadmap"] = resp.choices[0].message.content
            except Exception as e:
                st.error(f"Something went wrong: {e}")

if "roadmap" in st.session_state:
    st.markdown(st.session_state["roadmap"])
    st.download_button(
        "Download roadmap (.md)",
        st.session_state["roadmap"],
        file_name="roadmap.md",
        mime="text/markdown",
    )
