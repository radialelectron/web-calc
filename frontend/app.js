// Standard Calculator — GUI shell (WEBCALC-2)
// Handles digit/operator entry and display. Actual calculation is wired to the
// backend API in the Frontend/API integration story (WEBCALC-5).

const expressionEl = document.getElementById("expression");
const resultEl = document.getElementById("result");

let currentExpression = "";

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

// Placeholder — replaced by a real /api/calculate call in WEBCALC-5.
function handleEquals() {
  resultEl.textContent = "...";
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
