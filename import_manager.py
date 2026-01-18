#!/usr/bin/env python3
"""Data import manager for payment controller.

Handles importing user data from JSON files exported by export_manager.
Restores user data into session state for immediate use.
"""

import json
import streamlit as st
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional


def parse_json_file(uploaded_file) -> Tuple[bool, Dict[str, Any], str]:
    """Parse and validate uploaded JSON file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Tuple of (success: bool, data: dict, message: str)
    """
    try:
        content = uploaded_file.read().decode('utf-8')
        data = json.loads(content)
        return True, data, "Archivo leído exitosamente"
    except json.JSONDecodeError as e:
        return False, {}, f"Error al parsear JSON: {str(e)}"
    except Exception as e:
        return False, {}, f"Error inesperado: {str(e)}"


def validate_import_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate imported data structure.
    
    Args:
        data: Parsed JSON data
        
    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    required_keys = ['version', 'app_name', 'transactions']
    for key in required_keys:
        if key not in data:
            return False, f"Falta clave requerida: {key}"
    
    if not isinstance(data['transactions'], list):
        return False, "Las transacciones deben ser una lista"
    
    for trans in data['transactions']:
        if not isinstance(trans, dict):
            return False, "Cada transacción debe ser un diccionario"
        required_trans_keys = ['fecha', 'monto', 'concepto', 'tipo']
        for key in required_trans_keys:
            if key not in trans:
                return False, f"Transacción sin clave: {key}"
    
    return True, ""


def deserialize_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert ISO datetime strings back to datetime objects.
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        List with deserialized transactions
    """
    from datetime import date
    deserialized = []
    for trans in transactions:
        trans_copy = trans.copy()
        if 'fecha' in trans_copy and isinstance(trans_copy['fecha'], str):
            try:
                trans_copy['fecha'] = datetime.fromisoformat(trans_copy['fecha']).date()
            except:
                pass
        deserialized.append(trans_copy)
    return deserialized


def import_from_json(uploaded_file) -> Tuple[bool, str]:
    """Import data from JSON file and restore to session state.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    success, data, parse_msg = parse_json_file(uploaded_file)
    if not success:
        return False, parse_msg
    
    is_valid, validation_msg = validate_import_data(data)
    if not is_valid:
        return False, validation_msg
    
    try:
        transactions = deserialize_transactions(data.get('transactions', []))
        st.session_state.transactions = transactions
        
        count = len(transactions)
        return True, f"✅ Importados {count} registros exitosamente"
    except Exception as e:
        return False, f"Error al restaurar datos: {str(e)}"


def create_upload_widget() -> None:
    """Create file uploader widget for Streamlit."""
    st.markdown("### 📤 Cargar mis datos")
    st.info("Sube un archivo JSON que hayas descargado anteriormente para recuperar tus datos")
    
    uploaded_file = st.file_uploader(
        "Selecciona archivo JSON",
        type=['json'],
        key="import_file"
    )
    
    if uploaded_file is not None:
        success, message = import_from_json(uploaded_file)
        if success:
            st.success(message)
            st.balloons()
        else:
            st.error(message)


def get_import_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract statistics from imported data.
    
    Args:
        data: Parsed JSON data
        
    Returns:
        Dictionary with statistics
    """
    transactions = data.get('transactions', [])
    total_ingresos = sum(
        t.get('monto', 0) for t in transactions if t.get('tipo') == 'Ingreso'
    )
    total_gastos = sum(
        t.get('monto', 0) for t in transactions if t.get('tipo') == 'Gasto'
    )
    
    return {
        "total_registros": len(transactions),
        "total_ingresos": total_ingresos,
        "total_gastos": total_gastos,
        "saldo": total_ingresos - total_gastos,
        "exported_at": data.get('exported_at', 'Desconocido')
    }
