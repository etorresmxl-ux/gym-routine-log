import os
from datetime import date

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Gym Routine Planner",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "gym_routines.csv")
COLUMNS = [
    "id",
    "routine_id",
    "fecha",
    "rutina",
    "bloque",
    "ejercicio",
    "series",
    "reps",
    "peso",
    "comentario",
]
ROUTINE_OPTIONS = ["Push", "Pull", "Legs", "Other"]

st.markdown(
    """
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
            border-radius: 18px;
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
        .stTextInput input, .stNumberInput input, .stDateInput input, .stTextArea textarea, .stSelectbox > div > div {
            background: #0b1220;
            color: white;
            border-radius: 10px;
            border: 1px solid #334155;
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
    """,
    unsafe_allow_html=True,
)


def ensure_data_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        pd.DataFrame(columns=COLUMNS).to_csv(DATA_FILE, index=False)


def load_data():
    ensure_data_file()
    df = pd.read_csv(DATA_FILE)

    if df.empty:
        return pd.DataFrame(columns=COLUMNS)

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = df[COLUMNS].copy()
    df["id"] = pd.to_numeric(df["id"], errors="coerce").fillna(0).astype(int)
    df["routine_id"] = pd.to_numeric(df["routine_id"], errors="coerce").fillna(0).astype(int)
    df["series"] = pd.to_numeric(df["series"], errors="coerce").fillna(0).astype(int)
    df["reps"] = pd.to_numeric(df["reps"], errors="coerce").fillna(0).astype(int)
    df["peso"] = pd.to_numeric(df["peso"], errors="coerce").fillna(0.0)
    return df


def save_data(df):
    empty_df = pd.DataFrame(columns=COLUMNS)
    if df.empty:
        empty_df.to_csv(DATA_FILE, index=False)
        return

    df = df[COLUMNS].copy()
    df["id"] = pd.to_numeric(df["id"], errors="coerce").fillna(0).astype(int)
    df["routine_id"] = pd.to_numeric(df["routine_id"], errors="coerce").fillna(0).astype(int)
    df["series"] = pd.to_numeric(df["series"], errors="coerce").fillna(0).astype(int)
    df["reps"] = pd.to_numeric(df["reps"], errors="coerce").fillna(0).astype(int)
    df["peso"] = pd.to_numeric(df["peso"], errors="coerce").fillna(0.0)
    df.to_csv(DATA_FILE, index=False)


def get_next_routine_id(df):
    if df.empty:
        return 1
    return int(df["routine_id"].max()) + 1


def get_next_exercise_id(df):
    if df.empty:
        return 1
    return int(df["id"].max()) + 1


def get_routine_label(routine_id, fecha, rutina):
    return f"{fecha} · {rutina} · ID {routine_id}"


if "selected_routine_id" not in st.session_state:
    st.session_state.selected_routine_id = None


st.title("🏋️ Registro de rutinas de gimnasio")
st.caption("Organiza tus entrenamientos por fecha, rutina, bloques y super series.")

# Cargar datos
df = load_data()

# 1. Seleccionar fecha y tipo de rutina
st.subheader("1) Fecha y tipo de rutina")
selected_date = st.date_input("Fecha", value=date.today())
selected_rutina = st.selectbox("Rutina", ROUTINE_OPTIONS)

existing_routines = (
    df[["routine_id", "fecha", "rutina"]]
    .drop_duplicates()
    .sort_values(["fecha", "rutina"], ascending=[False, True])
    .reset_index(drop=True)
)

if not existing_routines.empty:
    routine_options = [
        (int(row["routine_id"]), get_routine_label(row["routine_id"], row["fecha"], row["rutina"]))
        for _, row in existing_routines.iterrows()
    ]
    routine_id_from_dropdown = st.selectbox(
        "Rutina ya registrada",
        options=[None] + [routine_id for routine_id, _ in routine_options],
        index=0,
        format_func=lambda x: "Nueva rutina" if x is None else next(label for routine_id, label in routine_options if routine_id == x),
    )
else:
    routine_id_from_dropdown = None

if st.button("Abrir / crear rutina"):
    if routine_id_from_dropdown is not None:
        st.session_state.selected_routine_id = int(routine_id_from_dropdown)
    else:
        existing_match = df[
            (df["fecha"] == str(selected_date)) & (df["rutina"] == selected_rutina)
        ]
        if existing_match.empty:
            new_routine_id = get_next_routine_id(df)
            st.session_state.selected_routine_id = new_routine_id
        else:
            st.session_state.selected_routine_id = int(existing_match["routine_id"].iloc[0])

