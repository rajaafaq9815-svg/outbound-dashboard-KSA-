import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Warehouse Performance Dashboard",
    page_icon="📦",
    layout="wide"
)

# Custom Styling (Dark Mode Theme matching warehouse aesthetic)
st.markdown("""
    <style>
    .main {
        background-color: #0b1020;
    }
    .stApp {
        background: radial-gradient(ellipse at top left, #172b49 0%, #0b1020 55%, #090d18 100%);
        color: #f4f7ff;
    }
    .kpi-card {
        background: linear-gradient(145deg, rgba(35,51,79,0.82), rgba(19,29,49,0.82));
        border: 1px solid #2a3b5a;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.035);
    }
    .kpi-title {
        font-size: 13px;
        color: #aab8d0;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initial Default Data from your table
DEFAULT_DATA = [
    ["MZWKSA007","HAKIMUL",13,105,10,18,79,144,0,0],
    ["MZWKSA007","MAHAFUZ",7,354,4,8,148,255,0,0],
    ["MZWKSA007","MAMON",10,191,8,31,184,317,0,0],
    ["MZWKSA007","ROMAN",9,191,2,14,179,295,0,0],
    ["MZWKSA007","SAMI",13,360,21,49,141,246,0,0],
    ["MZWKSA007","SOFLUK",6,84,0,0,134,181,0,0],
    ["MZWKSA009","ARSLAN",13,251,21,52,66,122,14,27],
    ["MZWKSA009","NIJAM",1,1,0,0,0,0,0,0],
    ["MZWKSA009","SAHIN",3,18,2,14,52,97,151,510],
    ["MZWKSA011","SHAFIQ",4,122,7,15,30,40,0,0],
    ["MZWKSA012","JAKIR",0,0,0,0,16,20,0,0],
    ["MZWKSA013","JUBAYER1",1,22,0,0,1,3,0,0],
    ["MZWKSA013","MAHAFUZ",2,89,0,0,0,0,0,0],
    ["MZWKSA013","SHAHADAT.1",11,138,14,36,67,99,0,0],
    ["MZWKSA014","SHISHIR",5,9,6,15,28,40,86,184],
    ["MZWKSA015","AKRAM",12,46,5,9,1,1,0,0],
    ["MZWKSA015","AZIZUR",7,14,0,0,0,0,0,0],
    ["MZWKSA018","SUMON",0,0,27,65,8,8,0,0],
    ["MZWKSA002","AYON",0,0,0,0,0,0,2,3],
    ["MZWKSA002","ARMAN",0,0,0,0,26,72,37,86],
    ["MZWKSA002","JUBAYER",0,0,0,0,21,28,120,289],
    ["MZWKSA002","MEHEDI",1,6,0,0,9,9,235,584],
    ["MZWKSA002","BALLAL",0,0,0,0,10,16,209,637]
]

COLUMNS = [
    "User ID", "Staff Name", "Zone Pick Orders", "Zone Pick Items",
    "Normal Pick Orders", "Normal Pick Items", "Sorter Orders", "Sorter Items",
    "Packing Orders", "Packing Items"
]

# Header Section
st.markdown("<p style='color:#aab1c1; font-size:12px; letter-spacing:1px; margin-bottom:2px;'>DAILY OPERATIONS · WAREHOUSE (OUTBOUND) SHIFT PERFORMANCE</p>", unsafe_allow_html=True)
st.title("Performance Dashboard")

# File Upload Section
st.subheader(" Upload Daily Data")
uploaded_file = st.file_uploader("Upload CSV or Excel file to update dashboard", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
else:
    df = pd.DataFrame(DEFAULT_DATA, columns=COLUMNS)

# Ensure numeric columns are properly formatted
numeric_cols = ["Zone Pick Orders", "Zone Pick Items", "Normal Pick Orders", "Normal Pick Items", 
                "Sorter Orders", "Sorter Items", "Packing Orders", "Packing Items"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Calculate totals
df["Picking Items"] = df["Zone Pick Items"] + df["Normal Pick Items"]
df["Sorting Items"] = df["Sorter Items"]
df["Packing Items"] = df["Packing Items"]
df["Total Items"] = df["Picking Items"] + df["Sorting Items"] + df["Packing Items"]

total_picking = int(df["Picking Items"].sum())
total_sorting = int(df["Sorting Items"].sum())
total_packing = int(df["Packing Items"].sum())
total_items = int(df["Total Items"].sum())
total_staff = len(df)

# KPI Cards
st.write("---")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Items Processed</div><div class="kpi-value" style="color:#ffffff;">{total_items:,}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Staff Records</div><div class="kpi-value" style="color:#54d68a;">{total_staff}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Picking Items</div><div class="kpi-value" style="color:#35d7d0;">{total_picking:,}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Sorting Items</div><div class="kpi-value" style="color:#c6f36b;">{total_sorting:,}</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">Packing Items</div><div class="kpi-value" style="color:#ffad66;">{total_packing:,}</div></div>', unsafe_allow_html=True)

st.write("---")

# Visualizations Section
left_col, right_col = st.columns([1.7, 1])

with left_col:
    st.subheader("Staff Performance — Total Items per Staff")
    st.bar_chart(df.set_index("Staff Name")["Total Items"])

with right_col:
    st.subheader("Task Volume Share")
    task_df = pd.DataFrame({
        "Task": ["Picking", "Sorting", "Packing"],
        "Items": [total_picking, total_sorting, total_packing]
    })
    st.dataframe(task_df, hide_index=True, use_container_width=True)

# Staff Detail Table
st.subheader("Staff Detail Breakdown")
st.dataframe(df, use_container_width=True)
