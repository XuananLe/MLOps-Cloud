import streamlit as st
import pandas as pd
import requests
import time

st.write("Fill in the form below and click create  button to create a new deployment")
st.text("")
st.text("")

# Dữ liệu JSON
data = {
    "pipelines": [
        {
            "pipeline_name": "yolov7s",
            "version_count": 1,
            "created_at": "2021-10-01",
            "days_per_train": "7",
        },
        {
            "pipeline_name": "computer-vision",
            "version_count": 4,
            "created_at": "2021-10-01",
            "days_per_train": "3",
        },
        {
            "pipeline_name": "text-embedding",
            "version_count": 2,
            "created_at": "2021-10-01",
            "days_per_train": "2",
        },
    ]
}

count = 0
for item in data["pipelines"]:
    count += 1
    box = st.container(border=True)
    with box:
        col1, col2 = st.columns([0.9, 0.07])
        with col1:
            st.markdown(f"### Pipeline: {item['pipeline_name']}")
        with col2:
            update = st.button("Update", key=f"update_{count}")
        st.write(f"Version count: {item['version_count']}")
        st.write(f"Created at: {item['created_at']}")

        col3, col4 = st.columns([0.9, 0.07])
        with col3:
            input = st.text_input("Days per train", value=item['days_per_train'], key=f"days_per_train_{count}")

        st.text("")