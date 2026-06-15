import streamlit as st
import pandas as pd
import tempfile

from utils.pdf_parser import extract_pdf_data
from utils.validator import validate

st.set_page_config(layout="wide")

st.title("Site Imprest automation")

uploaded_pdf = st.file_uploader(
    "Upload Site Imprest PDF",
    type=["pdf"]
)

if uploaded_pdf:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:

        tmp.write(uploaded_pdf.read())
        pdf_path = tmp.name

    data = extract_pdf_data(pdf_path)

    st.header("Raw Extracted Data")
    st.write(data)

    st.header("Project Details")

    details_df = pd.DataFrame(
        data["project_details"].items(),
        columns=["Field", "Value"]
    )

    st.dataframe(details_df, use_container_width=True)

    st.header("Main Sheet Categories")

    main_df = pd.DataFrame(
        data["main_categories"].items(),
        columns=["Category", "Amount"]
    )

    st.dataframe(main_df, use_container_width=True)

    st.header("Sub Sheet Categories")

    sub_df = pd.DataFrame(
        data["subsheet_categories"].items(),
        columns=["Category", "Amount"]
    )

    st.dataframe(sub_df, use_container_width=True)

    validation = validate(
        data["main_categories"],
        data["subsheet_categories"]
    )

    validation_df = pd.DataFrame(validation)

    st.header("Validation Table")

    st.dataframe(validation_df, use_container_width=True)

    passed = len(
        validation_df[
            validation_df["Status"] == "PASS"
        ]
    )

    failed = len(
        validation_df[
            validation_df["Status"] == "FAIL"
        ]
    )

    st.header("Final Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Passed", passed)

    with col2:
        st.metric("Failed", failed)

    if failed == 0:
        st.success("All Sub Sheet Totals Match Main Sheet")
    else:
        st.error("Mismatch Found")
