from fastapi import FastAPI
from app.utils import order_queue
worker_app = FastAPI()

@worker_app.get("/start/")
async def start_order():
  order = order_queue.get_order()
  if order:
    order["status"] = "brewing"
    return {"message": "Order obtained", "order_id": order["order_id"]}
  return {"message": "No orders in queue"}

@worker_app.post("/finish/")
async def finish_order(order_id: int):
  for order in order_queue.queue:
    if order["order_id"] == order_id:
      order["status"] = "ready"
      return {"message": "Successfuly reported", "order_id": order_id}
  return {"message": "Order not found"}
