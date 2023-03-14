"""This is the frontend of the app."""


import requests
import pandas as pd
import streamlit as st


st.title("Classificador de sentimentos para seguradoras de saúde")
st.write(
    """
    É muito comum que as seguradoras de saúde possuam aplicativos mobile para que
    seus clientes possam fazer reclamações, sugestões e elogios. Com isso, é possível
    obter uma visão geral de como os clientes estão satisfeitos com os serviços
    prestados pela empresa em seus apps. No entanto, é necessário que esses dados
    sejam coletados e analisados de forma automatizada das lojas de aplicativos em 
    seguida para que a empresa possa tomar decisões estratégicas com base nos feedbacks
    dos clientes, além de poder comparar como estão diante de seus concorrentes.
    """
)


input_text = st.text_area("Enter your text here")


if st.button("Predict"):
    data = {"review": input_text}

    response = requests.post("http://127.0.0.1:8000/predict", json=data)

    prediction = response.json()["prediction"]
    probability = response.json()["probability"]

    prob_df = pd.DataFrame(
        {"class": ["Negativo", "Positivo"], "probability": probability}
    ).round(2)

    if prediction == 0:
        st.write("Review negativo")
    else:
        st.write("Review positivo")

    st.bar_chart(prob_df, x="class", y="probability")
