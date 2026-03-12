import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

# ---------- USER DATABASE ----------
USER_DB = "users.csv"

def load_users():
    try:
        return pd.read_csv(USER_DB)
    except:
        return pd.DataFrame(columns=["username","password"])

def save_user(username,password):
    df = load_users()
    new_user = pd.DataFrame([[username,password]],columns=["username","password"])
    df = pd.concat([df,new_user],ignore_index=True)
    df.to_csv(USER_DB,index=False)

def login(username,password):
    df = load_users()
    user = df[(df["username"]==username) & (df["password"]==password)]
    return not user.empty


menu = ["Login","Register"]
choice = st.sidebar.selectbox("Menu",menu)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# LOGIN PAGE
if choice == "Login":

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password",type="password")

    if st.button("Login"):
        if login(username,password):
            st.success("Login Successful")
            st.session_state.logged_in = True
        else:
            st.error("Invalid Username or Password")

# REGISTER PAGE
elif choice == "Register":

    st.title("📝 Register")

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password",type="password")

    if st.button("Register"):
        save_user(new_user,new_pass)
        st.success("Account Created Successfully")



st.set_page_config(page_title="AI Car Advisor",page_icon="🚗",layout="wide")

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🚗 AI Car Advisor</div>',unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart Car Price Prediction & Recommendation System</div>',unsafe_allow_html=True)

# Load data
data = pd.read_csv("car_price_dataset.csv")
data = data.drop(["Car ID","Model"],axis=1)

encoded = pd.get_dummies(data,drop_first=True)

X = encoded.drop("Price",axis=1)
y = encoded["Price"]

model = RandomForestRegressor()
model.fit(X,y)

# Sidebar
st.sidebar.header("🚗 Enter Car Details")

year = st.sidebar.number_input("Year",2000,2025)
engine = st.sidebar.number_input("Engine Size")
mileage = st.sidebar.number_input("Mileage")

brand = st.sidebar.selectbox("Brand",
["Toyota","BMW","Honda","Hyundai","Ford"])

fuel = st.sidebar.selectbox("Fuel Type",
["Petrol","Diesel","Electric"])

transmission = st.sidebar.selectbox("Transmission",
["Manual","Automatic"])

# Prediction Card
st.markdown('<div class="card">',unsafe_allow_html=True)

if st.button("Predict Price"):

    input_df = pd.DataFrame(columns=X.columns)
    input_df.loc[0] = 0

    if "Year" in input_df.columns:
        input_df["Year"] = year
    if "Engine Size" in input_df.columns:
        input_df["Engine Size"] = engine
    if "Mileage" in input_df.columns:
        input_df["Mileage"] = mileage

    brand_col = "Brand_" + brand
    fuel_col = "Fuel_" + fuel
    trans_col = "Transmission_" + transmission

    if brand_col in input_df.columns:
        input_df[brand_col] = 1

    if fuel_col in input_df.columns:
        input_df[fuel_col] = 1

    if trans_col in input_df.columns:
        input_df[trans_col] = 1

    prediction = model.predict(input_df)

    st.success(f"💰 Estimated Price: ${prediction[0]:,.2f}")

st.markdown('</div>',unsafe_allow_html=True)

# AI Advisor
st.header("🤖 AI Car Advisor")

budget = st.number_input("Enter Your Budget ($)",1000,200000)

if st.button("Recommend Cars"):

    result = data[data["Price"] <= budget]

    if len(result)>0:

        top = result.sort_values("Price",ascending=False).head(5)

        st.dataframe(top)

    else:
        st.warning("No cars found in this budget")

# Chart
st.header("📊 Car Market Insights")

fig = px.histogram(data,x="Price",title="Car Price Distribution")
st.plotly_chart(fig,use_container_width=True)

if st.session_state.logged_in:

    st.title("🚗 Car Price Prediction System")

    # PUT YOUR EXISTING CAR PRICE CODE HERE

else:
    st.warning("Please login to access the application")