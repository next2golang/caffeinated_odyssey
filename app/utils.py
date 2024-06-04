import time
from collections import deque

class OrderQueue:
  def __init__(self):
    self.queue = deque()
    self.current_order_id = 0
    self.current_brewing_order_id = 0

  def add_order(self):
    self.current_order_id += 1
    order = {"order_id": self.current_order_id, "status": "pending"}
    self.queue.append(order)
    print("Queue:", self.queue)
    return order

  def get_order(self):
    print("Queue:", self.queue)
    if self.queue:
      self.current_brewing_order_id += 1
      return self.queue[self.current_brewing_order_id]
    return None
  
  def get_order_status(self, order_id):
    for order in self.queue:
      if order["order_id"] == order_id:
        return order["status"]
  
  def remove_order(self, order_id):
    for order in self.queue:
      if order["order_id"] == order_id:
        self.queue.remove(order)
        return True
    return False

order_queue = OrderQueue()

def simulate_brewing_time():
  time.sleep(30) 
