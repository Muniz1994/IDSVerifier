import streamlit as st
import ifcopenshell
from ifctester import ids, reporter
from io import StringIO
from report import render_validation_report

st.set_page_config(page_title="IFC vs IDS Validator", layout="wide")

st.title("🔍 IFC-IDS File Validator")
st.write("Upload an IFC model and an IDS file to validate conformance.")

# File upload
uploaded_ifc = st.file_uploader("Upload IFC file", type=["ifc"])
uploaded_ids = st.file_uploader("Upload IDS file", type=["ids"])

# Process and validate
if uploaded_ifc and uploaded_ids:
        st.info("Reading IFC and IDS files...")
        
        # Read IFC file
        ifc_file = ifcopenshell.file.from_string(uploaded_ifc.getvalue().decode("utf-8", errors="ignore"))


        ids_obj = ids.open(uploaded_ids)

        # Validate  
        st.info("Running validation...")    
        results = ids_obj.validate(ifc_file)



        report = reporter.Json(ids_obj).report()


        if report:
            render_validation_report(report)


else:
    st.warning("Please upload both an IFC file and an IDS file.")
