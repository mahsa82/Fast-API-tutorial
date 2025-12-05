from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

cost_list = {}
current_id = 0


# ✅ مدل ورودی (بدون id)
class ExpenseCreate(BaseModel):
    description: Annotated[
        str,
        Field(
            min_length=5,
            max_length=100,
            pattern=r'^[A-Za-z0-9\s\-\_,\.]+$',
            description='write a description'
        )
    ]
    
    amount: float = Field(
        ...,
        gt=0,
        lt=1000,
        description="enter your expense"
    )

class Expense(ExpenseCreate):
    """
    This class shows that the user can not write an id it should come from server.
    """
    id: int


@app.get("/expenses")
def get_all_expenses():
    return list(cost_list.values())


@app.post("/expenses", status_code=201, response_model=Expense)
def create_expense(data: ExpenseCreate):
    global current_id
    current_id += 1

    new_cost = Expense(id=current_id, **data.model_dump())
    cost_list[current_id] = new_cost.model_dump()
    return new_cost



@app.get("/expenses/{expense_id}",response_model=Expense)
def get_expense(expense_id: int):
    if expense_id not in cost_list:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return cost_list[expense_id]


@app.put("/expenses/{expense_id}",response_model=Expense)
def update_expense(expense_id: int, data:ExpenseCreate):
    if expense_id not in cost_list:
        raise HTTPException(status_code=404, detail="Expense not found")

    updated_cost = Expense(id=expense_id, **data.model_dump())
    cost_list[expense_id] = updated_cost.model_dump()
    return updated_cost


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    if expense_id not in cost_list:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    del cost_list[expense_id]
    return None
