from select import select
import pytest
import time
import json
from datetime import datetime
import datetime
import os
import json

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

    def cargar_datos_alumnos(self, archivo):
        try:
            with open(archivo, 'r') as file:
                datos = json.load(file)
            return datos
        except FileNotFoundError:
            print(f"■■■■■-El archivo {archivo} no se encontró-■■■■■")
            return {}
        except json.JSONDecodeError:
            print(f"■■■■■-Error al decodificar el archivo {archivo}. Asegúrate de que el archivo JSON esté bien formado-■■■■■")
            return {}

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
        print("■■■■■-Fin Acceso Nominas-■■■■■")
        time.sleep(2)
        
    def AccesoCrusos(self):
        print(f"■■■■■-Acceso Cursos-■■■■■")
        self.driver.find_element(By.XPATH, Campos.botonCursos).click()
        self.driver.implicitly_wait(20)
        time.sleep(2)
        self.driver.find_element(By.XPATH, Campos.CursoPrimero).click()
        self.driver.implicitly_wait(20)
        time.sleep(2)
        print(f"■■■■■-Fin Acceso Cursos-■■■■■")
        
    def Nominas_Ordenamiento(self, Orden, Primer_Apellido, Segundo_Apellido, Nombre, ID):

        criterios = [
            Campos.AZPrimerApellido,
            Campos.AZNombre,
            Campos.AZVaronesMujeres,
            Campos.AZMjeresVarones
        ]

        ordenamientos = [
            Campos.NumeroDeLista,
            Campos.AZOPrimerApellido,
            Campos.AZONombre,
            Campos.AZOVaronesMujeres,
            Campos.AZOMujeresVarones
        ]

        alumnos_por_ordenamiento1 = self.cargar_datos_alumnos('alumnos.json')

        for criterio in criterios:
            print(f"■■■■■-Inicio Asignación de criterio {criterio}-■■■■■")

            #Seleccionando Criterio
            self.driver.find_element(By.XPATH, Campos.BotonDespliegueCriterio).click()
            self.driver.implicitly_wait(20)
            time.sleep(2)
            self.driver.find_element(By.XPATH, criterio).click()
            self.driver.implicitly_wait(20)
            time.sleep(2)

            #Dando Aceptar en el label
            self.driver.find_element(By.XPATH, Campos.botonContinuar).click()
            self.driver.implicitly_wait(20)
            time.sleep(2)            
            
            # Verificar mensaje de éxito
            assert Campos.MensajeExito in self.driver.find_element(By.XPATH, Campos.LabelAceptar).text, "Mensaje Erroneo"
                        
            print(f"■■■■■-Fin asignación de criterio {criterio}-■■■■■")

            for ordenamiento in ordenamientos:
                print(f"■■■■■-Aplicando ordenamiento {ordenamiento}-■■■■■")
                
                #Seleccionando Ordenamiento
                self.driver.find_element(By.XPATH, Campos.BotonDespliegueOrdenamiento).click()
                self.driver.implicitly_wait(20)
                time.sleep(2)
                self.driver.find_element(By.XPATH, ordenamiento).click()
                self.driver.implicitly_wait(20)
                time.sleep(2)
                
                #Dando Aceptar en el label
                self.driver.find_element(By.XPATH, Campos.botonContinuar).click()
                self.driver.implicitly_wait(20)
                time.sleep(2) 
                
                # Verificar mensaje de éxito
                assert Campos.MensajeExito in self.driver.find_element(By.XPATH, Campos.LabelAceptar).text, "Mensaje Erroneo"

                print(f"■■■■■-Fin Aplicando ordenamiento {ordenamiento}-■■■■■")
                
                #Acceso Cursos
                self.AccesoCrusos()
                self.driver.implicitly_wait(20)
                time.sleep(2)
                    
                # Validar la información de tres alumnos
                alumnos = alumnos_por_ordenamiento1.get(ordenamiento, [])
                               
                
                    
                print(f"■■■■■-Validando Información del alumno-■■■■■")

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


            print(f"■■■■■-Fin Validando Información del alumno-■■■■■")
                    
            #Regreso a nominas
            self.AccesoNominas()
            self.driver.implicitly_wait(20)
            time.sleep(2) 
            
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



