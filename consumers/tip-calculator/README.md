# tip-calculator (Webcalc consumer)

Small downstream service that computes restaurant tips by calling Webcalc's
`POST /api/calculate`:

| Webcalc usage | Where |
|---|---|
| `operator: "%"` → tip = `result` of "`tip_percent` percent of `bill`" | `tip_calculator/webcalc_client.py::percent_of` |
| `operator: "+"` → total = `result` of bill + tip | `tip_calculator/webcalc_client.py::add` |
| Response field `result` | `webcalc_client.py::_calculate` |
| Base URL / contract reference | `tip_calculator/config.py` |
| Contract | `../../contracts/webcalc-openapi.json` |

It lives in the Webcalc repo as a separate component (own requirements and tests)
rather than a separate repository; no new repo was created or authorised.

## Tests

```bash
pip install -r requirements.txt
pytest tests -v     # contract checks + integration against the real Webcalc app, in-process
```
