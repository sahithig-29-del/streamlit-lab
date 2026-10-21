
import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

st.title("Iris Flower Prediction")

model = joblib.load("model.pkl")

iris = load_iris()
X, y = iris.data, iris.target

logistic_model = LogisticRegression(max_iter=200)
logistic_model.fit(X, y)

classes = ["Setosa", "Versicolor", "Virginica"]

if "history" not in st.session_state:
    st.session_state.history = []

with st.form("prediction_form"):
    sl = st.slider("Sepal Length", 4.0, 8.0, 5.1)
    sw = st.slider("Sepal Width", 2.0, 4.5, 3.5)
    pl = st.slider("Petal Length", 1.0, 7.0, 1.4)
    pw = st.slider("Petal Width", 0.1, 2.5, 0.2)

    submit = st.form_submit_button("Predict")

if submit:
    features = np.array([[sl, sw, pl, pw]])

    pred = model.predict(features)[0]
    proba = model.predict_proba(features)[0]

    st.success(f"Prediction: **{classes[pred]}**")
    st.metric("Random Forest Confidence", f"{max(proba)*100:.1f}%")

    st.subheader("Exercise 1: Class Probabilities")

    proba_df = pd.DataFrame({
        "Class": classes,
        "Probability": proba
    })

    st.bar_chart(proba_df.set_index("Class"))

    logistic_pred = logistic_model.predict(features)[0]
    logistic_proba = logistic_model.predict_proba(features)[0]

    st.subheader("Exercise 3: Model Comparison")

    comparison = pd.DataFrame({
        "Model": ["Random Forest", "Logistic Regression"],
        "Predicted Class": [
            classes[pred],
            classes[logistic_pred]
        ],
        "Confidence (%)": [
            round(max(proba) * 100, 1),
            round(max(logistic_proba) * 100, 1)
        ]
    })

    st.dataframe(comparison, use_container_width=True)

    st.session_state.history.append({
        "Sepal Length": sl,
        "Sepal Width": sw,
        "Petal Length": pl,
        "Petal Width": pw,
        "Random Forest Prediction": classes[pred],
        "Confidence (%)": round(max(proba) * 100, 1)
    })

st.subheader("Exercise 2: Prediction History")

if st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)
else:
    st.write("No predictions made yet.")
