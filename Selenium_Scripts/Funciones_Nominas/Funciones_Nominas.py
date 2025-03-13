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
                "Estudiante_1": {
                    "Orden": "1",
                    "Primer_Apellido": "Diaz",
                    "Segundo_Apellido": "Mendoza",
                    "Nombre": "Sofia",
                    "ID": "2181782-1"
                },
                "Estudiante_2": {
                    "Orden": "2",
                    "Primer_Apellido": "Fernandez",
                    "Segundo_Apellido": "Garcia",
                    "Nombre": "Ana",
                    "ID": "14119475-5"
                },
                "Estudiante_3": {
                    "Orden": "5",
                    "Primer_Apellido": "Martinez",
                    "Segundo_Apellido": "Sanchez",
                    "Nombre": "Juan",
                    "ID": "8571154-7"
                }
            },
            "Orden_2": {
                "Estudiante_4": {
                    "Orden": "1",
                    "Primer_Apellido": "Diaz",
                    "Segundo_Apellido": "Mendoza",
                    "Nombre": "Sofia",
                    "ID": "2181782-1"
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
            },
            "Orden_3": {
                "Estudiante_7": {
                    "Orden": "7",
                    "Primer_Apellido": "Gonzalez",
                    "Segundo_Apellido": "Sanchez",
                    "Nombre": "Laura",
                    "ID": "2181782-7"
                },
                "Estudiante_8": {
                    "Orden": "8",
                    "Primer_Apellido": "Ramirez",
                    "Segundo_Apellido": "Torres",
                    "Nombre": "Pedro",
                    "ID": "2181782-8"
                },
                "Estudiante_9": {
                    "Orden": "9",
                    "Primer_Apellido": "Flores",
                    "Segundo_Apellido": "Diaz",
                    "Nombre": "Lucia",
                    "ID": "2181782-9"
                }
            },
            "Orden_4": {
                "Estudiante_10": {
                    "Orden": "10",
                    "Primer_Apellido": "Torres",
                    "Segundo_Apellido": "Gutierrez",
                    "Nombre": "Diego",
                    "ID": "2181782-10"
                },
                "Estudiante_11": {
                    "Orden": "11",
                    "Primer_Apellido": "Vargas",
                    "Segundo_Apellido": "Castillo",
                    "Nombre": "Elena",
                    "ID": "2181782-11"
                },
                "Estudiante_12": {
                    "Orden": "12",
                    "Primer_Apellido": "Rojas",
                    "Segundo_Apellido": "Mendez",
                    "Nombre": "Fernando",
                    "ID": "2181782-12"
                }
            },
            "Orden_5": {
                "Estudiante_13": {
                    "Orden": "13",
                    "Primer_Apellido": "Morales",
                    "Segundo_Apellido": "Ortega",
                    "Nombre": "Gabriela",
                    "ID": "2181782-13"
                },
                "Estudiante_14": {
                    "Orden": "14",
                    "Primer_Apellido": "Silva",
                    "Segundo_Apellido": "Paredes",
                    "Nombre": "Hector",
                    "ID": "2181782-14"
                },
                "Estudiante_15": {
                    "Orden": "15",
                    "Primer_Apellido": "Castro",
                    "Segundo_Apellido": "Rios",
                    "Nombre": "Isabel",
                    "ID": "2181782-15"
                }
            },
            "Orden_6": {
                "Estudiante_16": {
                    "Orden": "16",
                    "Primer_Apellido": "Navarro",
                    "Segundo_Apellido": "Fuentes",
                    "Nombre": "Javier",
                    "ID": "2181782-16"
                },
                "Estudiante_17": {
                    "Orden": "17",
                    "Primer_Apellido": "Molina",
                    "Segundo_Apellido": "Carrasco",
                    "Nombre": "Karina",
                    "ID": "2181782-17"
                },
                "Estudiante_18": {
                    "Orden": "18",
                    "Primer_Apellido": "Perez",
                    "Segundo_Apellido": "Aguilar",
                    "Nombre": "Luis",
                    "ID": "2181782-18"
                }
            },
            "Orden_7": {
                "Estudiante_19": {
                    "Orden": "19",
                    "Primer_Apellido": "Gomez",
                    "Segundo_Apellido": "Vega",
                    "Nombre": "Monica",
                    "ID": "2181782-19"
                },
                "Estudiante_20": {
                    "Orden": "20",
                    "Primer_Apellido": "Herrera",
                    "Segundo_Apellido": "Miranda",
                    "Nombre": "Nicolas",
                    "ID": "2181782-20"
                },
                "Estudiante_21": {
                    "Orden": "21",
                    "Primer_Apellido": "Luna",
                    "Segundo_Apellido": "Reyes",
                    "Nombre": "Olga",
                    "ID": "2181782-21"
                }
            },
            "Orden_8": {
                "Estudiante_22": {
                    "Orden": "22",
                    "Primer_Apellido": "Soto",
                    "Segundo_Apellido": "Cortes",
                    "Nombre": "Pablo",
                    "ID": "2181782-22"
                },
                "Estudiante_23": {
                    "Orden": "23",
                    "Primer_Apellido": "Campos",
                    "Segundo_Apellido": "Santos",
                    "Nombre": "Quintin",
                    "ID": "2181782-23"
                },
                "Estudiante_24": {
                    "Orden": "24",
                    "Primer_Apellido": "Guerrero",
                    "Segundo_Apellido": "Lagos",
                    "Nombre": "Rosa",
                    "ID": "2181782-24"
                }
            },
            "Orden_9": {
                "Estudiante_25": {
                    "Orden": "25",
                    "Primer_Apellido": "Rios",
                    "Segundo_Apellido": "Mendoza",
                    "Nombre": "Sergio",
                    "ID": "2181782-25"
                },
                "Estudiante_26": {
                    "Orden": "26",
                    "Primer_Apellido": "Vega",
                    "Segundo_Apellido": "Castro",
                    "Nombre": "Teresa",
                    "ID": "2181782-26"
                },
                "Estudiante_27": {
                    "Orden": "27",
                    "Primer_Apellido": "Miranda",
                    "Segundo_Apellido": "Navarro",
                    "Nombre": "Ulises",
                    "ID": "2181782-27"
                }
            },
            "Orden_10": {
                "Estudiante_28": {
                    "Orden": "28",
                    "Primer_Apellido": "Fuentes",
                    "Segundo_Apellido": "Morales",
                    "Nombre": "Valeria",
                    "ID": "2181782-28"
                },
                "Estudiante_29": {
                    "Orden": "29",
                    "Primer_Apellido": "Carrasco",
                    "Segundo_Apellido": "Silva",
                    "Nombre": "Walter",
                    "ID": "2181782-29"
                },
                "Estudiante_30": {
                    "Orden": "30",
                    "Primer_Apellido": "Aguilar",
                    "Segundo_Apellido": "Rojas",
                    "Nombre": "Ximena",
                    "ID": "2181782-30"
                }
            },
            "Orden_11": {
                "Estudiante_31": {
                    "Orden": "31",
                    "Primer_Apellido": "Paredes",
                    "Segundo_Apellido": "Campos",
                    "Nombre": "Yolanda",
                    "ID": "2181782-31"
                },
                "Estudiante_32": {
                    "Orden": "32",
                    "Primer_Apellido": "Ortega",
                    "Segundo_Apellido": "Guerrero",
                    "Nombre": "Zacarias",
                    "ID": "2181782-32"
                },
                "Estudiante_33": {
                    "Orden": "33",
                    "Primer_Apellido": "Santos",
                    "Segundo_Apellido": "Luna",
                    "Nombre": "Alejandro",
                    "ID": "2181782-33"
                }
            },
            "Orden_12": {
                "Estudiante_34": {
                    "Orden": "34",
                    "Primer_Apellido": "Lagos",
                    "Segundo_Apellido": "Soto",
                    "Nombre": "Beatriz",
                    "ID": "2181782-34"
                },
                "Estudiante_35": {
                    "Orden": "35",
                    "Primer_Apellido": "Cortes",
                    "Segundo_Apellido": "Vega",
                    "Nombre": "Carlos",
                    "ID": "2181782-35"
                },
                "Estudiante_36": {
                    "Orden": "36",
                    "Primer_Apellido": "Reyes",
                    "Segundo_Apellido": "Miranda",
                    "Nombre": "Diana",
                    "ID": "2181782-36"
                }
            },
            "Orden_13": {
                "Estudiante_37": {
                    "Orden": "37",
                    "Primer_Apellido": "Mendoza",
                    "Segundo_Apellido": "Fuentes",
                    "Nombre": "Eduardo",
                    "ID": "2181782-37"
                },
                "Estudiante_38": {
                    "Orden": "38",
                    "Primer_Apellido": "Castro",
                    "Segundo_Apellido": "Carrasco",
                    "Nombre": "Fabiola",
                    "ID": "2181782-38"
                },
                "Estudiante_39": {
                    "Orden": "39",
                    "Primer_Apellido": "Navarro",
                    "Segundo_Apellido": "Aguilar",
                    "Nombre": "Gabriel",
                    "ID": "2181782-39"
                }
            },
            "Orden_14": {
                "Estudiante_40": {
                    "Orden": "40",
                    "Primer_Apellido": "Morales",
                    "Segundo_Apellido": "Paredes",
                    "Nombre": "Hilda",
                    "ID": "2181782-40"
                },
                "Estudiante_41": {
                    "Orden": "41",
                    "Primer_Apellido": "Silva",
                    "Segundo_Apellido": "Ortega",
                    "Nombre": "Ignacio",
                    "ID": "2181782-41"
                },
                "Estudiante_42": {
                    "Orden": "42",
                    "Primer_Apellido": "Rojas",
                    "Segundo_Apellido": "Santos",
                    "Nombre": "Jazmin",
                    "ID": "2181782-42"
                }
            },
            "Orden_15": {
                "Estudiante_43": {
                    "Orden": "43",
                    "Primer_Apellido": "Campos",
                    "Segundo_Apellido": "Lagos",
                    "Nombre": "Kevin",
                    "ID": "2181782-43"
                },
                "Estudiante_44": {
                    "Orden": "44",
                    "Primer_Apellido": "Guerrero",
                    "Segundo_Apellido": "Cortes",
                    "Nombre": "Laura",
                    "ID": "2181782-44"
                },
                "Estudiante_45": {
                    "Orden": "45",
                    "Primer_Apellido": "Luna",
                    "Segundo_Apellido": "Reyes",
                    "Nombre": "Manuel",
                    "ID": "2181782-45"
                }
            },
            "Orden_16": {
                "Estudiante_46": {
                    "Orden": "46",
                    "Primer_Apellido": "Soto",
                    "Segundo_Apellido": "Mendoza",
                    "Nombre": "Natalia",
                    "ID": "2181782-46"
                },
                "Estudiante_47": {
                    "Orden": "47",
                    "Primer_Apellido": "Vega",
                    "Segundo_Apellido": "Castro",
                    "Nombre": "Oscar",
                    "ID": "2181782-47"
                },
                "Estudiante_48": {
                    "Orden": "48",
                    "Primer_Apellido": "Miranda",
                    "Segundo_Apellido": "Navarro",
                    "Nombre": "Patricia",
                    "ID": "2181782-48"
                }
            },
            "Orden_17": {
                "Estudiante_49": {
                    "Orden": "49",
                    "Primer_Apellido": "Fuentes",
                    "Segundo_Apellido": "Morales",
                    "Nombre": "Quetzal",
                    "ID": "2181782-49"
                },
                "Estudiante_50": {
                    "Orden": "50",
                    "Primer_Apellido": "Carrasco",
                    "Segundo_Apellido": "Silva",
                    "Nombre": "Raul",
                    "ID": "2181782-50"
                },
                "Estudiante_51": {
                    "Orden": "51",
                    "Primer_Apellido": "Aguilar",
                    "Segundo_Apellido": "Rojas",
                    "Nombre": "Sara",
                    "ID": "2181782-51"
                }
            },
            "Orden_18": {
                "Estudiante_52": {
                    "Orden": "52",
                    "Primer_Apellido": "Paredes",
                    "Segundo_Apellido": "Campos",
                    "Nombre": "Tomas",
                    "ID": "2181782-52"
                },
                "Estudiante_53": {
                    "Orden": "53",
                    "Primer_Apellido": "Ortega",
                    "Segundo_Apellido": "Guerrero",
                    "Nombre": "Ursula",
                    "ID": "2181782-53"
                },
                "Estudiante_54": {
                    "Orden": "54",
                    "Primer_Apellido": "Santos",
                    "Segundo_Apellido": "Luna",
                    "Nombre": "Victor",
                    "ID": "2181782-54"
                }
            },
            "Orden_19": {
                "Estudiante_55": {
                    "Orden": "55",
                    "Primer_Apellido": "Lagos",
                    "Segundo_Apellido": "Soto",
                    "Nombre": "Wendy",
                    "ID": "2181782-55"
                },
                "Estudiante_56": {
                    "Orden": "56",
                    "Primer_Apellido": "Cortes",
                    "Segundo_Apellido": "Vega",
                    "Nombre": "Xavier",
                    "ID": "2181782-56"
                },
                "Estudiante_57": {
                    "Orden": "57",
                    "Primer_Apellido": "Reyes",
                    "Segundo_Apellido": "Miranda",
                    "Nombre": "Yolanda",
                    "ID": "2181782-57"
                }
            },
            "Orden_20": {
                "Estudiante_58": {
                    "Orden": "58",
                    "Primer_Apellido": "Mendoza",
                    "Segundo_Apellido": "Fuentes",
                    "Nombre": "Zoe",
                    "ID": "2181782-58"
                },
                "Estudiante_59": {
                    "Orden": "59",
                    "Primer_Apellido": "Castro",
                    "Segundo_Apellido": "Carrasco",
                    "Nombre": "Aaron",
                    "ID": "2181782-59"
                },
                "Estudiante_60": {
                    "Orden": "60",
                    "Primer_Apellido": "Navarro",
                    "Segundo_Apellido": "Aguilar",
                    "Nombre": "Bianca",
                    "ID": "2181782-60"
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