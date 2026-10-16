import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from automator import run_test

# ========================================================
# === CONFIGURACION DE PRUEBA RAPIDA INDIVIDUAL (PILOTO) =
# ========================================================
test_campaign = {
    "name": "Prueba Rapida Individual",
    "newsletter_url": "https://info.deeplearning.ai/e3t/Ctc/LX+113/cJhC404/VWkctQ5rrbPdW2czqNR8fhLTXW6klx535W9r_PN84393W5nR3bW7Y9pgv6lZ3lpVwts_t5b8MvPW4ZVT6T4lnDYMW2JxxRX4d952XW4r9FKy1KQ-jSW90GDGQ8GRF85N5xFFBk6gXcMW4Z5LQP3LYmHzW8CNKyX5K-B-4W7d9j2148S3gtW6y7MVS41btrfW4v_7MP5LgKDnVxYrgR53vNbDW5m4nzn3gKLrWW7_kjVR6D4YFVW6vWcht60pF9DW3gK46T2SX273N3FcQr-2dJh-VPQK7j1d-m59W1SDs9T8R4yNtW8m06476TbkcJW6kwSMy3GyshvVWVGtN7y_kDlW4dwDWb7jZFzCW3tb1f35wycNHVGR5WV2wQSqHW2lM_MD4W1nhXW25LPBm3G6Ym6W2gVJX18TfhQVW3gDzdl14tHX2W8mQ8m948s6PwW5ckY5J809BSgW3-Vkw94xdl55W3bLvy954TMW3Vp6F8c4cPpCDW1XyPPt18c6PRW7qRkm24hlt8LN7S_gH3ZB2kMW3T79zF80hrlCW3VlWG9496bYTW9fBcqK4j-bPNW1r1r-f4pY9yfN7PQ0L6sqGvvf9j0XGv04",
    "opens_desktop": 1,
    "opens_mobile": 1,
    "clicks_desktop": 1,
    "clicks_mobile": 1,
}

if __name__ == "__main__":
    print("[*] Iniciando prueba rapida de piloto (Opens + Clicks)...")
    results = run_test(test_campaign)
    print("\n--- Resultados ---")
    print(f"  * Opens  Desktop/Mobile OK: {results['opens_success']} | Fail: {results['opens_fail']}")
    print(f"  * Clicks Desktop/Mobile OK: {results['clicks_success']} | Fail: {results['clicks_fail']}")
    print(f"  * Enlaces detectados: {len(results['article_links_found'])}")
    if results['details']:
        print("  * Errores/Detalles:", results['details'])