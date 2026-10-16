def run_daily_campaigns():
    conn = get_connection()
    campaigns = pd.read_sql("SELECT * FROM campaigns WHERE daily=1 AND status='active'", conn)
    
    for _, camp in campaigns.iterrows():
        # Aquí llamas a run_test() con los números de la campaña
        # Luego guardas los resultados en la tabla executions
        pass

# Para ejecutar manualmente:
# schedule.every().day.at("09:00").do(run_daily_campaigns)