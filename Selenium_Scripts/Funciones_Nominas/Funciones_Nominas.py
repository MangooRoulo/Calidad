from select import select
import time
import json
from datetime import datetime
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
                print(f"■■■■■-Error al validar información del curso: {str(e)} ❌❌❌ -■■■■■")
                return False



#TEsteos

    def pruebas(self, Orden, Primer_Apellido, Segundo_Apellido, Nombre, ID):
        DatosAlumnos = {
            "Orden_1": {
                "Estudiante_1": {"Orden": "1", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"},
                "Estudiante_2": {"Orden": "2", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_3": {"Orden": "3", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"}
            },
            "Orden_2": {
                "Estudiante_4": {"Orden": "1", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"},
                "Estudiante_5": {"Orden": "2", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_4": {"Orden": "3", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"}
            },
            "Orden_3": {
                "Estudiante_7": {"Orden": "2", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_8": {"Orden": "6", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_9": {"Orden": "5", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"}
            },
            "Orden_4": {
                "Estudiante_10": {"Orden": "6", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_11": {"Orden": "5", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"},
                "Estudiante_12": {"Orden": "4", "Primer_Apellido": "Herrera", "Segundo_Apellido": "Jimenez", "Nombre": "Luis", "ID": "3660580-4"}
            },
            "Orden_5": {
                "Estudiante_13": {"Orden": "2", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_14": {"Orden": "3", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"},
                "Estudiante_15": {"Orden": "1", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"}
            },
            "Orden_6": {
                "Estudiante_16": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_17": {"Orden": "2", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_18": {"Orden": "3", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"}
            },
            "Orden_7": {
                "Estudiante_19": {"Orden": "6", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"},
                "Estudiante_20": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_21": {"Orden": "5", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"}
            },
            "Orden_8": {
                "Estudiante_22": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_23": {"Orden": "2", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_24": {"Orden": "3", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"}
            },
            "Orden_9": {
                "Estudiante_25": {"Orden": "2", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_26": {"Orden": "3", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"},
                "Estudiante_27": {"Orden": "4", "Primer_Apellido": "Herrera", "Segundo_Apellido": "Jimenez", "Nombre": "Luis", "ID": "3660580-4"}
            },
            "Orden_10": {
                "Estudiante_28": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_29": {"Orden": "5", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"},
                "Estudiante_30": {"Orden": "6", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"}
            },
            "Orden_11": {
                "Estudiante_31": {"Orden": "1", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_32": {"Orden": "2", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"},
                "Estudiante_33": {"Orden": "3", "Primer_Apellido": "Herrera", "Segundo_Apellido": "Jimenez", "Nombre": "Luis", "ID": "3660580-4"}
            },
            "Orden_12": {
                "Estudiante_34": {"Orden": "6", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"},
                "Estudiante_35": {"Orden": "4", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_36": {"Orden": "5", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"}
            },
            "Orden_13": {
                "Estudiante_37": {"Orden": "4", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_38": {"Orden": "1", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_39": {"Orden": "2", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"}
            },
            "Orden_14": {
                "Estudiante_40": {"Orden": "1", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_41": {"Orden": "2", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"},
                "Estudiante_42": {"Orden": "3", "Primer_Apellido": "Herrera", "Segundo_Apellido": "Jimenez", "Nombre": "Luis", "ID": "3660580-4"}
            },
            "Orden_15": {
                "Estudiante_43": {"Orden": "4", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_44": {"Orden": "5", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"},
                "Estudiante_45": {"Orden": "6", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"}
            },
            "Orden_16": {
                "Estudiante_46": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_47": {"Orden": "2", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"},
                "Estudiante_48": {"Orden": "3", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"}
            },
            "Orden_17": {
                "Estudiante_49": {"Orden": "3", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"},
                "Estudiante_50": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_51": {"Orden": "2", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"}
            },
            "Orden_18": {
                "Estudiante_52": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_53": {"Orden": "4", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_54": {"Orden": "5", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"}
            },
            "Orden_19": {
                "Estudiante_55": {"Orden": "4", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_56": {"Orden": "5", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"},
                "Estudiante_57": {"Orden": "6", "Primer_Apellido": "Herrera", "Segundo_Apellido": "Jimenez", "Nombre": "Luis", "ID": "3660580-4"}
            },
            "Orden_20": {
                "Estudiante_58": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_59": {"Orden": "2", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"},
                "Estudiante_60": {"Orden": "3", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"}
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

        # Contador para llevar el seguimiento de los órdenes
        contador_orden = 1

        # Variable de bandera para verificar si todos los datos son correctos
        todos_correctos = True

        for criterio in criterios:
            print(f"■■■■■-Inicio Asignación de criterio {criterio}-■■■■■")
            
            # Seleccionar Criterio
            self.driver.find_element(By.XPATH, Campos.BotonDespliegueCriterio).click()
            self.driver.implicitly_wait(20)
            time.sleep(2)
            self.driver.find_element(By.XPATH, criterio).click()
            self.driver.implicitly_wait(20)
            time.sleep(2)
            
            # Aceptar el criterio seleccionado
            self.driver.find_element(By.XPATH, Campos.botonContinuar).click()
            self.driver.implicitly_wait(20)
            time.sleep(2)            
            
            # Verificar mensaje de éxito
            assert Campos.MensajeExito in self.driver.find_element(By.XPATH, Campos.LabelAceptar).text, "Mensaje Erroneo"
                        
            print(f"■■■■■-Fin asignación de criterio {criterio}-■■■■■")
            
            for ordenamiento in ordenamientos:
                print(f"■■■■■-Aplicando ordenamiento {ordenamiento}-■■■■■")
                
                # Seleccionar Ordenamiento
                self.driver.find_element(By.XPATH, Campos.BotonDespliegueOrdenamiento).click()
                self.driver.implicitly_wait(20)
                time.sleep(2)
                self.driver.find_element(By.XPATH, ordenamiento).click()
                self.driver.implicitly_wait(20)
                time.sleep(2)
                
                # Aceptar el ordenamiento seleccionado
                self.driver.find_element(By.XPATH, Campos.botonContinuar).click()
                self.driver.implicitly_wait(20)
                time.sleep(2) 
                
                # Verificar mensaje de éxito
                assert Campos.MensajeExito in self.driver.find_element(By.XPATH, Campos.LabelAceptar).text, "Mensaje Erroneo"
                        
                print(f"■■■■■-Fin Aplicando ordenamiento {ordenamiento}-■■■■■")
                
                # Acceder a la sección de cursos
                self.AccesoCrusos()
                self.driver.implicitly_wait(20)
                time.sleep(2)
                    
                # Validar la información de los alumnos según el orden actual
                orden_key = f"Orden_{contador_orden}"  # Orden_1, Orden_2, etc.
                alumnos = DatosAlumnos.get(orden_key, {})
                
                print(f"■■■■■-Validando Información del {orden_key}-■■■■■")
                
                for alumno_key, alumno in alumnos.items():
                    print(f"■■■■■-Validando Información del {alumno_key}-■■■■■")
                    
                    try:
                        # Esperar a que la tabla esté presente en el DOM y sea visible
                        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//table[@id='filterTbl']")))
                    
                        # Encontrar todas las filas de la tabla
                        filas = self.driver.find_elements(By.XPATH, "(//tbody)[1]/tr")
                    
                        encontrado = False
                        
                        # Iterar sobre cada fila para buscar la información específica
                        for fila in filas:
                            # Obtener el texto de cada columna en la fila
                            columnas = fila.find_elements(By.TAG_NAME, "td")
                            texto_columnas = [columna.text.strip() for columna in columnas]
                        
                            # Validar si la fila coincide con el alumno actual
                            if (alumno["Orden"] == texto_columnas[0] and
                                alumno["Primer_Apellido"] == texto_columnas[1] and
                                alumno["Segundo_Apellido"] == texto_columnas[2] and
                                alumno["Nombre"] == texto_columnas[3] and
                                alumno["ID"] == texto_columnas[4]):
                                encontrado = True
                                print(f"■■■■■-Información del alumno {alumno['Nombre']} es correcta ✅✅✅ -■■■■■")
                                break  # Salir del bucle si se encuentra el alumno
                        
                        # Si no se encontró la información, mostrar errores detallados
                        if not encontrado:
                            print(f"■■■■■-Error: La Información del alumno {alumno['Nombre']} es Incorrecta ❌❌❌ -■■■■■")
                            # Comparar los datos esperados con los datos de la primera fila (o cualquier fila)
                            #primera_fila = filas[0].find_elements(By.TAG_NAME, "td")
                            #texto_primera_fila = [columna.text.strip() for columna in primera_fila]
                            
                            #if alumno["Orden"] != texto_primera_fila[0]:
                            #    print(f"  - Campo 'Orden' incorrecto. Esperado: {alumno['Orden']}, Encontrado: {texto_primera_fila[0]}")
                            #if alumno["Primer_Apellido"] != texto_primera_fila[1]:
                            #    print(f"  - Campo 'Primer_Apellido' incorrecto. Esperado: {alumno['Primer_Apellido']}, Encontrado: {texto_primera_fila[1]}")
                            #if alumno["Segundo_Apellido"] != texto_primera_fila[2]:
                            #    print(f"  - Campo 'Segundo_Apellido' incorrecto. Esperado: {alumno['Segundo_Apellido']}, Encontrado: {texto_primera_fila[2]}")
                            #if alumno["Nombre"] != texto_primera_fila[3]:
                            #   print(f"  - Campo 'Nombre' incorrecto. Esperado: {alumno['Nombre']}, Encontrado: {texto_primera_fila[3]}")
                            #if alumno["ID"] != texto_primera_fila[4]:
                            #    print(f"  - Campo 'ID' incorrecto. Esperado: {alumno['ID']}, Encontrado: {texto_primera_fila[4]}")
                            
                            todos_correctos = False  # Cambiar la bandera a False
                    
                    except Exception as e:
                        print(f"■■■■■-Error al validar información del alumno: {str(e)} ❌❌❌ -■■■■■")
                        todos_correctos = False  # Cambiar la bandera a False
                    
                    print(f"■■■■■-Fin Validando Información del {alumno_key}-■■■■■")
                
                print(f"■■■■■-Fin Validando Información del {orden_key}-■■■■■")
                
                # Incrementar el contador de órdenes
                contador_orden += 1
                
                # Regresar a la sección de nóminas
                self.AccesoNominas()
                self.driver.implicitly_wait(20)
                time.sleep(2)

        # Verificar si todos los datos fueron correctos
        if todos_correctos:
            print("■■■■■-El script se ejecutó con éxito. Todos los datos son correctos ✅✅✅ -■■■■■")
        else:
            print("■■■■■-El script falló. Al menos un dato es incorrecto ✅✅✅ -■■■■■")
            raise AssertionError("■■■■■-Al menos un dato es incorrecto ❌❌❌ -■■■■■")
        
        
        
        
    def pruebas3filas(self, Orden, Primer_Apellido, Segundo_Apellido, Nombre, ID):
            DatosAlumnos = {
                "Orden_1": {
                "Estudiante_1": {"Orden": "1", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"},
                "Estudiante_2": {"Orden": "2", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_3": {"Orden": "3", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"}
            },
            "Orden_2": {
                "Estudiante_4": {"Orden": "1", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"},
                "Estudiante_5": {"Orden": "2", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_4": {"Orden": "3", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"}
            },
            "Orden_3": {
                "Estudiante_7": {"Orden": "2", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_8": {"Orden": "6", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_9": {"Orden": "5", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"}
            },
            "Orden_4": {
                "Estudiante_10": {"Orden": "6", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_11": {"Orden": "5", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"},
                "Estudiante_12": {"Orden": "4", "Primer_Apellido": "Herrera", "Segundo_Apellido": "Jimenez", "Nombre": "Luis", "ID": "3660580-4"}
            },
            "Orden_5": {
                "Estudiante_13": {"Orden": "2", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_14": {"Orden": "3", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"},
                "Estudiante_15": {"Orden": "1", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"}
            },
            "Orden_6": {
                "Estudiante_16": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_17": {"Orden": "2", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_18": {"Orden": "3", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"}
            },
            "Orden_7": {
                "Estudiante_19": {"Orden": "6", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"},
                "Estudiante_20": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_21": {"Orden": "5", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"}
            },
            "Orden_8": {
                "Estudiante_22": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_23": {"Orden": "2", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_24": {"Orden": "3", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"}
            },
            "Orden_9": {
                "Estudiante_25": {"Orden": "2", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_26": {"Orden": "3", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"},
                "Estudiante_27": {"Orden": "4", "Primer_Apellido": "Herrera", "Segundo_Apellido": "Jimenez", "Nombre": "Luis", "ID": "3660580-4"}
            },
            "Orden_10": {
                "Estudiante_28": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_29": {"Orden": "5", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"},
                "Estudiante_30": {"Orden": "6", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"}
            },
            "Orden_11": {
                "Estudiante_31": {"Orden": "1", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_32": {"Orden": "2", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"},
                "Estudiante_33": {"Orden": "3", "Primer_Apellido": "Herrera", "Segundo_Apellido": "Jimenez", "Nombre": "Luis", "ID": "3660580-4"}
            },
            "Orden_12": {
                "Estudiante_34": {"Orden": "6", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"},
                "Estudiante_35": {"Orden": "4", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_36": {"Orden": "5", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"}
            },
            "Orden_13": {
                "Estudiante_37": {"Orden": "4", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_38": {"Orden": "1", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_39": {"Orden": "2", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"}
            },
            "Orden_14": {
                "Estudiante_40": {"Orden": "1", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_41": {"Orden": "2", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"},
                "Estudiante_42": {"Orden": "3", "Primer_Apellido": "Herrera", "Segundo_Apellido": "Jimenez", "Nombre": "Luis", "ID": "3660580-4"}
            },
            "Orden_15": {
                "Estudiante_43": {"Orden": "4", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_44": {"Orden": "5", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"},
                "Estudiante_45": {"Orden": "6", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"}
            },
            "Orden_16": {
                "Estudiante_46": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_47": {"Orden": "2", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"},
                "Estudiante_48": {"Orden": "3", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"}
            },
            "Orden_17": {
                "Estudiante_49": {"Orden": "3", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"},
                "Estudiante_50": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_51": {"Orden": "2", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"}
            },
            "Orden_18": {
                "Estudiante_52": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_53": {"Orden": "4", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_54": {"Orden": "5", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"}
            },
            "Orden_19": {
                "Estudiante_55": {"Orden": "4", "Primer_Apellido": "Ramirez", "Segundo_Apellido": "Torres", "Nombre": "Carlos", "ID": "19270619-K"},
                "Estudiante_56": {"Orden": "5", "Primer_Apellido": "Martinez", "Segundo_Apellido": "Sanchez", "Nombre": "Juan", "ID": "8571154-7"},
                "Estudiante_57": {"Orden": "6", "Primer_Apellido": "Herrera", "Segundo_Apellido": "Jimenez", "Nombre": "Luis", "ID": "3660580-4"}
            },
            "Orden_20": {
                "Estudiante_58": {"Orden": "1", "Primer_Apellido": "Fernandez", "Segundo_Apellido": "Garcia", "Nombre": "Ana", "ID": "14119475-5"},
                "Estudiante_59": {"Orden": "2", "Primer_Apellido": "Gonzalez", "Segundo_Apellido": "Lopez", "Nombre": "Maria", "ID": "2987505-7"},
                "Estudiante_60": {"Orden": "3", "Primer_Apellido": "Diaz", "Segundo_Apellido": "Mendoza", "Nombre": "Sofia", "ID": "2181782-1"}
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

            # Contador para llevar el seguimiento de los órdenes
            contador_orden = 1

            # Variable de bandera para verificar si todos los datos son correctos
            todos_correctos = True

            for criterio in criterios:
                print(f"■■■■■-Inicio Asignación de criterio {criterio}-■■■■■")
                
                # Seleccionar Criterio
                self.driver.find_element(By.XPATH, Campos.BotonDespliegueCriterio).click()
                self.driver.implicitly_wait(20)
                time.sleep(2)
                self.driver.find_element(By.XPATH, criterio).click()
                self.driver.implicitly_wait(20)
                time.sleep(2)
                
                # Aceptar el criterio seleccionado
                self.driver.find_element(By.XPATH, Campos.botonContinuar).click()
                self.driver.implicitly_wait(20)
                time.sleep(2)            
                
                # Verificar mensaje de éxito
                assert Campos.MensajeExito in self.driver.find_element(By.XPATH, Campos.LabelAceptar).text, "Mensaje Erroneo"
                            
                print(f"■■■■■-Fin asignación de criterio {criterio}-■■■■■")
                
                for ordenamiento in ordenamientos:
                    print(f"■■■■■-Aplicando ordenamiento {ordenamiento}-■■■■■")
                    
                    # Seleccionar Ordenamiento
                    self.driver.find_element(By.XPATH, Campos.BotonDespliegueOrdenamiento).click()
                    self.driver.implicitly_wait(20)
                    time.sleep(2)
                    self.driver.find_element(By.XPATH, ordenamiento).click()
                    self.driver.implicitly_wait(20)
                    time.sleep(2)
                    
                    # Aceptar el ordenamiento seleccionado
                    self.driver.find_element(By.XPATH, Campos.botonContinuar).click()
                    self.driver.implicitly_wait(20)
                    time.sleep(2) 
                    
                    # Verificar mensaje de éxito
                    assert Campos.MensajeExito in self.driver.find_element(By.XPATH, Campos.LabelAceptar).text, "Mensaje Erroneo"
                            
                    print(f"■■■■■-Fin Aplicando ordenamiento {ordenamiento}-■■■■■")
                    
                    # Acceder a la sección de cursos
                    self.AccesoCrusos()
                    self.driver.implicitly_wait(20)
                    time.sleep(2)
                        
                    # Validar la información de los alumnos según el orden actual
                    orden_key = f"Orden_{contador_orden}"  # Orden_1, Orden_2, etc.
                    alumnos = DatosAlumnos.get(orden_key, {})

                    print(f"■■■■■-Validando Información del {orden_key}-■■■■■")

                    for alumno_key, alumno in alumnos.items():
                        print(f"■■■■■-Validando Información del {alumno_key}-■■■■■")
                        
                        try:
                            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//table[@id='filterTbl']")))
                            filas = self.driver.find_elements(By.XPATH, "(//tbody)[1]/tr")
                            
                            # Limitar la validación a las primeras 3 filas
                            primeras_tres_filas = filas[:3]  # <-- Modificación clave
                            encontrado = False
                            
                            for fila in primeras_tres_filas:  # <-- Solo procesa las 3 primeras
                                columnas = fila.find_elements(By.TAG_NAME, "td")
                                texto_columnas = [columna.text.strip() for columna in columnas]
                                
                                if (alumno["Orden"] == texto_columnas[0] and
                                    alumno["Primer_Apellido"] == texto_columnas[1] and
                                    alumno["Segundo_Apellido"] == texto_columnas[2] and
                                    alumno["Nombre"] == texto_columnas[3] and
                                    alumno["ID"] == texto_columnas[4]):
                                    encontrado = True
                                    print(f"■■■■■-Información del alumno {alumno['Nombre']} es correcta ✅✅✅ -■■■■■")
                                    break
                            
                            if not encontrado:
                                print(f"■■■■■-Error: La Información del {alumno['Nombre']} en el {orden_key} es Incorrecta ❌❌❌ -■■■■■")
                                # Comparar con las primeras 3 filas
                                for idx, fila in enumerate(primeras_tres_filas, 1):
                                    columnas_fila = fila.find_elements(By.TAG_NAME, "td")
                                    texto_fila = [col.text.strip() for col in columnas_fila]
                                    print(f"Datos fila {idx}: {texto_fila}")
                                    
                                todos_correctos = False
                        except Exception as e:
                            print(f"■■■■■-Error al validar información del alumno: {str(e)} ❌❌❌ -■■■■■")
                            todos_correctos = False  # Cambiar la bandera a False
                        
                        print(f"■■■■■-Fin Validando Información del {alumno_key}-■■■■■")
                    
                    print(f"■■■■■-Fin Validando Información del {orden_key}-■■■■■")
                    
                    # Incrementar el contador de órdenes
                    contador_orden += 1
                    
                    # Regresar a la sección de nóminas
                    self.AccesoNominas()
                    self.driver.implicitly_wait(20)
                    time.sleep(2)

            # Verificar si todos los datos fueron correctos
            if todos_correctos:
                print("■■■■■-El script se ejecutó con éxito. Todos los datos son correctos ✅✅✅ -■■■■■")
            else:
                print("■■■■■-El script falló. Al menos un dato es incorrecto ✅✅✅ -■■■■■")
                raise AssertionError("■■■■■-Al menos un dato es incorrecto ❌❌❌ -■■■■■")