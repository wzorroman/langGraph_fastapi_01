from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Grafo 1: Cálculo Básico (Paridad/Suma/Resta)
from demo_langgraph_01 import create_and_compile_graph as compile_basic_graph
# Grafo 2: Media y Decisión (Media/Resta/Multiplicación)
from demo_langgraph_02 import create_and_compile_graph as compile_advanced_graph

# ==============================================================================
# 1. ESQUEMA DE DATOS PARA FASTAPI
# ==============================================================================

# Esquema para el Endpoint /calculo_basico (usa el grafo 1)
class BasicCalculationInput(BaseModel):
    number: int
    modifier: int

# Esquema para el Endpoint /calcular (usa el grafo 2)
class AdvancedCalculationInput(BaseModel):
    num_a: int
    num_b: int
# ==============================================================================
# 2. INICIALIZACIÓN Y COMPILACIÓN DEL GRAFO
# ==============================================================================

# Compilamos el grafo de LangGraph una única vez al iniciar la API.
try:
    LANGGRAPH_ADVANCED_APP = compile_advanced_graph()
    LANGGRAPH_BASIC_APP = compile_basic_graph()
    print("🚀 LangGraph compilado exitosamente y listo para la API.")
except Exception as e:
    print(f"Error al compilar LangGraph: {e}")
    LANGGRAPH_APP = None # Evita que la API se lance si la compilación falla.


# ==============================================================================
# 3. APLICACIÓN FASTAPI Y ENDPOINT
# ==============================================================================

app = FastAPI(
    title="LangGraph Decision Flow API",
    description="API que delega la lógica de negocio al flujo de LangGraph."
)

# --- ENDPOINT 1: /calcular (Flujo Media y Decisión - Grafo 2) ---
@app.post("/calcular")
async def calcular_avanzado(data: AdvancedCalculationInput):
    """
    Invoca el flujo de LangGraph de Media y Decisión (demo_langgraph_02.py).
    """
    print(f"\n--- ENDPOINT: /calcular (Flujo Avanzado) --- Input: A={data.num_a}, B={data.num_b}")

    initial_state = {
        "num_a": data.num_a,
        "num_b": data.num_b,
    }

    try:
        final_state = LANGGRAPH_ADVANCED_APP.invoke(initial_state)

        return {
            "status": "success",
            "media_calculada": final_state.get("mean_result"),
            "flujo_ejecutado": final_state.get("final_message")
        }

    except Exception as e:
        print(f"Error en LangGraph Avanzado: {e}")
        raise HTTPException(status_code=500, detail=f"Error al ejecutar el grafo avanzado: {str(e)}")


# --- ENDPOINT 2: /calculo_basico (Flujo Paridad/Suma/Resta - Grafo 1) ---
@app.post("/calculo_basico")
async def calculo_basico(data: BasicCalculationInput):
    """
    Invoca el flujo de LangGraph de Paridad y Operación (demo_langgraph_01.py).
    """
    print(f"\n--- ENDPOINT: /calculo_basico (Flujo Básico) --- Input: Num={data.number}, Mod={data.modifier}")

    initial_state = {
        "number": data.number,
        "modifier": data.modifier,
        "result": 0 # Inicializar el resultado para el grafo 1
    }

    try:
        # LangGraph permite la creación de múltiples grafos de trabajo que pueden ser invocados independientemente[cite: 10].
        final_state = LANGGRAPH_BASIC_APP.invoke(initial_state)

        return {
            "status": "success",
            "operacion_final": "Suma si es par, Resta si es impar",
            "resultado": final_state.get("result")
        }

    except Exception as e:
        print(f"Error en LangGraph Básico: {e}")
        raise HTTPException(status_code=500, detail=f"Error al ejecutar el grafo básico: {str(e)}")
