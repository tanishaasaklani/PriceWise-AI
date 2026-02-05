import streamlit as st
import pickle
import numpy as np

# Page configuration
st.set_page_config(
    page_title="PriceWise AI | Smart Optimizer",
    layout="wide"
)

# Custom CSS for premium look
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
div.stButton > button:first-child {
    background-color: #00ffbd;
    color: black;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #00d49e;
    color: black;
    box-shadow: 0 0 15px #00ffbd;
}
.result-card {
    background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
    padding: 30px;
    border-radius: 15px;
    border-left: 5px solid #00ffbd;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Load Model
try:
    model = pickle.load(open('pricewise_model.pkl', 'rb'))
except:
    st.error("Model file not found. Please ensure 'pricewise_model.pkl' exists.")
    model = None

# Sidebar Inputs
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    st.title("Input Settings")
    st.markdown("---")

    st.subheader("Product Details")

    quantity = st.number_input("Quantity Sold", min_value=1, value=10)

    unitprice = st.number_input("Unit Price ($)", min_value=0.1, value=5.0)

    price_cat_map = {"Economy": 1, "Mid-Range": 2, "Premium": 3, "Luxury": 4}
    price_cat_label = st.selectbox("Product Category", list(price_cat_map.keys()))
    pricecat = price_cat_map[price_cat_label]

    st.markdown("---")

    st.subheader("Market Demand")

    demand_map = {"Low": 1, "Moderate": 2, "High": 3, "Very High": 4}
    demand_label = st.select_slider(
        "Demand Level",
        options=list(demand_map.keys()),
        value="Moderate"
    )
    demand = demand_map[demand_label]

# Main Page
st.title("PriceWise AI – Smart Discount Optimizer")
st.caption("AI Powered Retail Pricing Decision Support System")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Timing Information")

    month = st.slider("Month", 1, 12, 6)
    day = st.slider("Day of Month", 1, 31, 15)
    hour = st.slider("Selling Hour (24h)", 0, 23, 12)

with col2:
    st.subheader("Context")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"]

    day_name = st.selectbox("Day of Week", days)
    dayofweek = days.index(day_name)

    totalprice = quantity * unitprice

    st.metric("Estimated Base Revenue", f"${totalprice:,.2f}")

with col3:
    st.subheader("AI Strategy")

    st.info(
        "The model analyzes sales trends, demand patterns, "
        "and seasonality to recommend the best discount."
    )

    predict_btn = st.button("Generate Discount Strategy")

st.markdown("---")

with st.expander("What do these inputs mean?"):
    st.write("""
    - Quantity Sold: Expected number of units to be sold  
    - Unit Price: Original price before any discount  
    - Product Category: Pricing segment of product  
    - Demand Level: Current market interest  
    - Timing Inputs: Help model understand seasonality  
    """)

# Prediction Logic
if predict_btn:
    if unitprice <= 0:
        st.warning("Unit price must be greater than 0")
    else:
        if model:
            input_data = np.array([[
                quantity,
                unitprice,
                totalprice,
                month,
                day,
                hour,
                dayofweek,
                demand,
                pricecat
            ]])

            result = model.predict(input_data)[0]
            discount = result
            discounted_price = unitprice * (1 - discount/100)
            revenue_after_discount = discounted_price * quantity
            base_revenue = totalprice
            difference = revenue_after_discount - base_revenue
            st.markdown(f"""
                        <div class="result-card">
                        <p style="color: #aaa; font-size:18px;">
                        Recommended Discount Strategy
                        </p>
                        <h1 style="color:#00ffbd; font-size:60px;">
                        {discount:.2f} %
                        </h1>
                        </div>
                        """, unsafe_allow_html=True)
            # Show revenue analytics
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Base Revenue", f"${base_revenue:,.2f}")
            with c2:
                st.metric("Revenue After Discount", f"${revenue_after_discount:,.2f}")
            with c3:
                st.metric("Change in Revenue", f"${difference:,.2f}")
            
            
            if difference > 0:
                st.success("This discount strategy increases total revenue.")
            else:
                st.warning("This discount may reduce revenue but could increase sales volume.")
