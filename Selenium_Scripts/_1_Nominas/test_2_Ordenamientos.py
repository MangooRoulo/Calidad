import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import allure
from allure_commons.types import AttachmentType
from Funciones_Globales.Funciones_Globales import global_functions
from Funciones_Nominas.Funciones_Nominas import nominas_functions

def abrirNavegador(navegador="chrome", incognito=True, download_path=None, token=None, url="http://app.colegium.cloud"):
    if navegador == "chrome":
        options = ChromeOptions()
        if incognito:
            options.add_argument("--incognito")
        # Configuraciones para evitar las ventanas emergentes de descarga
        prefs = {
            "download.default_directory": download_path,  # Directorio de descarga
            "download.prompt_for_download": False,  # Desactivar la solicitud de confirmación de descarga
            "directory_upgrade": True,  # Permite la sobreescritura del archivo sin pedir confirmación
            "safebrowsing.enabled": True,  # Habilita la protección contra descargas peligrosas
            "profile.default_content_settings.popups": 0,  # Desactiva los popups (en incognito)
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1  # Permitir múltiples descargas automáticas
        }
        options.add_experimental_option("prefs", prefs)
        # Argumentos adicionales para mejorar la estabilidad
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Desactiva el mensaje de "Controlado por software"
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    elif navegador == "firefox":
        options = FirefoxOptions()
        if incognito:
            options.add_argument("-private")
        # Configuraciones para la descarga en Firefox
        prefs = {
            "browser.download.dir": download_path,
            "browser.download.folderList": 2,  # Establece el directorio de descarga personalizado
            "browser.download.useDownloadDir": True,
            "browser.helperApps.neverAsk.saveToDisk": "application/octet-stream"  # Tipo MIME
        }
        options.set_preference("browser.download.manager.showWhenStarting", False)
        for key, value in prefs.items():
            options.set_preference(key, value)
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    elif navegador == "edge":
        options = EdgeOptions()
        if incognito:
            options.add_argument("--inprivate")
        # Configuraciones para la descarga en Edge
        prefs = {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

    # Agregar el header x-test-run antes de cargar la página
    if token:
        driver.execute_cdp_cmd("Network.enable", {})  # Habilita la interceptación de la red
        driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
            "headers": {
                "X-test-run": token  # Token proporcionado
            }
        })
        print(f"Token aplicado correctamente: {token}")

    driver.maximize_window()
    driver.get(url)  # Navegar a la URL especificada
    print(f"■■■■■-Iniciando Tests en {navegador}■■■■■")
    return driver

@pytest.fixture(scope="function")
def driver_setup():
    token = 'U8xv6X$L2>l&'  # El token que te proporcionaron
    driver = abrirNavegador(navegador="chrome", download_path=os.path.join(os.getcwd(), "Descargas"), token=token, url="http://app.colegium.cloud")
    yield driver
    cerrar_driver(driver)

def cerrar_driver(driver):
    if driver:
        print("Cerrando el driver...")
        driver.quit()

def take_screenshot_on_failure(driver, header):
    print("Intentando tomar screenshot...")
    if driver:
        allure.attach(driver.get_screenshot_as_png(), name="screenshot", attachment_type=AttachmentType.PNG)
        print(f"Captura de pantalla guardada para {header}")
    else:
        print("Driver no disponible para tomar screenshot")

def pytest_runtest_makereport(item, call):
    print(f"Ejecutando prueba: {item.name}")
    if call.excinfo is not None:
        try:
            driver = item.funcargs['driver_setup']
        except KeyError:
            print("No se encontró el fixture 'driver_setup'")
        else:
            take_screenshot_on_failure(driver, item.name)

@allure.feature('Nominas Test')
def test_AccesoNominas(driver_setup):
    driver = driver_setup

    Ordenamientos = {
        "Estudiante_1": {
            "Orden": "1",
            "Primer_Apellido": "Diaz",
            "Segundo_Apellido": "Mendoza",
            "Nombre": "Sofia",
            "ID": "2181782-1"
        },
        "Estudiante_2": {
            "Orden": "3",
            "Primer_Apellido": "Gonadasdzalez",
            "Segundo_Apellido": "Lopez",
            "Nombre": "Maria",
            "ID": "2987505-7"
        },
        "Estudiante_3": {
            "Orden": "5",
            "Primer_Apellido": "Martinez",
            "Segundo_Apellido": "Sanchez",
            "Nombre": "Juan",
            "ID": "8571154-7"
        }
    }

    try:
        funcion = global_functions(driver)
        funcionNominas = nominas_functions(driver)

        funcion.inicioSesion()
        funcionNominas.AccesoNominas()
        funcionNominas.Ordenamientossasasd()
        funcionNominas.validar_informacion_curso(Ordenamientos)
        funcion.cerrarSesion()

    except Exception as e:
        # Tomar la captura de pantalla si ocurre un error
        allure.attach(driver.get_screenshot_as_png(), name="screenshot_error", attachment_type=AttachmentType.PNG)
        print(f"Error: {e}")
        raise  # Re-lanzar la excepción para que pytest la maneje
