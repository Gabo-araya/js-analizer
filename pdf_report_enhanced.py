#!/usr/bin/env python3
"""
Generador de Reportes PDF Mejorado para Analizador de Librerías JavaScript & CSS

Este módulo proporciona generación avanzada de PDF con estilo profesional,
contenido integral y elementos visuales para reportes de análisis de seguridad.
"""

import io
import json
from datetime import datetime
import pytz
from urllib.parse import urlparse

# Configuración de timezone para Chile
CHILE_TZ = pytz.timezone('America/Santiago')

def get_chile_time():
    """Obtiene la fecha y hora actual en timezone de Chile."""
    return datetime.now(CHILE_TZ)

def format_chile_time(dt_obj=None, fmt='%d-%m-%Y %H:%M'):
    """Formatea fecha/hora en timezone de Chile."""
    if dt_obj is None:
        dt_obj = get_chile_time()
    elif dt_obj.tzinfo is None:
        # Si el datetime no tiene timezone, asumimos UTC y convertimos a Chile
        dt_obj = pytz.UTC.localize(dt_obj).astimezone(CHILE_TZ)
    elif dt_obj.tzinfo != CHILE_TZ:
        # Si tiene otro timezone, convertir a Chile
        dt_obj = dt_obj.astimezone(CHILE_TZ)
    return dt_obj.strftime(fmt)

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.graphics.shapes import Drawing, Circle, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas


