import sys
import time
from playwright.sync_api import sync_playwright, expect

def get_postal_code(commune: str, street: str, number: str) -> str:
    print(f"[INFO] Launching Playwright for commune='{commune}', street='{street}', number='{number}'")

    browser = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            print("[INFO] Navigating to Correos de Chile postal code page...")
            page.goto("https://www.correos.cl/codigo-postal", timeout=15000)

            print("[INFO] Waiting for page to fully render...")
            time.sleep(3)

            print("[INFO] Typing commune into input field...")
            page.fill('input#mini-search-form-text', commune)
            page.keyboard.press("Enter")
            time.sleep(1.5)

            print("[INFO] Typing street into input field...")
            page.fill('input#mini-search-form-text-direcciones', street)
            page.keyboard.press("Enter")
            time.sleep(1.5)

            print("[INFO] Typing number into input field...")
            page.fill('#_cl_cch_codigopostal_portlet_CodigoPostalPortlet_INSTANCE_MloJQpiDsCw9_numero', number)
            time.sleep(1)

            print("[INFO] Simulating blur by clicking outside...")
            page.click("label[for='mini-search-form-text']")
            time.sleep(1.5)

            search_button = page.locator('#_cl_cch_codigopostal_portlet_CodigoPostalPortlet_INSTANCE_MloJQpiDsCw9_searchDirection')
            print("[INFO] Waiting for the 'Search' button to be enabled...")
            expect(search_button).to_be_enabled(timeout=10000)
            print("[INFO] Search button is now enabled. Clicking it...")
            search_button.click()

            print("[INFO] Waiting for the postal code box to appear...")
            page.wait_for_selector("div.codigo-postal-box", timeout=12000)

            print("[INFO] Reading postal code from DOM...")
            raw_result = page.inner_text("div.codigo-postal-box").strip()
            print(f"[DEBUG] Raw result: '{raw_result}'")

            if "Código Postal:" in raw_result:
                code = raw_result.split("Código Postal:")[-1].strip().split()[0]
                print(f"[INFO] Postal code found: {code}")
                return code
            else:
                print("[WARNING] Could not extract code from visible text.")
                return "Postal code not found."

    except KeyboardInterrupt:
        print("\n[INFO] Script interrupted by user.")
        return "Execution manually interrupted."

    except Exception as e:
        print(f"[ERROR] Exception occurred: {str(e)}")
        try:
            page.screenshot(path="error_screenshot.png")
            print("[DEBUG] Screenshot saved as error_screenshot.png")
        except:
            pass
        return f"Error: {str(e)}"

    finally:
        if browser:
            try:
                print("[INFO] Closing browser...")
                browser.close()
            except Exception:
                print("[WARNING] Browser was already closed or unreachable.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python index.py 'Commune' 'Street' 'Number'")
        print("Example: python index.py 'PUENTE ALTO' 'AVENIDA LAS PERDICES' '3462'")
        sys.exit(1)

    commune, street, number = sys.argv[1], sys.argv[2], sys.argv[3]
    result = get_postal_code(commune, street, number)
    print(f"[FINAL RESULT] {result}")