#TEsteos

    def pruebas(self, Orden, Primer_Apellido, Segundo_Apellido, Nombre, ID):

            DatosAlumnos = {
                "Orden_1": {
                    "Estudiante_1": {
                        "Orden": "1",
                        "Primer_Apellido": "Diaz",
                        "Segundo_Apellido": "Mendoza",
                        "Nombre": "Sofia",
                        "ID": "2181782-1"
                    },
                    "Estudiante_2": {
                        "Orden": "2",
                        "Primer_Apellido": "Garcia",
                        "Segundo_Apellido": "Lopez",
                        "Nombre": "Juan",
                        "ID": "2181782-2"
                    },
                    "Estudiante_3": {
                        "Orden": "3",
                        "Primer_Apellido": "Martinez",
                        "Segundo_Apellido": "Perez",
                        "Nombre": "Ana",
                        "ID": "2181782-3"
                    }
                },
                "Orden_2": {
                    "Estudiante_4": {
                        "Orden": "4",
                        "Primer_Apellido": "Fernandez",
                        "Segundo_Apellido": "Gomez",
                        "Nombre": "Luis",
                        "ID": "2181782-4"
                    },
                    "Estudiante_5": {
                        "Orden": "5",
                        "Primer_Apellido": "Hernandez",
                        "Segundo_Apellido": "Ruiz",
                        "Nombre": "Maria",
                        "ID": "2181782-5"
                    },
                    "Estudiante_6": {
                        "Orden": "6",
                        "Primer_Apellido": "Lopez",
                        "Segundo_Apellido": "Martinez",
                        "Nombre": "Carlos",
                        "ID": "2181782-6"
                    }
                }
            }

            criterios = [
                Campos.AZPrimerApellido,
                Campos.AZNombre,
                Campos.AZVaronesMujeres,
                Campos.AZMjeresVarones
            ]

            ordenamientos = [
                Campos.NumeroDeLista,
                Campos.AZOPrimerApellido,
                Campos.AZONombre,
                Campos.AZOVaronesMujeres,
                Campos.AZOMujeresVarones
            ]

            alumnos_por_ordenamiento1 = self.cargar_datos_alumnos("alumnos.json")

            for criterio in criterios:
                print(f"■■■■■-Inicio Asignación de criterio {criterio}-■■■■■")
                
                #Seleccionando Criterio
                self.driver.find_element(By.XPATH, Campos.BotonDespliegueCriterio).click()
                self.driver.implicitly_wait(20)
                time.sleep(2)
                self.driver.find_element(By.XPATH, criterio).click()
                self.driver.implicitly_wait(20)
                time.sleep(2)
                
                
                #Dando Aceptar en el label
                self.driver.find_element(By.XPATH, Campos.botonContinuar).click()
                self.driver.implicitly_wait(20)
                time.sleep(2)            
                
                # Verificar mensaje de éxito
                assert Campos.MensajeExito in self.driver.find_element(By.XPATH, Campos.LabelAceptar).text, "Mensaje Erroneo"
                            
                print(f"■■■■■-Fin asignación de criterio {criterio}-■■■■■")
                
                for ordenamiento in ordenamientos:
                    print(f"■■■■■-Aplicando ordenamiento {ordenamiento}-■■■■■")
                    
                    #Seleccionando Ordenamiento
                    self.driver.find_element(By.XPATH, Campos.BotonDespliegueOrdenamiento).click()
                    self.driver.implicitly_wait(20)
                    time.sleep(2)
                    self.driver.find_element(By.XPATH, ordenamiento).click()
                    self.driver.implicitly_wait(20)
                    time.sleep(2)
                    
                    #Dando Aceptar en el label
                    self.driver.find_element(By.XPATH, Campos.botonContinuar).click()
                    self.driver.implicitly_wait(20)
                    time.sleep(2) 
                    
                    # Verificar mensaje de éxito
                    assert Campos.MensajeExito in self.driver.find_element(By.XPATH, Campos.LabelAceptar).text, "Mensaje Erroneo"
                            
                    print(f"■■■■■-Fin Aplicando ordenamiento {ordenamiento}-■■■■■")
                    
                    #Acceso Cursos
                    self.AccesoCrusos()
                    self.driver.implicitly_wait(20)
                    time.sleep(2)
                        
                    # Validar la información de tres alumnos
                    alumnos1 = alumnos_por_ordenamiento1.get(ordenamiento, [])
                    
                    for alumno in alumnos1:            
                        print(f"■■■■■-Validando Información del alumno-■■■■■")
                        
                        #self.validar_informacion_curso()
                        
                        print(f"■■■■■-Fin Validando Información del alumno-■■■■■")
                        
                    #Regreso a nominas
                    self.AccesoNominas()
                    self.driver.implicitly_wait(20)
                    time.sleep(2) 