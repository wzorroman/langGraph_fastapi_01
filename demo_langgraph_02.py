from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, END


# Define el esquema de estado compartido
class State(TypedDict):
    """Estado compartido: Almacena números iniciales, la suma, la media y el resultado final."""
    num_a: int
    num_b: int
    sum_result: int
    mean_result: float
    final_message: Annotated[str, operator.add] # Usa el operador 'add' para concatenar mensajes


# Nodo 1: Sumar 2 números iniciales
def sum_numbers_node(state: State) -> dict:
    """Calcula la suma de num_a y num_b."""
    sum_res = state['num_a'] + state['num_b']
    print(f"-> Node: SUMA -> {state['num_a']} + {state['num_b']} = {sum_res}")
    return {"sum_result": sum_res} # Actualiza el estado con la suma

# Nodo 2: Calcular la media
def mean_node(state: State) -> dict:
    """Calcula la media de la suma."""
    mean_res = state['sum_result'] / 2.0
    print(f"-> Node: MEDIA -> {state['sum_result']} / 2.0 = {mean_res}")
    return {"mean_result": mean_res} # Actualiza el estado con la media

# Nodo de Operación A: Resta (Reutilizado)
def subtract_node(state: State) -> dict:
    """Si la media > num_a, resta la media menos el num_a."""
    result = state['mean_result'] - state['num_a']
    message = f"Ruta RESTA: Media ({state['mean_result']}) es MAYOR que NumA ({state['num_a']}). Resultado: {result}"
    return {"final_message": message}

# Nodo de Operación B: Multiplicación (Nuevo)
def multiply_node(state: State) -> dict:
    """Si la media <= num_a, multiplica la media por 2."""
    result = state['mean_result'] * 2
    message = f"Ruta MULTIPLICACIÓN: Media ({state['mean_result']}) es MENOR/IGUAL que NumA ({state['num_a']}). Resultado: {result}"
    return {"final_message": message}

# Nodo 3: Decisión/Enrutamiento Condicional (Selector)
def route_decision(state: State) -> str:
    """Decide el siguiente nodo basado en si la media > num_a."""
    if state['mean_result'] > state['num_a']:
        return "subtract_node" # Va a la resta
    else:
        return "multiply_node" # Va a la multiplicación

# Nodo 4: Mensaje Final
def final_message_node(state: State) -> dict:
    """Muestra el mensaje final y termina el grafo. Retorna un dict vacío."""
    print("\n----------------------------------------------------")
    print("-> Node: MENSAJE_FINAL")
    print(f"Flujo Finalizado. Mensaje: {state['final_message']}")
    print("----------------------------------------------------")
    return {} # Retorna dict vacío, ya que el mensaje ya fue agregado al estado.

def create_and_compile_graph():
    builder = StateGraph(State)

    # 1. Añadir Nodos
    builder.add_node("sum_node", sum_numbers_node)
    builder.add_node("mean_node", mean_node)
    builder.add_node("subtract_node", subtract_node)
    builder.add_node("multiply_node", multiply_node)
    builder.add_node("final_node", final_message_node)

    # 2. Definir Punto de Entrada
    builder.set_entry_point("sum_node")

    # 3. Definir Bordes Secuenciales
    builder.add_edge("sum_node", "mean_node")

    # 4. Definir Borde Condicional desde 'mean_node'
    # La media debe ser calculada antes de la decisión de ruta.
    builder.add_conditional_edges(
        "mean_node",        # Nodo de origen
        route_decision,     # Función selectora
        {
            "subtract_node": "subtract_node",
            "multiply_node": "multiply_node",
        }
    )

    # 5. Definir Bordes de Salida al Mensaje Final
    builder.add_edge("subtract_node", "final_node")
    builder.add_edge("multiply_node", "final_node")

    # 6. Definir la Salida del Grafo
    builder.add_edge("final_node", END)

    app = builder.compile()
    return app

# ==============================================================================
# 4. EXECUTION (Ejecución de Pruebas)
# ==============================================================================

if __name__ == "__main__":
    app = create_and_compile_graph()

    print("=====================================================")
    print("🚀 LangGraph Demo: Media y Decisión Condicional")
    print("=====================================================")

    # --- PRUEBA 1: Media MAYOR que NumA (Ruta RESTA) ---
    # 10 + 30 = 40. Media = 20. 20 > 10. Va a RESTA (20 - 10 = 10)
    print("\n--- EJECUCIÓN 1: Ruta RESTA (Media > NumA) ---")
    initial_state_1 = {"num_a": 10, "num_b": 30}
    final_state_1 = app.invoke(initial_state_1)

    # --- PRUEBA 2: Media MENOR/IGUAL que NumA (Ruta MULTIPLICACIÓN) ---
    # 20 + 20 = 40. Media = 20. 20 <= 20. Va a MULTIPLICACIÓN (20 * 2 = 40)
    print("\n--- EJECUCIÓN 2: Ruta MULTIPLICACIÓN (Media <= NumA) ---")
    initial_state_2 = {"num_a": 20, "num_b": 20}
    final_state_2 = app.invoke(initial_state_2)
