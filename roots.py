import streamlit as st
import numpy as np
import pandas as pd

# --- Configuración Profesional de la App ---
st.set_page_config(
    page_title="Calculadora de Raíces Móvil",
    page_icon="🧮",
    layout="centered"  # 'centered' funciona mejor en móviles que 'wide'
)

# --- Lógica Matemática ---
def calcular_raices(coeficientes):
    """Calcula raíces reales e imaginarias usando NumPy."""
    raices = np.roots(coeficientes)
    datos = []
    for i, r in enumerate(raices):
        datos.append({
            "ID": f"x{i+1}",
            "Valor": f"{r.real:.3f} {'+' if r.imag >= 0 else '-'} {abs(r.imag):.3f}i" if r.imag != 0 else f"{r.real:.3f}",
            "Tipo": "Real" if np.isreal(r) else "Compleja",
            "Real": r.real,
            "Imag": r.imag
        })
    return pd.DataFrame(datos)

# --- Interfaz de Usuario ---
st.title("🧮 Analizador Polinomial")
st.info("Introduce los coeficientes para obtener las raíces (reales y complejas) automáticamente.")

# --- Configuración en Sidebar (Colapsable en móvil) ---
with st.sidebar:
    st.header("Ajustes")
    grado = st.number_input("Grado del Polinomio", min_value=1, max_value=15, value=3)
    st.caption("Nota: El grado define cuántas cajas de entrada verás.")

# --- Contenedor de Entradas (Optimizado para móvil) ---
# Usamos un expander para que el teclado del celular no tape toda la pantalla
with st.expander("📝 Ingresar Coeficientes", expanded=True):
    coefs = []
    # Usamos columnas pequeñas para que en móvil se vean de 2 en 2 o 1 en 1
    # Streamlit maneja el wrapping automáticamente
    cols = st.columns(2) 
    
    for i in range(grado + 1):
        idx_col = i % 2 # Alterna entre las 2 columnas
        potencia = grado - i
        label = f"x^{potencia}" if potencia > 0 else "T. Independiente"
        
        with cols[idx_col]:
            val = st.number_input(label, value=1.0 if i == 0 else 0.0, key=f"c_{i}")
            coefs.append(val)

# --- Botón de Acción Principal ---
if st.button("🚀 Calcular Raíces", type="primary", use_container_width=True):
    if coefs[0] == 0:
        st.error("El primer coeficiente no puede ser cero (define el grado).")
    else:
        df_raices = calcular_raices(coefs)
        
        # --- Visualización de Resultados ---
        st.subheader("📍 Resultados")
        
        # Tabla compacta para pantallas pequeñas
        st.dataframe(
            df_raices[["ID", "Valor", "Tipo"]], 
            hide_index=True, 
            use_container_width=True
        )
        
        # Gráfico del Plano Complejo
        st.subheader("📊 Plano de Argand")
        st.scatter_chart(
            df_raices,
            x="Real",
            y="Imag",
            color="Tipo",
            size=80,
            use_container_width=True
        )
        
        # Resumen rápido
        reales = len(df_raices[df_raices["Tipo"] == "Real"])
        imaginarias = len(df_raices) - reales
        
        c1, c2 = st.columns(2)
        c1.metric("Reales", reales)
        c2.metric("Imaginarias", imaginarias)

# --- Footer Informativo ---
st.divider()
st.caption("Desarrollado con Streamlit • Motor NumPy 1.26+")