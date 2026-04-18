# SQL RAG Agent con DuckDB y OpenAI

Sistema de **Text-to-SQL con RAG (Retrieval-Augmented Generation)** que permite hacer preguntas en lenguaje natural sobre una base de datos y obtener:

* Consulta SQL generada automáticamente
* Ejecución sobre DuckDB
* Respuesta final en lenguaje natural

---

## Características

*  Retrieval semántico con FAISS
*  Generación SQL con OpenAI
*  Ejecución directa en DuckDB
*  Interpretación de resultados con DataFrame Agent

---

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/Jesus-Guzman-21/NLP-RAG.git
cd NLP-RAG
```

Instala dependencias:

```bash
pip install -r requirements.txt
```

---

## Configuración

Crea un archivo `.env`:

```env
OPENAI_API_KEY=tu_api_key_aqui
```

---

## Uso

Ejecuta el programa principal:

```bash
python Reto_5_RAG.py
```

Luego escribe preguntas como:

```
¿Cuanto valen las ventas totales?
Enlista todos los productos con 0 existencias en el inventario.
```

---

## Flujo del sistema

1. Usuario hace una pregunta
2. RAG recupera tablas relevantes (FAISS + embeddings)
3. Se genera una consulta SQL
4. Se ejecuta en DuckDB
5. Se devuelve una respuesta en lenguaje natural

---

## Estructura del proyecto

```
NLP-RAG/
│
├── agents/
│   ├── SQL_RAG_Agent.py
│   └── DataFrame_Agent.py
│
├── data/
│   └── sql_dataset_bourbaki.json
│
├── database/
│   └── Reto_5_RAG_DB.duckdb
│
├── Reto_5_RAG.py
├── requirements.txt
└── README.md
```

---

## Tecnologías usadas

* FAISS (búsqueda vectorial)
* DuckDB (base de datos analítica)
* OpenAI API (LLM + embeddings)
* Pandas (manejo de datos)

---

## Limitaciones

* No soporta queries de escritura (INSERT, DELETE, etc.)
* Depende de la calidad del dataset JSON
* Requiere conexión a la API de OpenAI

---

## Futuras mejoras

* API con FastAPI
* Validación avanzada de SQL antes de ejecución en DuckDB
* Interfaz web

---

## Autor

Jesús Daniel Guzmán Valenzuela

---

## 📄 Licencia

MIT
