from select import select
import pytest
import time
import json
from datetime import datetime
import datetime
import os

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
import Campos
# Espera implicita
driver = webdriver.Chrome()
driver.implicitly_wait(10)

class nominas_functions():
    def __init__(self, driver):
        self.driver = driver

# Funciones

    # *************************************************Funciones Recurrentes*************************************************
    def AccesoNominas(self):

        print("■■■■■-Inicio Acceso Nominas-■■■■■")
        time.sleep(2)
        self.driver.implicitly_wait(20) 
        self.driver.find_element(By.XPATH, Campos.Configuracion).click()
        self.driver.implicitly_wait(20) 
        #self.driver.find_element(By.XPATH, Campos.CerrarModal)
        self.driver.implicitly_wait(20) 
        self.driver.find_element(By.XPATH, Campos.BotonConfiguracion).click()
        self.driver.implicitly_wait(20) 
        self.driver.find_element(By.XPATH, Campos.BotonNominas).click()
        self.driver.implicitly_wait(20) 
        # Verificar que se haya ingresado en la sección correspondiente
        assert Campos.SeccionNominas in self.driver.find_element(By.XPATH, Campos.NombreNominas).text, "Sección Erronea"
        print("■■■■■-Fin inicio sesion-■■■■■")
        time.sleep(2)
        
    def Nominas_Ordenamiento1(self):

        print("■■■■■-Inicio Ordenamiento 1-■■■■■")
        time.sleep(2)
        
        # Desplegar criterio de ordenamiento
        self.driver.find_element(By.XPATH, Campos.botonDespliegueCriterio).click()
        self.driver.implicitly_wait(20)
        time.sleep(2)
        
        # Seleccionar criterio de ordenamiento Apellido A-Z
        self.driver.find_element(By.XPATH, Campos.CriterioApellidpAZ).click()
        self.driver.implicitly_wait(20)
        time.sleep(2)
        
        # Continuar con el criterio seleccionado
        self.driver.find_element(By.XPATH, Campos.botonContinuarCriterio).click()
        self.driver.implicitly_wait(20)
        time.sleep(2)
        
        # Verificar mensaje de éxito
        assert Campos.MensajeExito in self.driver.find_element(By.XPATH, Campos.LabelAceptar).text, "Mensaje Erroneo"
        
        # Navegar a la sección de cursos
        self.driver.find_element(By.XPATH, Campos.botonCursos).click()
        self.driver.implicitly_wait(20)
        assert Campos.NombreCursos in self.driver.find_element(By.XPATH, Campos.SecciónCursos).text, "Seccion Erronea"
        
        # Seleccionar el primer curso
        self.driver.find_element(By.XPATH, Campos.CursoPrimero).click()
        self.driver.implicitly_wait(20)
        assert Campos.CursoNombre in self.driver.find_element(By.XPATH, Campos.CursoItem).text, "Curso Erroneo"

    def validar_informacion_curso(self, Orden, Primer_Apellido, Segundo_Apellido, Nombre, ID):
            try:
                # Esperar a que la tabla esté presente en el DOM y sea visible
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//table[@id='filterTbl']")))
            
                # Encontrar todas las filas de la tabla
                filas = self.driver.find_elements(By.XPATH, "(//tbody)[1]")
            
                encontrado = False
            
                # Iterar sobre cada fila para buscar la información específica
                for fila in filas:
                    # Obtener el texto de cada columna en la fila
                    columnas = fila.find_elements(By.TAG_NAME, "td")
                    texto_columnas = [columna.text.strip() for columna in columnas]
                
                    # Validar que la fila contenga la información esperada
                    if (Orden in texto_columnas[0] and
                        Primer_Apellido in texto_columnas[1] and
                        Segundo_Apellido in texto_columnas[2] and
                        Nombre in texto_columnas[3] and
                        ID in texto_columnas[4]):
                        encontrado = True
                        break
            
                # Si se encontró la información, retornar True (existente y visible)
                if encontrado:
                    return True
                else:
                    return False
        
            except Exception as e:
                print(f"Error al validar información del curso: {str(e)}")
                return False
