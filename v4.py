from playwright.sync_api import sync_playwright
import requests
import json
import logging
import pytest
import os
import yaml
import time
from datetime import datetime
from jsonschema import validate
from dotenv import load_dotenv
from multiprocessing import Pool
from faker import Faker

# Cargar variables de entorno
load_dotenv()

# Cargar configuración desde YAML
def load_config(env="config.yaml"):
    with open(env, "r") as file:
        return yaml.safe_load(file)

CONFIG = load_config()
FAKE = Faker()

class UIFramework:
    def __init__(self, browser='chromium', headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright[browser].launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        logging.basicConfig(level=logging.INFO, filename="test_logs.log", filemode='w')
    
    def open_url(self, url):
        """Abre una URL en el navegador."""
        logging.info(f'Abrir URL: {url}')
        self.page.goto(url)
    
    def click(self, selector):
        """Hace clic en un elemento."""
        logging.info(f'Clic en: {selector}')
        self.page.click(selector)
    
    def fill(self, selector, text):
        """Rellena un campo de texto."""
        logging.info(f'Rellenar {selector} con {text}')
        self.page.fill(selector, text)
    
    def get_text(self, selector):
        """Obtiene el texto de un elemento."""
        text = self.page.inner_text(selector)
        logging.info(f'Texto de {selector}: {text}')
        return text
    
    def take_screenshot(self, filename=None):
        """Toma una captura de pantalla con timestamp."""
        if filename is None:
            filename = f'screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        self.page.screenshot(path=filename)
        logging.info(f'Screenshot guardado en {filename}')
    
    def request_api(self, url, method='GET', data=None, headers=None):
        """Realiza una solicitud HTTP a una API y devuelve la respuesta."""
        logging.info(f'Realizando solicitud {method} a {url}')
        response = requests.request(method, url, json=data, headers=headers)
        return response.json()
    
    def validate_json_schema(self, response, schema):
        """Valida una respuesta de API contra un JSON Schema."""
        try:
            validate(instance=response, schema=schema)
            logging.info("Validación JSON Schema exitosa")
        except Exception as e:
            logging.error(f'Error en la validación de JSON Schema: {e}')
            raise
    
    def wait_for_element(self, selector, timeout=5000):
        """Espera hasta que un elemento esté visible."""
        logging.info(f'Esperando por {selector}')
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def close(self):
        """Cierra el navegador y detiene Playwright."""
        self.browser.close()
        self.playwright.stop()
        logging.info('Navegador cerrado.')
    
    def get_api_response_status(self, url, method='GET', data=None, headers=None):
        """Obtiene el código de estado de una API."""
        logging.info(f'Obteniendo estado de respuesta de {url}')
        response = requests.request(method, url, json=data, headers=headers)
        return response.status_code
    
    def validate_api_response(self, url, expected_status, method='GET', data=None, headers=None):
        """Valida el código de estado de la API contra un esperado."""
        status = self.get_api_response_status(url, method, data, headers)
        assert status == expected_status, f'Esperado {expected_status}, pero obtenido {status}'
    
    def run_ui_test(self, test_func):
        """Ejecuta una prueba UI específica y captura errores."""
        try:
            test_func()
            logging.info("Prueba UI pasada correctamente.")
        except Exception as e:
            logging.error(f'Error en la prueba UI: {e}')
            self.take_screenshot()
            raise
    
    def run_api_test(self, url, expected_status, method='GET', data=None, headers=None):
        """Ejecuta una prueba de aceptación de API."""
        logging.info(f'Ejecutando prueba de API para {url}')
        try:
            self.validate_api_response(url, expected_status, method, data, headers)
            logging.info("Prueba de API pasada correctamente.")
        except AssertionError as e:
            logging.error(f'Error en la prueba de API: {e}')
            raise
    
    def parallel_execution(self, test_functions):
        """Ejecuta múltiples pruebas en paralelo."""
        with Pool(len(test_functions)) as pool:
            pool.map(lambda func: func(), test_functions)
    
    def generate_fake_data(self):
        """Genera datos falsos para pruebas automatizadas."""
        return {
            "name": FAKE.name(),
            "email": FAKE.email(),
            "address": FAKE.address(),
            "phone": FAKE.phone_number()
        }

# Ejemplo de uso:
if __name__ == "__main__":
    ui = UIFramework(headless=False)
    
    print("Opening URL")
    ui.open_url(CONFIG['test_url'])
    
    print("Taking screenshot")
    ui.take_screenshot()
    
    print("Running API test")
    ui.run_api_test("https://jsonplaceholder.typicode.com/posts/1", 200)
    
    print("Generating fake data")
    fake_data = ui.generate_fake_data()
    print(f'Datos falsos generados: {fake_data}')
    
    print("Closing UI")
    ui.close()
