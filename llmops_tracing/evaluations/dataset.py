# evaluation/dataset.py

TEST_CASES = [
    {
        "id": "TX001",
        "description": "Customer makes a normal AED 500 purchase in the UAE.",
        "transaction": {
            "user_id": "user_101",
            "amount": 500,
            "country": "UAE",
            "transaction_count_last_hour": 1,
        },
        "expected": {
            "risk_level": "LOW",
            "decision": "APPROVE",
        },
    },
    {
        "id": "TX002",
        "description": "Customer makes an AED 6000 transaction in the UAE.",
        "transaction": {
            "user_id": "user_101",
            "amount": 6000,
            "country": "UAE",
            "transaction_count_last_hour": 1,
        },
        "expected": {
            "risk_level": "HIGH",
            "decision": "BLOCK",
        },
    },
    {
        "id": "TX003",
        "description": "Customer makes an AED 2000 transaction from a different country.",
        "transaction": {
            "user_id": "user_101",
            "amount": 2000,
            "country": "Pakistan",
            "transaction_count_last_hour": 1,
        },
        "expected": {
            "risk_level": "HIGH",
            "decision": "BLOCK",
        },
    },
    {
        "id": "TX004",
        "description": "Customer performs many transactions within one hour.",
        "transaction": {
            "user_id": "user_101",
            "amount": 500,
            "country": "UAE",
            "transaction_count_last_hour": 5,
        },
        "expected": {
            "risk_level": "HIGH",
            "decision": "BLOCK",
        },
    },
]

llm_judge_dataset = [
    {
        "id": "Q1",
        "question": "What is the capital of France?",
        "reference": "Paris",
    },
    {
        "id": "Q2",
        "question": "What is 2 + 2?",
        "reference": "4",
    },
    {
        "id": "Q3",
        "question": "What planet do humans live on?",
        "reference": "Earth",
    },
]
