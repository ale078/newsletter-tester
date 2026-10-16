import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from playwright.sync_api import sync_playwright
import time
import random
from urllib.parse import urlparse

# Filtros para ignorar enlaces que no son artículos
IGNORE_KEYWORDS = [
    "unsubscribe", "optout", "opt-out", "preferences", "cancelar",
    "bajarme", "privacy", "terms", "twitter.com", "x.com", "facebook.com",
    "instagram.com", "linkedin.com", "youtube.com", "mailto:", "javascript:",
    "#", "view-in-browser"
]

def extract_article_links(page):
    """Extrae enlaces relevantes a artículos del cuerpo del newsletter."""
    links = []
    try:
        elements = page.query_selector_all("a[href]")
        for el in elements:
            href = el.get_attribute("href")
            if not href:
                continue
            href_clean = href.strip().lower()
            
            # Filtrar enlaces de redes, desuscripción, mailto o vacíos
            if any(keyword in href_clean for keyword in IGNORE_KEYWORDS):
                continue
            
            parsed = urlparse(href)
            if parsed.scheme in ["http", "https"] and href not in links:
                links.append(href)
    except Exception as e:
        print(f"Error extrayendo enlaces: {e}")
    return links

def run_test(campaign, email_link=None, on_progress=None):
    """
    Ejecuta la prueba completa de Opens y Clicks en Desktop y Mobile.
    
    campaign: dict con keys:
        - opens_desktop (int)
        - opens_mobile (int)
        - clicks_desktop (int)
        - clicks_mobile (int)
        - newsletter_url (opcional si se pasa email_link)
    """
    target_url = email_link or campaign.get("newsletter_url")
    if not target_url:
        raise ValueError("No se proporcionó una URL de newsletter válida.")

    opens_desktop = int(campaign.get("opens_desktop", 0))
    opens_mobile = int(campaign.get("opens_mobile", 0))
    clicks_desktop = int(campaign.get("clicks_desktop", 0))
    clicks_mobile = int(campaign.get("clicks_mobile", 0))

    results = {
        "opens_success": 0,
        "opens_fail": 0,
        "clicks_success": 0,
        "clicks_fail": 0,
        "details": [],
        "article_links_found": []
    }

    def log(msg):
        print(msg)
        if on_progress:
            on_progress(msg)

    desktop_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    mobile_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        detected_links = []

        # ==========================================
        # 1. APERTURAS (OPENS) - DESKTOP
        # ==========================================
        if opens_desktop > 0:
            log(f"Iniciando {opens_desktop} aperturas Desktop...")
            for i in range(opens_desktop):
                try:
                    context = browser.new_context(
                        user_agent=desktop_ua,
                        viewport={"width": 1280, "height": 800}
                    )
                    page = context.new_page()
                    page.goto(target_url, timeout=20000, wait_until="domcontentloaded")
                    
                    # Extraer enlaces en la primera apertura exitosa
                    if not detected_links:
                        detected_links = extract_article_links(page)
                    
                    results["opens_success"] += 1
                    log(f"  [OK] Open Desktop #{i+1}")
                    time.sleep(random.uniform(1.2, 2.5))
                    context.close()
                except Exception as e:
                    results["opens_fail"] += 1
                    err_msg = f"Fallo Open Desktop #{i+1}: {str(e)}"
                    results["details"].append(err_msg)
                    log(f"  [FAIL] {err_msg}")

        # ==========================================
        # 2. APERTURAS (OPENS) - MOBILE
        # ==========================================
        if opens_mobile > 0:
            log(f"Iniciando {opens_mobile} aperturas Mobile...")
            for i in range(opens_mobile):
                try:
                    context = browser.new_context(
                        user_agent=mobile_ua,
                        viewport={"width": 390, "height": 844},
                        is_mobile=True,
                        has_touch=True
                    )
                    page = context.new_page()
                    page.goto(target_url, timeout=20000, wait_until="domcontentloaded")
                    
                    if not detected_links:
                        detected_links = extract_article_links(page)
                        
                    results["opens_success"] += 1
                    log(f"  [OK] Open Mobile #{i+1}")
                    time.sleep(random.uniform(1.2, 2.5))
                    context.close()
                except Exception as e:
                    results["opens_fail"] += 1
                    err_msg = f"Fallo Open Mobile #{i+1}: {str(e)}"
                    results["details"].append(err_msg)
                    log(f"  [FAIL] {err_msg}")

        results["article_links_found"] = detected_links
        log(f"Enlaces de artículos identificados: {len(detected_links)}")

        # ==========================================
        # 3. CLICS (CLICKS) - DESKTOP
        # ==========================================
        if clicks_desktop > 0:
            if not detected_links:
                log("  [WARN] No se encontraron enlaces de artículos para clics Desktop.")
                results["clicks_fail"] += clicks_desktop
                results["details"].append("No se detectaron enlaces para clics Desktop")
            else:
                log(f"Iniciando {clicks_desktop} clics Desktop...")
                for i in range(clicks_desktop):
                    link_to_click = detected_links[i % len(detected_links)]
                    try:
                        context = browser.new_context(
                            user_agent=desktop_ua,
                            viewport={"width": 1280, "height": 800}
                        )
                        page = context.new_page()
                        page.goto(link_to_click, timeout=20000, wait_until="domcontentloaded")
                        results["clicks_success"] += 1
                        log(f"  [OK] Click Desktop #{i+1} -> {link_to_click[:50]}...")
                        time.sleep(random.uniform(1.5, 3.0))
                        context.close()
                    except Exception as e:
                        results["clicks_fail"] += 1
                        err_msg = f"Fallo Click Desktop #{i+1}: {str(e)}"
                        results["details"].append(err_msg)
                        log(f"  [FAIL] {err_msg}")

        # ==========================================
        # 4. CLICS (CLICKS) - MOBILE
        # ==========================================
        if clicks_mobile > 0:
            if not detected_links:
                log("  [WARN] No se encontraron enlaces de artículos para clics Mobile.")
                results["clicks_fail"] += clicks_mobile
                results["details"].append("No se detectaron enlaces para clics Mobile")
            else:
                log(f"Iniciando {clicks_mobile} clics Mobile...")
                for i in range(clicks_mobile):
                    link_to_click = detected_links[i % len(detected_links)]
                    try:
                        context = browser.new_context(
                            user_agent=mobile_ua,
                            viewport={"width": 390, "height": 844},
                            is_mobile=True,
                            has_touch=True
                        )
                        page = context.new_page()
                        page.goto(link_to_click, timeout=20000, wait_until="domcontentloaded")
                        results["clicks_success"] += 1
                        log(f"  [OK] Click Mobile #{i+1} -> {link_to_click[:50]}...")
                        time.sleep(random.uniform(1.5, 3.0))
                        context.close()
                    except Exception as e:
                        results["clicks_fail"] += 1
                        err_msg = f"Fallo Click Mobile #{i+1}: {str(e)}"
                        results["details"].append(err_msg)
                        log(f"  [FAIL] {err_msg}")

        browser.close()

    log("Prueba finalizada.")
    return results