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
botonDespliegueCriterio = "//tbody/tr[1]/td[2]/div[1]/div[1]/div[1]/button[1]/div[1]/i[1]"
CriterioApellidpAZ = "//tbody/tr[1]/td[2]/div[1]/div[1]/div[1]/ul[1]/li[1]/button[1]"
botonContinuarCriterio = "//button[normalize-space()='Continuar']"
LabelAceptar = "//p[@class='gris mb-0']"
MensajeExito = "Se regeneraron los números de lista exitosamente."

#Campos Cursos
botonCursos = "//span[normalize-space()='Cursos']"
SecciónCursos = "//a[contains(text(),'Cursos')]"
NombreCursos = "Cursos"
CursoPrimero = "//td[normalize-space()='Enseñanza Básica']"
CursoItem = "//span[normalize-space()='1º Primero-Basico-SA']"
CursoNombre = "1º Primero-Basico-SA"
