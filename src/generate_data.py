import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "constructora_data")
os.makedirs(DATA_DIR, exist_ok=True)

def generate_csv_inventario():
    data = {
        "ID": ["INV-001", "INV-002", "INV-003", "INV-004"],
        "Material": ["Cemento Melón", "Fierro Estructural 12mm", "Hormigón Preparado H30", "Ladrillo Cerámico 10x20x30"],
        "Cantidad_Stock": [450, 1200, 85, 3500],
        "Unidad": ["Sacos", "Barras", "m3", "Unidades"],
        "Ubicacion_Bodega": ["Bodega Central - A1", "Bodega Exterior - B3", "Planta Meclados", "Bodega Central - C2"],
        "Proveedor": ["Distribuidora El Teniente", "Acero Sur SpA", "Concrete Mix Chile", "Cerámicas del Pacífico"],
        "Precio_Unitario_CLP": [4800, 8500, 75000, 650],
        "Precio_Mayorista_CLP": [4200, 7800, 68000, 580],
        "Condicion_Mayorista": ["A partir de 100 sacos", "A partir de 500 barras", "A partir de 50 m3", "A partir de 1000 unidades"]
    }
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(DATA_DIR, "inventario_materiales.csv"), index=False)
    print("✓ inventario_materiales.csv generado.")

def generate_csv_nomina():
    data = {
        "ID_Empleado": ["EMP-101", "EMP-102", "EMP-103", "EMP-104"],
        "Nombre": ["María Paz Salamanca", "Carlos Ruiz Tagle", "Rodrigo Morales", "Valentina Silva"],
        "Cargo": ["Ingeniera Civil Estructural", "Jefe de Obra", "Técnico Electricista", "Especialista en Prevención de Riesgos"],
        "Certificaciones": ["LEED Green Associate, PMP", "Liderazgo en Inspección Técnica", "Certificación SEC Clase A", "ISO 45001 Auditor"],
        "Tipo_Contrato": ["Planta", "Planta", "Subcontratista", "Planta"],
        "Posibilidad_Ascenso": ["Sí (Candidata a Jefa de Proyecto)", "No", "Evaluación Anual", "Sí (Candidata a Directora HSE)"],
        "Renta_Aproximada_CLP": [2800000, 2100000, 1400000, 2300000]
    }
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(DATA_DIR, "nomina_y_personal.csv"), index=False)
    print("✓ nomina_y_personal.csv generado.")

def generate_pdf_catalogo():
    pdf_path = os.path.join(DATA_DIR, "catalogo_y_proyectos.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, leading=22)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=14, leading=18)
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, leading=14)

    story.append(Paragraph("Catálogo Oficial de Proyectos — Constructora Nova Build SpA", title_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Proyecto 1: Torre Miramar (Valparaíso)", heading_style))
    p1_text = (
        "La Torre Miramar es un desarrollo residencial ubicado en la costa de Valparaíso. "
        "Actualmente presenta un <b>65% de avance</b> en su ejecución. "
        "Inmobiliaria del Mar destacó la precisión en los plazos y la alta resistencia de la estructura ante marejadas e inviernos."
    )
    story.append(Paragraph(p1_text, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Proyecto 2: Parque Logístico San Pedro (Concepción)", heading_style))
    p2_text = (
        "Complejo industrial de alta eficiencia energética. Cuenta con un <b>90% de avance</b>. "
        "Logística Express resaltó la excelente distribución de bodegas y cumplimiento de normativas medioambientales."
    )
    story.append(Paragraph(p2_text, body_style))

    doc.build(story)
    print("✓ catalogo_y_proyectos.pdf generado.")

if __name__ == "__main__":
    print("Generando dataset inicial en constructora_data/...")
    generate_csv_inventario()
    generate_csv_nomina()
    generate_pdf_catalogo()
    print("¡Generación de datos completada!")