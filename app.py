#!/usr/bin/env python3
"""Main Streamlit application for payment controller (2026)."""

import streamlit as st
from datetime import datetime, timedelta
from decimal import Decimal
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Control de Pagos 2026",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 class='main-header'>💳 Control de Pagos 2026</h1>", unsafe_allow_html=True)
st.markdown("*Aplicación Streamlit para gestionar y controlar los pagos mensuales*")
st.divider()

# Sidebar - Navegación
with st.sidebar:
    st.header("⚙️ Configuración")
    menu = st.radio(
        "Selecciona una página:",
        ["Dashboard", "Registrar Pago", "Reportes", "Análisis"]
    )
    st.divider()
    st.info("👨‍💼 Aplicación desarrollada con Streamlit y Python")

# Datos de ejemplo (simulado en sesión)
if "transactions" not in st.session_state:
    st.session_state.transactions = [
        {"fecha": datetime.now() - timedelta(days=30), "monto": 500, "concepto": "Salario", "tipo": "Ingreso"},
        {"fecha": datetime.now() - timedelta(days=25), "monto": 150, "concepto": "Servicios", "tipo": "Gasto"},
        {"fecha": datetime.now() - timedelta(days=20), "monto": 80, "concepto": "Comida", "tipo": "Gasto"},
        {"fecha": datetime.now() - timedelta(days=15), "monto": 200, "concepto": "Consultoría", "tipo": "Ingreso"},
        {"fecha": datetime.now() - timedelta(days=10), "monto": 50, "concepto": "Transporte", "tipo": "Gasto"},
    ]

# Página: Dashboard
if menu == "Dashboard":
    st.subheader("📊 Dashboard Principal")
    
    # Cálculos
    total_ingresos = sum([t["monto"] for t in st.session_state.transactions if t["tipo"] == "Ingreso"])
    total_gastos = sum([t["monto"] for t in st.session_state.transactions if t["tipo"] == "Gasto"])
    saldo = total_ingresos - total_gastos
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Ingresos", f"€{total_ingresos:,.2f}", delta="+2.5%")
    
    with col2:
        st.metric("💸 Gastos", f"€{total_gastos:,.2f}", delta="-1.2%")
    
    with col3:
        st.metric("💎 Saldo", f"€{saldo:,.2f}", delta=f"+€{saldo:,.2f}")
    
    with col4:
        st.metric("📈 Ratio", f"{(saldo/total_ingresos*100):.1f}%", delta="+5.2%")
    
    st.divider()
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📉 Ingresos vs Gastos")
        data = pd.DataFrame({
            "Tipo": ["Ingresos", "Gastos"],
            "Monto": [total_ingresos, total_gastos]
        })
        fig = px.bar(data, x="Tipo", y="Monto", color="Tipo", 
                     color_discrete_map={"Ingresos": "#2ecc71", "Gastos": "#e74c3c"})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Distribución de Gastos")
        gastos_df = pd.DataFrame(st.session_state.transactions)
        gastos_df = gastos_df[gastos_df["tipo"] == "Gasto"]
        if not gastos_df.empty:
            fig = px.pie(gastos_df, values="monto", names="concepto", title="Por Concepto")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay gastos registrados")
    
    st.divider()
    
    # Tabla de transacciones
    st.subheader("📋 Últimas Transacciones")
    df_display = pd.DataFrame(st.session_state.transactions)
    df_display["fecha"] = df_display["fecha"].dt.strftime("%d/%m/%Y")
    df_display["monto"] = "€" + df_display["monto"].astype(str)
    st.dataframe(df_display, use_container_width=True, hide_index=True)

# Página: Registrar Pago
elif menu == "Registrar Pago":
    st.subheader("➕ Registrar Nueva Transacción")
    
    with st.form("form_pago"):
        col1, col2 = st.columns(2)
        
        with col1:
            fecha = st.date_input("Fecha", value=datetime.now())
            monto = st.number_input("Monto (€)", min_value=0.01, value=100.0, step=0.01)
        
        with col2:
            tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
            concepto = st.text_input("Concepto", placeholder="Ej: Salario, Comida, etc.")
        
        submitted = st.form_submit_button("✅ Registrar Transacción")
        
        if submitted:
            if concepto:
                st.session_state.transactions.append({
                    "fecha": datetime.combine(fecha, datetime.min.time()),
                    "monto": monto,
                    "concepto": concepto,
                    "tipo": tipo
                })
                st.success(f"✅ Transacción de €{monto:.2f} ({tipo}) registrada correctamente")
            else:
                st.error("⚠️ Por favor ingresa un concepto")

# Página: Reportes
elif menu == "Reportes":
    st.subheader("📊 Reportes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Transacciones", len(st.session_state.transactions))
    
    with col2:
        st.metric("Período", "Último mes")
    
    st.divider()
    
    # Resumen mensual
    st.subheader("📅 Resumen por Tipo")
    total_ingresos = sum([t["monto"] for t in st.session_state.transactions if t["tipo"] == "Ingreso"])
    total_gastos = sum([t["monto"] for t in st.session_state.transactions if t["tipo"] == "Gasto"])
    saldo = total_ingresos - total_gastos
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"<div class='metric-card'><h4>📈 Ingresos</h4><p style='font-size: 1.5rem;'>€{total_ingresos:,.2f}</p></div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div class='metric-card'><h4>📉 Gastos</h4><p style='font-size: 1.5rem;'>€{total_gastos:,.2f}</p></div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<div class='metric-card'><h4>💰 Saldo</h4><p style='font-size: 1.5rem; color: {'#2ecc71' if saldo >= 0 else '#e74c3c'};'>€{saldo:,.2f}</p></div>", unsafe_allow_html=True)

# Página: Análisis
elif menu == "Análisis":
    st.subheader("📈 Análisis Avanzado")
    
    # Proyección de saldo
    st.subheader("📊 Proyección de Saldo (Próximos 3 meses)")
    
    total_ingresos = sum([t["monto"] for t in st.session_state.transactions if t["tipo"] == "Ingreso"])
    total_gastos = sum([t["monto"] for t in st.session_state.transactions if t["tipo"] == "Gasto"])
    saldo_inicial = total_ingresos - total_gastos
    
    meses = []
    saldos = []
    
    for i in range(1, 4):
        saldo_proyectado = saldo_inicial + (total_ingresos - total_gastos) * i
        meses.append(f"Mes {i}")
        saldos.append(saldo_proyectado)
    
    df_proyeccion = pd.DataFrame({"Mes": meses, "Saldo Proyectado": saldos})
    fig = px.line(df_proyeccion, x="Mes", y="Saldo Proyectado", markers=True, 
                  title="Proyección de Saldo")
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    st.success("✅ Aplicación funcionando correctamente")
    st.info("💡 Próximas mejoras: Exportación a PDF, Gráficos avanzados, Integración con APIs bancarias")
