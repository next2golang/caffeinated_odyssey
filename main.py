import uvicorn
from multiprocessing import Process
from app.client_server import client_app
from app.worker_server import worker_app

def run_client_server():
  uvicorn.run(client_app, host="localhost", port=8000)

def run_worker_server():
  uvicorn.run(worker_app, host="localhost", port=8001)

if __name__ == "__main__":
  Process(target=run_client_server).start()
  Process(target=run_worker_server).start()
