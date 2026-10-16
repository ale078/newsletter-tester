from playwright.sync_api import sync_playwright
import time
import random

def run_simple_test(email_link, opens_desktop=3, opens_mobile=2):
    results = {
        "opens_success": 0,
        "opens_fail": 0,
        "details": []
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # === DESKTOP ===
        for i in range(opens_desktop):
            try:
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                page = context.new_page()
                page.goto(email_link, timeout=15000, wait_until="domcontentloaded")
                results["opens_success"] += 1
                print(f"✅ Desktop open #{i+1} OK")
                time.sleep(random.uniform(1.5, 3))
                context.close()
            except Exception as e:
                results["opens_fail"] += 1
                results["details"].append(f"Desktop fail: {str(e)}")
                print(f"❌ Desktop fail: {e}")

        # === MOBILE (iPhone) ===
        for i in range(opens_mobile):
            try:
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
                )
                page = context.new_page()
                page.goto(email_link, timeout=15000, wait_until="domcontentloaded")
                results["opens_success"] += 1
                print(f"✅ Mobile open #{i+1} OK")
                time.sleep(random.uniform(1.5, 3))
                context.close()
            except Exception as e:
                results["opens_fail"] += 1
                results["details"].append(f"Mobile fail: {str(e)}")
                print(f"❌ Mobile fail: {e}")

        browser.close()

    return results


# ======================
# === CONFIGURACIÓN ===
# ======================
email_link = "https://info.deeplearning.ai/e3t/Ctc/LX+113/cJhC404/VWkctQ5rrbPdW2czqNR8fhLTXW6klx535W9r_PN84393W5nR3bW7Y9pgv6lZ3lpVwts_t5b8MvPW4ZVT6T4lnDYMW2JxxRX4d952XW4r9FKy1KQ-jSW90GDGQ8GRF85N5xFFBk6gXcMW4Z5LQP3LYmHzW8CNKyX5K-B-4W7d9j2148S3gtW6y7MVS41btrfW4v_7MP5LgKDnVxYrgR53vNbDW5m4nzn3gKLrWW7_kjVR6D4YFVW6vWcht60pF9DW3gK46T2SX273N3FcQr-2dJh-VPQK7j1d-m59W1SDs9T8R4yNtW8m06476TbkcJW6kwSMy3GyshvVWVGtN7y_kDlW4dwDWb7jZFzCW3tb1f35wycNHVGR5WV2wQSqHW2lM_MD4W1nhXW25LPBm3G6Ym6W2gVJX18TfhQVW3gDzdl14tHX2W8mQ8m948s6PwW5ckY5J809BSgW3-Vkw94xdl55W3bLvy954TMW3Vp6F8c4cPpCDW1XyPPt18c6PRW7qRkm24hlt8LN7S_gH3ZB2kMW3T79zF80hrlCW3VlWG9496bYTW9fBcqK4j-bPNW1r1r-f4pY9yfN7PQ0L6sqGvvf9j0XGv04"   # ←←← PEGA AQUÍ EL ENLACE REAL DEL EMAIL

print("🚀 Iniciando prueba...")
result = run_simple_test(email_link, opens_desktop=3, opens_mobile=2)
print("\n📊 Resultado final:")
print(result)