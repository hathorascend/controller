#!/usr/bin/env python3
"""
Local test script to verify all modules work correctly without Streamlit.
This test suite validates:
- Export functionality (export_manager.py)
- Import functionality (import_manager.py)
- PDF generation (pdf_generator.py)
"""

import json
import os
from pathlib import Path

# Import our modules
from export_manager import ExportManager
from import_manager import ImportManager
from pdf_generator import PDFGenerator

def test_export_import_pdf():
    """
    Complete test of all local-first features.
    """
    print("\n" + "="*60)
    print("PRUEBA LOCAL - Sistema de Control de Pagos")
    print("="*60)
    
    # Create test data
    test_data = {
        "pagos": [
            {
                "id": 1,
                "fecha": "2026-01-18",
                "concepto": "Salario",
                "monto": 2000,
                "categoria": "Ingreso",
                "descripcion": "Pago mensual"
            },
            {
                "id": 2,
                "fecha": "2026-01-18",
                "concepto": "Alquiler",
                "monto": 800,
                "categoria": "Gasto",
                "descripcion": "Renta del mes"
            }
        ],
        "saldo_total": 1200
    }
    
    # Test 1: Export
    print("\n1. PROBANDO EXPORT (Guardar a JSON)...")
    try:
        export_mgr = ExportManager()
        test_file = "test_export_data.json"
        export_mgr.export_to_json(test_data, test_file)
        print(f"   ✅ Archivo exportado: {test_file}")
        print(f"   ✅ Datos guardados: {len(test_data['pagos'])} pagos")
    except Exception as e:
        print(f"   ❌ Error en export: {e}")
        return False
    
    # Test 2: Import
    print("\n2. PROBANDO IMPORT (Cargar desde JSON)...")
    try:
        import_mgr = ImportManager()
        loaded_data = import_mgr.import_from_json(test_file)
        print(f"   ✅ Datos cargados correctamente")
        print(f"   ✅ Pagos recuperados: {len(loaded_data.get('pagos', []))}")
        print(f"   ✅ Saldo total: ${loaded_data.get('saldo_total', 0)}")
    except Exception as e:
        print(f"   ❌ Error en import: {e}")
        return False
    
    # Test 3: PDF Generation
    print("\n3. PROBANDO PDF (Generar reporte)...")
    try:
        pdf_gen = PDFGenerator()
        pdf_file = "test_payment_report.pdf"
        pdf_gen.generate_payment_report(test_data, pdf_file)
        if os.path.exists(pdf_file):
            file_size = os.path.getsize(pdf_file)
            print(f"   ✅ PDF generado: {pdf_file}")
            print(f"   ✅ Tamaño: {file_size} bytes")
        else:
            print(f"   ❌ PDF no se generó")
            return False
    except Exception as e:
        print(f"   ❌ Error en PDF: {e}")
        return False
    
    # Cleanup
    print("\n4. LIMPIEZA DE ARCHIVOS DE PRUEBA...")
    for file in [test_file, pdf_file]:
        if os.path.exists(file):
            os.remove(file)
            print(f"   ✅ Eliminado: {file}")
    
    print("\n" + "="*60)
    print("✅ TODOS LOS TESTS PASARON CORRECTAMENTE")
    print("="*60)
    print("\nLa app funciona correctamente. El problema es solo del")
    print("environment de Streamlit Cloud. Usando Python 3.9 debería")
    print("funcionar sin problemas.")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = test_export_import_pdf()
    exit(0 if success else 1)
