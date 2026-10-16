import streamlit as st
import pandas as pd
import json
from database import get_connection, create_tables, save_execution
from automator import run_test

# Inicializar base de datos
create_tables()

st.set_page_config(
    page_title="Newsletter Tester Automator",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Newsletter Testing Automator")
st.caption("Herramienta de simulación de aperturas (Opens) y clics de artículos en entornos Desktop y Mobile.")

menu = st.sidebar.radio("Navegación", ["Crear Campaña", "Campañas y Ejecución", "Reportes y Resultados"])

# ========================================================
# 1. CREAR CAMPAÑA
# ========================================================
if menu == "Crear Campaña":
    st.subheader("➕ Crear nueva campaña de pruebas")
    
    with st.form("campaign_form", clear_on_submit=True):
        name = st.text_input("Nombre de la Campaña", placeholder="Ej: Newsletter Tech Semanal #42")
        newsletter_url = st.text_input("URL del Newsletter (Versión web / Tracking Link)", placeholder="https://mi-newsletter.com/p/...")
        
        st.write("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💻 Desktop Web")
            opens_desktop = st.number_input("Opens Desktop planeados", min_value=0, max_value=500, value=10, step=1)
            clicks_desktop = st.number_input("Clicks Desktop planeados", min_value=0, max_value=500, value=5, step=1)
            
        with col2:
            st.markdown("#### 📱 Mobile Web (iPhone)")
            opens_mobile = st.number_input("Opens Mobile planeados", min_value=0, max_value=500, value=10, step=1)
            clicks_mobile = st.number_input("Clicks Mobile planeados", min_value=0, max_value=500, value=5, step=1)
            
        st.write("---")
        daily = st.checkbox("Programar ejecución diaria automática", value=True)
        
        submitted = st.form_submit_button("💾 Guardar Campaña", use_container_width=True)
        
        if submitted:
            if not name.strip() or not newsletter_url.strip():
                st.error("Por favor completa tanto el nombre como la URL del newsletter.")
            else:
                conn = get_connection()
                c = conn.cursor()
                c.execute("""
                    INSERT INTO campaigns (name, newsletter_url, opens_desktop, opens_mobile, clicks_desktop, clicks_mobile, daily)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (name.strip(), newsletter_url.strip(), opens_desktop, opens_mobile, clicks_desktop, clicks_mobile, int(daily)))
                conn.commit()
                conn.close()
                st.success(f"¡Campaña '{name}' creada con éxito!")

# ========================================================
# 2. CAMPAÑAS Y EJECUCIÓN MANUAL
# ========================================================
elif menu == "Campañas y Ejecución":
    st.subheader("📋 Campañas Registradas")
    
    conn = get_connection()
    df_campaigns = pd.read_sql("SELECT * FROM campaigns ORDER BY id DESC", conn)
    conn.close()
    
    if df_campaigns.empty:
        st.info("No hay campañas creadas aún. Dirígete a la sección 'Crear Campaña'.")
    else:
        st.dataframe(df_campaigns, use_container_width=True)
        
        st.write("---")
        st.markdown("### 🚀 Ejecución Inmediata de Campaña")
        
        campaign_options = {f"#{row['id']} - {row['name']}": row['id'] for _, row in df_campaigns.iterrows()}
        selected_label = st.selectbox("Selecciona la campaña a ejecutar:", list(campaign_options.keys()))
        selected_id = campaign_options[selected_label]
        
        selected_campaign = df_campaigns[df_campaigns['id'] == selected_id].iloc[0].to_dict()
        
        col_c1, col_c2 = st.columns([3, 1])
        with col_c1:
            st.info(f"**URL:** {selected_campaign.get('newsletter_url')}\n\n"
                    f"**Desktop:** {selected_campaign.get('opens_desktop')} opens | {selected_campaign.get('clicks_desktop')} clicks  \n"
                    f"**Mobile:** {selected_campaign.get('opens_mobile')} opens | {selected_campaign.get('clicks_mobile')} clicks")
        
        with col_c2:
            run_btn = st.button("▶️ Ejecutar Prueba Ahora", type="primary", use_container_width=True)

        if run_btn:
            if not selected_campaign.get("newsletter_url"):
                st.error("Esta campaña no tiene una URL de newsletter configurada.")
            else:
                progress_container = st.empty()
                status_log = []

                def update_progress(msg):
                    status_log.append(msg)
                    progress_container.text_area("Registro en vivo:", "\n".join(status_log[-12:]), height=220)

                with st.spinner("Ejecutando simulación de opens y clicks con Playwright..."):
                    try:
                        results = run_test(selected_campaign, on_progress=update_progress)
                        save_execution(selected_campaign["id"], results)
                        st.success("¡Prueba finalizada y guardada en el historial de reportes!")
                        
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Opens Exitosos", results["opens_success"])
                        m2.metric("Opens Fallidos", results["opens_fail"])
                        m3.metric("Clicks Exitosos", results["clicks_success"])
                        m4.metric("Clicks Fallidos", results["clicks_fail"])
                        
                        if results.get("article_links_found"):
                            with st.expander(f"Ver enlaces de artículos detectados ({len(results['article_links_found'])})"):
                                for link in results["article_links_found"]:
                                    st.write(f"- [{link}]({link})")
                                    
                    except Exception as e:
                        st.error(f"Error durante la ejecución: {e}")

# ========================================================
# 3. REPORTES Y RESULTADOS
# ========================================================
elif menu == "Reportes y Resultados":
    st.subheader("📊 Historial de Ejecuciones y Reportes")
    
    conn = get_connection()
    query = """
    SELECT 
        e.id AS execution_id,
        c.name AS campaign_name,
        e.date,
        e.opens_success,
        e.opens_fail,
        e.clicks_success,
        e.clicks_fail,
        e.details
    FROM executions e
    LEFT JOIN campaigns c ON e.campaign_id = c.id
    ORDER BY e.id DESC
    """
    df_exec = pd.read_sql(query, conn)
    conn.close()
    
    if df_exec.empty:
        st.info("Aún no se han registrado ejecuciones de campañas.")
    else:
        # Métricas Globales
        tot_opens_ok = df_exec["opens_success"].sum()
        tot_opens_fail = df_exec["opens_fail"].sum()
        tot_clicks_ok = df_exec["clicks_success"].sum()
        tot_clicks_fail = df_exec["clicks_fail"].sum()
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Opens OK", int(tot_opens_ok))
        c2.metric("Total Opens Fallidos", int(tot_opens_fail), delta_color="inverse")
        c3.metric("Total Clicks OK", int(tot_clicks_ok))
        c4.metric("Total Clicks Fallidos", int(tot_clicks_fail), delta_color="inverse")
        
        st.write("---")
        st.dataframe(df_exec.drop(columns=["details"], errors="ignore"), use_container_width=True)
        
        st.markdown("#### Detalle de Ejecuciones")
        for _, row in df_exec.head(10).iterrows():
            with st.expander(f"Ejecución #{row['execution_id']} - {row['campaign_name']} ({row['date']})"):
                st.write(f"- **Opens Exitosos:** {row['opens_success']} | **Fallidos:** {row['opens_fail']}")
                st.write(f"- **Clicks Exitosos:** {row['clicks_success']} | **Fallidos:** {row['clicks_fail']}")
                try:
                    details = json.loads(row["details"]) if row["details"] else []
                    if details:
                        st.write("**Detalles / Errores registrados:**")
                        for d in details:
                            st.text(f"• {d}")
                    else:
                        st.write("Sin errores reportados.")
                except Exception:
                    st.text(row["details"])