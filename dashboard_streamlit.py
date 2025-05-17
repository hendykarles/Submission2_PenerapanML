import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
from PIL import Image
import time
from data_preprocessing import data_preprocessing

from data_preprocessing import encoder_Daytime_evening_attendance, encoder_Debtor, encoder_Displaced, encoder_Gender, encoder_Scholarship_holder, encoder_Tuition_fees_up_to_date
from data_preprocessing import scaler_Admission_grade, scaler_Curricular_units_1st_sem_approved, scaler_Curricular_units_1st_sem_credited, scaler_Curricular_units_1st_sem_enrolled, scaler_Curricular_units_1st_sem_grade, scaler_Curricular_units_2nd_sem_approved, scaler_Curricular_units_2nd_sem_credited, scaler_Curricular_units_2nd_sem_enrolled, scaler_Curricular_units_2nd_sem_grade, scaler_Previous_qualification_grade
from prediction import prediction


#Setting page
st.set_page_config(page_title="Performance Siswa", layout="wide")

#Introduction
#List of image file names
image_files = ['https://github.com/hendykarles/Submission2_PenerapanML/blob/19d0b074d755d81623d31f2fd811bcf61e77eb84/logo_jji.jpeg']

#Desired image size in pixels
desired_width = 150
desired_height = 150

col1, col2 = st.columns([2, 10])

with col1:
    for idx, image_file in enumerate(image_files):
        img = Image.open(image_file)
        resized_img = img.resize((desired_width, desired_height))
        st.image(resized_img)
with col2:
    st.header(':sparkles: JAYA JAYA INSTITUTE :sparkles:')
    st.subheader(":mortar_board: Prediksi Kinerja Akademik Siswa :mortar_board:")

st.sidebar.write("""
    Jaya Jaya Institut merupakan salah satu institusi pendidikan perguruan yang telah berdiri sejak tahun 2000. Hingga saat ini ia telah mencetak banyak lulusan dengan reputasi yang sangat baik. Akan tetapi, terdapat banyak juga siswa yang tidak menyelesaikan pendidikannya alias dropout.

    Jumlah dropout yang tinggi ini tentunya menjadi salah satu masalah yang besar untuk sebuah institusi pendidikan. Oleh karena itu, Jaya Jaya Institut ingin mendeteksi/memprediksi secepat mungkin siswa yang mungkin akan melakukan dropout sehingga dapat diberi bimbingan khusus.
""")

# Initialize an empty dictionary to store user input
data = {}

# Convert user input dictionary to DataFrame
user_input_df = pd.DataFrame(data, index=[0])

st.markdown("### Informasi Siswa")
col1, col2, col3 = st.columns(3)
with col1:
    encoder_Tuition_fees_up_to_date = LabelEncoder()
    encoder_Tuition_fees_up_to_date.fit(['Not Update', 'Update'])
    Tuition_fees_up_to_date = st.selectbox(label='Tuition fees', options=['Not Update', 'Update'], index=1)
    data['Tuition_fees_up_to_date'] = [encoder_Tuition_fees_up_to_date.transform([Tuition_fees_up_to_date])[0]]
with col2:
    encoder_Scholarship_holder = LabelEncoder()
    encoder_Scholarship_holder.fit(['Non Scholarship', 'Scholarship'])
    Scholarship_holder = st.selectbox(label='Scholarship holder', options=['Non Scholarship', 'Scholarship'], index=0)
    data['Scholarship_holder'] = [encoder_Scholarship_holder.transform([Scholarship_holder])[0]]
with col3:
    encoder_Debtor = LabelEncoder()
    encoder_Debtor.fit(['Non Debtor', 'Debtor'])
    Debtor = st.selectbox(label='Debtor', options=['Non Debtor', 'Debtor'], index=1)
    data['Debtor'] = [encoder_Debtor.transform([Debtor])[0]]
    
