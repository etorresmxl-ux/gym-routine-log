# Gym Routine Log

Aplicación personal para registrar rutinas del gym con Streamlit.

## Funcionalidades

- Registro de fecha
- Tipo de rutina: `push`, `pull`, `legs`, `otros`
- Ejercicio
- Repeticiones
- Peso (kg)
- Historial de registros
- Filtro por rutina
- Edición de registros existentes
- Eliminación de un registro
- Gráficas de progreso y frecuencia por rutina

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar la app

```bash
streamlit run app.py
```

## Datos

Los registros se guardan automáticamente en:

```text
data/gym_routines.csv
```

## Nota

La app está pensada para uso personal, sin usuarios ni autenticación, y optimizada para móvil.
