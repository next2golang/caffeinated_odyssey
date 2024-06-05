from fastapi import FastAPI, Request, HTTPException
from app.utils import order_queue
import asyncio

client_app = FastAPI()

@client_app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
  client_ip = request.client.host
  if client_ip == "ddoser_ip":
    raise HTTPException(status_code=429, detail="Too many requests")
  response = await call_next(request)
  return response

@client_app.post("/order/")
async def place_order():
  order = order_queue.add_order()
  while True:
    order_status = order_queue.get_order_status(order["order_id"])
    if order_status == "ready":
      # can keep the following line if worry about queue stack size, and if worry about losting task in extra cases like connection lost, can remove the line.
      order_queue.remove_order(order["order_id"])
      break
    await asyncio.sleep(1)
  return {"message": "Your americano is ready!", "order_id": order["order_id"]}