if st.session_state.selected_routine_id is not None:
    selected_routine_id = int(st.session_state.selected_routine_id)
    current_routine = df[df["routine_id"] == selected_routine_id].copy()
    if current_routine.empty:
        routine_label = f"{selected_date} · {selected_rutina} · ID {selected_routine_id}"
    else:
        routine_label = get_routine_label(
            int(current_routine["routine_id"].iloc[0]),
            current_routine["fecha"].iloc[0],
            current_routine["rutina"].iloc[0],
        )

    st.info(f"Rutina activa: {routine_label}")

    # 2. Agregar ejercicio dentro de la rutina
    st.subheader("2) Agregar ejercicio dentro de la rutina")
    with st.form("exercise_form", clear_on_submit=True):
        bloque = st.text_input("Bloque / Super serie", value="Bloque 1", placeholder="Bloque 1, Bloque 2, Super serie A...")
        ejercicio = st.text_input("Ejercicio", placeholder="Press banca, sentadilla, dominadas...")
        series = st.number_input("Series", min_value=1, step=1, value=3)
        reps = st.number_input("Reps", min_value=1, step=1, value=8)
        peso = st.number_input("Peso (kg)", min_value=0.0, step=0.5, value=0.0, format="%.1f")

        submitted_exercise = st.form_submit_button("Guardar ejercicio")

    if submitted_exercise:
        if not ejercicio.strip():
            st.warning("Escribe el nombre del ejercicio antes de guardar.")
        else:
            new_row = pd.DataFrame(
                [{
                    "id": get_next_exercise_id(df),
                    "routine_id": selected_routine_id,
                    "fecha": str(selected_date),
                    "rutina": selected_rutina,
                    "bloque": bloque.strip() if bloque.strip() else "Bloque 1",
                    "ejercicio": ejercicio.strip(),
                    "series": int(series),
                    "reps": int(reps),
                    "peso": float(peso),
                    "comentario": "",
                }]
            )
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.success("✅ Ejercicio agregado a la rutina.")
            st.rerun()

    # 3. Detalle de la rutina / bloque o super serie
    st.subheader("3) Detalle de la rutina")
    routine_comment = ""
    if not current_routine.empty:
        routine_comment = current_routine["comentario"].dropna().iloc[0] if current_routine["comentario"].notna().any() else ""

    with st.form("routine_comment_form"):
        comment_text = st.text_area(
            "Comentarios de la rutina",
            value=routine_comment,
            placeholder="Ejemplo: bajar la velocidad, enfocarme en técnica, descanso 90 segundos, superserie con sentadilla y press...",
            height=120,
        )
        save_comment = st.form_submit_button("Guardar comentario")

    if save_comment:
        df.loc[df["routine_id"] == selected_routine_id, "comentario"] = comment_text
        save_data(df)
        st.success("✅ Comentario guardado.")
        st.rerun()

    # 4. Mostrar ejercicios de la rutina y permitir editar
    st.subheader("4) Ejercicios dentro de la rutina")
    routine_exercises = df[df["routine_id"] == selected_routine_id].copy().sort_values(["bloque", "ejercicio"]).reset_index(drop=True)

    if routine_exercises.empty:
        st.info("Aún no hay ejercicios en esta rutina.")
    else:
        exercise_options = routine_exercises["id"].tolist()
        labels = [
            f"{row['bloque']} | {row['ejercicio']} | {row['series']}x{row['reps']} | {row['peso']} kg"
            for _, row in routine_exercises.iterrows()
        ]

        selected_exercise_id = st.selectbox(
            "Selecciona un ejercicio para editar o eliminar",
            options=exercise_options,
            format_func=lambda x: next(label for idx, label in zip(routine_exercises["id"], labels) if idx == x),
        )

        exercise_row = routine_exercises[routine_exercises["id"] == selected_exercise_id].iloc[0]

        with st.form("update_exercise_form"):
            edit_bloque = st.text_input("Bloque / Super serie", value=str(exercise_row["bloque"]))
            edit_ejercicio = st.text_input("Ejercicio", value=str(exercise_row["ejercicio"]))
            edit_series = st.number_input("Series", min_value=1, step=1, value=int(exercise_row["series"]))
            edit_reps = st.number_input("Reps", min_value=1, step=1, value=int(exercise_row["reps"]))
            edit_peso = st.number_input("Peso (kg)", min_value=0.0, step=0.5, value=float(exercise_row["peso"]), format="%.1f")

            col_update, col_delete = st.columns(2)
            update_click = col_update.form_submit_button("Actualizar ejercicio")
            delete_click = col_delete.form_submit_button("Eliminar ejercicio")

        if update_click:
            df.loc[df["id"] == selected_exercise_id, "bloque"] = edit_bloque.strip() if edit_bloque.strip() else "Bloque 1"
            df.loc[df["id"] == selected_exercise_id, "ejercicio"] = edit_ejercicio.strip()
            df.loc[df["id"] == selected_exercise_id, "series"] = int(edit_series)
            df.loc[df["id"] == selected_exercise_id, "reps"] = int(edit_reps)
            df.loc[df["id"] == selected_exercise_id, "peso"] = float(edit_peso)
            save_data(df)
            st.success("✅ Ejercicio actualizado.")
            st.rerun()

        if delete_click:
            df = df[df["id"] != int(selected_exercise_id)].copy()
            save_data(df)
            st.success("✅ Ejercicio eliminado.")
            st.rerun()

# Resumen y gráficos globales
st.subheader("Resumen")
if not df.empty:
    summary_df = df.copy()
    summary_df["fecha"] = pd.to_datetime(summary_df["fecha"])
    summary_df = summary_df.sort_values("fecha")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de ejercicios", len(summary_df))
    col2.metric("Peso máximo", f"{summary_df['peso'].max():.1f} kg")
    col3.metric("Rutinas registradas", summary_df["routine_id"].nunique())

    st.subheader("Gráficas")
    # Tendencia de peso por fecha
    trend = summary_df.groupby("fecha", as_index=False)["peso"].max().rename(columns={"peso": "Peso (kg)"})
    if not trend.empty:
        st.line_chart(trend.set_index("fecha"))

    # Frecuencia por rutina
    routine_count = summary_df.groupby("rutina").size().rename("cantidad").reset_index()
    st.bar_chart(routine_count.set_index("rutina")["cantidad"])

    # Máximo peso por ejercicio
    exercise_max = summary_df.groupby("ejercicio", as_index=False)["peso"].max().sort_values("peso", ascending=False).head(10)
    if not exercise_max.empty:
        st.bar_chart(exercise_max.set_index("ejercicio")["peso"])

    # Tabla general
    st.dataframe(summary_df[["fecha", "rutina", "bloque", "ejercicio", "series", "reps", "peso", "comentario"]].sort_values("fecha", ascending=False).reset_index(drop=True), use_container_width=True)

else:
    st.info("Todavía no hay información para graficar.")

