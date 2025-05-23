import streamlit as st
import sqlalchemy
from sqlalchemy import text
from models.eat import *
import base64
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title='Nutrition Guide', 
     page_icon='images/1.jpg',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Add this after page configuration
st.markdown("""
    <style>
    /* Hide sidebar */
    .css-1d391kg {
        display: none;
    }
    
    /* Style logo container */
    .logo-wrapper {
        display: flex;
        justify-content: center;
        margin-bottom: 1rem;
    }
    
    .logo-container img {
        border-radius: 15px;
        max-width: auto;
        height: auto;
    }
    
    /* Additional sidebar hiding */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load shared CSS
with open('styles/main.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Center logo and title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        # Read and encofuzzy the GIF file
        with open('images/burger.gif', 'rb') as f:
            gif_bytes = f.read()
            encoded_gif = base64.b64encode(gif_bytes).decode()
            
        # Display the GIF with CSS styling
        st.markdown(f"""
            <div class="logo-wrapper">
                <div class="logo-container" style="border-radius: 15px;;">
                    <img src="data:image/gif;base64,{encoded_gif}" alt="Burger Logo">
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error loading logo: {str(e)}")
        
    # Title and subtitle
    st.markdown("""
        <div class='main'>
            <h1>Nutrition Guide</h1>
            <p style='font-size:22px;'><i>All Guide You need to know about your meals</i></p>
        </div>
    """, unsafe_allow_html=True)

# Initialize database connection
try:
    engine = sqlalchemy.create_engine("sqlite:///database/eatandfit.db")
except Exception as e:
    st.error(f"Database connection error: {str(e)}")
    st.stop()
def create_nutrition_chart(nutrition_data):
    try:
        # Configure font size
        plt.rcParams.update({
            'font.size': 6,  # Smaller font size
            'font.family': 'sans-serif',
        })

        labels = ['Carbs', 'Fat', 'Protein']
        colors = ['#F7D300', '#38BC56', '#D35454']
        data = [
            nutrition_data.get_carbs_percentage(),
            nutrition_data.get_fat_percentage(),
            nutrition_data.get_protein_percentage()
        ]

        # Increase figure size for bigger pie chart
        fig, ax = plt.subplots(figsize=(2, 2))  # Bigger figure size
        ax.pie(
            data,
            labels=labels,
            colors=colors,
            explode=(0.15, 0.075, 0.075),
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 6},  # Consistent font size for percentages
            wedgeprops={
                "edgecolor": "black",
                'linewidth': 0.5,  # Thinner borders
                'antialiased': True
            }
        )
        ax.axis('equal')
        plt.tight_layout(pad=0)  # Reduce padding around the chart
        return fig
    except Exception as e:
        st.error(f"Error creating nutrition chart: {str(e)}")
        return None

# Add helper function for database operations
def execute_query(conn, query, params=None):
    try:
        if params:
            return conn.execute(text(query), params)
        return conn.execute(text(query))
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None

# Fetch all dishes
with engine.connect() as conn:
    all_dish_results = execute_query(conn, "SELECT * FROM Dish")
    if all_dish_results is None:
        st.error("Failed to load dishes")
        st.stop()
    all_dish_results = all_dish_results.fetchall()

# Create dish keywords list with error handling
dish_keywords = ['']
try:
    for d in all_dish_results:
        dish = Dish(*d)
        dish_keywords.append(dish.name)
except Exception as e:
    st.error(f"Error processing dish data: {str(e)}")
    st.stop()

# مربع بحث
col1, col2, col3 = st.columns([0.4, 1.2, 0.4])
with col2:
    st.markdown("<h1 style='text-align: center'>Food & Recipe Browser</h1>", unsafe_allow_html=True)
    dish_keyword = st.selectbox("**Search**", tuple(dish_keywords))

# عرض تفاصيل الطبق المحدد
if dish_keyword != '':
    with engine.connect() as conn:
        dish_result = execute_query(
            conn,
            "SELECT * FROM Dish WHERE Name = :name",
            {'name': dish_keyword}
        ).fetchone()

    if dish_result:
        dish = Dish(*dish_result)

        st.markdown(f"<h2 style='text-align: center'>{dish.name}</h2>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1.3, 0.55, 0.15])

        # عرض الصورة
        with col1:
            st.markdown(
                f"""
                <p style="text-align: right">
                    <img src="data:image/jpeg;base64,{base64.b64encode(dish.image).decode('utf-8')}" width="90%">
                </p>
                """,
                unsafe_allow_html=True
            )

        # عرض القيم الغذائية
        with col2:
            nutrition = dish.get_nutrition_detail()
            st.markdown(
                f"""
                <table style="width:100%">
                    <tr><th style="font-size: 22px;">Nutrition</th></tr>
                    <tr><td>
                        <b>Calories:</b><text style="float:right">{round(nutrition.calories)} cal</text><br/>
                        <b>Carbs:</b><text style="float:right">{nutrition.carbs} g</text><br/>
                        <b>Fat:</b><text style="float:right">{nutrition.fat} g</text><br/>
                        <b>Protein:</b><text style="float:right">{nutrition.protein} g</text><br/>
                    </td></tr>
                </table>
                <br/>
                <div style="text-align:center; font-size:20px"><b>Percent Calories From:</b></div>
                """,
                unsafe_allow_html=True
            )

            # رسم الدائرة النسبية للعناصر الغذائية
            fig = create_nutrition_chart(nutrition)
            if fig:
                st.pyplot(fig)

        # عرض الوصفة وخطوات التحضير
        col1, col2, col3, col4 = st.columns([0.122, 0.45, 1.278, 0.15])

        # عرض المقادير
        with col2:
            recipe_html = '''<table style="width: 100%;">
                                <tr><th style="font-size: 22px;">Recipe</th></tr>
                                <tr><td>'''
            for ingredient, amount in dish.get_recipe_detail().ingredients.items():
                recipe_html += f'<b>{ingredient}:</b><text style="float:right">{amount}</text><br/>'
            recipe_html += '</td></tr></table>'
            st.markdown(recipe_html, unsafe_allow_html=True)

        # عرض الخطوات
        with col3:
            steps_html = '''<table style="width: 100%;">
                                <tr><th colspan="2" style="font-size: 22px;">Steps to cook</th></tr>'''

