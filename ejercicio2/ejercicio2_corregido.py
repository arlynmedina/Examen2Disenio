from abc import ABC, abstractmethod
from datetime import datetime
import json

# Interfaces que son la base para el Patron Strategy
# Esto para la Inversión de Dependencias (DIP) en donde el sistema no depende de clases concretas como PDF o EMAIL.
class ContentGenerator(ABC):
    @abstractmethod
    def generate(self, data):
        pass

class ReportFormatter(ABC):
    @abstractmethod
    def format(self, text):
        pass

class DeliveryChannel(ABC):
    @abstractmethod
    def deliver(self, document, meta_data):
        pass

# Clases Concretas que son la tipo lógica
# Esto para la Responsabilidad Uníca (SRP) en donde cada clase hace solo una cosa. Entonces si falla la generación de por ejemplo PDF, podrías saber que el error esta en PdfFormatter
class SalesGenerator(ContentGenerator):
    def generate(self, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = "="*60 + "\n"
        text += "           REPORTE DE VENTAS\n"
        text += "="*60 + "\n"
        text += f"Fecha de generación: {timestamp}\n\n"
        
        if 'period' in data:
            text += f"Periodo: {data['period']}\n"
            
        total = sum(item['amount'] for item in data['sales'])
        text += f"Total de ventas: ${total:.2f}\n"
        text += f"Número de transacciones: {len(data['sales'])}\n\n"
        
        text += "Detalle de ventas:\n"
        text += "-" * 60 + "\n"
        for sale in data['sales']:
            text += f"  • Producto: {sale['product']} - ${sale['amount']:.2f}\n"
        return text

class InventoryGenerator(ContentGenerator):
    def generate(self, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = "="*60 + "\n"
        text += "           REPORTE DE INVENTARIO\n"
        text += "="*60 + "\n"
        text += f"Fecha de generación: {timestamp}\n\n"
        
        total_items = sum(item['quantity'] for item in data['items'])
        text += f"Total de productos: {total_items}\n"
        
        # Lógica simple para contar categorías únicas
        categories = set(item.get('category', 'General') for item in data['items'])
        text += f"Categorías: {len(categories)}\n\n"
        
        text += "Inventario actual:\n"
        text += "-" * 60 + "\n"
        for item in data['items']:
            text += f"  • {item['name']} ({item.get('category', 'General')}): {item['quantity']} unidades\n"
        return text

class FinancialGenerator(ContentGenerator):
    def generate(self, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = "="*60 + "\n"
        text += "           REPORTE FINANCIERO\n"
        text += "="*60 + "\n"
        text += f"Fecha de generación: {timestamp}\n\n"
        
        income = data['income']
        expenses = data['expenses']
        text += f"Ingresos: ${income:.2f}\n"
        text += f"Gastos: ${expenses:.2f}\n"
        text += f"Balance: ${income - expenses:.2f}\n"
        return text

# --- Formatters ---
class PdfFormatter(ReportFormatter):
    def format(self, text):
        print(f"📄 Generando reporte en formato PDF...")
        return f"[PDF FORMAT]\n{text}\n[END PDF]"

class ExcelFormatter(ReportFormatter):
    def format(self, text):
        print(f"📊 Generando reporte en formato Excel...")
        return f"[EXCEL FORMAT]\n{text}\n[END EXCEL]"

class HtmlFormatter(ReportFormatter):
    def format(self, text):
        print(f"🌐 Generando reporte en formato HTML...")
        return f"<html><body><pre>{text}</pre></body></html>"

class EmailDelivery(DeliveryChannel):
    def deliver(self, document, meta_data):
        print(f"📧 Enviando reporte por email...")
        print(f"   Destinatario: admin@company.com")

class DownloadDelivery(DeliveryChannel):
    def deliver(self, document, meta_data):
        filename = f"report_{meta_data['type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{meta_data['format']}"
        print(f"💾 Reporte disponible para descarga: {filename}")

class CloudDelivery(DeliveryChannel):
    def deliver(self, document, meta_data):
        print(f"☁️  Subiendo reporte a la nube...")
        print(f"   URL: https://cloud.company.com/reports/{meta_data['type']}")

# Patrón Factory que es el creador de los objetos
# Se centraliza todos los if/else de creación de objetos en un solo lugar.
# También aquí se respera SRP porque esta clase solo crea objetos Y OCP porque si agregamos un nuevo tipo de reporte, solo modificamos esta clase.
class ReportFactory:
    def get_generator(self, report_type):
        if report_type == 'sales':
            return SalesGenerator()
        elif report_type == 'inventory':
            return InventoryGenerator()
        elif report_type == 'financial':
            return FinancialGenerator()
        else:
            return None

    def get_formatter(self, output_format):
        if output_format == 'pdf':
            return PdfFormatter()
        elif output_format == 'excel':
            return ExcelFormatter()
        elif output_format == 'html':
            return HtmlFormatter()
        else:
            return HtmlFormatter()

    def get_delivery(self, delivery_method):
        if delivery_method == 'email':
            return EmailDelivery()
        elif delivery_method == 'download':
            return DownloadDelivery()
        elif delivery_method == 'cloud':
            return CloudDelivery()
        else:
            return DownloadDelivery()

# Sistema principal
# Se aplica el principio OCP ya que no se modifica esta clase para agregar nuevos tipos de reportes, formatos o métodos de entrega.
# Pide las piezas del fatcory y las ejecuta en orden.
class ReportSystem:
    def __init__(self):
        self.reports_generated = []
        self.factory = ReportFactory()
    
    def generate_report(self, report_type, data, output_format, delivery_method):
        generator = self.factory.get_generator(report_type)
        formatter = self.factory.get_formatter(output_format)
        delivery = self.factory.get_delivery(delivery_method)
        
        if generator is None:
            print("Error: No se pudo generar el reporte")
            return

        raw_content = generator.generate(data)
        final_document = formatter.format(raw_content)
        
        meta_data = {'type': report_type, 'format': output_format}
        delivery.deliver(final_document, meta_data)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.reports_generated.append({
            'type': report_type,
            'format': output_format,
            'delivery': delivery_method,
            'timestamp': timestamp
        })
        
        print(f"\n✅ Reporte generado exitosamente\n")
        print(final_document)
        print("\n" + "="*60 + "\n")
        
        return final_document
    
    def get_report_history(self):
        return self.reports_generated

# Prueba de Código
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