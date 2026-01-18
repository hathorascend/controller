#!/usr/bin/env python3
"""Data export manager for payment controller.

Handles exporting user data to JSON format for local-first storage.
Enables users to download and restore their data without a database.
"""

import json
import streamlit as st
from datetime import datetime
from typing import Dict, List, Any, Optional


def serialize_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert transaction list to serializable format.
    
    Handles datetime objects which are not JSON serializable.
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        List of serialized transactions
    """
    serialized = []
    for trans in transactions:
        trans_copy = trans.copy()
        if 'fecha' in trans_copy and hasattr(trans_copy['fecha'], 'isoformat'):
            trans_copy['fecha'] = trans_copy['fecha'].isoformat()
        serialized.append(trans_copy)
    return serialized


def export_to_json(session_data: Dict[str, Any]) -> str:
    """Export session data to JSON format.
    
    Creates a structured JSON export with metadata and transactions.
    
    Args:
        session_data: Dictionary with key 'transactions' from st.session_state
        
    Returns:
        JSON string with all session data
    """
    export_data = {
        "version": "1.0",
        "exported_at": datetime.now().isoformat(),
        "app_name": "Control de Pagos 2026",
        "transactions": serialize_transactions(
            session_data.get('transactions', [])
        )
    }
    return json.dumps(export_data, indent=2, ensure_ascii=False)


def generate_export_filename() -> str:
    """Generate a timestamped filename for the export.
    
    Returns:
        Filename with format: pagos_control_YYYYMMDD_HHMMSS.json
    """
    now = datetime.now()
    return f"pagos_control_{now.strftime('%Y%m%d_%H%M%S')}.json"


def create_download_button(json_data: str, filename: str) -> None:
    """Create a download button for JSON export in Streamlit.
    
    Args:
        json_data: JSON string to download
        filename: Name for the downloaded file
    """
    st.download_button(
        label="💾 Descargar mis datos (JSON)",
        data=json_data,
        file_name=filename,
        mime="application/json",
        key="download_data"
    )


def export_summary(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a summary of exported data.
    
    Args:
        transactions: List of transactions
        
    Returns:
        Dictionary with summary statistics
    """
    total_ingresos = sum(
        t.get('monto', 0) for t in transactions if t.get('tipo') == 'Ingreso'
    )
    total_gastos = sum(
        t.get('monto', 0) for t in transactions if t.get('tipo') == 'Gasto'
    )
    
    return {
        "total_transactions": len(transactions),
        "total_ingresos": total_ingresos,
        "total_gastos": total_gastos,
        "saldo_neto": total_ingresos - total_gastos,
        "exported_at": datetime.now().isoformat()
    }
