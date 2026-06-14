import pickle
import streamlit as st
import pandas as pd 
model = pickle.load(open("churn_model.pkl",'rb'))

st.markdown("""
<style>
            .stApp {
            background-color:#FFEE99;
            }
            </style>
            """,unsafe_allow_html= True)

st.markdown("---")
st.markdown("<h1 style ='text-align : center;'>Customer Churn Prediction </h1>",unsafe_allow_html=True)
st.markdown("---")
st.markdown("## Enter customer details")
tenure = int(st.number_input("Tenure (months)",step= 1))
monthly_charges = st.number_input("Monthly Charges")
contract = st.selectbox("Contract",("Month-to-month","One year","Two year"))
internet_service = st.selectbox("Internet Service",("DSL","Fiber optic","No internet"))
tech_support = st.selectbox("Tech Support",("Yes","No"))
if st.button("Predict Churn"):
    input_data = {
    "SeniorCitizen": 0,
    "tenure": tenure,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": tenure * monthly_charges,

    "gender_Male": 0,
    "Partner_Yes": 0,
    "Dependents_Yes": 0,
    "PhoneService_Yes": 1,

    "MultipleLines_No phone service": 0,
    "MultipleLines_Yes": 0,

    "InternetService_Fiber optic": 0,
    "InternetService_No": 0,

    "OnlineSecurity_No internet service": 0,
    "OnlineSecurity_Yes": 0,

    "OnlineBackup_No internet service": 0,
    "OnlineBackup_Yes": 0,

    "DeviceProtection_No internet service": 0,
    "DeviceProtection_Yes": 0,

    "TechSupport_No internet service": 0,
    "TechSupport_Yes": 0,

    "StreamingTV_No internet service": 0,
    "StreamingTV_Yes": 0,

    "StreamingMovies_No internet service": 0,
    "StreamingMovies_Yes": 0,

    "Contract_One year": 0,
    "Contract_Two year": 0,

    "PaperlessBilling_Yes": 0,

    "PaymentMethod_Credit card (automatic)": 0,
    "PaymentMethod_Electronic check": 0,
    "PaymentMethod_Mailed check": 0
    }
    
    if contract == "One year":
        input_data["Contract_One year"] = 1
    elif contract == "Two year":
        input_data["Contract_Two year"] = 1

    if internet_service == "Fiber optic":
        input_data["InternetService_Fiber optic"] = 1
    elif internet_service == "No internet":
        input_data["InternetService_No"] = 1

        input_data["OnlineSecurity_No internet service"] = 1
        input_data["OnlineBackup_No internet service"] = 1
        input_data["DeviceProtection_No internet service"] = 1
        input_data["TechSupport_No internet service"] = 1
        input_data["StreamingTV_No internet service"] = 1
        input_data["StreamingMovies_No internet service"] = 1

        input_data["OnlineSecurity_Yes"] = 0
        input_data["OnlineBackup_Yes"] = 0
        input_data["DeviceProtection_Yes"] = 0
        input_data["TechSupport_Yes"] = 0
        input_data["StreamingTV_Yes"] = 0
        input_data["StreamingMovies_Yes"] = 0

    if tech_support == "Yes":
        input_data["TechSupport_Yes"] = 1

    data = pd.DataFrame([input_data])

    predict = model.predict (data)
    st.markdown("---")
    st.markdown("### Prediction: ")
    if predict[0] == 1:
         st.error("Customer is likely to churn")

         prob = model.predict_proba(data)[0][1]
         st.progress (int(prob *100))
         st.warning(f"Churn Risk: {round(prob*100,2)} %")

         st.markdown("---")
         st.markdown("### Reasons: ")
        
         reasons = []

         if tenure < 12:
             reasons.append("Customer is very new (low tenure)")

         if monthly_charges > 80:
                reasons.append("High monthly charges may cause dissatisfaction")

         if contract == "Month-to-month":
                reasons.append("No long-term contract (unstable customer)")

         if internet_service == "Fiber optic":
                reasons.append("Fiber optic users show higher churn tendency")

         if internet_service == "No internet":
                reasons.append("Customer does not use internet service")

         if tech_support == "No":
                reasons.append("No technical support available")

         reasons.append("Customer profile matches churn pattern from past data")
         
         for r in reasons:
              st.write("•", r)



         st.markdown("---")
         st.markdown("### Suggestion: ")
         suggestions = []

         if tenure < 12:
                suggestions.append("Improve onboarding experience for new customers")

         if monthly_charges > 80:
                suggestions.append("Offer discount or cheaper plan options")

         if contract == "Month-to-month":
                suggestions.append("Encourage switching to yearly contract with benefits")

         if tech_support == "No":
                suggestions.append("Promote technical support add-on")

         if internet_service == "No internet":
                suggestions.append("Offer internet bundle (DSL/Fiber) to increase engagement")

         suggestions.append("Provide loyalty rewards or retention offers")
         
         for s in suggestions:
              st.write("•", s)
    
    else:
        st.success("Customer is likely to stay")
        st.markdown("---")
        st.markdown("### Reasons: ")
        reasons_stay = []

        if tenure > 24:
            reasons_stay.append("Long-term customer (high loyalty)")

        if monthly_charges < 60:
            reasons_stay.append("Affordable monthly charges")

        if contract in ["One year", "Two year"]:
            reasons_stay.append("Long-term contract ensures stability")

        if tech_support == "Yes":
            reasons_stay.append("Has technical support access")

        reasons_stay.append("Customer shows strong retention behavior")

        for rr in reasons_stay:
             st.write("•", rr)

        st.markdown("---")
        st.markdown("### Suggestion: ")
        suggestions_stay = []

        suggestions_stay.append("Maintain good service quality")

        if contract == "Month-to-month":
            suggestions_stay.append("Still encourage yearly plan upgrade")

        if monthly_charges > 70:
            suggestions_stay.append("Consider offering loyalty discounts")

        suggestions_stay.append("Engage customer with reward programs")

        for ss in suggestions_stay:
             st.write("•", ss)

            


    



