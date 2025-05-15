import sys
import time
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
        print(f"[DEBUG] Verificación {label}: intento {attempt + 1} → '{actual}'")
        if expected_value.upper() in actual:
            return True
        print(f"[WARNING] El valor de {label} no se aplicó correctamente, reintentando...")
    raise Exception(f"No se pudo seleccionar correctamente la {label} tras múltiples intentos.")

def ensure_number_filled(page, selector: str, value: str):
    page.fill(selector, value)
    wait(0.5)
    filled = page.input_value(selector).strip()
    if filled != value.strip():
        raise Exception(f"El campo número no se llenó correctamente: esperado '{value}', actual '{filled}'")
    return True

def get_postal_code(commune: str, street: str, number: str) -> str:
    print(f"[INFO] Búsqueda iniciada: comuna='{commune}', calle='{street}', número='{number}'")
    browser = None
    page = None

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(20000)

            print("[INFO] Cargando página de códigos postales...")
            page.goto("https://www.correos.cl/codigo-postal")
            page.wait_for_selector('input#mini-search-form-text', state="visible")
            wait(1)

            print("[INFO] Seleccionando comuna con verificación...")
            ensure_autocomplete_selected(page, 'input#mini-search-form-text', commune, "comuna")

            print("[INFO] Seleccionando calle con verificación...")
            ensure_autocomplete_selected(page, 'input#mini-search-form-text-direcciones', street, "calle")

            print("[INFO] Ingresando número con verificación...")
            ensure_number_filled(page, '#_cl_cch_codigopostal_portlet_CodigoPostalPortlet_INSTANCE_MloJQpiDsCw9_numero', number)

            print("[INFO] Click fuera para activar validación...")
            page.click("label[for='mini-search-form-text']", force=True)
            wait(1)

            search_btn = page.locator('#_cl_cch_codigopostal_portlet_CodigoPostalPortlet_INSTANCE_MloJQpiDsCw9_searchDirection')
            print("[INFO] Esperando que el botón 'Buscar' esté habilitado...")
            expect(search_btn).to_be_enabled(timeout=10000)

            print("[INFO] Haciendo click en 'Buscar'...")
            search_btn.click(force=True)
            wait(2)

            print("[INFO] Esperando resultado del código postal...")
            result_locator = page.locator('#_cl_cch_codigopostal_portlet_CodigoPostalPortlet_INSTANCE_MloJQpiDsCw9_ddCodPostal')
            result_locator.wait_for(state="visible", timeout=15000)

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
