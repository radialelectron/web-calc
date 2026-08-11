import math
import time
from collections import defaultdict
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

# Basic per-IP rate limit for the unauthenticated calculate endpoints, to bound
# resource consumption (CPU + unbounded row growth in `calculations`). An
# in-memory sliding window is sufficient for this scope; a production
# deployment behind multiple workers would use a shared store (e.g. Redis).
RATE_LIMIT_WINDOW_SECONDS = 10
RATE_LIMIT_MAX_REQUESTS = 60
RATE_LIMITED_PATHS = {"/api/calculate", "/api/calculate/scientific"}

_request_log: dict[str, list[float]] = defaultdict(list)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path not in RATE_LIMITED_PATHS:
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW_SECONDS

    recent = [t for t in _request_log[client_ip] if t > window_start]
    if len(recent) >= RATE_LIMIT_MAX_REQUESTS:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests, please slow down"},
        )

    recent.append(now)
    _request_log[client_ip] = recent
    return await call_next(request)


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
    function_type: str | None = None
    angle_mode: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


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


class ScientificRequest(BaseModel):
    function: str
    value: float
    angle_mode: str = "deg"
    exponent: float | None = None


def apply_scientific(function: str, value: float, angle_mode: str, exponent: float | None) -> float:
    if function in ("sin", "cos", "tan"):
        angle = math.radians(value) if angle_mode == "deg" else value
        return {"sin": math.sin, "cos": math.cos, "tan": math.tan}[function](angle)
    if function == "log":
        if value <= 0:
            raise HTTPException(status_code=400, detail="log is undefined for non-positive numbers")
        return math.log10(value)
    if function == "ln":
        if value <= 0:
            raise HTTPException(status_code=400, detail="ln is undefined for non-positive numbers")
        return math.log(value)
    if function == "sqrt":
        if value < 0:
            raise HTTPException(status_code=400, detail="sqrt is undefined for negative numbers")
        return math.sqrt(value)
    if function == "pow":
        if exponent is None:
            raise HTTPException(status_code=400, detail="exponent is required for pow")
        return math.pow(value, exponent)
    raise HTTPException(status_code=400, detail=f"Unsupported function: {function}")


@app.post("/api/calculate/scientific", response_model=CalculateResponse)
def calculate_scientific(req: ScientificRequest, db: Session = Depends(get_db)):
    result = apply_scientific(req.function, req.value, req.angle_mode, req.exponent)
    expression = (
        f"{req.value} ^ {req.exponent}" if req.function == "pow" else f"{req.function}({req.value})"
    )

    record = Calculation(
        expression=expression,
        result=result,
        mode="scientific",
        function_type=req.function,
        angle_mode=req.angle_mode if req.function in ("sin", "cos", "tan") else None,
    )
    db.add(record)
    db.commit()

    return CalculateResponse(result=result, expression=expression)
