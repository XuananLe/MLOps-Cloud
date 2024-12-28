import streamlit as st
import requests
import time
import pandas as pd
import numpy as np

from altair import value

st.write("Fill in the form below and click create  button to create a new deployment")
st.text("")
st.text("")

deployments = ["yolov7s", "computer-vision", "text-embedding"]
version = ["v2024-12-12", "v2024-12-10", "v2024-12-08"]

select_deployments = st.selectbox("Select deployment", deployments)
view = st.button("View", key="view")

if view:
    box = st.container(border=True)
    with box:
        st.markdown(f"### Deployment: {select_deployments}")
        description = st.text_area("Description", value = "This is a deployment")
        # training_pipeline = st.selectbox("Select training pipeline", deployments)
        training_pipeline = st.text_input("Training pipeline", value = deployments[0])
        # training_version = st.selectbox("Select training version", version, value = version[0])
        training_version = st.text_input("Training version", value = version[0])
        port = st.number_input("Port", min_value=1, value=8080)
        replica_count = st.number_input("Replica count", min_value=1, value=1)

        update = st.button("Update", key=f"update")
        if update:
            st.session_state.submit = True

    box2 = st.container(border=True)
    with box2:
        st.markdown(f"### Logs: {select_deployments}")
        log = st.code(
            """
            INFO:     Started server process [7]
            INFO:     Waiting for application startup.
            INFO:     CUDA_PER_PROCESS_MEMORY_FRACTION set to 1.0
            INFO:     Running on CPU
            INFO:     Running ONNX vectorizer with quantized model for amd64 (AVX2)
            INFO:     Application startup complete.
            INFO:     Uvicorn running on http://
            """
        )

    box3 = st.container(border=True)
    with box3:
        st.markdown(f"### Usage by time: {select_deployments}")
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        st.line_chart(chart_data)
