import os
import duckdb
from openai import OpenAI
from dotenv import load_dotenv
from agents.Test_Txt2Sql_Agent_ import SQL_RAG_Agent 
from agents.Test_DF_Agent import DataFrame_Agent 

def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    db_path = "database/Reto_5_RAG_DB.duckdb"
    json_path = "data/sql_dataset_bourbaki.json" 

    if not api_key:
        print("Error: Configura OPENAI_API_KEY en tu .env")
        return

    client = OpenAI(api_key=api_key)
    
    agent_1 = SQL_RAG_Agent(model="gpt-4o-mini", client=client, json_path=json_path)
    agent_2 = DataFrame_Agent(model="gpt-4o-mini", client=client)

    try:
        con = duckdb.connect(db_path)
    except Exception as e:
        print(f"Error de conexión con la base de datos: {e}")
        return

    print("\n--- Doo Doo Dynamics Analytics AI ---")
    
    # Loop for continous execution
    continuar = True
    while continuar:
        pregunta = input("\n¿Qué deseas saber?: ")

        if pregunta.strip():
            # 1. Agent 1
            print("\n🔍 Analizando esquemas y generando consulta...")
            sql_generated = agent_1.run(query=pregunta)

            if sql_generated.startswith("Error"):
                print(f"Lo siento, hubo un problema al procesar la consulta: {sql_generated}")
            else:
                try:
                    # 2. DuckDB
                    df = con.execute(sql_generated).df()
                    
                    if df.empty:
                        print("\nNo encontré información que coincida con tu consulta en la base de datos.")
                    else:
                        # 3. Agent 2
                        respuesta_final = agent_2.run(question=pregunta, df=df)
                        print("🤖 Redactando respuesta final 🤖")
                        print("\n" + "="*40)
                        print(f"RESPUESTA:\n{respuesta_final}")
                        print("="*40)
                        
                        # 4. Technical details
                        print("\n" + "-"*30)
                        ver_detalles = input("¿Te gustaría ver el query SQL y la tabla de datos? (s/n): ").lower()
                        
                        if ver_detalles == 's':
                            print(f"\n[QUERY EJECUTADO]:\n{sql_generated}")
                            print("-" * 30)
                            print(f"[DATOS OBTENIDOS]:")
                            print(df.to_string(index=False))
                            print("-" * 30)
                        
                except Exception as e:
                    print(f"\nHubo un error técnico al ejecutar la consulta en la base de datos.")
                    # In case it fails show the query
                    opcion_error = input("¿Quieres ver el query que causó el error para revisarlo? (s/n): ").lower()
                    if opcion_error == 's':
                        print(f"\nSQL Fallido:\n{sql_generated}")
                        print(f"Error técnico: {e}")
        
        # Continue?
        print("\n" + "="*40)
        decision = input("¿Deseas realizar otra consulta? (s/n): ").lower()
        if decision != 's':
            continuar = False

    con.close()
    print("\nSesión finalizada. ¡Hasta luego!")

if __name__ == "__main__":
    main()