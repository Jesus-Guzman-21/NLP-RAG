# SQL RAG Agent with DuckDB and OpenAI

Sistema de **Text-to-SQL basado en RAG (Retrieval-Augmented Generation)** que permite transformar consultas en lenguaje natural en consultas SQL ejecutables sobre una base de datos, retornando resultados interpretados en lenguaje natural.

---

## Descripción

El sistema combina recuperación semántica, generación de código SQL y ejecución sobre un motor analítico. A partir de una pregunta del usuario:

* Se identifican las tablas relevantes mediante embeddings y búsqueda vectorial
* Se genera una consulta SQL alineada con el esquema disponible
* Se ejecuta la consulta en DuckDB
* Se produce una respuesta final en lenguaje natural basada en los resultados

---

## Características

* Retrieval semántico mediante FAISS
* Generación de consultas SQL con OpenAI
* Ejecución directa sobre DuckDB
* Interpretación de resultados mediante un agente basado en DataFrames

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/Jesus-Guzman-21/NLP-RAG.git
cd NLP-RAG
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Configuración

Crear un archivo `.env` en la raíz del proyecto:

```env
OPENAI_API_KEY=tu_api_key_aqui
```

---

## Uso

Ejecutar el programa principal:

```bash
python Reto_5_RAG.py
```

Ejemplos de consultas:

```
¿Cuánto valen las ventas totales?
Enlista todos los productos con 0 existencias en el inventario.
```

---

## Flujo del sistema

1. El usuario realiza una consulta en lenguaje natural
2. El módulo RAG recupera las tablas más relevantes mediante embeddings
3. Se genera una consulta SQL condicionada al esquema disponible
4. La consulta se ejecuta en DuckDB
5. Se genera una respuesta en lenguaje natural a partir de los resultados

---

Estructura del proyecto
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
├── docs/
│   ├── benchmark_modelo_clasico.pdf
│   └── propuesta_proyecto.pdf
│
├── Reto_5_RAG.py
├── requirements.txt
└── README.md
```
---

## Benchmark y propuesta

En la carpeta `docs/` se incluye material complementario que documenta el análisis teórico del proyecto:

* **Benchmark alternativo con modelos clásicos de Machine Learning**
  Se propone un enfoque basado en clasificación de intenciones utilizando modelos como árboles de decisión o Random Forest, el cual actúa como línea base frente al sistema RAG.

* **Presentación de propuesta de aplicación**
  Se incluye una propuesta de aplicación práctica en el dominio de análisis de creativos y automatización con agentes de IA, donde se describe la problemática, los datos y un enfoque de modelado híbrido (ML clásico + LLMs).

Este material tiene como objetivo complementar la implementación con una perspectiva comparativa y aplicada.


## Tecnologías utilizadas

* FAISS — búsqueda vectorial
* DuckDB — motor de base de datos analítica
* OpenAI API — generación de texto y embeddings
* Pandas — manipulación de datos tabulares

---

## Limitaciones

* No se permiten operaciones de escritura (INSERT, UPDATE, DELETE, etc.)
* La precisión depende de la calidad y cobertura del dataset JSON
* Requiere conexión a la API de OpenAI

---

## Posibles mejoras

* Utilizar parámetros como overlapping y chunks para evitar saturar la ventana de contexto
* Validación previa de consultas SQL antes de su ejecución
* Persistencia del índice vectorial (FAISS)
* Desarrollo de una interfaz de usuario

---

## Autor

Jesús Daniel Guzmán Valenzuela

---

## Licencia

MIT
