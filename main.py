from graph import app
from langchain_core.messages import HumanMessage


def run_research_agent():
    # getting the user query initially before running planner_node
    user_query = input("\nAsk me about anything about the latest current affairs: ").strip()
    if not user_query:
        print("No query provided. Exiting.")
        return

    state = {"messages": [HumanMessage(content=user_query)],
             "human_feedback": None,
             "plan": [],
             "research": {},
             "revision_score": 0
             }
    result = app.invoke(state)

    print("\nGenerated plan for your question:")
    for step in result["plan"]:
        print("-",step)
    
    print(f"\nFinal Report: \n{result["final_report"]}")
    print(f"\nThe accuracy report generated: \n{result["accuracy_report"]}\n")
    print(f"\nTotal Revisions: {result['revision_score']}")


if __name__ == "__main__":
    run_research_agent()    