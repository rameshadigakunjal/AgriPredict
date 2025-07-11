
import streamlit as st
import joblib
import numpy as np

# Load Random Forest model and encoder for combined dataset
rf_model = joblib.load("app/models/rf_combined_model.pkl")
district_encoder = joblib.load("preprocessing/district_encoder_combined.pkl")


st.set_page_config(page_title="Rice Yield Predictor (Random Forest)", layout="centered")
st.title("🌾 Rice Yield Prediction System (Random Forest)")

st.sidebar.title("Prediction Options")
option = st.sidebar.radio("Select a prediction type", [
    "Predict Rice Yield"
])

if option == "Predict Rice Yield":
    st.header("🔹 Predict Rice Yield (Auto NPK & pH)")
    district = st.text_input("District Name", "Durg")
    year = st.number_input("Year", 1978, 2050, step=1, value=2012)
    dist_code = st.number_input("District Code", 1, 1000, value=107)
    state_code = st.number_input("State Code", 1, 50, value=14)
    area = st.number_input("RICE AREA (1000 ha)", 0.1, 10000.0, value=807.07)
    production = st.number_input("RICE PRODUCTION (1000 tons)", 0.0, 10000.0, value=1534.22)
    temperature = st.number_input("Temperature (°C)", 10.0, 45.0, value=25.0)
    humidity = st.number_input("Humidity (%)", 20.0, 100.0, value=80.0)
    rainfall = st.number_input("Rainfall (mm)", 0.0, 500.0, value=250.0)

    # Load NPK and pH prediction models
    rf_n = joblib.load("app/models/rf_n.pkl")
    rf_p = joblib.load("app/models/rf_p.pkl")
    rf_k = joblib.load("app/models/rf_k.pkl")
    rf_ph = joblib.load("app/models/rf_ph.pkl")

    if st.button("Predict Yield"):
        try:
            district_encoded = district_encoder.transform([district])[0]
            npk_input = np.array([[district_encoded, year, dist_code, state_code, area, production, temperature, humidity, rainfall]])
            N = rf_n.predict(npk_input)[0]
            P = rf_p.predict(npk_input)[0]
            K = rf_k.predict(npk_input)[0]
            ph = rf_ph.predict(npk_input)[0]
            # Features for rice yield prediction
            input_arr = np.array([[N, P, K, temperature, humidity, ph, rainfall,
                                  district_encoded, year, dist_code, state_code, area, production]])
            result = rf_model.predict(input_arr)[0]
            st.success(f"Predicted Rice Yield: {result:.2f} Kg/ha")
            st.info(f"Predicted NPK & pH values used:\nN: {N:.2f} | P: {P:.2f} | K: {K:.2f} | pH: {ph:.2f}")
        except Exception as e:
            st.error(f"Error: {e}")

## ...existing code...
## Removed old options and models. Only Random Forest prediction is available now.



# import streamlit as st
# import joblib
# import numpy as np

# # Load models
# mlr_p1 = joblib.load("app/models/mlr_p1.pkl")
# svm_n = joblib.load("app/models/svm_n.pkl")
# svm_p = joblib.load("app/models/svm_p.pkl")
# svm_k = joblib.load("app/models/svm_k.pkl")
# final_model = joblib.load("app/models/final_model.pkl")
# improved_model = joblib.load("app/models/improved_yield_model.pkl")
# encoder = joblib.load("preprocessing/encoders.pkl")

# st.set_page_config(page_title="Rice Yield & NPK Predictor", layout="centered")
# st.title("🌾 Integrated Prediction System for Rice Yield and Nutrients")

# st.sidebar.title("Prediction Options")
# option = st.sidebar.radio("Select a prediction type", [
#     "1️⃣ Predict Yield (P1)",
#     "2️⃣ Predict NPK (P2)",
#     "3️⃣ Final Yield (P3)",
#     "4️⃣ Improved Yield (Auto NPK)"
# ])

# # Option 1: Predict Yield using Production, Area, District, Year
# if option == "1️⃣ Predict Yield (P1)":
#     st.header("🔹 Predict Rice Yield (P1)")
#     district = st.text_input("District Name", "Tumkur")
#     year = st.number_input("Year", 1978, 2050, step=1)
#     production = st.number_input("Production (1000 tons)", 0.0, 10000.0)
#     area = st.number_input("Area (1000 ha)", 0.1, 10000.0)

