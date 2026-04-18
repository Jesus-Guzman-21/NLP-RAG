import os
import json
import faiss
import numpy as np
from openai import OpenAI
from langchain_core.documents import Document

class SQL_RAG_Agent:
    """Login and Embedding Model"""
    def __init__(self, model: str, client: OpenAI, json_path: str, embedding_model_id: str = "text-embedding-3-small"):
        self.client = client
        self.model = model
        self.embedding_model_id = embedding_model_id
        
        # Carga de datos y preparación del índice
        self.documents = self._load_json_data(json_path)
        self.index = self._build_faiss_index()

    """Central method for the embedding with the API of Openai"""
    def _get_embeddings(self, texts: list):
        cleaned_texts = [t.replace("\n", " ") for t in texts]
        response = self.client.embeddings.create(
            input=cleaned_texts,
            model=self.embedding_model_id
        )
        return np.array([res.embedding for res in response.data]).astype('float32')
    
    """Preprocess .json file with Documents object from Langchain"""
    def _load_json_data(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"No se encontró el archivo: {path}")
            
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        docs = []
        for table_name, details in data.items():
            doc = Document(
                page_content=details["description"],
                metadata={
                    "table_name": table_name,
                    "schema": details["schema"],
                    "examples": details["examples"]
                }
            )
            docs.append(doc)
        return docs
    
    """Generate the embeddings with the table descriptions and create the FAISS index"""
    def _build_faiss_index(self):
        table_descriptions = [doc.page_content for doc in self.documents]
        
        # Obtenemos los vectores vía API
        table_embeddings = self._get_embeddings(table_descriptions)
        
        dimension = table_embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(table_embeddings)

        return index
    """Global (table) and local (examples) search"""
    def _retrieve_context(self, query: str, k_tables: int, n_examples: int):
        query_vector = self._get_embeddings([query])
        
        # Table search
        _, indices = self.index.search(query_vector, k=k_tables)
        
        context_schemas = []
        all_selected_examples = []

        for idx in indices[0]:
            doc = self.documents[idx]
            meta = doc.metadata
            context_schemas.append(f"Tabla: {meta['table_name']}\nSchema: {meta['schema']}")

            # Local search
            table_examples = meta["examples"]
            if not table_examples:
                continue
                
            ex_desc = [ex["description"] for ex in table_examples]
            ex_vectors = self._get_embeddings(ex_desc)
            
            scores = np.dot(ex_vectors, query_vector.T).flatten()
            best_ex_indices = np.argsort(scores)[-n_examples:][::-1]
            
            for ex_idx in best_ex_indices:
                all_selected_examples.append({
                    "table": meta['table_name'],
                    "description": table_examples[ex_idx]['description'],
                    "sql": table_examples[ex_idx]['sql']
                })
        
        return context_schemas, all_selected_examples

    def _build_messages(self, query: str, schemas: list, examples: list):
        """Construye el prompt para el modelo de chat"""
        schemas_str = "\n\n".join(schemas)
        examples_str = ""
        for i, ex in enumerate(examples, 1):
            examples_str += f"\nEJEMPLO {i} (Tabla {ex['table']}):\n- Tarea: {ex['description']}\n- SQL: {ex['sql']}\n"

        system_prompt = (
            "Eres un experto en SQL corporativo. Genera consultas SQL válidas.\n"
            "Reglas:\n"
            "- Si requiere JOINs, usa los campos relacionales adecuados.\n"
            "- Usa EXCLUSIVAMENTE columnas y tablas de los esquemas proporcionados.\n"
            "- PROHIBIDO acciones de escritura: DROP, DELETE, UPDATE, INSERT, etc.\n"
            "- Salida: ÚNICAMENTE el código SQL plano, sin bloques de código Markdown ni explicaciones."
        )

        user_content = f"ESQUEMAS:\n{schemas_str}\n\nEJEMPLOS:\n{examples_str}\n\nPREGUNTA: {query}\nSQL:"
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

    def run(self, query: str, k_tables: int = 3, n_examples_per_table: int = 2, temperature: float = 0):
        """Ejecuta el flujo completo del Agente SQL RAG"""
        try:
            # 1. Retrieval 
            schemas, examples = self._retrieve_context(query, k_tables, n_examples_per_table)
            
            # 2. Generation 
            messages = self._build_messages(query, schemas, examples)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            
            # 3. Cleaning 
            raw_sql = response.choices[0].message.content.strip()
            return raw_sql.replace("```sql", "").replace("```", "").strip()
            
        except Exception as e:
            return f"Error en SQL Agent: {str(e)}"

## --- Execution example ---
#
#if __name__ == "__main__":
#    from dotenv import load_dotenv
#
#    load_dotenv()
#    
#    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
#    PATH_JSON = 'sql_dataset_bourbaki.json' 
#
#    if not OPENAI_KEY:
#        print("❌ Error: Falta la API Key de OpenAI en el archivo .env")
#    else:
#        print("🚀 Iniciando Agente SQL RAG con OpenAI Embeddings...")
#        
#        # Initialize client (openai)
#        client = OpenAI(api_key=OPENAI_KEY)
#
#        # Call the agent
#        agente = SQL_RAG_Agent(
#            model="gpt-4o-mini", # Model 
#            client=client,
#            json_path=PATH_JSON
#        )
#
#        # Execution example
#        q_test = "Muestra los nombres de productos y sus categorías"
#        print(f"\nPregunta: {q_test}")
#        
#        result = agente.run(query=q_test)
#
#        print("\nSQL Generado:")
#        print("-" * 30)
#        print(result)
#        print("-" * 30)