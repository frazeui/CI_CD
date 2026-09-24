import json
import os

from dataset import llm_judge_dataset
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


chat = ChatGroq(model="openai/gpt-oss-120b", temperature=0, max_tokens=300)


def generate_answer(question: str, system_prompt: str) -> str:
    message = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("user", "{question}")]
    )
    response = chat.invoke(message.format(question=question))
    return response.content


def judge_answer(question: str, reference: str, answer: str) -> dict:
    prompt = f"""
You are an evaluator for an AI question-answering system.
Evalute the AI answer against the reference answer.
Question: {question}

Reference Answer: {reference}

Answer:{answer}



Evaluate the answer based on: 
1.Relevance
2.Correctness
3.Wether it agress with the llm answer or not

Return only in JSON format: 
like->
{{
    "score":0,
    "pass":"false",
    "reason":"..."
}}
Scoring: 
9-10:fully correct
7-8:almost correct
6-5:partially correct 
3-4:mostly incorrect
1-2:fully incorrect

Set "pass" to true when the answer is sufficently correct.
    """

    judge = chat.invoke(prompt)

    return json.loads(judge.content)


A_PROMPT = "Answer the user's question consicely and accurately"
B_PROMPT = """Answer the user's question concisely and accurately Give a consice answer.
Don't mention anything else from your own thinking just mention the given referenced answer."""


def run_experiment(name, system_prompt):

    results = []

    for data in llm_judge_dataset:
        print(f"Evaluating {data['id']}")
        answer = generate_answer(data["question"], system_prompt=system_prompt)
        evaluation = judge_answer(data["question"], data["reference"], answer)
        result = {
            "id": data["id"],
            "question": data["question"],
            "answer": answer,
            "score": evaluation["score"],
            "pass": evaluation["pass"],
        }

        results.append(result)
    average_score = sum(result["score"] for result in results) / len(results)
    passed = sum(1 for result in results if result["pass"])
    pass_rate = passed / len(results)
    return {
        "experiment": name,
        "average_score": average_score,
        "pass_rate": pass_rate,
        "results": results,
    }


experiment_a = run_experiment("prompt_versionA", system_prompt=A_PROMPT)
experiment_b = run_experiment("prompt_versionB", system_prompt=B_PROMPT)

MIN_SCORE = 9.0
MAX_DEGRADATION = 0.05


baseline_score = experiment_a["average_score"]
new_score = experiment_b["average_score"]


if baseline_score < 1:
    raise ValueError("Baseline must be greater than 0.")

degradation = max(0.0, (baseline_score - new_score) / baseline_score)


print("\n=====Regression Check=====")
print(f"Baseline score: {baseline_score:.2f}")
print(f"New Score: {new_score:.2f}")
print(f"Degradataion: {degradation * 100:.2f}%")
print(f"Maximum allowed: {MAX_DEGRADATION * 100:.2f}%")
# print(f"Minimum Score: {MIN_SCORE:.2f}")


if degradation > MAX_DEGRADATION:
    print("❌ Regression Detected")
    raise SystemExit(1)
print("✅ Regression Check Passed.")


# if new_score<MIN_SCORE:
#     print(f'❌ Regression Detected')
#     raise SystemExit(1)
# print(f"✅ Regression Check Passed ")


# print("\n============Experiment Results============")

# print(
#     experiment_a['experiment'],
#     experiment_a['average_score'],
#     experiment_b['pass_rate'],

#     )

# print(
#     experiment_b['experiment'],
#     experiment_b['average_score'],
#     experiment_b['pass_rate'],

#     )
