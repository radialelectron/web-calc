from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="WEB Calc API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/api/calculate", response_model=CalculateResponse)
def calculate(req: CalculateRequest):
    result = apply_operator(req.a, req.b, req.operator)
    expression = f"{req.a} {req.operator} {req.b}"
    return CalculateResponse(result=result, expression=expression)
