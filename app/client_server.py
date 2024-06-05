from fastapi import FastAPI, Request, HTTPException
from app.utils import order_queue
import asyncio, time

client_app = FastAPI()

request_counts = {}

ddoser_ips = set()

REQUEST_LIMIT = 5
TIME_WINDOW = 300

@client_app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
  client_ip = request.client.host
  current_time = time.time()

  if request.url.path == "/order/":
    if client_ip in ddoser_ips:
      raise HTTPException(status_code=429, detail="Sorry, you are in the ddoser's list")
    
    if client_ip not in request_counts:
      request_counts[client_ip] = []
    
    request_counts[client_ip] = [timestamp for timestamp in request_counts[client_ip] if current_time - timestamp < TIME_WINDOW]
    
    if len(request_counts[client_ip]) >= REQUEST_LIMIT:
      ddoser_ips.add(client_ip)
      raise HTTPException(status_code=429, detail="Too many requests - You are blocked")

    request_counts[client_ip].append(current_time)

  response = await call_next(request)
  return response

@client_app.post("/order/")
async def place_order():
  try:
    order = order_queue.add_order()
    while True:
      order_status = order_queue.get_order_status(order["order_id"])
      if order_status == "ready":
        # can keep the following line if worry about queue stack size, and if worry about losting task in extra cases like connection lost, can remove the line.
        order_queue.remove_order(order["order_id"])
        break
      await asyncio.sleep(1)
    return {"message": "Your americano is ready!", "order_id": order["order_id"]}
  except Exception as e:
    raise HTTPException(status_code=500, detail="Internal Server Error")

@client_app.get("/")
async def read_root():
  return {"message": "Welcome to the Coffee Order API"}
