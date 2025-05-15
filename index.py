import sys
import time
from playwright.sync_api import sync_playwright, expect

def autocomplete_select(page, selector: str, value: str):
    page.click(selector)
    time.sleep(0.5)
    page.fill(selector, value)
    time.sleep(1.2)  # dejar que cargue las sugerencias
    page.keyboard.press("ArrowDown")
    time.sleep(0.3)
    page.keyboard.press("Enter")
    time.sleep(1)

def get_postal_code(commune: str, street: str, number: str) -> str:
    print(f"[INFO] Búsqueda iniciada: comuna='{commune}', calle='{street}', número='{number}'")
    browser = None
    page = None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.set_default_timeout(20000)

            print("[INFO] Cargando página de códigos postales...")
            page.goto("https://www.correos.cl/codigo-postal")
            page.wait_for_selector('input#mini-search-form-text', state="visible")
            time.sleep(1)

            print("[INFO] Seleccionando comuna con autocompletado...")
            autocomplete_select(page, 'input#mini-search-form-text', commune)

            print("[INFO] Seleccionando calle con autocompletado...")
            autocomplete_select(page, 'input#mini-search-form-text-direcciones', street)

            print("[INFO] Ingresando número...")
            page.fill('#_cl_cch_codigopostal_portlet_CodigoPostalPortlet_INSTANCE_MloJQpiDsCw9_numero', number)
            time.sleep(0.5)

            print("[INFO] Click fuera para activar validación...")
            page.click("label[for='mini-search-form-text']", force=True)
            time.sleep(1)

            search_btn = page.locator('#_cl_cch_codigopostal_portlet_CodigoPostalPortlet_INSTANCE_MloJQpiDsCw9_searchDirection')
            print("[INFO] Esperando que el botón 'Buscar' esté habilitado...")
            expect(search_btn).to_be_enabled(timeout=10000)

            print("[INFO] Haciendo click en 'Buscar'...")
            search_btn.click(force=True)
            time.sleep(2)

            print("[INFO] Esperando resultado del código postal...")
            result_locator = page.locator('#_cl_cch_codigopostal_portlet_CodigoPostalPortlet_INSTANCE_MloJQpiDsCw9_ddCodPostal')
            result_locator.wait_for(timeout=12000)

            code = result_locator.inner_text().strip()
            print(f"[INFO] Código postal encontrado: {code}")
            return code

    except Exception as e:
        print(f"[ERROR] Error durante la ejecución: {str(e)}")
        try:
            if page:
                page.screenshot(path="error.png")
                print("[DEBUG] Screenshot guardado como error.png")
        except Exception as ss_err:
            print(f"[WARNING] No se pudo capturar screenshot: {ss_err}")
        return f"Error: {str(e)}"

    finally:
        if browser:
            try:
                print("[INFO] Cerrando navegador...")
                browser.close()
            except Exception:
                print("[WARNING] El navegador ya estaba cerrado.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python script.py 'Comuna' 'Calle' 'Número'")
        print("Ejemplo: python script.py 'PUENTE ALTO' 'AVENIDA LAS PERDICES' '3462'")
        sys.exit(1)

    comuna, calle, numero = sys.argv[1], sys.argv[2], sys.argv[3]
    resultado = get_postal_code(comuna, calle, numero)
    print(f"[RESULTADO FINAL] {resultado}")
