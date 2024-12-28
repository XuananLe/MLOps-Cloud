import streamlit as st
import requests
import pandas as pd
import time

st.write("Fill in the form below and click create  button to create a new deployment")
st.text("")
st.text("")

col1, col2, col3 = st.columns(3)
deployments = 1
pod_count = 1
ready_count = 1

with col1:
    box = st.container(border=True)
    box.markdown(
        f"""
            # Deployments
            ## {deployments}
        """
    )

with col2:
    box = st.container(border=True)
    box.markdown(
        f"""
            # Pods
            ## {pod_count}
        """
    )

with col3:
    box = st.container(border=True)
    box.markdown(
        f"""
            # Ready
            ## {ready_count}
        """
    )



# Dữ liệu JSON
data = {
    "deployment": [
        {
            "model_name": "yolov7s",
            "replica": 1,
            "endpoint": "http://35.101.319.189:8000",
            "status": "RUNNING",
        },
        {
            "model_name": "computer-vision",
            "replica": 1,
            "endpoint": "http://35.101.319.189:8000",
            "status": "STOPPED",
        },
        {
            "model_name": "text-embedding",
            "replica": 1,
            "endpoint": "http://35.101.319.189:8000",
            "status": "RUNNING",
        },
    ]
}

# Chuyển đổi dữ liệu JSON thành DataFrame
deployments = pd.DataFrame(data["deployment"])

# Hiển thị dữ liệu lên bảng
st.text("")
st.text("")
st.text("")
st.markdown("### Deployments")
st.dataframe(deployments, use_container_width=True)
