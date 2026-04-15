import streamlit as st
from pdf_parser import extract_text_and_images
from ddr_generator import generate_ddr

st.set_page_config(page_title="AI DDR Generator", layout="wide")

st.title("🏗️ AI DDR Report Generator")

inspection_file = st.file_uploader("Upload Inspection Report (PDF)", type=["pdf"])
thermal_file = st.file_uploader("Upload Thermal Report (PDF)", type=["pdf"])

if st.button("Generate DDR Report"):

    if inspection_file and thermal_file:

        with open("inspection.pdf", "wb") as f:
            f.write(inspection_file.read())

        with open("thermal.pdf", "wb") as f:
            f.write(thermal_file.read())

        st.info("Extracting data...")

        inspection_text, inspection_images = extract_text_and_images("inspection.pdf")
        thermal_text, thermal_images = extract_text_and_images("thermal.pdf")

        st.info("Generating AI Report...")

        report = generate_ddr(inspection_text, thermal_text)

        st.success("DDR Generated!")

        st.subheader("📄 Final DDR Report")
        st.markdown(report, unsafe_allow_html=True)

        st.subheader("🖼 Extracted Images")

        for img in inspection_images + thermal_images:
            st.image(img, width=300)

    else:
        st.warning("Please upload both files.")
