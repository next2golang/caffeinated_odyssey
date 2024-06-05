from fastapi import FastAPI
from app.utils import order_queue

worker_app = FastAPI()

@worker_app.get("/start/")
async def start_order():
  order = order_queue.get_order()
  if order:
    order_queue.update_order_status(order['order_id'], 'brewing')
    return {"message": "Order obtained", "order_id": order["order_id"]}
  return {"message": "No orders in queue"}

@worker_app.post("/finish/")
async def finish_order(order_id: int):
  order_queue.update_order_status(order_id, 'ready')
  return {"message": "Successfully reported", "order_id": order_id}

@worker_app.get("/")
async def read_root():
  return {"message": "Welcome to the Coffee Worker API"}