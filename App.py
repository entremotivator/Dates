import streamlit as st
import pandas as pd
import io
import csv
from datetime import datetime
import base64

# Configure page
st.set_page_config(
    page_title="CSV Manager",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for light blue theme
st.markdown("""
<style>
    .main {
        background-color: #f0f8ff;
    }
    .stSidebar {
        background-color: #e6f3ff;
    }
    .stButton > button {
        background-color: #4a90e2;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #357abd;
    }
    .stSelectbox > div > div {
        background-color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
    }
    .stTextArea > div > div > textarea {
        background-color: #ffffff;
    }
    .header-style {
        background: linear-gradient(90deg, #4a90e2, #87ceeb);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4a90e2;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'generated_data' not in st.session_state:
    st.session_state.generated_data = None

# Sidebar navigation
st.sidebar.markdown("## 📊 CSV Manager")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["🏠 Home", "📝 Generate CSV", "📤 Upload CSV", "📊 View Data", "ℹ️ About"]
)

def create_sample_csv_data():
    """Create sample CSV data similar to the Kroon Beheer example"""
    data = []
    
    # Header section
    data.extend([
        ["Kroon Beheer Client Profile", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["General Client Info:", "", "", "", "", "", ""],
        ["", "", "", "", "Type of cleans:", "Status Code:", "Comments:"],
        ["Check-out time:", "12:00:00", "", "", "Check-In", "CI", "Alles schoonmaken en netjes zetten voor de volgende gasten."],
        ["Check-in time:", "16:00:00", "", "", "Stay-over", "SO", "Tussen schoonmaak wanneer gasten verblijven. (Linnen en Handoeken verversen.)"],
        ["Amenities Yes/No:", "YES", "", "", "Check-out/in", "CO/CI", "Check out check in op dezelfde dag."],
        ["Laundry Services Yes/No:", "Bayside Garage", "", "", "Fresh-up", "FU", "Villa/App is al schoon heeft alleen een fresh up nodig voor de volgende check in."],
        ["Keys Yes/No:", "Yes", "", "", "Deep Cleaning", "DC", "Grondige schoonmaak van de woning/app."],
        ["Codes Yes/No:", "Yes", "", "", "Construction Cleaning", "COC", "Constructie schoonmaak na renovaties bij woning/app."],
        ["", "", "", "", "", "", ""],
        ["Villas/Apartments:", "", "", "", "", "", ""],
        ["Villas/Apartments Name:", "Address", "Hours +/-", "SO +/-", "Keys & Codes:", "Comments:", ""],
    ])
    
    # Sample villa data
    villas = ["B01", "Bay 12", "C04", "C05", "CCBB02", "H24", "J9", "L13", "N03", "N18", 
              "O7", "O14", "P06", "P08", "P10", "Q04", "S02", "S16", "S17", "SUN 2", 
              "SUN 4", "U12", "U13", "V17", "VRD7"]
    
    for villa in villas:
        data.append([villa, "", "", "", "", "", ""])
    
    # Add empty rows
    for _ in range(10):
        data.append(["", "", "", "", "", "", ""])
    
    # Amenities section
    data.extend([
        ["List of Amenities:", "", "", "", "", "", ""],
        ["Item", "Quantity", "Comments:", "", "", "", ""],
        ["Toilet paper per bathroom", "1", "", "", "", "", ""],
        ["Coffee", "", "", "", "", "", ""],
        ["Tea", "", "", "", "", "", ""],
        ["Sugar", "", "", "", "", "", ""],
        ["Hand soap", "", "", "", "", "", ""],
        ["Shower gel", "", "", "", "", "", ""],
        ["Conditioner", "", "", "", "", "", ""],
        ["Welcome groceries package", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["Linens:", "", "", "", "", "", ""],
        ["Service/Item:", "# per guest/per clean", "Comments:", "", "", "", ""],
        ["Laundry service with Videmi", "No", "Laundry is at Bayside Garage", "", "", "", ""],
        ["Beach Towels per guest", "1", "", "", "", "", ""],
        ["Bath Towels per guest", "2", "", "", "", "", ""],
        ["Face Towels per guest", "1", "", "", "", "", ""],
        ["Kitchen Towels per clean", "1 set", "", "", "", "", ""],
    ])
    
    return data

def download_csv(data, filename):
    """Create download link for CSV data"""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(data)
    csv_string = output.getvalue()
    
    b64 = base64.b64encode(csv_string.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="background-color: #4a90e2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">📥 Download CSV</a>'
    return href

# Main content based on selected page
if page == "🏠 Home":
    st.markdown('<div class="header-style"><h1>🏠 CSV Manager Application</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h3>📝 Generate CSV</h3>
            <p>Create CSV files similar to the Kroon Beheer Client Profile template with customizable data.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h3>📤 Upload CSV</h3>
            <p>Upload your own CSV files and analyze their structure and content.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-box">
            <h3>📊 View Data</h3>
            <p>Visualize and explore your uploaded or generated CSV data with interactive tables.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🚀 Quick Start")
    st.markdown("""
    1. **Generate CSV**: Create a new CSV file based on the Kroon Beheer template
    2. **Upload CSV**: Upload your existing CSV files for analysis
    3. **View Data**: Explore your data with interactive tables and statistics
    """)

elif page == "📝 Generate CSV":
    st.markdown('<div class="header-style"><h1>📝 Generate CSV Template</h1></div>', unsafe_allow_html=True)
    
    st.markdown("### Customize Your CSV Template")
    
    col1, col2 = st.columns(2)
    
    with col1:
        client_name = st.text_input("Client Name", value="Kroon Beheer Client Profile")
        checkout_time = st.time_input("Check-out Time", value=datetime.strptime("12:00", "%H:%M").time())
        checkin_time = st.time_input("Check-in Time", value=datetime.strptime("16:00", "%H:%M").time())
        amenities = st.selectbox("Amenities Available", ["YES", "NO"])
        laundry_service = st.text_input("Laundry Service Location", value="Bayside Garage")
    
    with col2:
        keys_available = st.selectbox("Keys Available", ["Yes", "No"])
        codes_available = st.selectbox("Codes Available", ["Yes", "No"])
        num_villas = st.number_input("Number of Villas/Apartments", min_value=1, max_value=50, value=25)
        
        # Additional customization
        st.markdown("#### Additional Items")
        custom_amenities = st.text_area("Custom Amenities (one per line)", 
                                       value="Toilet paper per bathroom\nCoffee\nTea\nSugar\nHand soap")
    
    if st.button("🔄 Generate CSV Template", type="primary"):
        # Create customized data
        data = []
        
        # Header
        data.extend([
            [client_name, "", "", "", "", "", ""],
            ["", "", "", "", "", "", ""],
            ["General Client Info:", "", "", "", "", "", ""],
            ["", "", "", "", "Type of cleans:", "Status Code:", "Comments:"],
            ["Check-out time:", str(checkout_time), "", "", "Check-In", "CI", "Complete cleaning for next guests."],
            ["Check-in time:", str(checkin_time), "", "", "Stay-over", "SO", "Maintenance cleaning during guest stay."],
            ["Amenities Yes/No:", amenities, "", "", "Check-out/in", "CO/CI", "Same day checkout and checkin."],
            ["Laundry Services Yes/No:", laundry_service, "", "", "Fresh-up", "FU", "Light cleaning before next checkin."],
            ["Keys Yes/No:", keys_available, "", "", "Deep Cleaning", "DC", "Thorough cleaning of property."],
            ["Codes Yes/No:", codes_available, "", "", "Construction Cleaning", "COC", "Post-renovation cleaning."],
            ["", "", "", "", "", "", ""],
            ["Villas/Apartments:", "", "", "", "", "", ""],
            ["Villas/Apartments Name:", "Address", "Hours +/-", "SO +/-", "Keys & Codes:", "Comments:", ""],
        ])
        
        # Generate villa entries
        for i in range(num_villas):
            villa_name = f"Villa_{i+1:02d}"
            data.append([villa_name, "", "", "", "", "", ""])
        
        # Add spacing
        for _ in range(5):
            data.append(["", "", "", "", "", "", ""])
        
        # Amenities section
        data.extend([
            ["List of Amenities:", "", "", "", "", "", ""],
            ["Item", "Quantity", "Comments:", "", "", "", ""],
        ])
        
        # Add custom amenities
        if custom_amenities:
            for amenity in custom_amenities.split('\n'):
                if amenity.strip():
                    data.append([amenity.strip(), "", "", "", "", "", ""])
        
        st.session_state.generated_data = data
        st.success("✅ CSV template generated successfully!")
    
    if st.session_state.generated_data:
        st.markdown("### 📋 Preview Generated Data")
        df_preview = pd.DataFrame(st.session_state.generated_data[:20])  # Show first 20 rows
        st.dataframe(df_preview, use_container_width=True)
        
        # Download button
        filename = f"generated_template_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        st.markdown(download_csv(st.session_state.generated_data, filename), unsafe_allow_html=True)

elif page == "📤 Upload CSV":
    st.markdown('<div class="header-style"><h1>📤 Upload CSV File</h1></div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = df
            
            st.success("✅ File uploaded successfully!")
            
            # File information
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Rows", len(df))
            with col2:
                st.metric("📋 Columns", len(df.columns))
            with col3:
                st.metric("📁 File Size", f"{uploaded_file.size} bytes")
            with col4:
                st.metric("📝 File Name", uploaded_file.name)
            
            # Preview
            st.markdown("### 👀 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Column information
            st.markdown("### 📋 Column Information")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum()
            })
            st.dataframe(col_info, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("💡 Make sure your file is a valid CSV format.")

elif page == "📊 View Data":
    st.markdown('<div class="header-style"><h1>📊 Data Viewer</h1></div>', unsafe_allow_html=True)
    
    # Data source selection
    data_source = st.radio("Select data source:", ["📤 Uploaded Data", "📝 Generated Data"])
    
    if data_source == "📤 Uploaded Data" and st.session_state.uploaded_data is not None:
        df = st.session_state.uploaded_data
        st.markdown("### 📤 Uploaded CSV Data")
        
    elif data_source == "📝 Generated Data" and st.session_state.generated_data is not None:
        df = pd.DataFrame(st.session_state.generated_data)
        st.markdown("### 📝 Generated CSV Data")
        
    else:
        st.warning("⚠️ No data available. Please upload a CSV file or generate a template first.")
        st.stop()
    
    # Display options
    col1, col2 = st.columns(2)
    with col1:
        show_all = st.checkbox("Show all rows", value=False)
    with col2:
        if not show_all:
            num_rows = st.slider("Number of rows to display", 5, min(100, len(df)), 20)
    
    # Data display
    if show_all:
        st.dataframe(df, use_container_width=True)
    else:
        st.dataframe(df.head(num_rows), use_container_width=True)
    
    # Statistics (only for uploaded data with numeric columns)
    if data_source == "📤 Uploaded Data":
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            st.markdown("### 📈 Basic Statistics")
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)
    
    # Search functionality
    st.markdown("### 🔍 Search Data")
    search_term = st.text_input("Enter search term:")
    if search_term:
        # Search in all columns (convert to string first)
        mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        filtered_df = df[mask]
        st.markdown(f"**Found {len(filtered_df)} rows containing '{search_term}':**")
        st.dataframe(filtered_df, use_container_width=True)

elif page == "ℹ️ About":
    st.markdown('<div class="header-style"><h1>ℹ️ About CSV Manager</h1></div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Purpose
    This Streamlit application is designed to help you manage CSV files efficiently. It provides tools to:
    
    - **Generate** CSV templates based on the Kroon Beheer Client Profile format
    - **Upload** and analyze existing CSV files
    - **View** and explore data with interactive tables
    - **Search** through your data quickly
    
    ### 🛠️ Features
    
    #### 📝 CSV Generation
    - Customizable client information
    - Flexible villa/apartment listings
    - Configurable amenities and services
    - Professional template structure
    
    #### 📤 File Upload
    - Support for standard CSV files
    - Automatic data type detection
    - File size and structure analysis
    - Error handling for invalid files
    
    #### 📊 Data Visualization
    - Interactive data tables
    - Basic statistical analysis
    - Search and filter capabilities
    - Responsive design for all screen sizes
    
    ### 🎨 Design
    - Light blue color scheme for a professional look
    - Responsive layout that works on desktop and mobile
    - Intuitive navigation with sidebar menu
    - Clean and modern interface
    
    ### 🔧 Technical Details
    - Built with Streamlit
    - Uses Pandas for data manipulation
    - Responsive CSS styling
    - Session state management for data persistence
    """)
    
    st.markdown("---")
    st.markdown("**Created with ❤️ using Streamlit**")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "CSV Manager Application | Built with Streamlit 📊"
    "</div>", 
    unsafe_allow_html=True
)

