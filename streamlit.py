import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="⚡ Energy Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .energy-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    
    .appliance-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .stSelectbox > div > div {
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'calc_energy' not in st.session_state:
    st.session_state.calc_energy = 0
if 'breakdown' not in st.session_state:
    st.session_state.breakdown = {}

# Header
st.markdown("""
<div class="main-header">
    <h1>⚡ Smart Energy Consumption Calculator</h1>
    <p>Calculate your home's energy usage with style!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for user information
st.sidebar.header("👤 User Information")
name = st.sidebar.text_input("Name", value="Khush", help="Enter your name")
age = st.sidebar.number_input("Age", min_value=1, max_value=100, value=19)
city = st.sidebar.selectbox("City", ["Ahmedabad", "Mumbai", "Delhi", "Bangalore", "Chennai", "Pune"])
area = st.sidebar.text_input("Area", value="South Bopal", help="Enter your area/locality")

# Main content in columns
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🏠 Property Details")
    
    # Property type selection with radio buttons
    property_type = st.radio(
        "Select Property Type:",
        ["🏢 Flat", "🏘️ Tenement"],
        horizontal=True,
        help="Choose your property type"
    )
    
    # BHK selection
    bhk_options = ["1 BHK", "2 BHK", "3 BHK"]
    bhk_choice = st.selectbox(
        "🛏️ Select Number of BHK:",
        bhk_options,
        help="Choose your home configuration"
    )
    
    # Convert selections to numbers for calculation
    bhk_num = int(bhk_choice.split()[0])
    
    # Base energy calculation
    if bhk_num == 1:
        base_energy = 2 * 0.4 + 2 * 0.8
    elif bhk_num == 2:
        base_energy = 3 * 0.4 + 3 * 0.8
    else:  # 3 BHK
        base_energy = 4 * 0.4 + 4 * 0.8
    
    st.session_state.calc_energy = base_energy
    st.session_state.breakdown = {"Base Consumption": base_energy}

with col2:
    st.header("⚡ Live Energy Meter")
    
    # Display current energy in a styled card
    st.markdown(f"""
    <div class="energy-card">
        <h2>{st.session_state.calc_energy:.2f} kWh</h2>
        <p>Current Energy Consumption</p>
    </div>
    """, unsafe_allow_html=True)

# Appliances section
st.header("🔌 Appliances Configuration")

# Create three columns for appliances
app_col1, app_col2, app_col3 = st.columns(3)

with app_col1:
    st.markdown('<div class="appliance-section">', unsafe_allow_html=True)
    st.subheader("❄️ Air Conditioner")
    has_ac = st.checkbox("Do you have AC?", key="ac")
    if has_ac:
        ac_count = st.number_input("Number of ACs", min_value=1, max_value=10, value=1, key="ac_count")
        ac_energy = 3 * ac_count
        st.session_state.breakdown["Air Conditioner"] = ac_energy
        st.session_state.calc_energy = base_energy + ac_energy + st.session_state.breakdown.get("Refrigerator", 0) + st.session_state.breakdown.get("Washing Machine", 0)
    else:
        st.session_state.breakdown.pop("Air Conditioner", None)
        st.session_state.calc_energy = base_energy + st.session_state.breakdown.get("Refrigerator", 0) + st.session_state.breakdown.get("Washing Machine", 0)
    
    st.info(f"Energy: {st.session_state.breakdown.get('Air Conditioner', 0):.1f} kWh")
    st.markdown('</div>', unsafe_allow_html=True)

with app_col2:
    st.markdown('<div class="appliance-section">', unsafe_allow_html=True)
    st.subheader("🧊 Refrigerator")
    has_fridge = st.checkbox("Do you have Fridge?", key="fridge")
    if has_fridge:
        fridge_count = st.number_input("Number of Fridges", min_value=1, max_value=5, value=1, key="fridge_count")
        fridge_energy = 4 * fridge_count
        st.session_state.breakdown["Refrigerator"] = fridge_energy
        st.session_state.calc_energy = base_energy + st.session_state.breakdown.get("Air Conditioner", 0) + fridge_energy + st.session_state.breakdown.get("Washing Machine", 0)
    else:
        st.session_state.breakdown.pop("Refrigerator", None)
        st.session_state.calc_energy = base_energy + st.session_state.breakdown.get("Air Conditioner", 0) + st.session_state.breakdown.get("Washing Machine", 0)
    
    st.info(f"Energy: {st.session_state.breakdown.get('Refrigerator', 0):.1f} kWh")
    st.markdown('</div>', unsafe_allow_html=True)

with app_col3:
    st.markdown('<div class="appliance-section">', unsafe_allow_html=True)
    st.subheader("🧺 Washing Machine")
    has_wm = st.checkbox("Do you have Washing Machine?", key="wm")
    if has_wm:
        wm_count = st.number_input("Number of Washing Machines", min_value=1, max_value=3, value=1, key="wm_count")
        wm_energy = 2 * wm_count
        st.session_state.breakdown["Washing Machine"] = wm_energy
        st.session_state.calc_energy = base_energy + st.session_state.breakdown.get("Air Conditioner", 0) + st.session_state.breakdown.get("Refrigerator", 0) + wm_energy
    else:
        st.session_state.breakdown.pop("Washing Machine", None)
        st.session_state.calc_energy = base_energy + st.session_state.breakdown.get("Air Conditioner", 0) + st.session_state.breakdown.get("Refrigerator", 0)
    
    st.info(f"Energy: {st.session_state.breakdown.get('Washing Machine', 0):.1f} kWh")
    st.markdown('</div>', unsafe_allow_html=True)

# Results section
st.header("📊 Energy Consumption Analysis")

# Create two columns for results
result_col1, result_col2 = st.columns([1, 1])

with result_col1:
    # Energy breakdown chart
    if st.session_state.breakdown:
        fig = px.pie(
            values=list(st.session_state.breakdown.values()),
            names=list(st.session_state.breakdown.keys()),
            title="Energy Consumption Breakdown",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

with result_col2:
    # Monthly cost estimation
    st.subheader("💰 Cost Estimation")
    
    # Assuming average rate per kWh in India
    rate_per_kwh = st.slider("Rate per kWh (₹)", min_value=3.0, max_value=10.0, value=5.5, step=0.5)
    
    daily_cost = st.session_state.calc_energy * rate_per_kwh
    monthly_cost = daily_cost * 30
    yearly_cost = daily_cost * 365
    
    st.metric("Daily Cost", f"₹{daily_cost:.2f}")
    st.metric("Monthly Cost", f"₹{monthly_cost:.2f}")
    st.metric("Yearly Cost", f"₹{yearly_cost:.2f}")

# Energy efficiency tips
st.header("💡 Energy Efficiency Tips")

tips_col1, tips_col2 = st.columns(2)

with tips_col1:
    st.info("""
    **💡 Smart Tips:**
    - Use LED bulbs instead of traditional ones
    - Set AC temperature to 24°C for optimal efficiency
    - Regular maintenance of appliances
    - Use natural light during daytime
    """)

with tips_col2:
    st.success("""
    **🌱 Eco-Friendly:**
    - Unplug devices when not in use
    - Use energy-efficient appliances
    - Consider solar panels for roof-top installation
    - Use timers for water heaters
    """)

# Summary card
st.markdown(f"""
<div class="energy-card">
    <h3>📋 Energy Summary for {name}</h3>
    <p><strong>Property:</strong> {property_type.replace('🏢 ', '').replace('🏘️ ', '')} - {bhk_choice}</p>
    <p><strong>Location:</strong> {area}, {city}</p>
    <p><strong>Total Energy Consumption:</strong> {st.session_state.calc_energy:.2f} kWh per day</p>
    <p><strong>Estimated Monthly Bill:</strong> ₹{daily_cost * 30:.2f}</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #666;'>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>", unsafe_allow_html=True)