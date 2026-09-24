from dataset import TEST_CASES
from evalators import evaluate


def fake_llm(transaction: dict) -> dict:
    amount = transaction["amount"]
    country = transaction["country"]
    tx_count = transaction["transaction_count_last_hour"]

    if amount > 5000:
        return {"risk_level": "HIGH", "decision": "BLOCK"}
    elif country != "UAE":
        return {"risk_level": "MEDIUM", "decision": "REVIEW"}
    elif tx_count > 3:
        return {"risk_level": "HIGH", "decision": "BLOCK"}
    else:
        return {"risk_level": "LOW", "decision": "APPROVE"}


results = []
for test in TEST_CASES:
    actual = fake_llm(test["transaction"])
    passed = evaluate(expected=test["expected"], actual=actual)

    results.append(
        {
            "id": test["id"],
            "expected": test["expected"],
            "actual": actual,
            "passed": passed,
        }
    )

# for result in results:
#     print(result)

passed = sum(result["passed"] for result in results)
total = len(results)

pass_rate = passed / total
print(f"Pass rate: {pass_rate * 100:.2f}% ({passed}/{total})")

MIN_PASS_RATE = 0.90

if pass_rate < MIN_PASS_RATE:
    raise RuntimeError(f"Evaluation Failed: {pass_rate:.2%}")
