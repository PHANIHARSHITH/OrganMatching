import streamlit as st
import pickle
import time

models = {
    'heart_matching': pickle.load(open('pickel_files/heart_transplant.sav', 'rb'))
}

# Example mappings for categorical features (update these based on your model training)
diagnosis_mapping = {'Diagnosis1': 0, 'Diagnosis2': 1, 'Diagnosis3': 2}
CODDON_mapping = {'COD1': 0, 'COD2': 1, 'COD3': 2}
mcs_mapping = {'Score1': 0, 'Score2': 1, 'Score3': 2}
medcondition_mapping = {'Cond1': 0, 'Cond2': 1, 'Cond3': 2}
abo_mapping = {'A': 0, 'B': 1, 'AB': 2, 'O': 3}
ABOMAT_mapping = {'Match': 1, 'No Match': 0}
HIST_MI_mapping = {'No': 0, 'Yes': 1}
diabetes_mapping = {'No': 0, 'Yes': 1}

def main_app():
    st.title("Organ Matching Prediction")
    
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    background_image_url = "https://c4.wallpaperflare.com/wallpaper/697/865/74/abstract-abstraction-biology-chemistry-wallpaper-preview.jpg"  

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url({background_image_url});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.7);
    }}
    .stButton > button {{
    background-color: #4CAF50; 
    color: white;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
}}

.stButton > button:hover {{
    background-color: #45a049; 
    transform: scale(1.05); 
    color:gold;
}}

input[type="text"], input[type="number"] {{
    border: 2px solid #ccc;
    border-radius: 4px;
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
    transition: border-color 0.3s;
}}

input[type="text"]:focus, input[type="number"]:focus {{
    border-color: #4CAF50; 
    outline: none; 
}}

    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    selected = st.sidebar.selectbox(
        'Select a Organ to Predict',
        [
         'Heart'
         ]
    )

    def display_input(label, tooltip, key, type="text"):
        if type == "text":
            return st.text_input(label, key=key, help=tooltip)
        elif type == "number":
            return st.number_input(label, key=key, help=tooltip, step=1.0, format="%.2f", value=0.0)

    if selected == 'Heart':
        st.title('Heart Match Prediction')
        st.write("Enter the following details to determine the heart match prediction:")

        # Numeric and simple categorical
        AGE = display_input('Recipient Age', 'Enter recipient\'s age', 'AGE', 'number')
        AGE_DON = display_input('Donor Age', 'Enter donor\'s age', 'AGE_DON', 'number')
        CREAT_TRR = display_input('Recipient Creatinine', 'Enter recipient\'s creatinine level', 'CREAT_TRR', 'number')
        CREAT_DON = display_input('Donor Creatinine', 'Enter donor\'s creatinine level', 'CREAT_DON', 'number')
        BMI_CALC = display_input('Recipient BMI', 'Enter recipient\'s Body Mass Index', 'BMI_CALC', 'number')
        BMI_DON_CALC = display_input('Donor BMI', 'Enter donor\'s Body Mass Index', 'BMI_DON_CALC', 'number')
        DAYSWAIT_CHRON = display_input('Days on Waiting List', 'Enter number of days on waiting list', 'DAYSWAIT_CHRON', 'number')
        medcondition = st.selectbox('Medical Condition', ['0', '1', '2'])  # Use your actual codes
        ABOMAT = st.selectbox('Blood Type Match', ['0', '1'])
        DISTANCE = display_input('Distance', 'Enter distance between donor and recipient', 'DISTANCE', 'number')
        TX_YEAR = display_input('Transplant Year', 'Enter year of transplant', 'TX_YEAR', 'number')


        diagnosis_options = [
            'FAILED OHT', 'HCM', 'ICM', 'NICM', 'OTHER/UNKNOWN', 'RESTRICTIVE', 'VALVULAR'
        ]
        diagnosis = st.selectbox('Diagnosis', diagnosis_options)

        mcs_options = [
            'IABP', 'bivad/tah', 'dischargeable VAD', 'left endo device', 'non-dischargeable VAD', 'none', 'right endo device'
        ]
        mcs = st.selectbox('Medical Condition Score', mcs_options)

        abo_options = ['AB', 'B', 'O']
        abo = st.selectbox('Recipient Blood Type', abo_options)

        CODDON_options = [
            'Cardiovascular', 'Drowning', 'Drug Intoxication', 'IntracranHem/Stroke/Seiz', 'Natural Causes', 'Trauma'
        ]
        CODDON = st.selectbox('Cause of Death (Donor)', CODDON_options)

        HIST_MI = st.selectbox('History of Myocardial Infarction', ['No', 'Yes'])


        diagnosis_bools = [1 if diagnosis == opt else 0 for opt in diagnosis_options]
        mcs_bools = [1 if mcs == opt else 0 for opt in mcs_options]
        abo_bools = [1 if abo == opt else 0 for opt in abo_options]
        CODDON_bools = [1 if CODDON == opt else 0 for opt in CODDON_options]
        HIST_MI_Y = 1 if HIST_MI == 'Yes' else 0

        if st.button('Predict Match'):
            try:
                input_data = [
                    float(AGE),             
                    float(AGE_DON),         
                    float(CREAT_TRR),         
                    float(CREAT_DON),         
                    float(BMI_CALC),           
                    float(BMI_DON_CALC),       
                    float(DAYSWAIT_CHRON),    
                    int(medcondition),         
                    int(ABOMAT),              
                    float(DISTANCE),          
                    int(TX_YEAR),              
                
                    *diagnosis_bools,          
                  
                    *mcs_bools,               
                 
                    *abo_bools,                
            
                    *CODDON_bools,             
                    HIST_MI_Y                  
                ]
            

                heart_prediction = models['heart_matching'].predict([input_data])
                heart_matching = 'The heart is a match' if heart_prediction[0] == 1 else 'The heart is not a match'

                if heart_prediction[0] == 1:
                    st.success(heart_matching)
                else:
                    st.error(heart_matching)
            except Exception as e:
                st.error(f"Error in prediction: {e}")

main_app()