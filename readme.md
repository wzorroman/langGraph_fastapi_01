# 📚 LangGraph FastAPI Monorepo (Cálculo y Decisión)

[cite_start]Este proyecto demuestra la integración de **LangGraph** (usando la **Graph API** [cite: 10] [cite_start]de estilo declarativo [cite: 10]) con **FastAPI** para gestionar múltiples flujos de trabajo de lógica de negocio (Grafos) a través de distintos *endpoints*.

[cite_start]Se sigue la metodología LangGraph de "Pensar en LangGraph" [cite: 27] [cite_start]al descomponer la lógica en pasos discretos [cite: 27][cite_start], diseñar un esquema de estado compartido [cite: 28, 29][cite_start], y utilizar un patrón de **Enrutamiento Condicional** (`lg:Routing`)[cite: 20, 21].

---

## 🎯 Arquitectura del Proyecto

El proyecto está dividido en tres archivos principales para una clara separación de responsabilidades:

1.  **`demo_langgraph_01.py` (Flujo Básico):** Lógica del primer grafo.
    * **Función:** Decide si un `number` es par o impar y aplica Suma o Resta.
    * [cite_start]**Conceptos Clave:** Estado tipado con reducción (`AnnotatedState`) [cite: 15][cite_start], Enrutamiento Condicional[cite: 21].

2.  **`demo_langgraph_02.py` (Flujo Avanzado):** Lógica del segundo grafo.
    * **Función:** Calcula la media de dos números y aplica Resta o Multiplicación basado en una decisión.
    * [cite_start]**Metodología:** Mapeado en Pasos Discretos [cite: 27][cite_start], Diseño de Estado Tipado[cite: 16].

3.  **`api_langgraph.py` (API Gateway):** Contiene la lógica de FastAPI.
    * **Función:** Compila ambos grafos (`demo_langgraph_01.py` y `demo_langgraph_02.py`) al inicio y los expone a través de dos *endpoints* independientes.

---

## ⚙️ Configuración y Ejecución

### 1. Requisitos

  Asegúrate de que los tres archivos (`demo_langgraph_01.py`, `demo_langgraph_02.py`, `api_langgraph.py`) estén en el mismo directorio.

### 2. Instalación de Dependencias
  Instala los paquetes necesarios:
  ```bash
  pip install fastapi uvicorn langgraph pydantic
  ```

### 3. Ejecución del Servidor
  Inicia el servidor Uvicorn apuntando al archivo de la API:
  ```bash
  uvicorn api_langgraph:app --reload
  ```
  El servidor estará accesible en http://127.0.0.1:8000.

### 🚀 Endpoints de la API
  Los flujos de trabajo son invocados a través de la API, donde cada endpoint corresponde a un grafo LangGraph distinto.

  1. Endpoint: /calculo_basico (Flujo Básico)
    - Método: POST
    - Propósito: Aplica modifier a number mediante Suma (si par) o Resta (si impar).
    - Input JSON Ejemplo: {"number": 10, "modifier": 5}

  2. Endpoint: /calcular (Flujo Avanzado)
    - Método: POST
    - Propósito: Calcula la media de num_a y num_b. Si la media es mayor que num_a, resta; si es menor o igual, multiplica.
    - Input JSON Ejemplo: {"num_a": 10, "num_b": 30}
    