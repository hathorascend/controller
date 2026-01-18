#!/usr/bin/env python3
"""PDF report generator for payment controller.

Generates professional PDF reports with transaction data and statistics.
"""

import streamlit as st
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Any


def generate_pdf_report(transactions: List[Dict[str, Any]]) -> bytes:
    """Generate PDF report from transaction data.
    
    Uses reportlab to create professional PDF with transaction summary.
    
    Args:
        transactions: List of transaction dictionaries
        
    Returns:
        PDF file bytes
    """
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.units import inch
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=1
    )
    title = Paragraph("💳 Control de Pagos 2026 - Reporte", title_style)
    elements.append(title)
    
    # Fecha del reporte
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=20
    )
    date_text = Paragraph(
        f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        date_style
    )
    elements.append(date_text)
    elements.append(Spacer(1, 0.3*inch))
    
    # Cálculos
    total_ingresos = sum(t.get('monto', 0) for t in transactions if t.get('tipo') == 'Ingreso')
    total_gastos = sum(t.get('monto', 0) for t in transactions if t.get('tipo') == 'Gasto')
    saldo = total_ingresos - total_gastos
    
    # Resumen
    summary_data = [
        ['Concepto', 'Monto (€)'],
        ['Total Ingresos', f'{total_ingresos:.2f}'],
        ['Total Gastos', f'{total_gastos:.2f}'],
        ['Saldo Neto', f'{saldo:.2f}']
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabla de transacciones
    if transactions:
        elements.append(Paragraph("Transacciones Detalladas", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        trans_data = [['Fecha', 'Concepto', 'Tipo', 'Monto (€)']]
        for trans in transactions[:20]:  # Limita a 20 transacciones
            fecha = trans.get('fecha')
            if hasattr(fecha, 'strftime'):
                fecha_str = fecha.strftime('%d/%m/%Y')
            else:
                fecha_str = str(fecha)
            
            trans_data.append([
                fecha_str,
                str(trans.get('concepto', '')),
                str(trans.get('tipo', '')),
                f"{trans.get('monto', 0):.2f}"
            ])
        
        trans_table = Table(trans_data, colWidths=[1.2*inch, 2*inch, 1*inch, 1.3*inch])
        trans_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(trans_table)
    
    # Construir PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


def create_pdf_download_button(transactions: List[Dict[str, Any]]) -> None:
    """Create a download button for PDF report in Streamlit.
    
    Args:
        transactions: List of transaction dictionaries
    """
    pdf_bytes = generate_pdf_report(transactions)
    filename = f"reporte_pagos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    st.download_button(
        label="📄 Descargar Reporte PDF",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        key="download_pdf"
    )
