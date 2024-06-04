from pydantic import BaseModel
from typing import Optional

# status can be pending/brewing/ready
class Order(BaseModel):
  order_id: int
  status: Optional[str] = "pending"
