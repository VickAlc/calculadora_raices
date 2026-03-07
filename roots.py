import streamlit as st
import numpy as np
import pandas as pd

# --- Configuración de la App ---
st.set_page_config(
    page_title="Analizador Polinomial",
    page_icon="🎯",
    layout="centered"
)

# --- Lógica de Cálculo ---
def calcular_raices(coeficientes):
    """Calcula raíces reales e imaginarias."""
    raices = np.roots(coeficientes)
    datos = []
    for i, r in enumerate(raices):
        # Formateo de número complejo para visualización amigable
        if np.isreal(r):
            valor_str = f"{r.real:.4f}"
        else:
            signo = "+" if r.imag >= 0 else "-"
            valor_str = f"{r.real:.4f} {signo} {abs(r.imag):.4f}i"
            
        datos.append({
            "ID": f"x{i+1}",
            "Valor": valor_str,
            "Tipo": "Real" if np.isreal(r) else "Compleja",
            "Real": r.real,
            "Imag": r.imag
        })
    return pd.DataFrame(datos)

# --- Interfaz de Usuario ---
st.title("🎯 Buscador de Raíces")
st.markdown("---")

# --- Configuración en Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuración")
    grado = st.number_input("Grado del Polinomio", min_value=1, max_value=20, value=3)
    st.info("Al cambiar el grado, se generarán automáticamente los campos de entrada abajo.")

# --- Entrada de Coeficientes (Columna Única) ---
st.subheader("📝 Coeficientes del Polinomio")
st.caption("Ingresa los valores de mayor a menor grado.")

with st.expander("Abrir Editor de Coeficientes", expanded=True):
    coefs = []
    # Al no usar st.columns(), Streamlit apila todo en una sola columna por defecto
    for i in range(grado + 1):
        potencia = grado - i
        if potencia > 1:
            label = f"Coeficiente de x^{potencia}"
        elif potencia == 1:
            label = "Coeficiente de x"
        else:
            label = "Término Independiente"
            
        val = st.number_input(
            label, 
            value=1.0 if i == 0 else 0.0, 
            key=f"c_input_{i}",
            format="%.4f" # Permite precisión decimal
        )
        coefs.append(val)

# --- Procesamiento y Resultados ---
st.markdown("---")
if st.button("🚀 Calcular Raíces Ahora", type="primary", use_container_width=True):
    if coefs[0] == 0:
        st.warning("⚠️ El coeficiente principal (el primero) no puede ser 0.")
    else:
        try:
            df_raices = calcular_raices(coefs)
            
            # Métricas rápidas
            c1, c2 = st.columns(2)
            reales = len(df_raices[df_raices["Tipo"] == "Real"])
            imaginarias = len(df_raices) - reales
            c1.metric("Raíces Reales", reales)
            c2.metric("Raíces Complejas", imaginarias)

            # Tabla de resultados
            st.markdown("### 📋 Soluciones Encontradas")
            st.dataframe(
                df_raices[["ID", "Valor", "Tipo"]], 
                use_container_width=True, 
                hide_index=True
            )

            # Visualización en Plano de Argand
            if imaginarias > 0:
                st.markdown("### 📊 Localización en Plano Complejo")
                st.scatter_chart(
                    df_raices,
                    x="Real",
                    y="Imag",
                    color="Tipo",
                    size=100,
                    use_container_width=True
                )
            else:
                st.success("✨ Todas las raíces son reales. Se encuentran sobre el eje X.")
                
        except Exception as e:
            st.error(f"Hubo un error en el cálculo: {e}")

# --- Pie de página móvil ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("📱 Optimizado para visualización en dispositivos móviles.")