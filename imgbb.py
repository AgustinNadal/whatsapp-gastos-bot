import requests
import base64
from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.getenv("IMGBB_API_KEY")

def subir_imagen_imgbb(path):
    if not API_KEY:
        print("Error: La variable de entorno IMGBB_API_KEY no está definida.")
        return None

    if not os.path.isfile(path):
        print(f"Error: El archivo {path} no existe.")
        return None

    with open(path, "rb") as f:
        imagen_data = f.read()

    encoded_image = base64.b64encode(imagen_data).decode('utf-8')

    payload = {
        "key": API_KEY,
        "image": encoded_image,
    }

    url = "https://api.imgbb.com/1/upload"
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        json_res = response.json()
        return json_res['data']['url']
    else:
        print(f"Error al subir la imagen: {response.status_code} - {response.text}")
        return None

