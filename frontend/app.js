// Standard Calculator — GUI shell (WEBCALC-2) + API integration (WEBCALC-5)

const API_BASE = window.WEB_CALC_API_BASE || "http://localhost:8000";

const expressionEl = document.getElementById("expression");
const resultEl = document.getElementById("result");

let currentExpression = "";

const OPERATOR_SYMBOL_TO_API = {
  "+": "+",
  "-": "-",
  x: "*",
  "/": "/",
};

function parseExpression(expr) {
  // Supports a single binary operation, e.g. "12 + 8" or "200 % 10"
  const match = expr.trim().match(/^(-?\d+(\.\d+)?)\s*([+\-x/%])\s*(-?\d+(\.\d+)?)$/);
  if (!match) return null;
  const [, aStr, , opSymbol, bStr] = match;
  return {
    a: parseFloat(aStr),
    b: parseFloat(bStr),
    operator: opSymbol === "%" ? "%" : OPERATOR_SYMBOL_TO_API[opSymbol],
  };
}

function render() {
  expressionEl.textContent = currentExpression;
}

function handleDigit(digit) {
  currentExpression += digit;
  render();
}

function handleDecimal() {
  currentExpression += ".";
  render();
}

function handleOperator(symbol) {
  currentExpression += ` ${symbol} `;
  render();
}

function handleClear() {
  currentExpression = "";
  resultEl.textContent = "0";
  render();
}

function handlePercent() {
  currentExpression += " % ";
  render();
}

async function handleEquals() {
  const parsed = parseExpression(currentExpression);
  if (!parsed) {
    resultEl.textContent = "Error";
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/calculate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(parsed),
    });

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      resultEl.textContent = body.detail ? "Error" : "Error";
      return;
    }

    const data = await res.json();
    resultEl.textContent = String(data.result);
    currentExpression = String(data.result);
    render();
  } catch (err) {
    resultEl.textContent = "Error";
  }
}

const ACTIONS = {
  clear: handleClear,
  percent: handlePercent,
  divide: () => handleOperator("/"),
  multiply: () => handleOperator("x"),
  subtract: () => handleOperator("-"),
  add: () => handleOperator("+"),
  equals: handleEquals,
  decimal: handleDecimal,
};

document.querySelectorAll(".btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const digit = btn.dataset.digit;
    const action = btn.dataset.action;
    if (digit !== undefined) {
      handleDigit(digit);
    } else if (action && ACTIONS[action]) {
      ACTIONS[action]();
    }
  });
});

document.getElementById("mode-standard").addEventListener("click", () => {
  document.getElementById("mode-standard").classList.add("active");
  document.getElementById("mode-scientific").classList.remove("active");
  document.getElementById("scientific-panel").classList.add("hidden");
  document.querySelector(".standard-buttons").classList.remove("hidden");
});

document.getElementById("mode-scientific").addEventListener("click", () => {
  document.getElementById("mode-scientific").classList.add("active");
  document.getElementById("mode-standard").classList.remove("active");
  document.getElementById("scientific-panel").classList.remove("hidden");
  document.querySelector(".standard-buttons").classList.add("hidden");
});
