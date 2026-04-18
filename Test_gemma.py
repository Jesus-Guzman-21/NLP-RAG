# Note: Find why I can use the gemma embedding

#import os
#from sentence_transformers import SentenceTransformer
#
## Intenta cargar solo la estructura del modelo
#try:
#    model_id = "google/embedding-gemma-2b" # Asegúrate que sea el ID correcto
#    print(f"Intentando cargar {model_id}...")
#    
#    # Esto verificará si el modelo existe localmente o puede conectarse
#    model = SentenceTransformer(model_id, device="cpu")
#    
#    # Prueba de fuego: Generar un embedding de prueba
#    test_vector = model.encode(["Hola mundo"])
#    print(f"✅ Éxito. Tamaño del vector: {test_vector.shape[1]}")
#
#except Exception as e:
#    print(f"❌ Error: {e}")

#import os
#from dotenv import load_dotenv
#from huggingface_hub import login
#from transformers import AutoModel, AutoTokenizer
#
#load_dotenv()
#
## 1. Autenticación (Asegúrate de tener HF_TOKEN en tu .env)
#token = os.getenv("HF_TOKEN")
#if token:
#    login(token=token)
#else:
#    print("❌ No se encontró HF_TOKEN en el .env")
#
#model_id = "google/embedding-gemma-300m"
#
#try:
#    print(f"📥 Iniciando descarga de {model_id}...")
#    
#    # Descarga el tokenizador y el modelo
#    tokenizer = AutoTokenizer.from_pretrained(model_id)
#    model = AutoModel.from_pretrained(model_id)
#    
#    print("✅ Modelo descargado y guardado en caché correctamente.")
#    
#except Exception as e:
#    print(f"❌ Error durante la descarga: {e}")
#    print("\n💡 Tip: Verifica que hayas aceptado los términos de Gemma en Hugging Face Hub.")


import os
from dotenv import load_dotenv
from transformers import AutoModel, AutoTokenizer

load_dotenv()
mi_token = os.getenv("HF_TOKEN")

# Intenta con este ID que es el oficial y estable
model_id = "google/gemma-2b" 

try:
    print(f"🚀 Cargando tokenizador con autenticación...")
    # ES CRUCIAL PASAR EL TOKEN AQUÍ
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=mi_token)
    
    print(f"🚀 Cargando modelo...")
    model = AutoModel.from_pretrained(model_id, token=mi_token)
    
    print("✅ ¡Conectado y cargado exitosamente!")
except Exception as e:
    print(f"❌ Error: {e}")