col4, col5, col6 = st.columns(3)
with col4:
    encoder_Displaced = LabelEncoder()
    encoder_Displaced.fit(['Non Displaced', 'Displaced'])
    Displaced = st.selectbox(label='Displaced', options=['Non Displaced', 'Displaced'], index=0)
    data['Displaced'] = [encoder_Displaced.transform([Displaced])[0]]
with col5:
    encoder_Daytime_evening_attendance = LabelEncoder()
    encoder_Daytime_evening_attendance.fit(['Daytime', 'Evening'])
    Daytime_evening_attendance = st.selectbox(label='Attendance', options=['Daytime', 'Evening'], index=0)
    data['Daytime_evening_attendance'] = [encoder_Daytime_evening_attendance.transform([Daytime_evening_attendance])[0]]
with col6:
    encoder_Gender = LabelEncoder()
    encoder_Gender.fit(['Female', 'Male'])
    Gender = st.selectbox(label='Gender', options=['Female', 'Male'], index=1)
    data['Gender'] = [encoder_Gender.transform([Gender])[0]]

st.markdown("### Nilai Akademik")
col7, col8 = st.columns(2)
with col7:
    Admission_grade = st.slider(label='Admission Grade', min_value=0, max_value=200, value=100)
    data['Admission_grade'] = [Admission_grade]
with col8:
    Previous_qualification_grade = st.slider(label='Previous Qualification Grade', min_value=0, max_value=200, value=100)
    data['Previous_qualification_grade'] = [Previous_qualification_grade]

st.markdown("#### Unit Kulikuler Semester 1")
col9, col10, col11, col12 = st.columns(4)
with col9:
    Curricular_units_1st_sem_approved = st.number_input(label='1st Sem Approved', value=5)
    data['Curricular_units_1st_sem_approved'] = [Curricular_units_1st_sem_approved]
with col10:
    Curricular_units_1st_sem_grade = st.number_input(label='1st Sem Grade', value=12)
    data['Curricular_units_1st_sem_grade'] = [Curricular_units_1st_sem_grade]
with col11:
    Curricular_units_1st_sem_enrolled = st.number_input(label='1st Sem Enrolled', value=6)
    data['Curricular_units_1st_sem_enrolled'] = [Curricular_units_1st_sem_enrolled]
with col12:
    Curricular_units_1st_sem_credited = st.number_input(label='1st Sem Credited', value=0)
    data['Curricular_units_1st_sem_credited'] = [Curricular_units_1st_sem_credited]

st.markdown("#### Unit Kulikuler Semester 2")
col13, col14, col15, col16 = st.columns(4)
with col13:
    Curricular_units_2nd_sem_approved = st.number_input(label='2nd Sem Approved', value=5)
    data['Curricular_units_2nd_sem_approved'] = [Curricular_units_2nd_sem_approved]
with col14:
    Curricular_units_2nd_sem_grade = st.number_input(label='2nd Sem Grade', value=12)
    data['Curricular_units_2nd_sem_grade'] = [Curricular_units_2nd_sem_grade]
with col15:
    Curricular_units_2nd_sem_enrolled = st.number_input(label='2nd Sem Enrolled', value=6)
    data['Curricular_units_2nd_sem_enrolled'] = [Curricular_units_2nd_sem_enrolled]
with col16:
    Curricular_units_2nd_sem_credited = st.number_input(label='2nd Sem Credited', value=0)
    data['Curricular_units_2nd_sem_credited'] = [Curricular_units_2nd_sem_credited]

# Convert user input dictionary to DataFrame
user_input_df = pd.DataFrame(data, index=[0])

# Display user input
with st.expander("Dataset"):
        st.dataframe(data=user_input_df, width=1200, height=20)
# Preprocess data and make prediction on button click
if st.button('Klik disini untuk prediksi'):
    new_data = data_preprocessing(data=data)
    with st.spinner("Predicting..."):
        time.sleep(2)  # Simulating prediction process
        output = prediction(new_data)
        st.toast("Prediction completed!")
        st.success(f"## 🎯 Prediction Result: {output}")
        

st.snow()
