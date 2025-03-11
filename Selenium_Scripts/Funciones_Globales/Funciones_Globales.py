from select import select
import pytest
import time
import json
from datetime import datetime
import datetime
import os
import Campos

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
# from datetime import datetime

usuario = "sarias@colegium.com"
clave = "PruebasQa."

class global_functions():
    def __init__(self, driver):
        self.driver = driver

# Funciones

    # *************************************************Funciones Recurrentes*************************************************
    def inicioSesion(self, usuario=usuario, clave=clave):
        print("■■■■■-Inicio inicio sesion-■■■■■")
        self.driver.implicitly_wait(20)
        email_input = self.driver.find_element(By.XPATH, "//input[@placeholder='ejemplo@colegium.com']")
        email_input.send_keys(str(usuario))
        self.driver.implicitly_wait(20)
        password_input = self.driver.find_element(By.XPATH, "//input[@placeholder='······']")
        password_input.send_keys(clave)
        self.driver.implicitly_wait(30)
        self.driver.find_element(By.XPATH, "//button[text()='Iniciar sesión']").click()
        time.sleep(1)
        self.driver.implicitly_wait(20)
        # nombre_colegio = self.driver.find_element(By. XPATH, "(//p[text()='colegio automatización chile'])[1]").text
        # print(f"■■■■■■■■■■ {nombre_colegio}")
        # assert nombre_colegio == colegio
        print("■■■■■-Fin inicio sesion-■■■■■")
        time.sleep(2)

    def cerrarSesion(self):
        print("■■■■■-Inicio cerrar sesion-■■■■■")
        time.sleep(2)
        self.driver.implicitly_wait(70)
        self.driver.find_element(By.ID, "avatar").click()
        self.driver.implicitly_wait(70)
        self.driver.find_element(By.XPATH, "//button[contains(.,'Cerrar Sesión')]").click()
        print("■■■■■-Fin cerrar sesion-■■■■■")
        time.sleep(2)
        
