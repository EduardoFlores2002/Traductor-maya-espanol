import json  # Importa el módulo json

# Función para cargar un diccionario desde un archivo JSON
def load_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)  # Carga contenido del archivo json

# Carga los diccionarios de traducción desde archivos JSON específicos
maya_to_spanish = load_dictionary('data/maya_to_spanish.json')  # Carga el diccionario Maya a Español
spanish_to_maya = load_dictionary('data/spanish_to_maya.json')  # Carga el diccionario Español a Maya

# Función para traducir texto de Maya a Español
def translate_maya_to_spanish(text):
    words = text.lower().split()  # Divide el texto en palabras individuales
    translation = []
    for word in words:
        if word in maya_to_spanish:  # Verifica si la palabra está en el diccionario Maya a Español
            translation.append(maya_to_spanish[word])  # Agrega la traducción al resultado
        else:
            translation.append(word)  # Si la palabra no está en el diccionario, conserva la palabra original
    return " ".join(translation)  # Une las palabras traducidas en un solo texto y lo devuelve


def translate_spanish_to_maya(text):
    words = text.capitalize().split()  # pone mayusculas a la primer letra y divide el texto en palabras individuales 
    translation = []
    for word in words:
        if word in spanish_to_maya:  # Verifica si la palabra está en el diccionario Español a Maya
            translation.append(spanish_to_maya[word])  # Agrega la traducción al resultado
        else:
            translation.append(word)  # Si la palabra no está en el diccionario, conserva la palabra original
    return " ".join(translation)  # Une las palabras traducidas en un solo texto y lo devuelve

