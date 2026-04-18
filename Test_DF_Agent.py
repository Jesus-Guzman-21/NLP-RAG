from openai import OpenAI
import pandas as pd
import concurrent.futures
from dotenv import load_dotenv
import os

# pip install tabulate

class DataFrame_Agent:
    def __init__(self, model: str, client: OpenAI, timeout: int = 15, max_rows: int = 20):
        self.client = client
        self.model = model
        self.timeout = timeout
        self.max_rows = max_rows

    def _prepare_context(self, df: pd.DataFrame) -> str:
        if len(df) > self.max_rows:
            df = df.head(self.max_rows)
        return df.to_markdown(index=False)

    def _build_messages(self, question: str, context: str):
        return [
            {"role": "system", 
             "content": """Eres un agente analista de datos. Responde usando únicamente la información del dataframe.
                          Responde en español y sé conciso. Si no se puede responder, di: 'No se puede determinar'. 
                          No inventes información"""},
            {"role": "user", "content": f"DataFrame:\n{context}\n\nPregunta: {question}"}
        ]

    def _call_model(self, messages):
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=100
        )

    def run(self, question: str, df: pd.DataFrame) -> str:
        context = self._prepare_context(df)
        messages = self._build_messages(question, context)
        try:
            response = self._call_model(messages)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
        
## --- Steps for execution ---
#
## 1. Client configuration 
#load_dotenv()
#api_key = os.getenv("OPENAI_API_KEY")
#client = OpenAI(api_key=api_key)
#llm_model = "gpt-4o-mini"
#
## 1. DataFrame and question dummy
#data = {
#    'Producto': ['Laptop', 'Mouse', 'Monitor', 'Teclado'],
#    'Precio': [1200, 25, 300, 75],
#    'Stock': [10, 50, 15, 30]
#}
#df_prueba = pd.DataFrame(data)
#
#pregunta = "¿Cuál es el producto más caro y cuántas unidades hay en stock?"
#
## 2. Show dataframe for manual validation
##print("\n--- Resultado de la ejecución del query ---")
##print(df_prueba.to_string(index=False)) 
##print("-" * 30)
#
## 3. Agent execution
#agente = DataFrame_Agent(model=llm_model , client=client)
#
#resultado = agente.run(pregunta, df_prueba)
#print(resultado)