import os
from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Gym Routine Log",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para mejorar la experiencia móvil
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background: #0f172a;
        color: #e2e8f0;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stForm"] {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #22c55e, #16a34a);
        color: white;
        font-weight: 700;
        height: 3rem;
        border: none;
    }
    .stTextInput input, .stNumberInput input, .stDateInput input {
        background: #0b1220;
        color: white;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    .stSelectbox > div > div {
        background: #0b1220;
        color: white;
        border-radius: 10px;
    }
    .stDataFrame {
        background: #111827;
        border-radius: 12px;
    }
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.6rem;
            padding-right: 0.6rem;
        }
        h1 {
            font-size: 2rem !important;
        }
        h2 {
            font-size: 1.4rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


DATA_FILE = "gym_routines.csv"

def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "fecha",
            "rutina",
            "ejercicio",
            "repeticiones",
            "pesos"
        ])
        df.to_csv(DATA_FILE, index=False)

def load_data():
    ensure_data_file()
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        return pd.DataFrame(columns=[
            "fecha",
            "rutina",
            "ejercicio",
            "repeticiones",
            "pesos"
        ])
    return df

def save_data(df):
    df = df[["fecha", "rutina", "ejercicio", "repeticiones", "pesos"]]
    df.to_csv(DATA_FILE, index=False)

def main():
    st.title("🏋️ Registro de rutinas")
    st.caption("Guarda tus ejercicios diarios de manera rápida y sencilla.")

    tabs = st.tabs(["Registrar", "Historial"])

    with tabs[0]:
        with st.form("routine_form", clear_on_submit=True):
            fecha = st.date_input("Fecha", value=date.today())
            rutina = st.selectbox(
                "Rutina",
                ["push", "pull", "legs", "otros"]
            )
            ejercicio = st.text_input(
                "Ejercicio",
                placeholder="Press banca, dominadas, sentadilla..."
            )
            repeticiones = st.number_input(
                "Repeticiones",
                min_value=1,
                step=1,
                value=8
            )
            pesos = st.number_input(
                "Peso (kg)",
                min_value=0.0,
                step=0.5,
                value=0.0,
                format="%.1f"
            )

            submitted = st.form_submit_button("Guardar rutina")

        if submitted:
            if not ejercicio.strip():
                st.warning("Escribe el nombre del ejercicio antes de guardar.")
                return

            df = load_data()
            nuevo_registro = pd.DataFrame([{
                "fecha": str(fecha),
                "rutina": rutina,
                "ejercicio": ejercicio.strip(),
                "repeticiones": int(repeticiones),
                "pesos": float(pesos)
            }])
            df = pd.concat([df, nuevo_registro], ignore_index=True)
            save_data(df)

            st.success("✅ Rutina guardada correctamente.")

    with tabs[1]:
        df = load_data()
        if df.empty:
            st.info("Todavía no hay registros.")
        else:
            df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m-%d")
            df = df.sort_values("fecha", ascending=False).reset_index(drop=True)

            # Filtro rápido
            rutina_filtro = st.selectbox(
                "Filtrar por rutina",
                ["Todas", "push", "pull", "legs", "otros"],
                key="filtro_rutina"
            )

            if rutina_filtro != "Todas":
                df = df[df["rutina"] == rutina_filtro]

            st.dataframe(df, use_container_width=True, hide_index=True)

            total = len(df)
            st.metric("Total de registros", total)

if __name__ == "__main__":
    main()
