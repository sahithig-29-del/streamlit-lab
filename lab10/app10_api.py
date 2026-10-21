
import streamlit as st
import requests
import time

st.title("Weather API Demo")

API_KEY = "demo_key"

city = st.text_input("Enter city", "Chennai")

if st.button("Get Weather"):
    try:
        with st.spinner("Fetching weather..."):
            time.sleep(1)

            resp = {
                "city": city,
                "temperature": 30,
                "condition": "Sunny",
                "humidity": 65
            }

        st.subheader("Weather Details")
        st.json(resp)

        c1, c2, c3 = st.columns(3)

        c1.metric("Temperature", f"{resp['temperature']}°C")
        c2.metric("Condition", resp["condition"])
        c3.metric("Humidity", f"{resp['humidity']}%")

    except requests.exceptions.Timeout:
        st.error("Request timed out. Try again.")

    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP error: {e}")

    except Exception as e:
        st.error(f"Something went wrong: {e}")

st.divider()

st.subheader("HTTP Methods")

st.markdown("""
- **GET** - Retrieve data
- **POST** - Send data
- **PUT** - Update data
- **DELETE** - Delete data
""")
