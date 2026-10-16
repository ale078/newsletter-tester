import time
import schedule
import pandas as pd
from database import get_connection, save_execution, create_tables
from automator import run_test

def run_daily_campaigns():
    """Ejecuta todas las campañas activas marcadas para ejecución diaria."""
    print("⏰ [SCHEDULER] Iniciando ciclo diario de campañas...")
    create_tables()
    conn = get_connection()
    campaigns = pd.read_sql("SELECT * FROM campaigns WHERE daily=1 AND status='active'", conn)
    conn.close()

    if campaigns.empty:
        print("ℹ️ [SCHEDULER] No hay campañas diarias activas.")
        return

    print(f"📋 [SCHEDULER] {len(campaigns)} campañas encontradas para ejecutar.")
    for _, camp in campaigns.iterrows():
        camp_dict = camp.to_dict()
        print(f"\n▶️ Ejecutando campaña: {camp_dict.get('name')} (ID: {camp_dict.get('id')})")
        
        if not camp_dict.get("newsletter_url"):
            print(f"⚠️ Campaña ID {camp_dict.get('id')} omitida: no tiene URL de newsletter configurada.")
            continue

        try:
            results = run_test(camp_dict)
            save_execution(camp_dict["id"], results)
            print(f"✅ Campaña ID {camp_dict.get('id')} completada y guardada en historial.")
        except Exception as e:
            print(f"❌ Error al ejecutar campaña ID {camp_dict.get('id')}: {e}")

def start_scheduler(run_at="09:00"):
    """Inicia el ciclo permanente del scheduler."""
    print(f"🚀 Scheduler programado todos los días a las {run_at}.")
    schedule.every().day.at(run_at).do(run_daily_campaigns)
    
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    # Si se ejecuta directamente, realiza una pasada inmediata y luego queda en espera diaria
    run_daily_campaigns()
    start_scheduler()