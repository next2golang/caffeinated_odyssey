import time
import pika
import json

class OrderQueue:
  def __init__(self, rabbitmq_host='localhost'):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    self.channel = self.connection.channel()
    self.channel.queue_declare(queue='order_queue')
    self.channel.queue_declare(queue='order_status')

  def add_order(self):
    order = {"order_id": int(time.time()), "status": "pending"}
    self.channel.basic_publish(exchange='', routing_key='order_queue', body=json.dumps(order))
    return order

  def get_order(self):
    method_frame, header_frame, body = self.channel.basic_get(queue='order_queue')
    if method_frame:
      order = json.loads(body)
      self.channel.basic_ack(method_frame.delivery_tag)
      return order
    return None
  
  def get_order_status(self, order_id):
    method_frame, header_frame, body = self.channel.basic_get(queue='order_status')
    while method_frame:
      status = json.loads(body)
      if status['order_id'] == order_id:
        return status['status']
      self.channel.basic_ack(method_frame.delivery_tag)
      method_frame, header_frame, body = self.channel.basic_get(queue='order_status')
    return None
  
  def update_order_status(self, order_id, status):
    order_status = {"order_id": order_id, "status": status}
    self.channel.basic_publish(exchange='', routing_key='order_status', body=json.dumps(order_status))

  def remove_order(self, order_id):
    method_frame, header_frame, body = self.channel.basic_get(queue='order_queue')
    while method_frame:
      order = json.loads(body)
      if order['order_id'] == order_id:
        self.channel.basic_ack(method_frame.delivery_tag)
        return True
      self.channel.basic_ack(method_frame.delivery_tag)
      method_frame, header_frame, body = self.channel.basic_get(queue='order_queue')
    return False

order_queue = OrderQueue()

def simulate_brewing_time():
  time.sleep(30) 
