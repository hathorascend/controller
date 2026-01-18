#!/usr/bin/env python3
"""Reusable Streamlit UI components for payment controller.

Provides wrapper functions and utilities for common Streamlit UI patterns
used throughout the application.
"""

import streamlit as st
from typing import Callable, Optional, Any
from datetime import datetime


def render_metric_card(
    title: str,
    value: str,
    delta: Optional[str] = None,
    icon: str = "📊",
    color_value: str = "#2ecc71"
) -> None:
    """Render a styled metric card with icon and optional delta.
    
    Args:
        title: Card title
        value: Main metric value
        delta: Optional percentage change indicator
        icon: Emoji icon for the card
        color_value: CSS color for the value text
    """
    html_content = f"""
    <div style="
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid {color_value};
        margin-bottom: 1rem;
    ">
        <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">
            {icon} {title}
        </div>
        <div style="font-size: 1.8rem; font-weight: bold; color: {color_value};">
            {value}
        </div>
        {f'<div style="font-size: 0.85rem; color: #888; margin-top: 0.5rem;">Δ {delta}</div>' if delta else ''}
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)


def render_header(title: str, subtitle: str = "") -> None:
    """Render a styled header section.
    
    Args:
        title: Main header text
        subtitle: Optional subtitle text
    """
    st.markdown(f"<h1 style='color: #1f77b4; margin-bottom: 0.5rem;'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p style='color: #666; margin-top: 0;'>{subtitle}</p>", unsafe_allow_html=True)
    st.divider()


def create_form_fields() -> dict[str, Any]:
    """Create a reusable transaction form with common fields.
    
    Returns:
        Dictionary with form field values
    """
    col1, col2 = st.columns(2)
    
    with col1:
        fecha = st.date_input("📅 Fecha", value=datetime.now())
        monto = st.number_input("💰 Monto (€)", min_value=0.01, value=100.0, step=0.01)
    
    with col2:
        tipo = st.selectbox("📍 Tipo", ["Ingreso", "Gasto"])
        concepto = st.text_input("🏷️ Concepto", placeholder="Ej: Salario, Comida, etc.")
    
    return {
        "fecha": fecha,
        "monto": monto,
        "tipo": tipo,
        "concepto": concepto
    }


def show_success_message(message: str) -> None:
    """Display a success message with icon.
    
    Args:
        message: Success message text
    """
    st.success(f"✅ {message}")


def show_error_message(message: str) -> None:
    """Display an error message with icon.
    
    Args:
        message: Error message text
    """
    st.error(f"⚠️ {message}")


def show_info_message(message: str) -> None:
    """Display an info message with icon.
    
    Args:
        message: Info message text
    """
    st.info(f"💡 {message}")


def render_sidebar_menu() -> str:
    """Render application sidebar menu.
    
    Returns:
        Selected menu option
    """
    with st.sidebar:
        st.header("⚙️ Menú Principal")
        selected = st.radio(
            "Selecciona una opción:",
            ["Dashboard", "Registrar Pago", "Reportes", "Análisis"]
        )
        st.divider()
        st.info("💳 Control de Pagos 2026 v1.0")
        return selected


def render_stats_row(
    stats: dict[str, tuple[str, str, Optional[str]]]
) -> None:
    """Render a row of statistics cards.
    
    Args:
        stats: Dict with stat_name: (value, delta, icon) tuples
    """
    cols = st.columns(len(stats))
    for col, (key, (value, delta, icon)) in zip(cols, stats.items()):
        with col:
            st.metric(
                label=f"{icon} {key}",
                value=value,
                delta=delta
            )
