# Campos 

# Inicio de Sesion
Usuario = "Steven Pruebas Arias"
Colegio = "Colegio automatización Chile"
Rol = "ADMINISTRADOR"
Email = "//input[@placeholder='ejemplo@colegium.com']"
Contraseña = "//input[@placeholder='······']"
BotonLogin = "//button[normalize-space()='Iniciar sesión']"
NombreColegio = "(//p[@class='ml-1 mb-0 title'][normalize-space()='Colegio automatización Chile'])[1]"
NombreUsuario = "(//p[@class='mb-0 title'])[1]"
NombreRolAdmin = "(//span[@class='mb-0 sub-title'])[1]"    

#Cierre de sesion
SimboloMenu = "//i[@class='clg clg-select-abajo']"
CerrarSesion = "//button[normalize-space()='Cerrar Sesión']"

#Configuracion Nominas
Configuracion = "//span[normalize-space()='Configuración']"
CerrarModal = "//button[normalize-space()='Cerrar']"
BotonConfiguracion = "//a[@href='administrador/configuracionColegio']//div[@class='grid-item-wrapper']//div[@class='grid-item-container']"
BotonNominas = "//a[@href='administrador/configuracion_numero_lista']"
NombreNominas = "//h2[normalize-space()='Nóminas']"
SeccionNominas = "Nóminas"

#Configuración Nóminas
BotonDespliegueCriterio = "(//i[@class='clg-ds-angle-down tw-text-lg tw-mr-1 tw-font-bold tw-transition-all tw-text-primary-500'])[1]"
BotonDespliegueOrdenamiento = "(//i[@class='clg-ds-angle-down tw-text-lg tw-mr-1 tw-font-bold tw-transition-all tw-text-primary-500'])[2]"
botonContinuar = "//button[normalize-space()='Continuar']"
LabelAceptar = "//p[@class='gris mb-0']"
MensajeExito = "Se regeneraron los números de lista exitosamente."

#Criterios
AZPrimerApellido = "(//span[@class='tw-text-sm'][normalize-space()='A-Z Primer apellido'])[1]"
AZNombre = "(//span[contains(text(),'A-Z Nombre')])[1]"
AZVaronesMujeres = "(//span[@class='tw-text-sm'][normalize-space()='A-Z Varones - Mujeres'])[1]"
AZMjeresVarones = "(//span[@class='tw-text-sm'][normalize-space()='A-Z Mujeres - Varones'])[1]"

#Ordenamientos
NumeroDeLista = "(//span[normalize-space()='Número de lista'])[1]"
AZOPrimerApellido = "(//span[@class='tw-text-sm'][normalize-space()='A-Z Primer apellido'])[2]"
AZONombre = "//tbody/tr[2]/td[2]/div[1]/div[1]/div[1]/ul[1]/li[3]/button[1]/div[1]/span[1]"
AZOVaronesMujeres = "(//span[@class='tw-text-sm'][normalize-space()='A-Z Varones - Mujeres'])[2]"
AZOMujeresVarones = "(//span[@class='tw-text-sm'][normalize-space()='A-Z Mujeres - Varones'])[2]"

#Campos Cursos
botonCursos = "//span[normalize-space()='Cursos']"
SecciónCursos = "//a[contains(text(),'Cursos')]"
NombreCursos = "Cursos"
CursoPrimero = "//td[normalize-space()='Enseñanza Básica']"
CursoItem = "//span[normalize-space()='1º Primero-Basico-SA']"
CursoNombre = "1º Primero-Basico-SA"
