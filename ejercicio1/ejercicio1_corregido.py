from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import json

# Enums y abstración
# Esto por la Inversión de Dependencias (DIP) en donde el sistema principal no sabe cómo se envía el mensaje, pero como se llama el método.
class NotificationType(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"

class INotificationSender(ABC):
    @abstractmethod
    def send(self, customer_data: dict, message: dict) -> dict:
        pass

# Implementaciones Concretas
# Esto por la Responsabilidad Uníca (SRP) en donde si el envío de emails falla, puedes saber exactamente que el error está en EmailSender.
class EmailSender(INotificationSender):
    def send(self, customer_data: dict, message_data: dict) -> dict:
        email = customer_data['email']
        body = message_data['body']
        subject = message_data.get('subject', 'Notificación')
        
        print(f"📧 EMAIL enviado a {email}")
        print(f"   Asunto: {subject}")
        print(f"   Mensaje: {body}\n")
        
        return {
            'type': 'email',
            'to': email,
            'message': body,
            'timestamp': datetime.now().isoformat()
        }

class SMSSender(INotificationSender):
    def send(self, customer_data: dict, message_data: dict) -> dict:
        phone = customer_data['phone']
        body = message_data['body']
        
        print(f"📱 SMS enviado a {phone}")
        print(f"   Mensaje: {body}\n")
        
        return {
            'type': 'sms',
            'to': phone,
            'message': body,
            'timestamp': datetime.now().isoformat()
        }

class PushSender(INotificationSender):
    def send(self, customer_data: dict, message_data: dict) -> dict:
        device_id = customer_data['device_id']
        body = message_data['body']
        
        print(f"🔔 PUSH enviada al dispositivo {device_id}")
        print(f"   Mensaje: {body}\n")
        
        return {
            'type': 'push',
            'to': device_id,
            'message': body,
            'timestamp': datetime.now().isoformat()
        }
    
# Patrion Strategy
# Para definir cómo se construye el mensaje dependiendo del canal, eliminando los if/else del sistema principal.
class IMessageStrategy(ABC):
    @abstractmethod
    def create_message(self, order_id: str, customer_name: str, total: float) -> dict:
        pass

class EmailMessageStrategy(IMessageStrategy):
    def create_message(self, order_id: str, customer_name: str, total: float) -> dict:
        return {
            'subject': f"Confirmación de Pedido #{order_id}",
            'body': f"Estimado {customer_name}, su pedido #{order_id} por ${total} ha sido confirmado."
        }

class ShortMessageStrategy(IMessageStrategy):
    def create_message(self, order_id: str, customer_name: str, total: float) -> dict:
        return {
            'body': f"Pedido #{order_id} confirmado. Total: ${total}. Gracias por su compra!"
        }

# Patrón Factory
# Esto para quitar el código de if/else y centrar la lógica de creación de objetos en un solo lugar.
class NotificationFactory:
    @staticmethod
    def get_sender(type_str: str) -> INotificationSender:
        try:
            notif_type = NotificationType(type_str)
            senders = {
                NotificationType.EMAIL: EmailSender(),
                NotificationType.SMS: SMSSender(),
                NotificationType.PUSH: PushSender()
            }
            return senders[notif_type]
        except ValueError:
            raise ValueError(f"Tipo de notificación no soportado: {type_str}")

    @staticmethod
    def get_strategy(type_str: str) -> IMessageStrategy:
        try:
            notif_type = NotificationType(type_str)
            strategies = {
                NotificationType.EMAIL: EmailMessageStrategy(),
                NotificationType.SMS: ShortMessageStrategy(),
                NotificationType.PUSH: ShortMessageStrategy()
            }
            return strategies[notif_type]
        except ValueError:
            return ShortMessageStrategy()

# Sistema Principal
# En esta sección el código solo orquesta. Basicamente usa las piezas creadas arriba y no le importa los detalles técnicos.
class OrderNotificationSystem:
    def __init__(self):
        self.notifications_sent = []
    
    def process_order(self, order_data, notification_types):
        order_id = order_data['order_id']
        customer = order_data['customer']
        total = order_data['total']
        
        print(f"\n{'='*50}")
        print(f"Procesando pedido #{order_id}")
        print(f"Cliente: {customer['name']}")
        print(f"Total: ${total}")
        print(f"{'='*50}\n")
        
        for type_str in notification_types:
            sender = NotificationFactory.get_sender(type_str)
            
            message_strategy = NotificationFactory.get_strategy(type_str)
            msg_data = message_strategy.create_message(order_id, customer['name'], total)
            
            log_entry = sender.send(customer, msg_data)
            self.notifications_sent.append(log_entry)
    
    def get_notification_history(self):
        return self.notifications_sent
        

# Prueba de Código
if __name__ == "__main__":
    system = OrderNotificationSystem()
    
    # Pedido 1: Cliente premium (todos los canales)
    order1 = {
        'order_id': 'ORD-001',
        'customer': {
            'name': 'Ana García',
            'email': 'ana.garcia@email.com',
            'phone': '+34-600-123-456',
            'device_id': 'DEVICE-ABC-123'
        },
        'total': 150.50
    }
    
    try:
        system.process_order(order1, ['email', 'sms', 'push'])
    except Exception as e:
        print(f"Error: {e}")
        
    print(f"\nTotal notificaciones enviadas: {len(system.get_notification_history())}")

    # Pedido 2: Cliente estándar (solo email)
    order1 = {
        'order_id': 'ORD-002',
        'customer': {
            'name': 'Carlos Ruiz',
            'email': 'carlos.ruiz@email.com',
            'phone': '+34-600-789-012',
            'device_id': 'DEVICE-XYZ-789'
        },
        'total': 75.00
    }
    
    try:
        system.process_order(order1, ['email'])
    except Exception as e:
        print(f"Error: {e}")
        
    print(f"\nTotal notificaciones enviadas: {len(system.get_notification_history())}")