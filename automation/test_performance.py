"""Automates TC-10 and TC-18 from the Confluence Test Cases page: basic
concurrency/response-time smoke checks against the calculate endpoints.
"""
import statistics
import time
from concurrent.futures import ThreadPoolExecutor

CONCURRENCY = 50


def _timed_request(fn):
    start = time.perf_counter()
    res = fn()
    elapsed_ms = (time.perf_counter() - start) * 1000
    return res.status_code, elapsed_ms


def test_tc10_standard_calculate_under_load(api):
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        results = list(
            pool.map(
                lambda _: _timed_request(lambda: api.calculate(3, 4, "+")),
                range(CONCURRENCY),
            )
        )

    statuses = [r[0] for r in results]
    latencies = [r[1] for r in results]

    assert all(s == 200 for s in statuses)
    avg_ms = statistics.mean(latencies)
    print(f"Standard calculate: {CONCURRENCY} concurrent requests, avg {avg_ms:.1f}ms")
    assert avg_ms < 200


def test_tc18_scientific_calculate_under_load(api):
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        results = list(
            pool.map(
                lambda _: _timed_request(lambda: api.calculate_scientific("sin", 45, "deg")),
                range(CONCURRENCY),
            )
        )

    statuses = [r[0] for r in results]
    latencies = [r[1] for r in results]

    assert all(s == 200 for s in statuses)
    avg_ms = statistics.mean(latencies)
    print(f"Scientific calculate: {CONCURRENCY} concurrent requests, avg {avg_ms:.1f}ms")
    assert avg_ms < 250