class EnhancedPDFReport:
    """Generador de reportes PDF mejorado con estilo profesional y contenido integral"""
    
    def __init__(self):
        self.story = []
        self.styles = self._create_custom_styles()
    
    def _row_to_dict(self, row):
        """Convierte sqlite3.Row a diccionario para compatibilidad"""
        if hasattr(row, 'keys'):
            return dict(row)
        return row
        
    def _create_custom_styles(self):
        """Crea estilos de párrafo personalizados para el reporte"""
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=1  # Alineación centrada
        ))
        
        styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=15,
            spaceBefore=20,
            borderWidth=1,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=8,
            backColor=colors.HexColor('#ecf0f1')
        ))
        
        styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=15,
            borderWidth=0,
            borderPadding=5,
            backColor=colors.HexColor('#f8f9fa'),
            borderColor=colors.HexColor('#3498db')
        ))
        
        styles.add(ParagraphStyle(
            name='SecurityCritical',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#e74c3c'),
            backColor=colors.HexColor('#fdf2f2'),
            borderWidth=1,
            borderColor=colors.HexColor('#e74c3c'),
            borderPadding=5,
            spaceBefore=5,
            spaceAfter=5
        ))
        
        styles.add(ParagraphStyle(
            name='SecurityGood',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#27ae60'),
            backColor=colors.HexColor('#f0f9f0'),
            borderWidth=1,
            borderColor=colors.HexColor('#27ae60'),
            borderPadding=5,
            spaceBefore=5,
            spaceAfter=5
        ))
        
        styles.add(ParagraphStyle(
            name='RecommendationBox',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#2c3e50'),
            backColor=colors.HexColor('#fff3cd'),
            borderWidth=1,
            borderColor=colors.HexColor('#ffc107'),
            borderPadding=8,
            spaceBefore=10,
            spaceAfter=10,
            leftIndent=20,
            rightIndent=20
        ))
        
        return styles
    
    def _create_header_footer(self, canvas_obj, doc):
        """Crea encabezado y pie de página personalizados para todas las páginas"""
        canvas_obj.saveState()
        
        # Encabezado
        canvas_obj.setFont('Helvetica-Bold', 10)
        canvas_obj.setFillColor(colors.HexColor('#34495e'))
        canvas_obj.drawString(50, A4[1] - 30, "Reporte de Análisis de Seguridad - Librerías JavaScript & CSS")
        canvas_obj.drawString(A4[0] - 150, A4[1] - 30, format_chile_time(fmt='%d-%m-%Y %H:%M'))
        
        # Línea del encabezado
        canvas_obj.setStrokeColor(colors.HexColor('#3498db'))
        canvas_obj.setLineWidth(2)
        canvas_obj.line(50, A4[1] - 40, A4[0] - 50, A4[1] - 40)
        
        # Pie de página
        canvas_obj.setFont('Helvetica', 8)
        canvas_obj.setFillColor(colors.grey)
        canvas_obj.drawString(50, 30, "Generado por Analizador de Librerías JS/CSS")
        canvas_obj.drawRightString(A4[0] - 50, 30, f"Página {doc.page}")
        
        # Línea del pie de página
        canvas_obj.setStrokeColor(colors.HexColor('#3498db'))
        canvas_obj.setLineWidth(1)
        canvas_obj.line(50, 45, A4[0] - 50, 45)
        
        canvas_obj.restoreState()
    
    def _create_security_score_visual(self, score):
        """Crea una representación visual del puntaje de seguridad"""
        drawing = Drawing(200, 100)
        
        # Círculo de fondo
        bg_circle = Circle(50, 50, 40, fillColor=colors.HexColor('#ecf0f1'), strokeColor=colors.grey)
        drawing.add(bg_circle)
        
        # Color basado en puntaje
        if score >= 80:
            color = colors.HexColor('#27ae60')  # Verde
        elif score >= 60:
            color = colors.HexColor('#f39c12')  # Naranja
        else:
            color = colors.HexColor('#e74c3c')  # Rojo
        
        # Círculo del puntaje
        score_circle = Circle(50, 50, 35, fillColor=color, strokeColor=color)
        drawing.add(score_circle)
        
        # Texto del puntaje
        score_text = String(50, 50, f"{score}%", fontSize=16, fillColor=colors.white, textAnchor='middle')
        drawing.add(score_text)
        
        # Etiqueta
        label_text = String(50, 20, "Puntaje de Seguridad", fontSize=10, fillColor=colors.black, textAnchor='middle')
        drawing.add(label_text)
        
        return drawing
    
    def _create_vulnerability_chart(self, libraries):
        """Create a chart showing vulnerability distribution"""
        vulnerable_count = 0
        safe_count = 0
        unknown_count = 0
        
        for lib in libraries:
            lib_dict = self._row_to_dict(lib)
            has_vuln = (lib_dict.get('latest_safe_version') and lib_dict.get('version') and 
                       lib_dict['version'] != lib_dict['latest_safe_version'] and 
                       lib_dict['version'] < lib_dict['latest_safe_version'])
            
            if has_vuln:
                vulnerable_count += 1
            elif lib_dict.get('latest_safe_version'):
                safe_count += 1
            else:
                unknown_count += 1
        
        if vulnerable_count + safe_count + unknown_count == 0:
            return None
        
        drawing = Drawing(300, 200)
        pie = Pie()
        pie.x = 50
        pie.y = 50
        pie.width = 150
        pie.height = 150
        pie.data = [vulnerable_count, safe_count, unknown_count]
        pie.labels = ['Vulnerables', 'Seguras', 'Desconocidas']
        pie.slices.strokeWidth = 2
        pie.slices[0].fillColor = colors.HexColor('#e74c3c')
        pie.slices[1].fillColor = colors.HexColor('#27ae60')
        pie.slices[2].fillColor = colors.HexColor('#95a5a6')
        
        drawing.add(pie)
        return drawing
    
    def generate_enhanced_report(self, data):
        """Generate the complete enhanced PDF report"""
        self.story = []
        
        # Title Page
        self._add_title_page(data)
        
        # Executive Summary
        self._add_executive_summary(data)
        
        # Scan Information
        self._add_scan_information(data)
        
        # Security Analysis (Enhanced)
        self._add_enhanced_security_analysis(data)
        
        # Libraries Analysis (Enhanced)
        self._add_enhanced_libraries_analysis(data)
        
        # Technical Details
        self._add_technical_details(data)
        
        # Recommendations
        self._add_recommendations(data)
        
        # Appendices
        self._add_appendices(data)
        
        return self.story
    
    def _add_title_page(self, data):
        """Add a professional title page"""
        self.story.append(Spacer(1, 2*inch))
        
        # Título principal
        self.story.append(Paragraph("Reporte de Análisis de Seguridad Web", self.styles['CustomTitle']))
        self.story.append(Spacer(1, 0.5*inch))
        
        # Convierte datos del escaneo a dict para compatibilidad
        scan_dict = self._row_to_dict(data['scan'])
        
        # URL que se está analizando
        url_display = scan_dict['url']
        if len(url_display) > 60:
            url_display = url_display[:57] + "..."
        
        self.story.append(Paragraph(f"<b>URL Objetivo:</b> {url_display}", self.styles['Heading2']))
        self.story.append(Spacer(1, 0.3*inch))
        
        # Metadatos del escaneo
        scan_date_str = scan_dict['scan_date']
        try:
            # Intentar diferentes formatos de fecha
            if 'Z' in scan_date_str:
                scan_date = datetime.fromisoformat(scan_date_str.replace('Z', '+00:00'))
            elif 'T' in scan_date_str:
                scan_date = datetime.fromisoformat(scan_date_str)
            else:
                scan_date = datetime.strptime(scan_date_str, '%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            scan_date = get_chile_time()  # Fallback a fecha actual de Chile
        
        info_data = [
            ['Fecha de Escaneo', format_chile_time(scan_date, '%d de %B, %Y a las %H:%M CLT')],
            ['Reporte Generado', format_chile_time(fmt='%d de %B, %Y a las %H:%M CLT')],
            ['Código de Estado', str(scan_dict.get('status_code') or 'Error')],
            ['Librerías Encontradas', str(len(data['libraries']))],
            ['Puntaje de Seguridad', f"{data['security_analysis']['security_score']}%"]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7'))
        ]))
        
        self.story.append(info_table)
        self.story.append(PageBreak())
    
    def _add_executive_summary(self, data):
        """Agrega una sección de resumen ejecutivo"""
        self.story.append(Paragraph("Resumen Ejecutivo", self.styles['CustomHeading1']))
        
        # Resumen general
        total_libs = len(data['libraries'])
        vulnerable_libs = sum(1 for lib in data['libraries'] 
                            if self._row_to_dict(lib).get('latest_safe_version') and self._row_to_dict(lib).get('version') 
                            and self._row_to_dict(lib)['version'] != self._row_to_dict(lib)['latest_safe_version'] 
                            and self._row_to_dict(lib)['version'] < self._row_to_dict(lib)['latest_safe_version'])
        
        security_score = data['security_analysis']['security_score']
        
        # Convierte datos del escaneo a dict para compatibilidad
        scan_dict = self._row_to_dict(data['scan'])
        
        summary_text = f"""
        Este reporte proporciona un análisis integral de seguridad de {scan_dict['url']}. 
        Nuestro escáner automatizado identificó {total_libs} librerías JavaScript y CSS, 
        con {vulnerable_libs} librerías potencialmente vulnerables que requieren atención.
        
        El sitio web obtuvo un puntaje de cabeceras de seguridad de {security_score}% basado en la presencia 
        de {len(data['security_analysis']['present'])} de 7 cabeceras de seguridad recomendadas.
        """
        
        self.story.append(Paragraph(summary_text, self.styles['Normal']))
        
        # Hallazgos clave
        self.story.append(Paragraph("Hallazgos Principales:", self.styles['CustomHeading2']))
        
        findings = []
        if vulnerable_libs > 0:
            findings.append(f"🔴 {vulnerable_libs} librerías pueden tener vulnerabilidades conocidas")
        if security_score < 70:
            findings.append(f"🟡 La implementación de cabeceras de seguridad necesita mejoras ({security_score}%)")
        if len(data['security_analysis']['missing']) > 0:
            findings.append(f"⚠️ {len(data['security_analysis']['missing'])} cabeceras de seguridad críticas están ausentes")
        
        if not findings:
            findings.append("✅ No se identificaron preocupaciones de seguridad inmediatas")
        
        for finding in findings:
            self.story.append(Paragraph(f"• {finding}", self.styles['Normal']))
        
        self.story.append(Spacer(1, 20))
    
    def _add_scan_information(self, data):
        """Agrega información detallada del escaneo"""
        self.story.append(Paragraph("Información del Escaneo", self.styles['CustomHeading1']))
        
        # Basic information table
        scan_dict = self._row_to_dict(data['scan'])
        parsed_url = urlparse(scan_dict['url'])
        
        scan_info = [
            ['Parámetro', 'Valor', 'Detalles'],
            ['URL Completa', scan_dict['url'], 'URL objetivo completa'],
            ['Dominio', parsed_url.netloc, 'Dominio objetivo'],
            ['Protocolo', parsed_url.scheme.upper(), 'Protocolo de conexión'],
            ['Título de Página', scan_dict.get('title') or 'Sin título encontrado', 'Elemento título HTML'],
            ['Estado HTTP', str(scan_dict.get('status_code')), 'Código de respuesta del servidor'],
            ['Timestamp del Escaneo', scan_dict['scan_date'], 'Cuándo se realizó el escaneo'],
            ['Archivos JS Encontrados', str(len([f for f in data['file_urls'] if self._row_to_dict(f)['file_type'] == 'js'])), 'Archivos JavaScript descubiertos'],
            ['Archivos CSS Encontrados', str(len([f for f in data['file_urls'] if self._row_to_dict(f)['file_type'] == 'css'])), 'Archivos de estilo descubiertos'],
            ['Cadenas de Versión', str(len(data['version_strings'])), 'Referencias de versión encontradas en archivos']
        ]
        
        scan_table = Table(scan_info, colWidths=[1.5*inch, 2*inch, 2.5*inch])
        scan_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#ecf0f1')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        self.story.append(scan_table)
        self.story.append(Spacer(1, 20))
    
    def _add_enhanced_security_analysis(self, data):
        """Agrega análisis de seguridad mejorado con elementos visuales"""
        self.story.append(Paragraph("Análisis de Seguridad", self.styles['CustomHeading1']))
        
        # Add security score visual
        score_visual = self._create_security_score_visual(data['security_analysis']['security_score'])
        self.story.append(score_visual)
        self.story.append(Spacer(1, 15))
        
        # Cabeceras presentes (detallado)
        if data['security_analysis']['present']:
            self.story.append(Paragraph("✅ Cabeceras de Seguridad Implementadas", self.styles['CustomHeading2']))
            
            present_data = [['Cabecera', 'Valor', 'Beneficio de Seguridad']]
            
            for header in data['security_analysis']['present']:
                value_display = header['value'][:50] + '...' if len(header['value']) > 50 else header['value']
                present_data.append([
                    header['name'],
                    value_display,
                    header['description']
                ])
            
            present_table = Table(present_data, colWidths=[1.8*inch, 2*inch, 2.2*inch])
            present_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#27ae60')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f9f0'))
            ]))
            
            self.story.append(present_table)
        
        # Cabeceras faltantes (críticas)
        if data['security_analysis']['missing']:
            self.story.append(Spacer(1, 15))
            self.story.append(Paragraph("🔴 Cabeceras de Seguridad Faltantes (Críticas)", self.styles['CustomHeading2']))
            
            missing_data = [['Cabecera', 'Nivel de Riesgo', 'Valor Recomendado', 'Impacto']]
            
            # Define risk levels for different headers
            risk_levels = {
                'Strict-Transport-Security': 'HIGH',
                'Content-Security-Policy': 'CRITICAL',
                'X-Frame-Options': 'HIGH',
                'X-Content-Type-Options': 'MEDIUM',
                'X-XSS-Protection': 'MEDIUM',
                'Referrer-Policy': 'LOW',
                'Permissions-Policy': 'LOW'
            }
            
            for header in data['security_analysis']['missing']:
                risk_level = risk_levels.get(header['name'], 'MEDIUM')
                missing_data.append([
                    header['name'],
                    risk_level,
                    header['recommendation'],
                    header['description']
                ])
            
            missing_table = Table(missing_data, colWidths=[1.5*inch, 0.8*inch, 2*inch, 1.7*inch])
            missing_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e74c3c')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fdf2f2'))
            ]))
            
            # Color-code risk levels
            for i, header in enumerate(data['security_analysis']['missing'], 1):
                risk_level = risk_levels.get(header['name'], 'MEDIUM')
                if risk_level == 'CRITICAL':
                    missing_table.setStyle(TableStyle([('BACKGROUND', (1, i), (1, i), colors.HexColor('#c0392b'))]))
                elif risk_level == 'HIGH':
                    missing_table.setStyle(TableStyle([('BACKGROUND', (1, i), (1, i), colors.HexColor('#e74c3c'))]))
                elif risk_level == 'MEDIUM':
                    missing_table.setStyle(TableStyle([('BACKGROUND', (1, i), (1, i), colors.HexColor('#f39c12'))]))
                else:
                    missing_table.setStyle(TableStyle([('BACKGROUND', (1, i), (1, i), colors.HexColor('#f1c40f'))]))
            
            self.story.append(missing_table)
        
        self.story.append(Spacer(1, 20))
    
    def _add_enhanced_libraries_analysis(self, data):
        """Agrega análisis mejorado de librerías con evaluación de vulnerabilidades"""
        self.story.append(Paragraph("Análisis de Librerías", self.styles['CustomHeading1']))
        
        if not data['libraries']:
            self.story.append(Paragraph("No se detectaron librerías automáticamente en este sitio web.", self.styles['Normal']))
            return
        
        # Add vulnerability distribution chart
        vuln_chart = self._create_vulnerability_chart(data['libraries'])
        if vuln_chart:
            self.story.append(vuln_chart)
            self.story.append(Spacer(1, 15))
        
        # Tabla detallada de librerías
        lib_data = [['Librería', 'Versión', 'Tipo', 'Estado', 'Nivel de Riesgo', 'Recomendación']]
        
        for lib in data['libraries']:
            # Vulnerability assessment
            lib_dict = self._row_to_dict(lib)
            has_vuln = (lib_dict.get('latest_safe_version') and lib_dict.get('version') and 
                       lib_dict['version'] != lib_dict['latest_safe_version'] and 
                       lib_dict['version'] < lib_dict['latest_safe_version'])
            
            if has_vuln:
                status = "🔴 VULNERABLE"
                risk_level = "ALTO"
                recommendation = f"Actualizar a {lib_dict['latest_safe_version']}"
            elif lib_dict.get('latest_safe_version'):
                status = "✅ SEGURA"
                risk_level = "BAJO"
                recommendation = "No se requiere acción"
            else:
                status = "⚠️ DESCONOCIDO"
                risk_level = "MEDIO"
                recommendation = "Revisión manual necesaria"
            
            lib_data.append([
                lib_dict['library_name'],
                lib_dict.get('version', 'Unknown'),
                lib_dict['type'].upper(),
                status,
                risk_level,
                recommendation
            ])
        
        lib_table = Table(lib_data, colWidths=[1.2*inch, 0.8*inch, 0.5*inch, 1*inch, 0.8*inch, 1.7*inch])
        lib_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        # Color-code rows based on vulnerability status
        for i, lib in enumerate(data['libraries'], 1):
            lib_dict = self._row_to_dict(lib)
            has_vuln = (lib_dict.get('latest_safe_version') and lib_dict.get('version') and 
                       lib_dict['version'] != lib_dict['latest_safe_version'] and 
                       lib_dict['version'] < lib_dict['latest_safe_version'])
            
            if has_vuln:
                lib_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.HexColor('#fdf2f2'))]))
            elif lib_dict.get('latest_safe_version'):
                lib_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f0f9f0'))]))
            else:
                lib_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.HexColor('#fff3cd'))]))
        
        self.story.append(lib_table)
        self.story.append(Spacer(1, 20))
    
    def _add_technical_details(self, data):
        """Agrega sección de detalles técnicos"""
        self.story.append(Paragraph("Detalles Técnicos", self.styles['CustomHeading1']))
        
        # Archivos analizados
        if data['file_urls']:
            self.story.append(Paragraph("Archivos Analizados", self.styles['CustomHeading2']))
            
            # Agrupar archivos por tipo
            js_files = [f for f in data['file_urls'] if self._row_to_dict(f)['file_type'] == 'js']
            css_files = [f for f in data['file_urls'] if self._row_to_dict(f)['file_type'] == 'css']
            
            files_summary = f"Total de archivos analizados: {len(data['file_urls'])} ({len(js_files)} JavaScript, {len(css_files)} CSS)"
            self.story.append(Paragraph(files_summary, self.styles['Normal']))
            
            # Todos los archivos encontrados
            sample_files = data['file_urls']
            file_data = [['URL del Archivo', 'Tipo', 'Tamaño', 'Estado']]
            
            for file_info in sample_files:
                file_dict = self._row_to_dict(file_info)
                file_url_display = file_dict['file_url']
                if len(file_url_display) > 40:
                    file_url_display = '...' + file_url_display[-37:]
                
                file_size = 'Unknown'
                if file_dict.get('file_size'):
                    size_kb = round(file_dict['file_size'] / 1024, 1)
                    file_size = f"{size_kb} KB"
                
                file_data.append([
                    file_url_display,
                    file_dict['file_type'].upper(),
                    file_size,
                    str(file_dict.get('status_code', 'Unknown'))
                ])
            
            file_table = Table(file_data, colWidths=[2.5*inch, 0.5*inch, 0.8*inch, 0.8*inch])
            file_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#95a5a6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            
            self.story.append(file_table)
            
            if len(data['file_urls']) > 10:
                self.story.append(Paragraph(f"+ {len(data['file_urls']) - 10} archivos más (ver lista completa en apéndice)", 
                                          self.styles['Normal']))
        
        self.story.append(Spacer(1, 20))
    
    def _add_recommendations(self, data):
        """Agrega sección de recomendaciones de seguridad"""
        self.story.append(Paragraph("Recomendaciones de Seguridad", self.styles['CustomHeading1']))
        
        recommendations = []
        
        # Recomendaciones basadas en cabeceras
        if data['security_analysis']['missing']:
            recommendations.append("🔒 <b>Implementar Cabeceras de Seguridad Faltantes:</b>")
            for header in data['security_analysis']['missing'][:3]:  # Top 3
                recommendations.append(f"• {header['name']}: {header['recommendation']}")
        
        # Recomendaciones basadas en librerías
        vulnerable_libs = []
        for lib in data['libraries']:
            lib_dict = self._row_to_dict(lib)
            if (lib_dict.get('latest_safe_version') and lib_dict.get('version') 
                and lib_dict['version'] != lib_dict['latest_safe_version'] 
                and lib_dict['version'] < lib_dict['latest_safe_version']):
                vulnerable_libs.append(lib_dict)
        
        if vulnerable_libs:
            recommendations.append("🔄 <b>Actualizar Librerías Vulnerables:</b>")
            for lib_dict in vulnerable_libs[:3]:  # Top 3
                recommendations.append(f"• {lib_dict['library_name']} de {lib_dict.get('version', 'desconocida')} a {lib_dict['latest_safe_version']}")
        
        # Recomendaciones generales
        if data['security_analysis']['security_score'] < 70:
            recommendations.append("📊 <b>Mejorar Puntaje de Seguridad:</b>")
            recommendations.append("• Implementar Política de Seguridad de Contenido (CSP) integral")
            recommendations.append("• Habilitar Seguridad de Transporte Estricta HTTP (HSTS)")
            recommendations.append("• Configurar adecuadamente la cabecera X-Frame-Options")
        
        if not recommendations:
            recommendations.append("✅ <b>Buena Postura de Seguridad:</b>")
            recommendations.append("• Continuar monitoreando nuevas vulnerabilidades")
            recommendations.append("• Actualizar regularmente librerías y dependencias")
            recommendations.append("• Implementar herramientas de monitoreo de seguridad")
        
        for rec in recommendations:
            if rec.startswith(('🔒', '🔄', '📊', '✅')):
                self.story.append(Paragraph(rec, self.styles['CustomHeading2']))
            else:
                self.story.append(Paragraph(rec, self.styles['RecommendationBox']))
        
        self.story.append(Spacer(1, 20))
    
    def _add_appendices(self, data):
        """Agrega apéndices con datos completos"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("Apéndices", self.styles['CustomHeading1']))
        
        # Apéndice A: Cabeceras HTTP Completas
        if data['headers']:
            self.story.append(Paragraph("Apéndice A: Cabeceras HTTP Completas", self.styles['CustomHeading2']))
            
            headers_data = [['Nombre de Cabecera', 'Valor de Cabecera']]
            for header_name, header_value in data['headers'].items():
                value_display = str(header_value)[:100] + '...' if len(str(header_value)) > 100 else str(header_value)
                headers_data.append([header_name, value_display])
            
            headers_table = Table(headers_data, colWidths=[2*inch, 4*inch])
            headers_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7f8c8d')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            
            self.story.append(headers_table)
        
        # Apéndice B: Cadenas de Versión Encontradas
        if data['version_strings']:
            self.story.append(Spacer(1, 15))
            self.story.append(Paragraph("Apéndice B: Cadenas de Versión Encontradas en Código", self.styles['CustomHeading2']))
            
            vs_data = [['Archivo', 'Línea', 'Vista Previa del Contenido']]
            for vs in data['version_strings'][:20]:  # First 20
                vs_dict = self._row_to_dict(vs)
                file_display = vs_dict['file_url'].split('/')[-1] if '/' in vs_dict['file_url'] else vs_dict['file_url']
                content_preview = vs_dict['line_content'][:60] + '...' if len(vs_dict['line_content']) > 60 else vs_dict['line_content']
                vs_data.append([file_display, str(vs_dict['line_number']), content_preview])
            
            vs_table = Table(vs_data, colWidths=[2*inch, 0.5*inch, 3.5*inch])
            vs_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7f8c8d')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            
            self.story.append(vs_table)
            
            if len(data['version_strings']) > 20:
                self.story.append(Paragraph(f"+ {len(data['version_strings']) - 20} cadenas de versión adicionales encontradas", 
                                          self.styles['Normal']))


def create_enhanced_pdf_report(data):
    """Función principal para crear reporte PDF mejorado"""
    report_generator = EnhancedPDFReport()
    story = report_generator.generate_enhanced_report(data)
    
    # Convertir scan a dict para acceso seguro
    scan_dict = report_generator._row_to_dict(data['scan'])
    
    # Crear documento PDF con configuraciones personalizadas
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        topMargin=50,
        bottomMargin=50,
        leftMargin=50,
        rightMargin=50,
        title=f"Reporte de Análisis de Seguridad - {scan_dict['url']}",
        author="Analizador de Librerías JS/CSS",
        subject="Análisis de Seguridad Web",
        creator="Generador de Reportes PDF Mejorado"
    )
    
    # Construir PDF con encabezado/pie de página personalizado
    doc.build(story, onFirstPage=report_generator._create_header_footer, 
              onLaterPages=report_generator._create_header_footer)
    
    buffer.seek(0)
    return buffer