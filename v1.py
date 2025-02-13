from playwright.sync_api import sync_playwright
import requests
import json
import logging

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
    
    def take_screenshot(self, filename='screenshot.png'):
        """Toma una captura de pantalla."""
        self.page.screenshot(path=filename)
        logging.info(f'Screenshot guardado en {filename}')
    
    def request_api(self, url, method='GET', data=None, headers=None):
        """Realiza una solicitud HTTP a una API y devuelve la respuesta."""
        logging.info(f'Realizando solicitud {method} a {url}')
        response = requests.request(method, url, json=data, headers=headers)
        return response.json()
    
    def close(self):
        """Cierra el navegador y detiene Playwright."""
        self.browser.close()
        self.playwright.stop()
        logging.info('Navegador cerrado.')
    
    def wait_for_element(self, selector, timeout=5000):
        """Espera hasta que un elemento esté visible."""
        logging.info(f'Esperando por {selector}')
        self.page.wait_for_selector(selector, timeout=timeout)

# Ejemplo de uso:
if __name__ == "__main__":
    ui = UIFramework(headless=False)
    ui.open_url("https://www.google.com")
    ui.fill("input[name='q']", "Playwright Python")
    ui.take_screenshot("google_search.png")
    ui.close()
