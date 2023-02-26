import streamlit as st
import app

st.title("Numadic Api Assignment")
st.subheader ("Enter details below")

with st.form("form", clear_on_submit=True):
    startdate = st.text_input ("Enter the Start Date")
    enddate = st.text_input("Enter the End Date")
    submit = st.form_submit_button ("Submit")

    if submit:
        if type(app.report(startdate,enddate)) == type('sus'):
            st.write(app.report(startdate,enddate))
        else:
            st.dataframe(app.report(startdate,enddate))


