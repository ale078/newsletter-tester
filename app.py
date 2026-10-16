import streamlit as st
import pandas as pd
from database import get_connection, create_tables
from automator import run_test
import schedule
import time

create_tables()

st.set_page_config(page_title="Newsletter Tester", layout="wide")
st.title("📰 Newsletter Testing Automator")

menu = st.sidebar.selectbox("Menú", ["Crear Campaña", "Ver Campañas", "Reportes"])

if menu == "Crear Campaña":
    st.header("Crear nueva campaña de pruebas")
    
    with st.form("campaign_form"):
        name = st.text_input("Nombre de la campaña")
        col1, col2 = st.columns(2)
        
        with col1:
            opens_desktop = st.number_input("Opens Desktop", min_value=0, value=50)
            clicks_desktop = st.number_input("Clicks Desktop", min_value=0, value=20)
        
        with col2:
            opens_mobile = st.number_input("Opens Mobile", min_value=0, value=50)
            clicks_mobile = st.number_input("Clicks Mobile", min_value=0, value=20)
        
        daily = st.checkbox("Ejecutar diariamente", value=True)
        
        submitted = st.form_submit_button("Crear Campaña")
        
        if submitted:
            conn = get_connection()
            c = conn.cursor()
            c.execute("""
                INSERT INTO campaigns (name, opens_desktop, opens_mobile, clicks_desktop, clicks_mobile, daily)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, opens_desktop, opens_mobile, clicks_desktop, clicks_mobile, int(daily)))
            conn.commit()
            st.success("Campaña creada correctamente!")

elif menu == "Ver Campañas":
    st.header("Campañas activas")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM campaigns", conn)
    st.dataframe(df)

elif menu == "Reportes":
    st.header("Reportes de ejecuciones")
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM executions", conn)
    st.dataframe(df)