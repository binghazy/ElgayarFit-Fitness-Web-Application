import streamlit as st
import sqlalchemy
from sqlalchemy import text
from models.fit import *
import base64

# Page configuration
st.set_page_config(
    page_title='Fitness Exercises', 
     page_icon='images/1.jpg',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Load shared CSS
with open('styles/main.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Center logo and title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        # Read and encode the GIF file
        with open('images/dumbbell.gif', 'rb') as f:
            gif_bytes = f.read()
            encoded_gif = base64.b64encode(gif_bytes).decode()
            
        # Display the GIF with CSS styling
        st.markdown(f"""
            <div class="logo-wrapper">
                <div class="logo-container">
                    <img src="data:image/gif;base64,{encoded_gif}" alt="Dumbbell Logo">
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error loading logo: {str(e)}")
        
    # Title and subtitle
    st.markdown("""
        <div class='main'>
            <h1>Fitness Exercises</h1>
            <p style='font-size:22px;'><i>Find Your Perfect Workout</i></p>
        </div>
    """, unsafe_allow_html=True)

engine = sqlalchemy.create_engine("sqlite:///database/eatandfit.db")
with engine.connect() as conn:
    # استخدم text() لتغليف الاستعلام
    all_exercise_results = conn.execute(text("SELECT * FROM Exercise")).fetchall()

exercise_keywords = ['',]
for e in all_exercise_results:
    exercise = Exercise(*e)
    exercise_keywords.append(exercise.name)

col1, col2, col3 = st.columns([0.4, 1.2, 0.4])
with col2:
    st.markdown(
        f"""
            <h1 style="text-align: center">Exercise Browser</h1>
        """, unsafe_allow_html=True
    )
    exercise_keyword = st.selectbox("**Search**", tuple(exercise_keywords))

if exercise_keyword != '':
    with engine.connect() as conn:
        # استخدم text() هنا أيضًا لتغليف الاستعلام
        exercise_result = conn.execute(text("SELECT * FROM Exercise WHERE Name = :name"), {'name': exercise_keyword}).fetchone()
        exercise = Exercise(*exercise_result)
        st.markdown(
            f"""
                <h2 style="text-align: center">{exercise.name}</h2>
            """, unsafe_allow_html=True
        )

    col1, col2, col3 = st.columns([0.15, 1.7, 0.15])
    with col2:
        st.markdown(
            f"""
                <iframe width="100%" height="500px" allow="fullscreen;" src="{exercise.link}"></iframe>
            """, unsafe_allow_html=True
        )
        st.subheader("I. Overview")

        overview_builder = ''

        for p in exercise.get_overview_paragraph():
            overview_builder += f"<p style='padding-left: 22px'>{p}</p>"

        st.markdown(overview_builder, unsafe_allow_html=True)

        st.subheader("II. Instructions")

        instructions_builder = "<ul style='list-style-type: decimal; padding-left: 22px'>"

        for li in exercise.get_introductions_detail():
            instructions_builder += f"<li>{li}</li>"

        instructions_builder += "</ul>"

        st.markdown(instructions_builder, unsafe_allow_html=True)
