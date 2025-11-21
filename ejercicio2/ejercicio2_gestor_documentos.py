# ejercicio2_gestor_documentos.py
from datetime import datetime
import json

class ReportSystem:
    def __init__(self):
        self.reports_generated = []
    
    def generate_report(self, report_type, data, output_format, delivery_method):
        """
        Genera un reporte con los datos proporcionados.
        
        report_type: 'sales', 'inventory', 'financial'
        output_format: 'pdf', 'excel', 'html'
        delivery_method: 'email', 'download', 'cloud'
        """
        
        report_content = ""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generar contenido según el tipo de reporte
        if report_type == 'sales':
            report_content += "="*60 + "\n"
            report_content += "           REPORTE DE VENTAS\n"
            report_content += "="*60 + "\n"
            report_content += f"Fecha de generación: {timestamp}\n\n"
            
            total_sales = sum(item['amount'] for item in data['sales'])
            report_content += f"Total de ventas: ${total_sales:.2f}\n"
            report_content += f"Número de transacciones: {len(data['sales'])}\n"
            report_content += f"Periodo: {data['period']}\n\n"
            
            report_content += "Detalle de ventas:\n"
            report_content += "-" * 60 + "\n"
            for sale in data['sales']:
                report_content += f"  • Producto: {sale['product']} - ${sale['amount']:.2f}\n"
            
        elif report_type == 'inventory':
            report_content += "="*60 + "\n"
            report_content += "           REPORTE DE INVENTARIO\n"
            report_content += "="*60 + "\n"
            report_content += f"Fecha de generación: {timestamp}\n\n"
            
            total_items = sum(item['quantity'] for item in data['items'])
            report_content += f"Total de productos: {total_items}\n"
            report_content += f"Categorías: {len(set(item['category'] for item in data['items']))}\n\n"
            
            report_content += "Inventario actual:\n"
            report_content += "-" * 60 + "\n"
            for item in data['items']:
                report_content += f"  • {item['name']} ({item['category']}): {item['quantity']} unidades\n"
        
        elif report_type == 'financial':
            report_content += "="*60 + "\n"
            report_content += "           REPORTE FINANCIERO\n"
            report_content += "="*60 + "\n"
            report_content += f"Fecha de generación: {timestamp}\n\n"
            
            report_content += f"Ingresos: ${data['income']:.2f}\n"
            report_content += f"Gastos: ${data['expenses']:.2f}\n"
            report_content += f"Balance: ${data['income'] - data['expenses']:.2f}\n"
        
        # Formatear según el formato de salida
        formatted_report = ""
        
        if output_format == 'pdf':
            formatted_report = f"[PDF FORMAT]\n{report_content}\n[END PDF]"
            print(f"📄 Generando reporte en formato PDF...")
            
        elif output_format == 'excel':
            formatted_report = f"[EXCEL FORMAT]\n{report_content}\n[END EXCEL]"
            print(f"📊 Generando reporte en formato Excel...")
            
        elif output_format == 'html':
            formatted_report = f"<html><body><pre>{report_content}</pre></body></html>"
            print(f"🌐 Generando reporte en formato HTML...")
        
        # Entregar según el método
        if delivery_method == 'email':
            print(f"📧 Enviando reporte por email...")
            print(f"   Destinatario: admin@company.com")
            
        elif delivery_method == 'download':
            filename = f"report_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{output_format}"
            print(f"💾 Reporte disponible para descarga: {filename}")
            
        elif delivery_method == 'cloud':
            print(f"☁️  Subiendo reporte a la nube...")
            print(f"   URL: https://cloud.company.com/reports/{report_type}")
        
        # Guardar registro
        self.reports_generated.append({
            'type': report_type,
            'format': output_format,
            'delivery': delivery_method,
            'timestamp': timestamp
        })
        
        print(f"\n✅ Reporte generado exitosamente\n")
        print(formatted_report)
        print("\n" + "="*60 + "\n")
        
        return formatted_report
    
    def get_report_history(self):
        return self.reports_generated


# Código de prueba
if __name__ == "__main__":
    system = ReportSystem()
    
    # Reporte de ventas
    sales_data = {
        'period': 'Enero 2024',
        'sales': [
            {'product': 'Laptop HP', 'amount': 899.99},
            {'product': 'Mouse Logitech', 'amount': 25.50},
            {'product': 'Teclado Mecánico', 'amount': 120.00},
            {'product': 'Monitor LG 24"', 'amount': 199.99}
        ]
    }
    
    system.generate_report('sales', sales_data, 'pdf', 'email')
    
    # Reporte de inventario
    inventory_data = {
        'items': [
            {'name': 'Laptop HP', 'category': 'Computadoras', 'quantity': 15},
            {'name': 'Mouse Logitech', 'category': 'Accesorios', 'quantity': 50},
            {'name': 'Teclado Mecánico', 'category': 'Accesorios', 'quantity': 30},
            {'name': 'Monitor LG', 'category': 'Pantallas', 'quantity': 20}
        ]
    }
    
    system.generate_report('inventory', inventory_data, 'excel', 'download')
    
    # Reporte financiero
    financial_data = {
        'income': 50000.00,
        'expenses': 32000.00
    }
    
    system.generate_report('financial', financial_data, 'html', 'cloud')
    
    # Mostrar historial
    print("\nHISTORIAL DE REPORTES GENERADOS:")
    print(json.dumps(system.get_report_history(), indent=2))
