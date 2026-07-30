import ai_vision
import streamlit as st
import os
from PIL import Image

import db
import qr_tools


# -----------------------------
# Initialization
# -----------------------------

db.db_init()

st.set_page_config(
    page_title="Herbarium Twin",
    layout="wide",
)

st.title("Herbarium Twin")
st.write("AI-assisted herbarium inventory system")


# -----------------------------
# Tabs
# -----------------------------

tab1, tab2 = st.tabs(
    [
        ":package: New Inventory",
        ":mag_right: Existing Collection",
    ]
)


# ==================================================
# TAB 1: NEW INVENTORY
# ==================================================

with tab1:
    st.header("Create Herbarium Box Record")

    # -----------------------------
    # Basic information
    # -----------------------------

    box_id = st.text_input(
        "Box ID",
        value=db.get_next_box_id(),
    )

    location = st.text_input(
        "Current Location *",
        placeholder="Example: Room 204 Shelf B",
    )

    inventor = st.text_input("Inventoried By")

    # -----------------------------
    # Image upload
    # -----------------------------

    st.subheader("Upload Images")

    uploaded_files = st.file_uploader(
        "Upload herbarium box photos",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )

    image_paths = []

    if uploaded_files:
        os.makedirs("captured_images", exist_ok=True)

        for i, file in enumerate(uploaded_files):
            img = Image.open(file)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            temp_path = os.path.join(
                "captured_images",
                f"{box_id}_{i}.jpg",
            )

            img.save(temp_path)
            image_paths.append(temp_path)

            st.image(
                img,
                caption=file.name,
                width=250,
            )

        # -----------------------------
        # AI analysis
        # -----------------------------

        if (
            "ai_results" not in st.session_state
            or st.session_state.get("last_box") != box_id
        ):
            with st.spinner(":robot_face: AI analyzing herbarium images..."):
                try:
                    st.session_state.ai_results = ai_vision.analyze_box_images(image_paths)
                    st.session_state.last_box = box_id
                except Exception as e:
                    st.error(f"AI failed: {e}")

    ai = st.session_state.get("ai_results", {})

    # -----------------------------
    # AI-generated fields
    # -----------------------------

    st.subheader("AI Generated Metadata")

    collection_area = st.text_input(
        "Collection Area",
        ai.get("collection_area", ""),
    )

    material_type = st.text_input(
        "Material Type",
        ai.get("material_type", ""),
    )

    packet_count = st.text_input(
        "Estimated Packet Count",
        ai.get("estimated_packet_count", ""),
    )

    taxonomic = st.text_area(
        "Taxonomic Clues",
        ai.get("taxonomic_clues", ""),
    )

    geographic = st.text_area(
        "Geographic Clues",
        ai.get("geographic_clues", ""),
    )

    collector = st.text_area(
        "Collector Clues",
        ai.get("collector_clues", ""),
    )

    condition = st.text_input(
        "Condition",
        ai.get("condition", ""),
    )

    processing = st.text_input(
        "Processing Status",
        ai.get("processing_status", ""),
    )

    priority = st.text_input(
        "Priority",
        ai.get("priority", ""),
    )

    # -----------------------------
    # Human input
    # -----------------------------

    human_notes = st.text_area("Human Notes")

    ai_summary = st.text_area(
        "AI Summary",
        ai.get("ai_summary", ""),
    )

    confidence = st.text_input(
        "AI Confidence Notes",
        ai.get("ai_confidence_notes", ""),
    )

    # -----------------------------
    # Save
    # -----------------------------

    if st.button(":floppy_disk: Save Herbarium Box"):
        if not location:
            st.error("Current location is required.")
        elif db.box_id_exists(box_id):
            st.error("Box ID already exists.")
        else:
            record = {
                "box_id": box_id,
                "current_location": location,
                "collection_area": collection_area,
                "material_type": material_type,
                "estimated_packet_count": packet_count,
                "taxonomic_clues": taxonomic,
                "geographic_clues": geographic,
                "collector_clues": collector,
                "condition": condition,
                "processing_status": processing,
                "priority": priority,
                "human_notes": human_notes,
                "ai_summary": ai_summary,
                "ai_confidence_notes": confidence,
                "image_paths": ",".join(image_paths),
                "inventoried_by": inventor,
            }

            db.save_box(record)
            qr_path = qr_tools.generate_box_qr(box_id, location)
            st.success(f"Saved {box_id}")
            st.image(qr_path, caption="Box QR Code")


# ==================================================
# TAB 2: EXISTING COLLECTION
# ==================================================

with tab2:
    st.header("Inventory Database")

    boxes = db.get_all_boxes()

    if not boxes:
        st.info("No boxes inventoried yet.")
    else:
        for box in boxes:
            with st.expander(f":package: {box[0]}"):
                st.write("Location:", box[1])
                st.write("Material:", box[3])
                st.write("Summary:", box[12])

                if box[14]:
                    st.image(box[14].split(",")[0])
