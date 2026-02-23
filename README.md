This project is an end-to-end self correcting agent that can be used for various purposes.

```markdown
**Research Agent with Reflection Loop.**
```

```markdown
It will:
- Plan how to answer a query
- Research using tools (web search)
- Write a structured report
- Critique itself
- If low quality → revise
- Human approval in the loop
- Output final cited answer
```

```markdown
This demonstrates:
- LangGraph state management
- Cycles (core differentiator from LangChain)
- Tool usage
- Reflection pattern
- Conditional routing
- Evaluation thinking
```

Improvement through reflection is going to be measured by:
- Baseline (no reflection) Planner agent -> Researcher agent -> Writer agent
- With reflection: Planner agent -> Researcher agent -> Writer agent -> Reflector agent -> Router agent (that controls whether to revise or not)

**Structure**
```
project/
│
├── agent.py      # State + LLM definitions (Used ChatOpenAI and OpenAI)
├── tools.py      # Tool definitions (Used one tool - Research tool for websearch using OpenAI)
├── nodes.py      # All node functions (Planner, Researcher, Writer, Reflector, Router)
├── graph.py      # Graph building + app = graph.compile() and baseline app without reflection
├── main.py       # Program execution entry point
├── app.py        # Streamlit UI
├── eval.py       # Evaluation script   
```
