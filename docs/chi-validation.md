# CHI change-intelligence validation fixture

Engineering fixture, not evidence of customer value. All statuses below are what was
actually run; anything not listed as verified is unverified.

## Scenario
Webcalc `POST /api/calculate`, operator `%`: **percent-of** (`a * b/100`) → **modulo** (`a % b`),
with 400 on `b == 0`. The request/response schema is unchanged; only the meaning of `result`
changes, so a schema diff alone cannot see it — the contract `description`, the code diff and
the consumer's code/tests must be read together.

## Evidence chain
| Link | Source |
|---|---|
| Jira issue | WEBCALC-26 (Story under epic WEBCALC-1, created and read back in Jira; links PRs #20 and #21) |
| Webcalc change | `backend/main.py::apply_operator`, branch `WEBCALC-4CHI-percent-operator-modulo` (branch name predates the real key WEBCALC-26) |
| Contract change | `contracts/webcalc-openapi.json` → `CalculateRequest.operator.description` |
| Consumer dependency | `consumers/tip-calculator/tip_calculator/webcalc_client.py::percent_of` (`operator="%"`, reads `result`), used by `tip.py::tip_for_bill`; contract ref in `tip_calculator/config.py` |
| Other in-repo dependents | `frontend/app.js` (`handlePercent`, `parseExpression` send `%`) — not changed, behavior changes for users |
| Test results | see below |

## Results (local, Python 3.11)
| Suite | Baseline `6b430cb` | Change branch |
|---|---|---|
| Webcalc `tests/` | 19 pass | 20 pass (updated `%` case, added `%` by zero) |
| Consumer `consumers/tip-calculator/tests` | 6 pass | **4 fail**, 2 pass (intentional; consumer not adapted) |

GitHub Actions (PR #21): Backend Tests pass, Automation Test Suite pass (includes updated TC-06),
Tip Calculator Consumer Tests **fail** (expected). Lint did not run on PR #21 (its workflow only
triggers for PRs to main/develop); PR #20 lint passed.

Not verified: Xray (the Jira project has Test/Test Set/Test Execution types, but no Xray workflow
was found or used, so nothing was published), merge, deployment, production behaviour.

## Recommended action
Do not merge while the consumer is red. Either keep `%` as percent-of and add a new
`mod` operator, or version the change and update `tip_calculator` (and `frontend/app.js`)
in lockstep.
