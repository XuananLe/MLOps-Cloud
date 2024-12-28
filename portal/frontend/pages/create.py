import streamlit as st
import requests
import time

st.write("Fill in the form below and click create  button to create a new deployment")
st.text("")
st.text("")

col1, col2, col3 = st.columns([0.3, 0.05, 0.6])
this_page = "create_new_test"

pipeline = ["yolov7s", "computer-vision", "text-embedding"]
version = ["v2024-12-12", "v2024-12-10", "v2024-12-08"]

with col1:
    deployment_name = st.text_input("Deployment name")
    description = st.text_area("Description")
    training_pipeline = st.selectbox("Select training pipeline", pipeline)
    training_version = st.selectbox("Select training version", version)

    port = st.number_input("Port", min_value=1, value=16000)
    replica_count = st.number_input("Replica count", min_value=1, value=10)

    submit = st.button("Deploy", key=f"deploy")
    if submit:
        st.session_state.submit = True

with col3:
    box = st.container(border=True)
    box.markdown(
        """
        ### Create a new deployment
        1. Enter the `deployment name`, `description` of the deployment
        2. Choose the `training pipeline` and `version` (from Container Registry)
        3. Choose the `port` and `replica count`
        4. Click the **Deploy** button  :rocket:
        """
    )