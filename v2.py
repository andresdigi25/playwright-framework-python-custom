from playwright.sync_api import sync_playwright
import requests
import json
import logging
import pytest
from datetime import datetime

class UIFramework:
    def __init__(self, browser='chromium', headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright[browser].launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        logging.basicConfig(level=logging.INFO)
    
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

# Ejemplo de uso:
if __name__ == "__main__":
    ui = UIFramework(headless=False)
    ui.open_url("https://www.google.com")
    ui.fill("input[name='q']", "Playwright Python")
    ui.take_screenshot()
    ui.run_api_test("https://jsonplaceholder.typicode.com/posts/1", 200)
    ui.close()
