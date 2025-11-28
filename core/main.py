from fastapi import FastAPI, HTTPException

app = FastAPI()

cost_list = {}
current_id = 0


@app.get("/expenses")
def get_all_expenses():
    return list(cost_list.values())


@app.post("/expenses", status_code=201)
def create_expense(description: str, amount: float):
    global current_id
    current_id += 1

    new_cost = {
        "id": current_id,
        "description": description,
        "amount": amount
    }

    cost_list[current_id] = new_cost
    return new_cost


@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    if expense_id not in cost_list:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return cost_list[expense_id]


@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, description: str, amount: float):
    if expense_id not in cost_list:
        raise HTTPException(status_code=404, detail="Expense not found")

    updated_cost = {
        "id": expense_id,
        "description": description,
        "amount": amount
    }

    cost_list[expense_id] = updated_cost
    return updated_cost


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    if expense_id not in cost_list:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    del cost_list[expense_id]
    return None
