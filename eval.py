import json
from nodes import *
from graph import app_without_reflection, app
from agent import LLM_Model  # using LLM model as a judge

llm_chat_model = LLM_Model()

def run_baseline(query: str):
    state = {
        "messages": [HumanMessage(content=query)],
        "human_feedback": None,
        "plan": [],
        "research": {},
        "revision_score": 0
    }

    # Temporarily remove reflection
    result = app_without_reflection.invoke(state)

    return result["final_report"]

def run_with_reflection(query: str):
    state = {
        "messages": [HumanMessage(content=query)],
        "human_feedback": None,
        "plan": [],
        "research": {},
        "revision_score": 0
    }

    result = app.invoke(state)
    return result["final_report"], result["accuracy_report"]["score"]
 

# Keyword coverage metric in both answers

def keyword_coverage(report: dict, expected_keywords: list):
    text = (report["title"] + " " + report["summary"]).lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in text)
    return hits / len(expected_keywords)

class LLM_as_Judge_Feedback(BaseModel):
    feedback: str
    score: int = Field(description="should be in range of 1-10")

def LLM_as_judge(report: dict, query: str):
    prompt = f"""
    You are an expert evaluator.
    Compare the following report with the query and decide if it is accurate.
    
    Query: {query}
    Report: {report}
    
    Provide:
    - feedback (max 20 words)
    - score (1-10)
    """
    return llm_chat_model.get_structured_output(LLM_as_Judge_Feedback).invoke(prompt)
    

def evaluate_agent():
    with open(r"C:\Users\Sneha\Documents\Interview Preparation 2026\Self-correcting-Agent\eval_dataset.json", "r") as f:
        dataset = json.load(f)

    baseline_scores = []
    reflection_scores = []

    for item in dataset:
        query = item["query"]
        expected_keywords = item["expected_keywords"]

        print(f"\nEvaluating: {query}")

        # Baseline
        baseline_report = run_baseline(query)
        baseline_metric = keyword_coverage(baseline_report, expected_keywords)
        baseline_scores.append(baseline_metric)
        baseline_llm_feedback = LLM_as_judge(baseline_report, query)

        # With reflection
        reflection_report, reflection_score = run_with_reflection(query)
        reflection_metric = keyword_coverage(reflection_report, expected_keywords)
        reflection_scores.append(reflection_metric)
        reflection_llm_feedback = LLM_as_judge(reflection_report, query)

        print(f"Baseline Coverage: {baseline_metric:.2f}")
        print(f"Reflection Coverage: {reflection_metric:.2f}")
        print(f"Baseline LLM Feedback: {baseline_llm_feedback}")
        print(f"Reflection LLM Feedback: {reflection_llm_feedback}")
    avg_baseline = sum(baseline_scores) / len(baseline_scores)
    avg_reflection = sum(reflection_scores) / len(reflection_scores)

    improvement = ((avg_reflection - avg_baseline) / avg_baseline) * 100

    print("\n FINAL RESULTS ")
    print(f"Average Baseline Score: {avg_baseline:.2f}")
    print(f"Average Reflection Score: {avg_reflection:.2f}")
    print(f"Improvement: {improvement:.2f}%")

if __name__ == "__main__":
    evaluate_agent()
