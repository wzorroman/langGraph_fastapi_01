# demo_langgraph_01.py

from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END

# ==============================================================================
# 1. DESIGN STATE SCHEMA (Diseño del Esquema de Estado) [cite: 29]
# ==============================================================================

class State(TypedDict):
    """
    Define el esquema de estado compartido (memoria) entre los nodos.
    'result' usa el operador de reducción 'add' para acumular el valor.
    """
    number: int
    modifier: int
    result: Annotated[int, operator.add]

# ==============================================================================
# 2. BUILD NODES AS FUNCTIONS (Implementación de Nodos/Pasos Discretos) [cite: 29]
# ==============================================================================

def add_node(state: State) -> dict:
    """
    Nodo de operación: Suma el valor 'modifier' al valor 'number'.
    Retorna un diccionario con los updates de estado.
    """
    print(f"-> Node: SUMA (Input: {state['number']}, Modificador: {state['modifier']})")
    new_result = state['number'] + state['modifier']
    return {"result": new_result}

def subtract_node(state: State) -> dict:
    """
    Nodo de operación: Resta el valor 'modifier' al valor 'number'.
    Retorna un diccionario con los updates de estado.
    """
    print(f"-> Node: RESTA (Input: {state['number']}, Modificador: {state['modifier']})")
    new_result = state['number'] - state['modifier']
    return {"result": new_result}

def check_number_node(state: State) -> dict:
    """
    Nodo que se ejecuta. Solo registra la decisión en el log y retorna
    un diccionario vacío para NO MODIFICAR el estado.
    """
    if state['number'] % 2 == 0:
        print(f"-> Node: CHECK_NODE -> El número {state['number']} es PAR. La ruta será a 'add_node'.")
    else:
        print(f"-> Node: CHECK_NODE -> El número {state['number']} es IMPAR. La ruta será a 'subtract_node'.")
    return {} # <-- CORRECCIÓN CLAVE: El nodo debe retornar un dict o None.

# --- FUNCIÓN CORREGIDA 2: El Selector Condicional (Retorna str) ---
def route_number_choice(state: State) -> str:
    """
    Función de Enrutamiento Condicional.
    Solo retorna el nombre del siguiente nodo (string) para guiar el flujo.
    """
    if state['number'] % 2 == 0:
        return "add_node"
    else:
        return "subtract_node"

# ==============================================================================
# 3. WIRE TOGETHER (Conexión del Grafo) [cite: 30]
# ==============================================================================

def create_and_compile_graph():
    """Crea y compila la aplicación LangGraph."""

    # 1. Inicializa el constructor del grafo
    builder = StateGraph(State)

    # 2. Agrega los nodos
    builder.add_node("check_node", check_number_node)
    builder.add_node("add_node", add_node)
    builder.add_node("subtract_node", subtract_node)

    # 3. Define el punto de entrada (el primer nodo a ejecutar)
    builder.set_entry_point("check_node")

    # 4. Define los bordes condicionales (Routing)
    # Desde 'check_node', la transición depende de lo que retorne 'check_number'
    # Usamos la nueva función 'route_number_choice' como selector.
    builder.add_conditional_edges(
        "check_node",           # Nodo de origen
        route_number_choice,    # Función selectora (retorna el string del nodo)
        {
            "add_node": "add_node",
            "subtract_node": "subtract_node",
        }
    )

    # 5. Define los bordes simples (transiciones al finalizar)
    # Una vez que la operación se realiza, se termina la ejecución del grafo.
    builder.add_edge("add_node", END)
    builder.add_edge("subtract_node", END)

    # 6. Compila el grafo para obtener la aplicación ejecutable
    app = builder.compile()

    return app

# ==============================================================================
# 4. EXECUTION (Ejecución y Pruebas)
# ==============================================================================

if __name__ == "__main__":
    app = create_and_compile_graph()

    print("=====================================================")
    print("🚀 LangGraph Demo: Enrutamiento Condicional de Cálculo")
    print("=====================================================")

    # --- PRUEBA 1: Número Par (Debe ir a SUMA) ---
    print("\n--- EJECUCIÓN 1: Input Par (10) ---")
    initial_state_1 = {"number": 10, "modifier": 4, "result": 0}
    # La ejecución toma el estado inicial y lo pasa por el grafo
    final_state_1 = app.invoke(initial_state_1)

    print(f"Estado Inicial: {initial_state_1}")
    print(f"Resultado Final: {final_state_1['result']}")
    print("-----------------------------------")

    # --- PRUEBA 2: Número Impar (Debe ir a RESTA) ---
    print("\n--- EJECUCIÓN 2: Input Impar (9) ---")
    initial_state_2 = {"number": 9, "modifier": 5, "result": 0}
    # La ejecución toma el estado inicial y lo pasa por el grafo
    final_state_2 = app.invoke(initial_state_2)

    print(f"Estado Inicial: {initial_state_2}")
    print(f"Resultado Final: {final_state_2['result']}")
    print("-----------------------------------")

    # --- PRUEBA 3: Otro Número Par (Debe ir a SUMA) ---
    print("\n--- EJECUCIÓN 3: Input Par (100) ---")
    initial_state_3 = {"number": 100, "modifier": 10, "result": 0}
    # La ejecución toma el estado inicial y lo pasa por el grafo
    final_state_3 = app.invoke(initial_state_3)

    print(f"Estado Inicial: {initial_state_3}")
    print(f"Resultado Final: {final_state_3['result']}")
    print("-----------------------------------")
