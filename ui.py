"""Streamlit UI components and utilities for the payment controller.

This module provides reusable UI components, styling functions, and
Streamlit-specific utilities for the payment control application.
"""

import streamlit as st
from typing import Optional, Dict, Callable, List, Any
from decimal import Decimal
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class UIConfig:
    """Configuration for UI styling and theming."""
    PRIMARY_COLOR = "#3B82F6"
    SUCCESS_COLOR = "#10B981"
    WARNING_COLOR = "#F59E0B"
    DANGER_COLOR = "#EF4444"
    
    METRIC_BOX_STYLE = """
    <div style=\"background-color: #f8f9fa; padding: 20px; border-radius: 10px; 
    border-left: 4px solid {color}; margin-bottom: 20px;\">
    <h4 style=\"color: {color}; margin: 0; font-size: 14px; text-transform: uppercase; 
    letter-spacing: 1px;\">{label}</h4>
    <p style=\"font-size: 28px; font-weight: bold; margin: 10px 0 0 0;\">{value}</p>
    </div>
    """


class StreamlitUI:
    """Core Streamlit UI components and utilities."""

    @staticmethod
    def render_metric_box(
        label: str,
        value: Any,
        color: str = UIConfig.PRIMARY_COLOR,
        suffix: str = ""
    ) -> None:
        """Render a custom metric box."""
        formatted_value = f"{value}{suffix}"
        html = UIConfig.METRIC_BOX_STYLE.format(
            label=label,
            color=color,
            value=formatted_value
        )
        st.markdown(html, unsafe_allow_html=True)

    @staticmethod
    def render_header(
        title: str,
        subtitle: Optional[str] = None,
        icon: str = "📊"
    ) -> None:
        """Render a styled page header."""
        st.markdown(f"# {icon} {title}")
        if subtitle:
            st.markdown(f"*{subtitle}*")
        st.divider()

    @staticmethod
    def render_sidebar_menu(
        menu_items: Dict[str, Callable]
    ) -> str:
        """Render a sidebar navigation menu.
        
        Args:
            menu_items: Dictionary of {label: callback_function}
            
        Returns:
            Selected menu item key
        """
        with st.sidebar:
            st.title("Navigation")
            selected = st.radio(
                "Select a page:",
                options=list(menu_items.keys()),
                label_visibility="collapsed"
            )
        return selected

    @staticmethod
    def render_input_form(
        fields: Dict[str, Dict[str, Any]],
        submit_button_label: str = "Submit"
    ) -> Dict[str, Any]:
        """Render a form with input fields.
        
        Args:
            fields: Dictionary defining form fields
            submit_button_label: Label for submit button
            
        Returns:
            Dictionary of form values
        """
        form_data = {}
        with st.form("input_form"):
            for field_name, field_config in fields.items():
                field_type = field_config.get("type", "text_input")
                label = field_config.get("label", field_name)
                
                if field_type == "text_input":
                    form_data[field_name] = st.text_input(
                        label,
                        value=field_config.get("value", "")
                    )
                elif field_type == "number_input":
                    form_data[field_name] = st.number_input(
                        label,
                        value=field_config.get("value", 0.0),
                        min_value=field_config.get("min_value", None),
                        max_value=field_config.get("max_value", None)
                    )
                elif field_type == "date_input":
                    form_data[field_name] = st.date_input(
                        label,
                        value=field_config.get("value", datetime.now())
                    )
                elif field_type == "selectbox":
                    form_data[field_name] = st.selectbox(
                        label,
                        options=field_config.get("options", [])
                    )
                elif field_type == "multiselect":
                    form_data[field_name] = st.multiselect(
                        label,
                        options=field_config.get("options", [])
                    )

            submitted = st.form_submit_button(submit_button_label)
            
        return form_data if submitted else None


class ChartsUI:
    """Components for data visualization."""

    @staticmethod
    def render_bar_chart(
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: str = "Bar Chart",
        color: str = UIConfig.PRIMARY_COLOR
    ) -> None:
        """Render a bar chart using Plotly."""
        fig = px.bar(
            data,
            x=x_column,
            y=y_column,
            title=title,
            color_discrete_sequence=[color]
        )
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def render_line_chart(
        data: pd.DataFrame,
        x_column: str,
        y_columns: List[str],
        title: str = "Line Chart"
    ) -> None:
        """Render a line chart using Plotly."""
        fig = px.line(
            data,
            x=x_column,
            y=y_columns,
            title=title
        )
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def render_pie_chart(
        data: pd.DataFrame,
        values_column: str,
        names_column: str,
        title: str = "Pie Chart"
    ) -> None:
        """Render a pie chart using Plotly."""
        fig = px.pie(
            data,
            values=values_column,
            names=names_column,
            title=title
        )
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def render_metric_gauge(
        value: float,
        min_value: float,
        max_value: float,
        title: str = "Metric"
    ) -> None:
        """Render a gauge chart."""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            gauge={
                'axis': {'range': [min_value, max_value]},
                'bar': {'color': UIConfig.PRIMARY_COLOR},
                'steps': [
                    {'range': [min_value, max_value * 0.33], 'color': UIConfig.DANGER_COLOR},
                    {'range': [max_value * 0.33, max_value * 0.66], 'color': UIConfig.WARNING_COLOR},
                    {'range': [max_value * 0.66, max_value], 'color': UIConfig.SUCCESS_COLOR}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)


class AlertsUI:
    """Components for displaying alerts and notifications."""

    @staticmethod
    def render_success_alert(message: str, icon: str = "✅") -> None:
        """Render a success alert."""
        st.success(f"{icon} {message}")

    @staticmethod
    def render_error_alert(message: str, icon: str = "❌") -> None:
        """Render an error alert."""
        st.error(f"{icon} {message}")

    @staticmethod
    def render_warning_alert(message: str, icon: str = "⚠️") -> None:
        """Render a warning alert."""
        st.warning(f"{icon} {message}")

    @staticmethod
    def render_info_alert(message: str, icon: str = "ℹ️") -> None:
        """Render an info alert."""
        st.info(f"{icon} {message}")


class TableUI:
    """Components for displaying tabular data."""

    @staticmethod
    def render_dataframe(
        data: pd.DataFrame,
        title: Optional[str] = None,
        use_container_width: bool = True,
        height: Optional[int] = None
    ) -> None:
        """Render a DataFrame with optional title."""
        if title:
            st.subheader(title)
        st.dataframe(
            data,
            use_container_width=use_container_width,
            height=height
        )

    @staticmethod
    def render_interactive_table(
        data: pd.DataFrame,
        title: Optional[str] = None
    ) -> None:
        """Render an interactive table using AgGrid."""
        if title:
            st.subheader(title)
        # Note: Requires streamlit-aggrid package
        try:
            from streamlit_aggrid import AgGrid
            AgGrid(data)
        except ImportError:
            st.warning("Install streamlit-aggrid for interactive tables")
            st.dataframe(data)