#     if st.button("Predict Yield"):
#         try:
#             district_encoded = encoder.transform([district])[0]
#             input_arr = np.array([[district_encoded, year, production, area]])
#             result = mlr_p1.predict(input_arr)[0]
#             st.success(f"Predicted Rice Yield: {result:.2f} Kg/ha")
#         except Exception as e:
#             st.error(f"Error: {e}")

# # Option 2: Predict NPK from climate data
# elif option == "2️⃣ Predict NPK (P2)":
#     st.header("🔹 Predict Soil Nutrients (P2)")
#     rainfall = st.slider("Rainfall (mm)", 0.0, 500.0, 200.0)
#     temp = st.slider("Temperature (°C)", 10.0, 45.0, 28.0)
#     hum = st.slider("Humidity (%)", 20.0, 100.0, 70.0)

#     if st.button("Predict NPK"):
#         x_input = np.array([[rainfall, temp, hum]])
#         n = svm_n.predict(x_input)[0]
#         p = svm_p.predict(x_input)[0]
#         k = svm_k.predict(x_input)[0]
#         st.success(f"Predicted NPK Values:\n\n🌿 N: {n:.2f}   🌱 P: {p:.2f}   🌾 K: {k:.2f}")

# # Option 3: Final model using P1 + P2
# elif option == "3️⃣ Final Yield (P3)":
#     st.header("🔹 Final Rice Yield Prediction (P3)")

#     district = st.text_input("District", "Tumkur")
#     year = st.number_input("Year", 2000, 2050, step=1)
#     production = st.number_input("Production (1000 tons)", 0.0, 10000.0)
#     area = st.number_input("Area (1000 ha)", 0.1, 10000.0)
#     rainfall = st.slider("Rainfall (mm)", 0.0, 500.0, 200.0)
#     temp = st.slider("Temperature (°C)", 10.0, 45.0, 28.0)
#     hum = st.slider("Humidity (%)", 20.0, 100.0, 70.0)

#     if st.button("Predict Final Yield"):
#         try:
#             x_input = np.array([[rainfall, temp, hum]])
#             n = svm_n.predict(x_input)[0]
#             p = svm_p.predict(x_input)[0]
#             k = svm_k.predict(x_input)[0]
#             district_encoded = encoder.transform([district])[0]
#             input_arr = np.array([[district_encoded, year, production, area, n, p, k, rainfall, temp, hum]])
#             result = final_model.predict(input_arr)[0]
#             st.success(f"📈 Final Predicted Rice Yield: {result:.2f} Kg/ha")
#         except Exception as e:
#             st.error(f"Error: {e}")

# # Option 4: Improved Model with Auto NPK
# elif option == "4️⃣ Improved Yield (Auto NPK)":
#     st.header("🔹 Improved Rice Yield Prediction (Auto NPK)")

#     district = st.text_input("District", "Durg")
#     year = st.number_input("Year", 1978, 2050, step=1, value=2012)
#     production = st.number_input("Production (1000 tons)", 0.0, 10000.0, value=1534.22)
#     area = st.number_input("Area (1000 ha)", 0.1, 10000.0, value=807.07)

#     rainfall = st.slider("Rainfall (mm)", 0.0, 500.0, 250.0)
#     temp = st.slider("Temperature (°C)", 10.0, 45.0, 28.0)
#     hum = st.slider("Humidity (%)", 20.0, 100.0, 70.0)

#     if st.button("Predict Improved Yield"):
#         try:
#             # Predict NPK using climate
#             x_climate = np.array([[rainfall, temp, hum]])
#             n = svm_n.predict(x_climate)[0]
#             p = svm_p.predict(x_climate)[0]
#             k = svm_k.predict(x_climate)[0]

#             district_encoded = encoder.transform([district])[0]
#             prod_per_area = production / area

#             input_arr = np.array([[district_encoded, year, production, area,
#                                    rainfall, temp, hum, n, p, k, prod_per_area]])

#             result = improved_model.predict(input_arr)[0]

#             st.success(f"🌟 Improved Predicted Rice Yield: {result:.2f} Kg/ha")
#             st.info(f"🔒 Auto-predicted NPK values used:\nN: {n:.2f} | P: {p:.2f} | K: {k:.2f}")

#         except Exception as e:
#             st.error(f"Error: {e}")



