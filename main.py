import pymongo
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://consultaweb.ant.gob.ec/PortalWEB/paginas/clientes/clp_criterio_consulta.jsp")

# Inicializamos la conexión a MongoDB
cliente = pymongo.MongoClient('localhost', 27017)
db = cliente['PruebaFinal']
base = db['citaciones']

try:
    # Buscamos el selector deseado
    dropdown = driver.find_element(By.CSS_SELECTOR, '#ps_tipo_identificacion')
    # debemos seleccionar un dropdown
    select = Select(dropdown)
    # a traves del indice seleccionamos el correspondiente a la cedula para este caso
    select.select_by_index(3)
    # Identificamos el campo donde se ingresa el texto y agregamos el texto deseado
    text_field = driver.find_element(By.CSS_SELECTOR, '#ps_identificacion')
    text_field.send_keys("1715335004")
    # buscamos el boton y damos click para obtener la consulta
    consultar_button = driver.find_element(By.CSS_SELECTOR, '#frm_consulta > div > a > img')
    consultar_button.click()

    # Procedemos con los resultados de la información desde el navegador

    tablaresultado = driver.find_element(By.CSS_SELECTOR, '#gview_list10 > div.ui-state-default.ui-jqgrid-hdiv > div > table')

    # Encontramos todas las filas de la tabla
    filas = tablaresultado.find_elements(By.TAG_NAME, 'tr')

    # Iteramos a través de las filas de la tabla
    for fila in filas[1:]:  # Comenzamos desde la segunda fila para omitir los encabezados
        # Encontramos las celdas que contiene la tabla
        celdas = fila.find_elements(By.TAG_NAME, 'td')
        # Extrae los valores de las celdas "orden", "fecha" y "nombre"
        infraccion = celdas[0].text
        entidad = celdas[1].text
        citacion = celdas[2].text
        placa = celdas[3].text
        fechaemision = celdas[4].text
        fechanotificacion = celdas[5].text
        puntos = celdas[6].text
        sancion = celdas[7].text
        multa = celdas[8].text
        remision = celdas[9].text
        totalpagar = celdas[10].text
        articulo = celdas[11].text

    # Creamos un diccionario con los datos
    registro = {
    'infraccion': infraccion,
    'entidad': entidad,
    'citacion': citacion,
    'placa': placa,
    'fechaemision': fechaemision,
    'fechanotificacion': fechanotificacion,
    'sancion': sancion,
    'puntos': puntos,
    'multa': multa,
    'remision': remision,
    'totalpagar': totalpagar,
    'articulo': articulo
    }

    # Inserta el documento en la colección de MongoDB
    base.insert_one(registro)

except Exception as e:
    print(f"La data ingresada no es correcta o no existen registros con esta solicitud")

finally:
    # Cerramos el navegador al finalizar
    driver.close()