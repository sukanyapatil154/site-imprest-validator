import streamlit as st
import pandas as pd
import tempfile
from utils.pdf_parser import extract_main_sheet_data
from utils.validator import validate

st.title("Site Imprest Validator")

uploaded_pdf = st.file_uploader(
    "Upload Site Imprest PDF",
    type=["pdf"]
)

if uploaded_pdf:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp:

        tmp.write(uploaded_pdf.read())

        pdf_path = tmp.name

    data = extract_main_sheet_data(pdf_path)

    st.subheader("Project Details")

    st.write(
        f"Project Name: {data['project_name']}"
    )

    st.write(
        f"Site Name: {data['site_name']}"
    )

    st.write(
        f"Employee ID: {data['emp_id']}"
    )

    st.subheader("Category Totals")

    category_df = pd.DataFrame(
        data["categories"].items(),
        columns=["Category","Amount"]
    )

    st.dataframe(category_df)

    bill_totals = data["categories"]

    validation = validate(
        data["categories"],
        bill_totals
    )

    validation_df = pd.DataFrame(validation)

    st.subheader("Validation Table")

    st.dataframe(validation_df)

    passed = len(
        validation_df[
            validation_df["Status"]=="PASS"
        ]
    )

    failed = len(
        validation_df[
            validation_df["Status"]=="FAIL"
        ]
    )

    st.subheader("Final Summary")

    st.write(f"Passed : {passed}")

    st.write(f"Failed : {failed}")

    if failed == 0:
        st.success("Verification Passed")
    else:
        st.error("Verification Failed")
