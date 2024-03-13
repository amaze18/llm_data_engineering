import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
import boto3
import os

st.cache_data.clear()

__login__obj = __login__(auth_token="courier_auth_token", 
                         company_name="Shims",
                         width=200, height=250, 
                         logout_button_name='Logout', hide_menu_bool=False, 
                         hide_footer_bool=False, 
                         lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    st.write("Your Streamlit Application Begins here!")

    text_input = st.text_input("Enter course name 👇")

    if text_input:
        st.write("You entered: ", text_input)

    S3_BUCKET_NAME = "yourbucketname"
    AWS_ACCESS_KEY_ID = "your_access_id"
    AWS_SECRET_ACCESS_KEY = "your_access_key"    


    def upload_to_s3(course_name, file):
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        subfolder_path = f"{course_name}/"
        s3_file_path = f"{subfolder_path}{file.name}"
        try:
            s3.upload_fileobj(file, S3_BUCKET_NAME, s3_file_path)
            st.success(f"File '{file.name}' uploaded successfully to '{subfolder_path}'")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    uploaded_filenames = []

    def upload():
        uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            local_file_path = os.path.join("temp", uploaded_file.name)
            with open(local_file_path, "wb") as local_file:
                local_file.write(bytes_data)
            upload_to_s3(text_input, uploaded_file)  # Call the upload_to_s3 function here
            uploaded_filenames.append(uploaded_file.name)
            os.remove(local_file_path)

        st.write("Uploaded filenames:", ', '.join(uploaded_filenames))

    upload()
