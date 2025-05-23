import streamlit as st
from algorithm.fuzzy_logic import FuzzyLogic
import sqlalchemy
from models.eat import *
from models.fit import *
import base64
import matplotlib
import matplotlib.pyplot as plt
from sqlalchemy import text

# Update the page configuration
st.set_page_config(
    page_title='ElgayarFit', 
    page_icon='images/1.jpg', 
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Add CSS to completely hide sidebar
st.markdown("""
    <style>
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Hide hamburger menu button */
    .css-1rs6os {
        display: none !important;
    }
    
    /* Hide any sidebar related elements */
    .css-17eq0hr {
        display: none !important;
    }
    
    .css-1d391kg {
        display: none !important;
    }
    
    /* Ensure main content takes full width */
    .css-1d8kby0 {
        width: 100% !important;
        padding: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Base variables */
    :root {
        --primary: #10b981;
        --secondary: #059669;
        --accent: #38BC56;
        --bg-dark: #171717;
        --bg-light: #262626;
        --text-light: #e5e7eb;
    }

    /* Page background and text color */
    .stApp {
        background-color: var(--bg-dark);
        color: var(--text-light);
    }

    /* Main container styling */
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        text-align: center;
    }

    /* Center image container */
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem auto;
        width: 200px;
        height: 200px;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* 1) Checkbox border */
    div[data-testid="stCheckbox"] > label > div[role="checkbox"] {
        border-color: var(--primary) !important;
    }
    /* 2) Checkbox checkmark background */
    div[data-testid="stCheckbox"] > label > div[role="checkbox"]::before {
        background-color: var(--primary) !important;
    }
    /* 3) Number-input focus/invalid outline */
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stNumberInput"] input:invalid {
        border-color: var(--primary) !important;
    }
    /* 4) Selectbox focus/invalid outline */
    div[data-testid="stSelectbox"] > div[role="button"]:focus,
    div[data-testid="stSelectbox"] > div[role="button"]:invalid {
        border-color: var(--primary) !important;
    }

    /* Headers and text */
    h1, h2, h3, p {
        color: var(--text-light);
        text-align: center !important;
    }

    /* Form elements */
    .stRadio, .stNumberInput, .stSelectbox {
        max-width: 600px;
        margin: 0 auto;
        background-color: var(--bg-light);
        border-radius: 8px;
        padding: 1rem;
    }

    /* Buttons */
    .stButton > button {
        background-color: var(--primary);
        border-color: var (--primary);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        margin: 1rem auto;
        display: block;
    }
    .stButton > button:hover {
        background-color: var(--secondary);
    }

    /* Tables */
    table {
        margin: 0 auto;
        width: 100%;
        border-collapse: collapse;
        background-color: var(--bg-light);
        border-radius: 8px;
        overflow: hidden;
    }
    th, td {
        padding: 0.75rem;
        border: 1px solid var(--primary);
        color: var(--text-light);
    }

    /* Metrics */
    [data-testid='stMetricValue'] {
        color: var(--primary) !important;
    }

    /* Media queries */
    @media (max-width: 768px) {
        .main { padding: 1rem; }
        table { font-size: 14px; }
        .stButton > button { width: 100%; }
    }
            /* 1) Checkbox border */
div[data-testid="stCheckbox"] > label > div[role="checkbox"] {
    border-color: var(--primary) !important;
}

/* 2) Checkbox checkmark background */
div[data-testid="stCheckbox"] > label > div[role="checkbox"]::before {
    background-color: var(--primary) !important;
}

/* 3) Number-input focus/invalid outline */
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stNumberInput"] input:invalid {
    border-color: var(--primary) !important;
}

/* 4) Selectbox focus/invalid outline */
div[data-testid="stSelectbox"] > div[role="button"]:focus,
div[data-testid="stSelectbox"] > div[role="button"]:invalid {
    border-color: var(--primary) !important;
}

    </style>
""", unsafe_allow_html=True)

# Update the CSS variables and button styles
st.markdown("""
    <style>
    /* Base variables */
    :root {
        --primary: #ff4444;        /* Changed to red */
        --secondary: #cc0000;      /* Changed to darker red */
        --accent: #ff6666;         /* Changed to light red */
        --bg-dark: #171717;
        --bg-light: #262626;
        --text-light: #e5e7eb;
    }

    /* Buttons */
    .stButton > button {
        background-color: var(--primary) !important;
        border-color: var(--primary) !important;
        color: white !important;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        margin: 1rem auto;
        display: block;
    }
    
    .stButton > button:hover {
        background-color: var(--secondary) !important;
        border-color: var(--secondary) !important;
    }

    /* Primary button specific styling */
    .stButton > button[kind="primary"] {
        background-color: var(--primary) !important;
        border-color: var(--primary) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: var(--secondary) !important;
        border-color: var(--secondary) !important;
    }

    /* Form elements focus states */
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stSelectbox"] > div[role="button"]:focus {
        border-color: var(--primary) !important;
    }

    /* Radio button and checkbox colors */
    div[data-testid="stRadio"] label span:hover,
    div[data-testid="stCheckbox"] label span:hover {
        color: var(--primary) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Add custom CSS for the navbar title
st.markdown("""
    <style>
    /* Add title to navbar */
    .css-1avcm0n {
        position: relative;
    }
    .css-1avcm0n::before {
        content: 'ElgayarFit';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #ff4444;
        font-size: 24px;
        font-weight: bold;
        z-index: 999;
    }
    
    /* Hide sidebar and keep existing styles */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    /* ...rest of your existing CSS... */
    </style>
""", unsafe_allow_html=True)

# Update the image display
st.markdown("""
    <div class="image-container">
        <img src="data:image/png;base64,{}" alt="Logo">
    </div>
""".format(
    base64.b64encode(open('images/1.jpg', 'rb').read()).decode()
), unsafe_allow_html=True)

# Logo and Title
st.markdown("""
    <div class='main'>
        <h1>Metrics Analysis</h1>
        <p style='font-size:22px;'><i>Stay Healthy with Balanced Nutrition & Fitness</i></p>
    </div>
""", unsafe_allow_html=True)

# Body Parameters Form
st.markdown("""
    <div class='main'>
        <h2>Body Parameters</h2>
    </div>
""", unsafe_allow_html=True)

with st.container():
    # Session state initialization
    if "page1" not in st.session_state:
        st.session_state.page1 = {
            'is_first_load': True,
            'sex': 0,
            'height': 175.0,
            'weight': 80.0,
            'stage': 0
        }

    # Form callbacks
    def submit_sex():
        st.session_state.page1['sex'] = 0 if st.session_state.sex_input_value == 'Male' else 1

    def submit_height():
        st.session_state.page1['height'] = st.session_state.height_input_value

    def submit_weight():
        st.session_state.page1['weight'] = st.session_state.weight_input_value

    def submit_stage():
        st.session_state.page1['stage'] = 0 if st.session_state.stage_input_value == "Yes, I'm a beginner" else 1

    # Form inputs
    sex_input = st.radio(
        "**What's your sex?**",
        ('Male', 'Female'),
        key='sex_input_value',
        index=st.session_state.page1['sex'],
        on_change=submit_sex,
        horizontal=True
    )

    height_input = st.number_input(
        "**Height (cm):**",
        key='height_input_value',
        min_value=130.0,
        max_value=220.0,
        step=0.1,
        value=st.session_state.page1['height'],
        on_change=submit_height
    )

    weight_input = st.number_input(
        "**Weight (kg):**",
        key='weight_input_value',
        min_value=30.0,
        max_value=150.0,
        step=0.1,
        value=st.session_state.page1['weight'],
        on_change=submit_weight
    )

    stage_input = st.selectbox(
        "**New to weight loss?**",
        ("Yes, I'm a beginner", "No, I'm intermediate"),
        key='stage_input_value',
        index=st.session_state.page1['stage'],
        on_change=submit_stage
    )

    # Center the buttons
    col1, col2, col3 = st.columns([3, 1.5, 3])  # Adjust column ratios
    with col2:
        c1, c2 = st.columns(2)  # Create two equal columns for buttons
        with c1:
            submit = st.button("Calculate", type="primary", use_container_width=True)
        with c2:
            reset = st.button("Reset", use_container_width=True)

    if submit:
        st.session_state.page1['is_first_load'] = False
    if reset:
        st.session_state.page1['is_first_load'] = True

# Matplotlib configuration
matplotlib.rcParams.update({'font.size': 8, 'figure.figsize': (4, 4), 'figure.autolayout': True})
colors = ['#F7D300', '#ff6666', '#ff4444']  # Yellow, Light red, Red
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)

# Update the Matplotlib configuration for smaller figures
matplotlib.rcParams.update({
    'font.size': 8,
    'figure.figsize': (2, 2),  # Reduce from previous size to 2x2 inches
    'figure.autolayout': True
})

if not st.session_state.page1['is_first_load']:
    # Perform Fuzzy Logic to determine the body state
    fuzzy_logic = FuzzyLogic()
    # Pass the required parameters from session state
    fuzzy_logic.do_fuzzification_of_height(
        height=st.session_state.page1['height'],
        sex=st.session_state.page1['sex']
    )
    fuzzy_logic.do_fuzzification_of_weight(
        weight=st.session_state.page1['weight'],
        sex=st.session_state.page1['sex']
    )
    fuzzy_logic.do_fuzzy_inference()
    body = fuzzy_logic.do_defuzzification_of_body()

    # Conclusion
    body_result = ''
    match body:
        case 2:
            body_result = 'overweight'
        case 3:
            body_result = 'pre-obese'
        case 4:
            body_result = 'obese'

    if body == 0:
        st.subheader("You are thin! You should gain weight instead of losing weight!")
    elif body == 1:
        st.subheader("You are in shape! Keep going! :sunglasses:")
    else:
        with st.container():
            st.markdown(
                f"""
                <div style="background-color: #262626; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3 style=" color: #ff4444; margin-left:32px;">You are {body_result}!</h3>
                    <p style="color: #e5e7eb; margin: 10px 0 0 0;">To Adjust your Weight, you can follow this guide:</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Diet plan overview
        st.markdown(
            f"""
            <br/>
            <br/>
            <h2 style="padding-left: 27px; color: #ff4444;">A. Diet</h2>
            
            <p style="padding-left: 55px; margin-bottom: 20px;">
                <b>Carbohydrates</b> or <i>carbs</i> (including <i>sugars</i>, <i>starch</i>, and <i>cellulose</i>) 
                are the main energy source of the human diet. To lose weight, you need to eat fewer carbs.
            </p>
            
            <p style="padding-left: 55px; margin-bottom: 30px;">
                In this diet plan, each week will consist of 3 different types of eating days:
            </p>
            <ul style="padding-left: 100px; margin-bottom: 40px;">
                <li style="margin-bottom: 10px;"><b>Low Carb Days</b> (below <b>26%</b> of total energy intake) - <b>3</b> days per week</li>
                <li style="margin-bottom: 10px;"><b>Moderate Carb Days</b> (between <b>26%</b> and <b>45%</b> of total energy intake) - <b>3</b> days per week</li>
                <li style="margin-bottom: 10px;"><b>High Carb Days</b> (above <b>45%</b> of total energy intake) - <b>1</b> day per week</li>
            </ul>
            """, 
            unsafe_allow_html=True
        )
        # Get and display diet plan from the database
        low_carb_1, moderate_carb_1, high_carb_1 = st.columns(3)
        low_carb_2, moderate_carb_2, high_carb_2 = st.columns(3)
        matplotlib.rcParams.update({'font.size': 5})
        label = ['Carbs', 'Fat', 'Protein']
        colors = ['#F7D300', '#ff6666', '#ff4444']  # Yellow, Light red, Red
        engine = sqlalchemy.create_engine("sqlite:///database/eatandfit.db")
        with engine.connect() as conn:
            # Get standard calories each day for the user
            sc_result = conn.execute(
                text("SELECT * FROM StandardCalories WHERE Stage = :stage AND Body = :body AND Sex = :sex"),
                {'stage': st.session_state.page1['stage'], 'body': body,
                 'sex': st.session_state.page1['sex']}).fetchone()

            standard_calories = StandardCalories(*sc_result)

            # Get low carb diet
            lc_result = conn.execute(text("SELECT * FROM LowCarb WHERE Calories = :calories"),
                                     {'calories': standard_calories.low_carb}).fetchone()
            low_carb_diet = Diet(*lc_result)

            low_carb_nutrition_detail = low_carb_diet.get_nutrition_detail()

            low_carb_data = [low_carb_nutrition_detail.get_carbs_percentage(), low_carb_nutrition_detail.get_fat_percentage(), low_carb_nutrition_detail.get_protein_percentage()]
            low_carb_fig, low_carb_ax = plt.subplots(figsize=(2, 2))
            low_carb_ax.pie(low_carb_data, labels=label, colors=colors, explode=(0.15, 0.075, 0.075), autopct='%1.1f%%', startangle=90,
                            wedgeprops= {"edgecolor":"black",
                            'linewidth': 1,
                            'antialiased': True})
            low_carb_ax.axis('equal')

            low_carb_breakfast_detail = low_carb_diet.get_breakfast_detail()
            low_carb_lunch_detail = low_carb_diet.get_lunch_detail()
            low_carb_dinner_detail = low_carb_diet.get_dinner_detail()

            lcb1_result = conn.execute(text("SELECT * FROM Dish WHERE Id = :id"),
                                       {'id': low_carb_breakfast_detail.id1}).fetchone()
            lcb2_result = conn.execute(text("SELECT * FROM Dish WHERE Id = :id"),
                                       {'id': low_carb_breakfast_detail.id2}).fetchone()

            lcl1_result = conn.execute(text("SELECT * FROM Dish WHERE Id = :id"),
                                       {'id': low_carb_lunch_detail.id1}).fetchone()

            lcl2_result = conn.execute(text("SELECT * FROM Dish WHERE Id = :id"),
                                       {'id': low_carb_lunch_detail.id2}).fetchone()

            lcd1_result = conn.execute(text("SELECT * FROM Dish WHERE Id = :id"),
                                       {'id': low_carb_dinner_detail.id1}).fetchone()

            lcd2_result = conn.execute(text("SELECT * FROM Dish WHERE Id = :id"),
                                       {'id': low_carb_dinner_detail.id2}).fetchone()

            low_carb_breakfast_1 = Dish(*lcb1_result)
            low_carb_breakfast_2 = Dish(*lcb2_result)
            low_carb_lunch_1 = Dish(*lcl1_result)
            low_carb_lunch_2 = Dish(*lcl2_result)
            low_carb_dinner_1 = Dish(*lcd1_result)
            low_carb_dinner_2 = Dish(*lcd2_result)

            with low_carb_1:
                st.markdown(
                    f"""
                        <h3 style="text-align: center">Low Carb Diet</h3>
                        <table style="width:100%">
                            <tr>
                                <th style="font-size:18px;">Nutrition</th>
                            </tr>
                            <tr>
                                <td>
                                    <b>Calories:</b>
                                    <text style="float:right">{round(low_carb_nutrition_detail.calories)} cal</text><br/>
                                    <b>Carbs:</b>
                                    <text style="float:right">{low_carb_nutrition_detail.carbs} g</text><br/>
                                    <b>Fat:</b>
                                    <text style="float:right">{low_carb_nutrition_detail.fat} g</text><br/>
                                    <b>Protein:</b>
                                    <text style="float:right">{low_carb_nutrition_detail.protein} g</text><br/>
                                </td>
                            </tr>
                        </table>
                        <br/>
                        <div class="figure_title" style="text-align:center; font-size:20px"><b>Percent Calories From:</b></div>
                    """, unsafe_allow_html=True
                )
                st.pyplot(low_carb_fig)
            with low_carb_2:
                st.markdown(
                    f"""
                        <table style="white-space:nowrap; width:100%;">
                            <tr>
                                <td colspan="2"><b style="font-size:18px;">Breakfast</b><text style="float:right">{low_carb_breakfast_detail.calories} calories</text></td>
                            </tr>                            
                            <tr>
                                <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(low_carb_breakfast_1.image).decode('utf-8')}" width="70"></td>
                                <td><b>{low_carb_breakfast_1.name}</b><br/>
                                {low_carb_breakfast_detail.amount1} &nbsp; serving</td>
                            </tr>
                            <tr>
                                <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(low_carb_breakfast_2.image).decode('utf-8')}" width="70"></td>
                                <td><b>{low_carb_breakfast_2.name}</b><br/>
                                {low_carb_breakfast_detail.amount2} &nbsp; serving</td>
                            </tr>
                            <tr>
                                <td colspan="2"><b style="font-size:18px;">Lunch</b><text style="float:right">{low_carb_lunch_detail.calories} calories</text></td>
                            </tr>
                            <tr>
                                <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(low_carb_lunch_1.image).decode('utf-8')}" width="70"></td>
                                <td><b>{low_carb_lunch_1.name}</b><br/>
                                {low_carb_lunch_detail.amount1} &nbsp; serving</td>
                            </tr>
                            <tr>
                                <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(low_carb_lunch_2.image).decode('utf-8')}" width="70"></td>
                                <td><b>{low_carb_lunch_2.name}</b><br/>
                                {low_carb_lunch_detail.amount2} &nbsp; serving</td>
                            </tr>
                            <tr>
                                <td colspan="2"><b style="font-size:18px;">Dinner</b><text style="float:right">{low_carb_dinner_detail.calories} calories</text></td>
                            </tr>
                            <tr>
                                <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(low_carb_dinner_1.image).decode('utf-8')}" width="70"></td>
                                <td><b>{low_carb_dinner_1.name}</b><br/>
                                {low_carb_dinner_detail.amount1} &nbsp; serving</td>
                            </tr>
                            <tr>
                                <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(low_carb_dinner_2.image).decode('utf-8')}" width="70"></td>
                                <td><b>{low_carb_dinner_2.name}</b><br/>
                                {low_carb_dinner_detail.amount2} &nbsp; serving</td>
                            </tr>
                        </table><br/> 
                    """, unsafe_allow_html=True
                )

            # Get moderate carb diet
            mc_result = conn.execute(text("SELECT * FROM ModerateCarb WHERE Calories = :calories"),
                                     {
                                         'calories': standard_calories.moderate_carb}).fetchone()  # استخدم fetchone إذا كنت تتوقع صفًا واحدًا
            if mc_result:
                moderate_carb_diet = Diet(*mc_result)

                moderate_carb_nutrition_detail = moderate_carb_diet.get_nutrition_detail()

                moderate_carb_data = [moderate_carb_nutrition_detail.get_carbs_percentage(),
                                      moderate_carb_nutrition_detail.get_fat_percentage(),
                                      moderate_carb_nutrition_detail.get_protein_percentage()]

                moderate_carb_fig, moderate_carb_ax = plt.subplots(figsize=(2, 2))
                moderate_carb_ax.pie(moderate_carb_data, labels=label, colors=colors,
                                     explode=(0.15, 0.075, 0.075), autopct='%1.1f%%', startangle=90,
                                     wedgeprops={"edgecolor": "black", 'linewidth': 1, 'antialiased': True})
                moderate_carb_ax.axis('equal')

                moderate_carb_breakfast_detail = moderate_carb_diet.get_breakfast_detail()
                moderate_carb_lunch_detail = moderate_carb_diet.get_lunch_detail()
                moderate_carb_dinner_detail = moderate_carb_diet.get_dinner_detail()

                # Fetch dish details for breakfast, lunch, and dinner
                mcb1_result = conn.execute(text("SELECT * FROM Dish WHERE Id = :id"),
                                           {'id': moderate_carb_breakfast_detail.id1}).fetchone()
                mcb2_result = conn.execute(text("SELECT * FROM Dish WHERE Id = :id"),
                                           {'id': moderate_carb_breakfast_detail.id2}).fetchone()

                mcl1_result = conn.execute(text("SELECT * FROM Dish WHERE Id = :id"),
                                           {'id': moderate_carb_lunch_detail.id1}).fetchone()
                mcl2_result = conn.execute(text("SELECT * FROM Dish WHERE Id = :id"),
                                           {'id': moderate_carb_lunch_detail.id2}).fetchone()

                mcd1_result = conn.execute(text("SELECT * FROM Dish WHERE Id = :id"),
                                           {'id': moderate_carb_dinner_detail.id1}).fetchone()
                mcd2_result = conn.execute(text("SELECT * FROM Dish WHERE Id = :id"),
                                           {'id': moderate_carb_dinner_detail.id2}).fetchone()

                moderate_carb_breakfast_1 = Dish(*mcb1_result)
                moderate_carb_breakfast_2 = Dish(*mcb2_result)
                moderate_carb_lunch_1 = Dish(*mcl1_result)
                moderate_carb_lunch_2 = Dish(*mcl2_result)
                moderate_carb_dinner_1 = Dish(*mcd1_result)
                moderate_carb_dinner_2 = Dish(*mcd2_result)

                with moderate_carb_1:
                    st.markdown(
                        f"""
                            <h3 style="text-align: center">Moderate Carb Diet</h3>
                            <table style="width:100%">
                                <tr>
                                    <th style="font-size:18px;">Nutrition</th>
                                </tr>
                                <tr>
                                    <td>
                                        <b>Calories:</b>
                                        <text style="float:right">{round(moderate_carb_nutrition_detail.calories)} cal</text><br/>
                                        <b>Carbs:</b>
                                        <text style="float:right">{moderate_carb_nutrition_detail.carbs} g</text><br/>
                                        <b>Fat:</b>
                                        <text style="float:right">{moderate_carb_nutrition_detail.fat} g</text><br/>
                                        <b>Protein:</b>
                                        <text style="float:right">{moderate_carb_nutrition_detail.protein} g</text><br/>
                                    </td>
                                </tr>
                            </table>
                            <br/>
                            <div class="figure_title" style="text-align:center; font-size:20px"><b>Percent Calories From:</b></div>
                        """, unsafe_allow_html=True
                    )
                    st.pyplot(moderate_carb_fig)

                with moderate_carb_2:
                    st.markdown(
                        f"""
                            <table style="white-space:nowrap; width:100%;">
                                <tr>
                                    <td colspan="2"><b style="font-size:18px;">Breakfast</b><text style="float:right">{moderate_carb_breakfast_detail.calories} calories</text></td>
                                </tr>                            
                                <tr>
                                    <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(moderate_carb_breakfast_1.image).decode('utf-8')}" width="70"></td>
                                    <td><b>{moderate_carb_breakfast_1.name}</b><br/>
                                    {moderate_carb_breakfast_detail.amount1} &nbsp; serving</td>
                                </tr>
                                <tr>
                                    <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(moderate_carb_breakfast_2.image).decode('utf-8')}" width="70"></td>
                                    <td><b>{moderate_carb_breakfast_2.name}</b><br/>
                                    {moderate_carb_breakfast_detail.amount2} &nbsp; serving</td>
                                </tr>
                                <tr>
                                    <td colspan="2"><b style="font-size:18px;">Lunch</b><text style="float:right">{moderate_carb_lunch_detail.calories} calories</text></td>
                                </tr>
                                <tr>
                                    <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(moderate_carb_lunch_1.image).decode('utf-8')}" width="70"></td>
                                    <td><b>{moderate_carb_lunch_1.name}</b><br/>
                                    {moderate_carb_lunch_detail.amount1} &nbsp; serving</td>
                                </tr>
                                <tr>
                                    <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(moderate_carb_lunch_2.image).decode('utf-8')}" width="70"></td>
                                    <td><b>{moderate_carb_lunch_2.name}</b><br/>
                                    {moderate_carb_lunch_detail.amount2} &nbsp; serving</td>
                                </tr>
                                <tr>
                                    <td colspan="2"><b style="font-size:18px;">Dinner</b><text style="float:right">{moderate_carb_dinner_detail.calories} calories</text></td>
                                </tr>
                                <tr>
                                    <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(moderate_carb_dinner_1.image).decode('utf-8')}" width="70"></td>
                                    <td><b>{moderate_carb_dinner_1.name}</b><br/>
                                    {moderate_carb_dinner_detail.amount1} &nbsp; serving</td>
                                </tr>
                                <tr>
                                    <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(moderate_carb_dinner_2.image).decode('utf-8')}" width="70"></td>
                                    <td><b>{moderate_carb_dinner_2.name}</b><br/>
                                    {moderate_carb_dinner_detail.amount2} &nbsp; serving</td>
                                </tr>
                            </table><br/> 
                        """, unsafe_allow_html=True
                    )

            # Get high carb diet
            hc_result = conn.execute(
                text("SELECT * FROM HighCarb WHERE Calories = :calories"),
                {"calories": standard_calories.high_carb}
            ).fetchone()
            high_carb_diet = Diet(*hc_result)
            high_carb_nutrition_detail = high_carb_diet.get_nutrition_detail()

            high_carb_data = [high_carb_nutrition_detail.get_carbs_percentage(), high_carb_nutrition_detail.get_fat_percentage(), high_carb_nutrition_detail.get_protein_percentage()]
            high_carb_fig, high_carb_ax = plt.subplots(figsize=(2, 2))
            high_carb_ax.pie(high_carb_data, labels=label, colors=colors, explode=(0.15, 0.075, 0.075), autopct='%1.1f%%', startangle=90,
                            wedgeprops= {"edgecolor":"black",
                            'linewidth': 1,
                            'antialiased': True})
            high_carb_ax.axis('equal')

            high_carb_breakfast_detail = high_carb_diet.get_breakfast_detail()
            high_carb_lunch_detail = high_carb_diet.get_lunch_detail()
            high_carb_dinner_detail = high_carb_diet.get_dinner_detail()

            lcb1_result = conn.execute(
                text("SELECT * FROM Dish WHERE Id = :id"),
                {'id': high_carb_breakfast_detail.id1}
            ).fetchone()

            lcb2_result = conn.execute(
                text("SELECT * FROM Dish WHERE Id = :id"), 
                {'id': high_carb_breakfast_detail.id2}
            ).fetchone()

            lcl1_result = conn.execute(
                text("SELECT * FROM Dish WHERE Id = :id"),
                {'id': high_carb_lunch_detail.id1}
            ).fetchone()

            lcl2_result = conn.execute(
                text("SELECT * FROM Dish WHERE Id = :id"),
                {'id': high_carb_lunch_detail.id2}
            ).fetchone()

            lcd1_result = conn.execute(
                text("SELECT * FROM Dish WHERE Id = :id"),
                {'id': high_carb_dinner_detail.id1}
            ).fetchone()

            lcd2_result = conn.execute(
                text("SELECT * FROM Dish WHERE Id = :id"),
                {'id': high_carb_dinner_detail.id2}
            ).fetchone()

            high_carb_breakfast_1 = Dish(*lcb1_result)
            high_carb_breakfast_2 = Dish(*lcb2_result)
            high_carb_lunch_1 = Dish(*lcl1_result)
            high_carb_lunch_2 = Dish(*lcl2_result)
            high_carb_dinner_1 = Dish(*lcd1_result)
            high_carb_dinner_2 = Dish(*lcd2_result)

            with high_carb_1:
                st.markdown(
                    f"""
                        <h3 style="text-align: center">High Carb Diet</h3>
                        <table style="width:100%">
                            <tr>
                                <th style="font-size:18px;">Nutrition</th>
                            </tr>
                            <tr>
                                <td>
                                    <b>Calories:</b>
                                    <text style="float:right">{round(high_carb_nutrition_detail.calories)} cal</text><br/>
                                    <b>Carbs:</b>
                                    <text style="float:right">{high_carb_nutrition_detail.carbs} g</text><br/>
                                    <b>Fat:</b>
                                    <text style="float:right">{high_carb_nutrition_detail.fat} g</text><br/>
                                    <b>Protein:</b>
                                    <text style="float:right">{high_carb_nutrition_detail.protein} g</text><br/>
                                </td>
                            </tr>
                        </table>
                        <br/>
                        <div class="figure_title" style="text-align:center; font-size:20px"><b>Percent Calories From:</b></div>
                    """, unsafe_allow_html=True
                )
                st.pyplot(high_carb_fig)
            with high_carb_2:
                st.markdown(
                    f"""
                        <table style="white-space:nowrap; width:100%;">
                            <tr>
                                <td colspan="2"><b style="font-size:18px;">Breakfast</b><text style="float:right">{high_carb_breakfast_detail.calories} calories</text></td>
                            </tr>                            
                            <tr>
                                <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(high_carb_breakfast_1.image).decode('utf-8')}" width="70"></td>
                                <td><b>{high_carb_breakfast_1.name}</b><br/>
                                {high_carb_breakfast_detail.amount1} &nbsp; serving</td>
                            </tr>
                            <tr>
                                <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(high_carb_breakfast_2.image).decode('utf-8')}" width="70"></td>
                                <td><b>{high_carb_breakfast_2.name}</b><br/>
                                {high_carb_breakfast_detail.amount2} &nbsp; serving</td>
                            </tr>
                            <tr>
                                <td colspan="2"><b style="font-size:18px;">Lunch</b><text style="float:right">{high_carb_lunch_detail.calories} calories</text></td>
                            </tr>
                            <tr>
                                <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(high_carb_lunch_1.image).decode('utf-8')}" width="70"></td>
                                <td><b>{high_carb_lunch_1.name}</b><br/>
                                {high_carb_lunch_detail.amount1} &nbsp; serving</td>
                            </tr>
                            <tr>
                                <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(high_carb_lunch_2.image).decode('utf-8')}" width="70"></td>
                                <td><b>{high_carb_lunch_2.name}</b><br/>
                                {high_carb_lunch_detail.amount2} &nbsp; serving</td>
                            </tr>
                            <tr>
                                <td colspan="2"><b style="font-size:18px;">Dinner</b><text style="float:right">{high_carb_dinner_detail.calories} calories</text></td>
                            </tr>
                            <tr>
                                <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(high_carb_dinner_1.image).decode('utf-8')}" width="70"></td>
                                <td><b>{high_carb_dinner_1.name}</b><br/>
                                {high_carb_dinner_detail.amount1} &nbsp; serving</td>
                            </tr>
                            <tr>
                                <td style="width: auto;"><img src="data:image/jpeg;base64,{base64.b64encode(high_carb_dinner_2.image).decode('utf-8')}" width="70"></td>
                                <td><b>{high_carb_dinner_2.name}</b><br/>
                                {high_carb_dinner_detail.amount2} &nbsp; serving</td>
                            </tr>
                        </table><br/> 
                    """, unsafe_allow_html=True
                )

        st.write('You may structure these days in any preferred manner. I suggest keeping the high carb day for special occasions. That way you can attend family functions, or eat out with friends, and indulge a little more than normal.')
        # Cardio
        with engine.connect() as conn:
            cardio_result = conn.execute(
                text("SELECT * FROM Cardio WHERE Stage = :stage AND Body = :body AND Sex = :sex"),
                {
                    'stage': st.session_state.page1['stage'],
                    'body': body,
                    'sex': st.session_state.page1['sex']
                }
            ).fetchone()
            
        cardio = Cardio(*cardio_result)

        # Gym
        st.markdown(
            f"""
              <br/>
               <br/>
            <br/>

            <h2 style="padding-left: 27px; color: #ff4444;">B. Excercises for first month</h2>

            <p style="padding-left: 55px">You will be using an upper/lower workout every week. Rep schemes are merely guidelines.</p>
            
            <p style="padding-left: 55px">When a weight becomes manageable using the given set and rep schemes, add weight to the bar. For sake of convenience, use the same weight for each of the sets for a given exercise.</p>
            <ul style="padding-left: 100px">
            <li><b>Day 1</b> - Upper</li>
            <li><b>Day 2</b> - Lower</li>
            <li><b>Day 3</b> - <i>Off</i></li>
            <li><b>Day 4</b> - Upper</li>
            <li><b>Day 5</b> - Lower</li>
            <li><b>Day 6</b> - <i>Off</i></li>
            <li><b>Day 7</b> - <i>Off</i></li>                                                
            </ul>            
            """, unsafe_allow_html=True
        )


        col1, col2 = st.columns(2)

        # Lower
        with col1:
            with engine.connect() as conn:
                lower_gym_result = conn.execute(
                    text("SELECT * FROM Gym WHERE Day = 'lower'")
                ).fetchall()

            lower_gym = []
            for lg_result in lower_gym_result:
                lg = Gym(*lg_result)
                with engine.connect() as conn:
                    exercise_result = conn.execute(
                        text("SELECT * FROM Exercise WHERE Id = :id"),
                        {'id': lg.exercise}
                    ).fetchone()
                    exercise = Exercise(*exercise_result)
                lg.exercise = exercise.name
                lower_gym.append(lg)

            table_builder = '''<h3 style="text-align: center">Lower</h3>
                                    <table style="width: 100%;">
                                    <tr>
                                        <th>Exercise</th>
                                        <th>Sets</th>
                                        <th>Reps</th>
                                    </tr>'''

            for lg in lower_gym:
                table_builder += f"""<tr>
                                        <td>{lg.exercise}</td>
                                        <td>{lg.sets}</td>
                                        <td>{lg.reps}</td>
                                    </tr>"""
            table_builder += "</table>"
            st.markdown(table_builder, unsafe_allow_html=True)

        # Upper
        with col2:
            with engine.connect() as conn:
                upper_gym_result = conn.execute(
                    text("SELECT * FROM Gym WHERE Day = 'upper'")
                ).fetchall()

            upper_gym = []
            for ug_result in upper_gym_result:
                ug = Gym(*ug_result)
                with engine.connect() as conn:
                    exercise_result = conn.execute(
                        text("SELECT * FROM Exercise WHERE Id = :id"),
                        {'id': ug.exercise}
                    ).fetchone()
                    exercise = Exercise(*exercise_result)
                ug.exercise = exercise.name
                upper_gym.append(ug)

            table_builder = '''<h3 style="text-align: center">Upper</h3>
                                <table style="width: 100%;">
                                    <tr>
                                        <th>Exercise</th>
                                        <th>Sets</th>
                                        <th>Reps</th>
                                    </tr>'''

            for ug in upper_gym:
                table_builder += f"""<tr>
                                        <td>{ug.exercise}</td>
                                        <td>{ug.sets}</td>
                                        <td>{ug.reps}</td>
                                    </tr>"""
            table_builder += "</table>"
            st.markdown(table_builder, unsafe_allow_html=True)