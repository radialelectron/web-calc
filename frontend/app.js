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

let currentMode = "standard";

function parseScientificExpression(expr) {
  const trimmed = expr.trim();

  const powMatch = trimmed.match(/^(-?\d+(\.\d+)?)\s*\^\s*(-?\d+(\.\d+)?)$/);
  if (powMatch) {
    return { function: "pow", value: parseFloat(powMatch[1]), exponent: parseFloat(powMatch[3]) };
  }

  const fnMatch = trimmed.match(/^(sin|cos|tan|log|ln|sqrt)\((-?\d+(\.\d+)?)\)$/);
  if (fnMatch) {
    return { function: fnMatch[1], value: parseFloat(fnMatch[2]) };
  }

  return null;
}

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

async function submitCalculation(endpoint, payload) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      resultEl.textContent = "Error";
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

async function handleEquals() {
  if (currentMode === "scientific") {
    const parsed = parseScientificExpression(currentExpression);
    if (!parsed) {
      resultEl.textContent = "Error";
      return;
    }
    await submitCalculation("/api/calculate/scientific", { ...parsed, angle_mode: angleMode });
    return;
  }

  const parsed = parseExpression(currentExpression);
  if (!parsed) {
    resultEl.textContent = "Error";
    return;
  }
  await submitCalculation("/api/calculate", parsed);
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

function setStdOpButtonsHidden(hidden) {
  document.querySelectorAll(".std-op").forEach((btn) => {
    btn.classList.toggle("hidden", hidden);
  });
}

document.getElementById("mode-standard").addEventListener("click", () => {
  currentMode = "standard";
  document.getElementById("mode-standard").classList.add("active");
  document.getElementById("mode-scientific").classList.remove("active");
  document.getElementById("scientific-panel").classList.add("hidden");
  setStdOpButtonsHidden(false);
});

document.getElementById("mode-scientific").addEventListener("click", () => {
  currentMode = "scientific";
  document.getElementById("mode-scientific").classList.add("active");
  document.getElementById("mode-standard").classList.remove("active");
  document.getElementById("scientific-panel").classList.remove("hidden");
  setStdOpButtonsHidden(true);
});

// Scientific mode (WEBCALC-8) — angle mode + function/constant buttons.
// Evaluation against /api/calculate/scientific is wired in WEBCALC-11.

let angleMode = "deg";

const CONSTANTS = { pi: Math.PI, e: Math.E };

document.querySelectorAll(".angle-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".angle-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    angleMode = btn.dataset.angle;
  });
});

document.querySelectorAll("[data-sci]").forEach((btn) => {
  btn.addEventListener("click", () => {
    const fn = btn.dataset.sci;
    currentExpression = fn === "pow" ? `${currentExpression} ^ ` : `${fn}(${currentExpression})`;
    render();
  });
});

document.querySelectorAll("[data-const]").forEach((btn) => {
  btn.addEventListener("click", () => {
    currentExpression += String(CONSTANTS[btn.dataset.const]);
    render();
  });
});
