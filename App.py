import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import io

st.set_page_config(page_title="📋 Kroon Beheer Client Calendar", layout="wide")
st.title("📋 Kroon Beheer Client Manager + Calendar View")

# Default file path
default_filename = "Reservations Kroon Beheer BV - Kroon Beheer Client Info .csv"
default_path = f"/mnt/data/{default_filename}"

# --- File Upload or Use Default ---
st.sidebar.header("📂 File Options")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Uploaded CSV loaded.")
    save_path = f"/mnt/data/{uploaded_file.name}"
else:
    if os.path.exists(default_path):
        df = pd.read_csv(default_path)
        st.sidebar.success(f"✅ Loaded: {default_filename}")
    else:
        df = pd.DataFrame(columns=[
            "First Name", "Last Name", "Email", "Phone", 
            "Reservation Dates", "Status"
        ])
        st.sidebar.warning("⚠️ No file found. A new file will be created.")
    save_path = default_path

# --- Add New Client with Multiple Dates ---
st.subheader("➕ Add New Client With Multiple Reservation Dates")

with st.form("add_multi_date_client", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
    with col2:
        last_name = st.text_input("Last Name")
        status = st.selectbox("Status", ["Pending", "Confirmed", "Cancelled"])

    reservation_dates = st.multiselect(
        "Select One or More Reservation Dates",
        options=pd.date_range(start=datetime.today(), periods=90).date,
        format_func=lambda x: x.strftime("%Y-%m-%d")
    )

    submit = st.form_submit_button("Add Client")
    if submit:
        new_entry = {
            "First Name": first_name,
            "Last Name": last_name,
            "Email": email,
            "Phone": phone,
            "Reservation Dates": ", ".join([str(d) for d in reservation_dates]),
            "Status": status
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(save_path, index=False)
        st.success(f"✅ Client added and saved to `{os.path.basename(save_path)}`")

# --- Editable Table ---
st.subheader("✏️ Edit Full Client Table")
edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
    key="client_editor"
)

if st.button("💾 Save Edited Table"):
    edited_df.to_csv(save_path, index=False)
    st.success(f"✅ Saved changes to `{os.path.basename(save_path)}`")

# --- Calendar Visualization ---
st.subheader("📆 Reservation Calendar View")

calendar_data = []
for _, row in df.iterrows():
    if pd.notna(row["Reservation Dates"]):
        for date in str(row["Reservation Dates"]).split(","):
            date = date.strip()
            if date:
                calendar_data.append({
                    "Client": f"{row['First Name']} {row['Last Name']}",
                    "Date": date,
                    "Status": row.get("Status", "Unknown")
                })

if calendar_data:
    calendar_df = pd.DataFrame(calendar_data)
    calendar_df["Date"] = pd.to_datetime(calendar_df["Date"], errors="coerce")

    fig = px.timeline(
        calendar_df,
        x_start="Date",
        x_end="Date",
        y="Client",
        color="Status",
        title="📅 Client Reservation Timeline",
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Clients",
        showlegend=True,
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No reservation data available yet to show.")

# --- Optional CSV Export ---
st.download_button(
    "📤 Download Current CSV",
    data=edited_df.to_csv(index=False).encode("utf-8"),
    file_name=os.path.basename(save_path),
    mime="text/csv"
)
