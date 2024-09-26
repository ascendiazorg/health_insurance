import streamlit as st
import joblib
import numpy as np
import pandas as pd

def main():
    st.set_page_config(
        page_title="Health Insurance Cost Prediction",
        page_icon=":hospital:",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(
        """
        <style>
        body {
            background-color: #f0f0f0; /* light gray */
            color: #333333; /* dark gray */
        }
        .sidebar .sidebar-content {
            background-color: #ffffff; /* white */
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* subtle shadow */
        }
        .stButton > button {
            background-color: #0066cc; /* blue */
            color: #ffffff; /* white */
            font-weight: bold;
            border-radius: 5px;
            padding: 10px 20px;
        }
        .stTextInput > div > div > input {
            border-radius: 5px;
            border: 1px solid #cccccc; /* light gray */
        }
        .stDataFrame > div > div > div > div > div.dataframe.sc-fjdhpX.kJdKtQ {
            background-color: #ffffff; /* white */
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* subtle shadow */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    menu = ["Home", "Predict Insurance Cost", "History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.markdown("<h1 style='text-align: center; color: #0066cc;'>Welcome to the Health Insurance Cost Prediction App</h1>", unsafe_allow_html=True)
        st.image('https://emerj.com/wp-content/uploads/2018/10/predictive-analytics-in-healthcare-current-applications-and-trends-3.jpg', use_column_width=True)
        st.markdown("""
            This application allows you to predict health insurance costs based on your personal information.
            Use the sidebar to navigate to the prediction page.
        """)

    elif choice == "Predict Insurance Cost":
        st.markdown("<h1 style='text-align: center; color: #0066cc;'>Health Insurance Cost Prediction</h1>", unsafe_allow_html=True)
        
        model = joblib.load('model_joblib_test')

        if 'history' not in st.session_state:
            st.session_state['history'] = []

        sex = st.selectbox('Sex', ('Male', 'Female'))
        sex = 1 if sex == 'Male' else 0

        age = st.number_input("Age", min_value=1, max_value=100)

        bmi = st.number_input("Enter Your BMI Value")
        st.markdown('You can check your BMI value here: [BMI Calculator](https://www.bupa.com.au/healthlink/health-tools/bmi-calculator)')

        children = st.selectbox('Enter Number of Children', (0, 1, 2, 3, 4))

        smoker = st.selectbox('Smoker', ('Yes', 'No'))
        smoker = 1 if smoker == 'Yes' else 0

        region = st.selectbox('Enter Your Region', ('Southwest', 'Southeast', 'Northwest', 'Northeast'))
        region_dict = {'Southwest': 1, 'Southeast': 2, 'Northwest': 3, 'Northeast': 4}
        region = region_dict[region]

        if st.button('Predict'):
            try:
                pred = model.predict(np.array([[age, sex, bmi, children, smoker, region]]))
                formatted_pred = f"${pred[0]:,.2f}"
                st.balloons()
                st.success(f'Your Insurance Cost is {formatted_pred}')
                
                st.session_state['history'].append({
                    'id': len(st.session_state['history']) + 1,
                    'age': age,
                    'sex': 'Male' if sex == 1 else 'Female',
                    'bmi': bmi,
                    'children': children,
                    'smoker': 'Yes' if smoker == 1 else 'No',
                    'region': [key for key, value in region_dict.items() if value == region][0],
                    'prediction': formatted_pred
                })
            except Exception as e:
                st.error(f"An error occurred: {e}")

            if st.button('Clear'):
               st.session_state['age'] = 18
               st.session_state['sex'] = 'Male'
               st.session_state['bmi'] = 0.0
               st.session_state['children'] = 0
               st.session_state['smoker'] = 'No'
               st.session_state['region'] = 'Southwest'
               st.experimental_rerun()

    elif choice == "History":
        st.markdown("<h1 style='text-align: center; color: #0066cc;'>Prediction History</h1>", unsafe_allow_html=True)
        
        if st.session_state['history']:
            history_df = pd.DataFrame(st.session_state['history'])
            st.dataframe(history_df.set_index('id'))
        else:
            st.markdown("<h3 style='text-align: center; color: #333333;'>No history available</h3>", unsafe_allow_html=True)

    elif choice == "About":
        st.markdown("<h1 style='text-align: center; color: #0066cc;'>About This App</h1>", unsafe_allow_html=True)
        st.markdown("""
                    The venerable insurance industry is no stranger to data driven decision making. Yet in today's rapidly
                    transforming digital landscape, Insurance is struggling to adapt and benefit from new technologies
                    compared to other industries, even within the BFSI sphere (compared to the Banking sector for example.) 
                    Extremely complex underwriting rule-sets that are radically different in different product lines, many 
                    non-KYC environments with a lack of centralized customer information base, complex relationship with 
                    consumers in traditional risk underwriting where sometimes customer centricity runs reverse to business 
                    profit, inertia of regulatory compliance - are some of the unique challenges faced by Insurance Business.
                    """)

if __name__ == '__main__':
    main()