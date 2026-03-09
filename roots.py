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
    """Calcula raíces con NumPy y formatea resultados."""
    raices = np.roots(coeficientes)
    datos = []
    for i, r in enumerate(raices):
        # Formateo a 1 decimal para consistencia
        if np.isreal(r):
            valor_str = f"{r.real:.1f}"
        else:
            signo = "+" if r.imag >= 0 else "-"
            valor_str = f"{r.real:.1f} {signo} {abs(r.imag):.1f}i"
            
        datos.append({
            "ID": f"x{i+1}",
            "Valor": valor_str,
            "Tipo": "Real" if np.isreal(r) else "Compleja",
            "Real": round(r.real, 1),
            "Imag": round(r.imag, 1)
        })
    return pd.DataFrame(datos)

# --- Interfaz de Usuario ---
st.title("🎯 Buscador de Raíces")
st.markdown("---")

# --- Configuración en Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuración")
    grado = st.number_input("Grado del Polinomio", min_value=1, max_value=20, value=3, step=1)
    st.info("Configurado para saltos de 1.0 unidad y precisión de 0.1.")

# --- Entrada de Coeficientes (Columna Única y Paso de 1 Unidad) ---
st.subheader("📝 Coeficientes del Polinomio")
st.caption("Usa los botones + / - para saltos de unidad completa.")

with st.expander("Abrir Editor de Coeficientes", expanded=True):
    coefs = []
    for i in range(grado + 1):
        potencia = grado - i
        if potencia > 1:
            label = f"Coeficiente de x^{potencia}"
        elif potencia == 1:
            label = "Coeficiente de x"
        else:
            label = "Término Independiente"
            
        # step=1.0 obliga al incremento de unidad en unidad
        # format="%.1f" limita la visualización a una decimal
        val = st.number_input(
            label, 
            value=1.0 if i == 0 else 0.0, 
            key=f"c_input_{i}",
            step=1.0,
            format="%.1f"
        )
        coefs.append(val)

# --- Procesamiento y Resultados ---
st.markdown("---")
if st.button("🚀 Calcular Raíces Ahora", type="primary", use_container_width=True):
    if coefs[0] == 0:
        st.warning("⚠️ El coeficiente principal no puede ser 0.")
    else:
        try:
            df_raices = calcular_raices(coefs)
            
            # Métricas
            c1, c2 = st.columns(2)
            reales = len(df_raices[df_raices["Tipo"] == "Real"])
            imaginarias = len(df_raices) - reales
            c1.metric("Raíces Reales", reales)
            c2.metric("Raíces Complejas", imaginarias)

            # Tabla
            st.markdown("### 📋 Soluciones")
            st.dataframe(
                df_raices[["ID", "Valor", "Tipo"]], 
                use_container_width=True, 
                hide_index=True
            )

            # Gráfico
            if imaginarias > 0:
                st.markdown("### 📊 Plano Complejo")
                st.scatter_chart(
                    df_raices,
                    x="Real",
                    y="Imag",
                    color="Tipo",
                    use_container_width=True
                )
            else:
                st.success("✨ Todas las raíces son reales.")
                
        except Exception as e:
            st.error(f"Error: {e}")

st.caption("📱 Interfaz optimizada: Saltos de 1.0 | Precisión 0.1")