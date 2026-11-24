
from pydantic import BaseModel
from typing import Literal


class Ticket(BaseModel):
    ticket_id: int
    equipment: str
    issue: str
    priority: Literal["Low", "Medium", "High"]
