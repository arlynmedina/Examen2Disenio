# ejercicio1_tienda_online.py
import json
from datetime import datetime

class OrderNotificationSystem:
    def __init__(self):
        self.notifications_sent = []
    
    def process_order(self, order_data, notification_types):
        """
        Procesa un pedido y envía notificaciones según los tipos especificados.
        notification_types puede incluir: 'email', 'sms', 'push'
        """
        order_id = order_data['order_id']
        customer = order_data['customer']
        total = order_data['total']
        
        print(f"\n{'='*50}")
        print(f"Procesando pedido #{order_id}")
        print(f"Cliente: {customer['name']}")
        print(f"Total: ${total}")
        print(f"{'='*50}\n")
        
        # Enviar notificaciones según el tipo
        for notif_type in notification_types:
            if notif_type == 'email':
                # Lógica de email
                message = f"Estimado {customer['name']}, su pedido #{order_id} por ${total} ha sido confirmado."
                print(f"📧 EMAIL enviado a {customer['email']}")
                print(f"   Asunto: Confirmación de Pedido #{order_id}")
                print(f"   Mensaje: {message}\n")
                self.notifications_sent.append({
                    'type': 'email',
                    'to': customer['email'],
                    'message': message,
                    'timestamp': datetime.now().isoformat()
                })
                
            elif notif_type == 'sms':
                # Lógica de SMS
                message = f"Pedido #{order_id} confirmado. Total: ${total}. Gracias por su compra!"
                print(f"📱 SMS enviado a {customer['phone']}")
                print(f"   Mensaje: {message}\n")
                self.notifications_sent.append({
                    'type': 'sms',
                    'to': customer['phone'],
                    'message': message,
                    'timestamp': datetime.now().isoformat()
                })
                
            elif notif_type == 'push':
                # Lógica de notificación push
                message = f"¡Pedido confirmado! #{order_id} - ${total}"
                print(f"🔔 PUSH enviada al dispositivo {customer['device_id']}")
                print(f"   Mensaje: {message}\n")
                self.notifications_sent.append({
                    'type': 'push',
                    'to': customer['device_id'],
                    'message': message,
                    'timestamp': datetime.now().isoformat()
                })
    
    def get_notification_history(self):
        """Devuelve el historial de notificaciones"""
        return self.notifications_sent


# Código de prueba
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
    
    system.process_order(order1, ['email', 'sms', 'push'])
    
    # Pedido 2: Cliente estándar (solo email)
    order2 = {
        'order_id': 'ORD-002',
        'customer': {
            'name': 'Carlos Ruiz',
            'email': 'carlos.ruiz@email.com',
            'phone': '+34-600-789-012',
            'device_id': 'DEVICE-XYZ-789'
        },
        'total': 75.00
    }
    
    system.process_order(order2, ['email'])
    
    # Mostrar historial
    print("\n" + "="*50)
    print("HISTORIAL DE NOTIFICACIONES")
    print("="*50)
    history = system.get_notification_history()
    print(json.dumps(history, indent=2, ensure_ascii=False))

    
