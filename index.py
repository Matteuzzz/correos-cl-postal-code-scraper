import sys
import time
import json
from playwright.sync_api import sync_playwright, expect

def wait(seconds: float, msg: str = ""):
    if msg:
        print(f"[WAIT] {msg} ({seconds}s)")
    time.sleep(seconds)

def autocomplete_select(page, selector: str, value: str):
    page.click(selector)
    wait(0.5)
    page.fill(selector, value)
    wait(1.2)
    page.keyboard.press("ArrowDown")
    wait(0.3)
    page.keyboard.press("Enter")
    wait(1)

def ensure_autocomplete_selected(page, selector: str, expected_value: str, label: str, max_retries: int = 2):
    for attempt in range(max_retries):
        autocomplete_select(page, selector, expected_value)
        actual = page.input_value(selector).strip().upper()
        print(f"[DEBUG] Verifying {label}: attempt {attempt + 1} → '{actual}'")
        if expected_value.upper() in actual:
            return True
        print(f"[WARNING] {label.capitalize()} value not correctly applied, retrying...")
    raise Exception(f"Failed to select {label} correctly after {max_retries} attempts.")

def ensure_number_filled(page, selector: str, value: str):
    page.fill(selector, value)
    wait(0.5)
    filled = page.input_value(selector).strip()
    if filled != value.strip():
        raise Exception(f"Number field not filled correctly: expected '{value}', got '{filled}'")
    return True

def get_postal_code(commune: str, street: str, number: str) -> dict:
    print(f"[INFO] Lookup started for commune='{commune}', street='{street}', number='{number}'")
    browser = None
    page = None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(20000)

            print("[INFO] Navigating to Correos de Chile postal code page...")
            page.goto("https://www.correos.cl/codigo-postal")
            page.wait_for_selector('input#mini-search-form-text', state="visible")
            wait(1)

            print("[INFO] Selecting commune with verification...")
            ensure_autocomplete_selected(page, 'input#mini-search-form-text', commune, "commune")

            print("[INFO] Selecting street with verification...")
            ensure_autocomplete_selected(page, 'input#mini-search-form-text-direcciones', street, "street")

            print("[INFO] Filling number with verification...")
            ensure_number_filled(page, '#_cl_cch_codigopostal_portlet_CodigoPostalPortlet_INSTANCE_MloJQpiDsCw9_numero', number)

            print("[INFO] Triggering form validation by clicking outside...")
            page.click("label[for='mini-search-form-text']", force=True)
            wait(1)

            search_btn = page.locator('#_cl_cch_codigopostal_portlet_CodigoPostalPortlet_INSTANCE_MloJQpiDsCw9_searchDirection')
            print("[INFO] Waiting for 'Search' button to be enabled...")
            expect(search_btn).to_be_enabled(timeout=10000)

            print("[INFO] Clicking 'Search'...")
            search_btn.click(force=True)
            wait(2)

            print("[INFO] Waiting for postal code result...")
            result_locator = page.locator('#_cl_cch_codigopostal_portlet_CodigoPostalPortlet_INSTANCE_MloJQpiDsCw9_ddCodPostal')
            result_locator.wait_for(state="visible", timeout=15000)

            code = result_locator.inner_text().strip()
            print(f"[INFO] Postal code retrieved: {code}")
            return { "postalCode": code }

    except Exception as e:
        error_message = f"Scraper failed: {str(e)}"
        print(f"[ERROR] {error_message}")
        try:
            if page:
                page.screenshot(path="error.png")
                print("[DEBUG] Screenshot saved as error.png")
        except Exception as ss_err:
            print(f"[WARNING] Could not capture screenshot: {ss_err}")
        return { "error": error_message }

    finally:
        if browser:
            try:
                print("[INFO] Closing browser...")
                browser.close()
            except Exception:
                print("[WARNING] Browser was already closed or unreachable.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(json.dumps({
            "error": "Invalid arguments. Usage: python index.py 'Commune' 'Street' 'Number'"
        }))
        sys.exit(1)

    commune, street, number = sys.argv[1], sys.argv[2], sys.argv[3]
    result = get_postal_code(commune, street, number)
    print(json.dumps(result))
