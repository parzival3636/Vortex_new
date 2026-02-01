"""
PDF Generator for Daily Financial Report feature
"""

from io import BytesIO
from datetime import datetime
from typing import Dict
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class PDFGenerator:
    """Generator for PDF reports"""
    
    def __init__(self):
        self.page_size = A4
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#4b5563'),
            spaceAfter=6
        ))
    
    def generate_pdf_report(self, report_data: Dict) -> bytes:
        """
        Generate PDF report from report data
        
        Requirements: 7.2, 7.3
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=self.page_size)
        story = []
        
        # Add header
        story.extend(self._create_header(report_data))
        story.append(Spacer(1, 0.3 * inch))
        
        # Add financial summary
        story.extend(self._create_financial_summary(report_data))
        story.append(Spacer(1, 0.2 * inch))
        
        # Add trips table
        story.extend(self._create_trips_section(report_data))
        story.append(Spacer(1, 0.2 * inch))
        
        # Add expense breakdown
        story.extend(self._create_expense_breakdown(report_data))
        story.append(Spacer(1, 0.2 * inch))
        
        # Add AI insights
        story.extend(self._create_insights_section(report_data))
        story.append(Spacer(1, 0.2 * inch))
        
        # Add footer
        story.extend(self._create_footer(report_data))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _create_header(self, report_data: Dict) -> list:
        """Create PDF header section"""
        story = []
        
        title = Paragraph(
            "Daily Financial Report",
            self.styles['CustomTitle']
        )
        story.append(title)
        
        date_text = f"Report Date: {report_data.get('date', 'N/A')}"
        story.append(Paragraph(date_text, self.styles['CustomBody']))
        
        driver_text = f"Driver ID: {report_data.get('driver_id', 'N/A')}"
        story.append(Paragraph(driver_text, self.styles['CustomBody']))
        
        generated_text = f"Generated: {report_data.get('generated_at', 'N/A')}"
        story.append(Paragraph(generated_text, self.styles['CustomBody']))
        
        return story
    
    def _create_financial_summary(self, report_data: Dict) -> list:
        """Create financial summary section"""
        story = []
        
        story.append(Paragraph("Financial Summary", self.styles['CustomHeading']))
        
        summary = report_data.get('financial_summary', {})
        
        # Create metrics table
        metrics_data = [
            ['Metric', 'Amount (₹)'],
            ['Total Earnings', f"₹{summary.get('total_earnings', 0):.2f}"],
            ['Total Expenses', f"₹{summary.get('total_expenses', 0):.2f}"],
            ['Net Profit', f"₹{summary.get('net_profit', 0):.2f}"],
            ['Trips Completed', str(summary.get('trips_completed', 0))],
            ['Avg Earnings/Trip', f"₹{summary.get('average_earnings_per_trip', 0):.2f}"],
            ['Expense Ratio', f"{summary.get('expense_ratio', 0):.2%}"],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
        ]))
        
        story.append(metrics_table)
        return story
    
    def _create_trips_section(self, report_data: Dict) -> list:
        """Create trips section"""
        story = []
        
        trips = report_data.get('trips', [])
        
        if not trips:
            story.append(Paragraph("Trips", self.styles['CustomHeading']))
            story.append(Paragraph("No trips completed on this date.", self.styles['CustomBody']))
            return story
        
        story.append(Paragraph("Trip Details", self.styles['CustomHeading']))
        
        # Create trips table
        trips_data = [['Origin', 'Destination', 'Load Details', 'Earnings (₹)']]
        
        for trip in trips:
            trips_data.append([
                trip.get('origin', 'N/A')[:20],
                trip.get('destination', 'N/A')[:20],
                trip.get('load_details', 'N/A')[:20],
                f"₹{trip.get('earnings', 0):.2f}"
            ])
        
        trips_table = Table(trips_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
        trips_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
        ]))
        
        story.append(trips_table)
        return story
    
    def _create_expense_breakdown(self, report_data: Dict) -> list:
        """Create expense breakdown section"""
        story = []
        
        story.append(Paragraph("Expense Breakdown", self.styles['CustomHeading']))
        
        summary = report_data.get('financial_summary', {})
        breakdown = summary.get('expense_breakdown', {})
        
        # Create breakdown table
        breakdown_data = [['Category', 'Amount (₹)']]
        
        for category, amount in breakdown.items():
            breakdown_data.append([
                category.capitalize(),
                f"₹{amount:.2f}"
            ])
        
        breakdown_table = Table(breakdown_data, colWidths=[2.5*inch, 2*inch])
        breakdown_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
        ]))
        
        story.append(breakdown_table)
        return story
    
    def _create_insights_section(self, report_data: Dict) -> list:
        """Create AI insights section"""
        story = []
        
        story.append(Paragraph("AI Insights & Recommendations", self.styles['CustomHeading']))
        
        insights = report_data.get('ai_insights', {})
        
        # Summary
        summary = insights.get('summary', 'No summary available.')
        story.append(Paragraph(f"<b>Summary:</b> {summary}", self.styles['CustomBody']))
        story.append(Spacer(1, 0.1 * inch))
        
        # Anomalies
        anomalies = insights.get('anomalies', [])
        if anomalies:
            story.append(Paragraph("<b>Anomalies Detected:</b>", self.styles['CustomBody']))
            for anomaly in anomalies:
                story.append(Paragraph(f"• {anomaly}", self.styles['CustomBody']))
            story.append(Spacer(1, 0.1 * inch))
        
        # Recommendations
        recommendations = insights.get('recommendations', [])
        if recommendations:
            story.append(Paragraph("<b>Recommendations:</b>", self.styles['CustomBody']))
            for rec in recommendations:
                story.append(Paragraph(f"• {rec}", self.styles['CustomBody']))
        
        return story
    
    def _create_footer(self, report_data: Dict) -> list:
        """Create PDF footer"""
        story = []
        
        footer_text = f"Report generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
        story.append(Paragraph(footer_text, self.styles['CustomBody']))
        
        return story
