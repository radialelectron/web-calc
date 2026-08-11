from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Calculation

app = FastAPI(title="WEB Calc API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/api/health")
def health():
    return {"status": "ok"}


class CalculateRequest(BaseModel):
    a: float
    b: float
    operator: str


class CalculateResponse(BaseModel):
    result: float
    expression: str


def apply_operator(a: float, b: float, operator: str) -> float:
    if operator == "+":
        return a + b
    if operator == "-":
        return a - b
    if operator == "*":
        return a * b
    if operator == "/":
        if b == 0:
            raise HTTPException(status_code=400, detail="Cannot divide by zero")
        return a / b
    if operator == "%":
        return a * (b / 100)
    raise HTTPException(status_code=400, detail=f"Unsupported operator: {operator}")


class HistoryItem(BaseModel):
    id: int
    expression: str
    result: float
    mode: str
    created_at: datetime

    class Config:
        from_attributes = True


@app.post("/api/calculate", response_model=CalculateResponse)
def calculate(req: CalculateRequest, db: Session = Depends(get_db)):
    result = apply_operator(req.a, req.b, req.operator)
    expression = f"{req.a} {req.operator} {req.b}"

    record = Calculation(expression=expression, result=result, mode="standard")
    db.add(record)
    db.commit()

    return CalculateResponse(result=result, expression=expression)


@app.get("/api/history", response_model=list[HistoryItem])
def history(limit: int = 50, db: Session = Depends(get_db)):
    rows = (
        db.query(Calculation)
        .order_by(Calculation.created_at.desc())
        .limit(limit)
        .all()
    )
    return rows
