from playwright.sync_api import sync_playwright
import time
import random

def run_test(campaign, email_link):
    """
    campaign = diccionario con los números de opens y clicks
    email_link = enlace de la newsletter de prueba
    """
    results = {
        "opens_success": 0,
        "opens_fail": 0,
        "clicks_success": 0,
        "clicks_fail": 0,
        "details": []
    }

    with sync_playwright() as p:
        # Desktop
        browser_desktop = p.chromium.launch(headless=True)
        for i in range(campaign["opens_desktop"]):
            try:
                context = browser_desktop.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
                page = context.new_page()
                page.goto(email_link, timeout=10000)
                results["opens_success"] += 1
                time.sleep(random.uniform(1, 3))
                context.close()
            except Exception as e:
                results["opens_fail"] += 1
                results["details"].append(f"Open Desktop fail: {str(e)}")

        # Mobile (simula iPhone)
        for i in range(campaign["opens_mobile"]):
            try:
                context = browser_desktop.new_context(
                    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
                )
                page = context.new_page()
                page.goto(email_link, timeout=10000)
                results["opens_success"] += 1
                time.sleep(random.uniform(1, 3))
                context.close()
            except Exception as e:
                results["opens_fail"] += 1
                results["details"].append(f"Open Mobile fail: {str(e)}")

        browser_desktop.close()

        # Aquí irían los clics en los enlaces de los artículos (similar lógica)
        # Por ahora solo un ejemplo de estructura

    return results