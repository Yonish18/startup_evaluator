import os

from crewai import Agent, Crew, Task


MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "openai/gpt-4o-mini")


def prompt_startup_idea():
    while True:
        idea = input("Enter a startup idea: ").strip()
        if idea:
            return idea
        print("Startup idea cannot be empty.")


def create_state(idea):
    state = {
        "idea": idea,
        "initial_analyses": {
            "market": None,
            "competitor": None,
            "business_model": None,
        },
        "risk_critique": None,
        "revised_analyses": {
            "market": None,
            "competitor": None,
            "business_model": None,
        },
        "final_verdict": None,
    }
    return state


def create_specialist_agents():
    market_agent = Agent(
        role="Market Analyst",
        goal="Judge real user pain, why this should work now, and what would prove demand.",
        backstory="You are skeptical about vague demand claims and care most about painful user problems.",
        llm=MODEL_NAME,
        verbose=False,
        allow_delegation=False,
    )

    competitor_agent = Agent(
        role="Competitor Analyst",
        goal="Judge substitutes, switching behavior, and why users may not leave current solutions.",
        backstory="You look for the practical reasons users stay with old tools, habits, or manual workarounds.",
        llm=MODEL_NAME,
        verbose=False,
        allow_delegation=False,
    )

    business_model_agent = Agent(
        role="Business Model Analyst",
        goal="Judge who pays, why they pay, monetization risks, and what could break financially.",
        backstory="You focus on whether the business can make money in a realistic way, not just sound interesting.",
        llm=MODEL_NAME,
        verbose=False,
        allow_delegation=False,
    )

    return {
        "market": market_agent,
        "competitor": competitor_agent,
        "business_model": business_model_agent,
    }


def create_risk_agent():
    risk_agent = Agent(
        role="Risk Analyst",
        goal="Harshly critique assumptions, contradictions, weak reasoning, and likely failure points.",
        backstory="You attack optimistic claims and look for the hidden reasons the startup might fail.",
        llm=MODEL_NAME,
        verbose=False,
        allow_delegation=False,
    )
    return risk_agent


def create_verdict_agent():
    verdict_agent = Agent(
        role="Final Startup Evaluator",
        goal="Make a practical final evaluation by weighing competing evidence from the revised analyses.",
        backstory="You write the final answer the user will read, so you include enough context to explain the decision clearly.",
        llm=MODEL_NAME,
        verbose=False,
        allow_delegation=False,
    )
    return verdict_agent


def run_specialist_analysis(agent, idea, focus):
    task = Task(
        description=(
            f"Analyze this startup idea from a {focus} perspective.\n\n"
            f"Startup idea: {idea}\n\n"
            "You are working as one independent specialist branch. "
            "Do not assume you can see any other specialist output.\n\n"
            "Do not give generic startup advice. "
            "Do not repeat the startup idea unless it is needed for your reasoning. "
            "Do not mention market size or statistics unless they were provided in the idea. "
            "Be specific, skeptical, and concrete.\n\n"
            "Keep the response short and structured with these sections:\n"
            "Core Judgment:\n"
            "Key Assumptions:\n"
            "Key Risks:\n"
            "Most Important Unknown:\n"
            "Confidence:"
        ),
        expected_output=(
            "A short structured analysis with Core Judgment, Key Assumptions, Key Risks, Most Important Unknown, and Confidence sections."
        ),
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()
    return str(result)


def run_initial_specialist_branches(idea, agents):
    print("Running independent specialist branches...")
    print()

    state = {}

    market_output = run_specialist_analysis(
        agents["market"],
        idea,
        "real user pain, why now, and what would prove demand",
    )
    state["market"] = market_output
    print("Market analysis complete.")
    print()

    competitor_output = run_specialist_analysis(
        agents["competitor"],
        idea,
        "substitutes, switching behavior, and reasons users may not switch",
    )
    state["competitor"] = competitor_output
    print("Competitor analysis complete.")
    print()

    business_model_output = run_specialist_analysis(
        agents["business_model"],
        idea,
        "who pays, why they pay, monetization risks, and financial weak points",
    )
    state["business_model"] = business_model_output
    print("Business model analysis complete.")
    print()

    return state


def run_risk_critique(idea, initial_analyses, risk_agent):
    task = Task(
        description=(
            "You are the shared risk critique stage in a startup evaluation workflow.\n\n"
            f"Startup idea: {idea}\n\n"
            "Below are the three initial specialist branch outputs.\n\n"
            "Market Analysis:\n"
            f"{initial_analyses['market']}\n\n"
            "Competitor Analysis:\n"
            f"{initial_analyses['competitor']}\n\n"
            "Business Model Analysis:\n"
            f"{initial_analyses['business_model']}\n\n"
            "Review all three together and write one shared critique.\n"
            "Do not simply repeat the previous outputs. "
            "Identify contradictions across the branches, weak or hidden assumptions, and what would most likely cause failure. "
            "Do not give generic startup advice or mention market size or statistics unless they were provided in the input.\n\n"
            "Keep the response short and structured with these sections:\n"
            "Main Weaknesses:\n"
            "Contradictions or Tensions:\n"
            "Questionable Assumptions:\n"
            "Biggest Failure Risks:"
        ),
        expected_output=(
            "One short shared critique with Main Weaknesses, Contradictions or Tensions, Questionable Assumptions, and Biggest Failure Risks sections."
        ),
        agent=risk_agent,
    )

    crew = Crew(
        agents=[risk_agent],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()
    return str(result)


def run_specialist_revision(agent, idea, focus, first_output, risk_critique):
    task = Task(
        description=(
            f"Revise your earlier startup analysis from a {focus} perspective.\n\n"
            f"Startup idea: {idea}\n\n"
            "This was your earlier analysis:\n"
            f"{first_output}\n\n"
            "This is the shared risk critique based on all specialist branches:\n"
            f"{risk_critique}\n\n"
            "Revise only your own analysis. Do not rewrite the other specialist branches.\n"
            "Respond directly to the critique and say what changed from your first version. "
            "Do not give generic startup advice. "
            "Do not mention market size or statistics unless they were provided in the idea. "
            "Be specific, skeptical, and concrete.\n\n"
            "Keep the response short and structured with these sections:\n"
            "Updated Judgment:\n"
            "What Changed:\n"
            "Key Assumptions:\n"
            "Key Risks:\n"
            "Confidence:"
        ),
        expected_output=(
            "A revised short structured analysis with Updated Judgment, What Changed, Key Assumptions, Key Risks, and Confidence sections."
        ),
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()
    return str(result)


def run_revised_specialist_branches(idea, agents, initial_analyses, risk_critique):
    print("Running revised specialist branches...")
    print()

    revised = {}

    market_revision = run_specialist_revision(
        agents["market"],
        idea,
        "real user pain, why now, and what would prove demand",
        initial_analyses["market"],
        risk_critique,
    )
    revised["market"] = market_revision
    print("Market revision complete.")
    print()

    competitor_revision = run_specialist_revision(
        agents["competitor"],
        idea,
        "substitutes, switching behavior, and reasons users may not switch",
        initial_analyses["competitor"],
        risk_critique,
    )
    revised["competitor"] = competitor_revision
    print("Competitor revision complete.")
    print()

    business_model_revision = run_specialist_revision(
        agents["business_model"],
        idea,
        "who pays, why they pay, monetization risks, and financial weak points",
        initial_analyses["business_model"],
        risk_critique,
    )
    revised["business_model"] = business_model_revision
    print("Business model revision complete.")
    print()

    return revised


def run_final_verdict(idea, revised_analyses, verdict_agent):
    task = Task(
        description=(
            "You are the final synthesis stage in a startup evaluation workflow.\n\n"
            f"Startup idea: {idea}\n\n"
            "Below are the three revised specialist branch outputs.\n\n"
            "Revised Market Analysis:\n"
            f"{revised_analyses['market']}\n\n"
            "Revised Competitor Analysis:\n"
            f"{revised_analyses['competitor']}\n\n"
            "Revised Business Model Analysis:\n"
            f"{revised_analyses['business_model']}\n\n"
            "Make a final practical decision under uncertainty. "
            "This is the only output the user will see, so include enough context to explain the final reasoning. "
            "You may summarize the revised branches, but do not just copy them or list them one by one. "
            "Reconcile the tradeoffs across market demand, competition, and business model. "
            "Choose exactly one overall label: Promising, Needs Validation, or Weak. "
            "Explain the strongest advantages, the most important risks, and the final judgment. "
            "Name the single biggest constraint holding the idea back. "
            "If there is still a viable path, identify the narrowest promising wedge or use case. "
            "If the idea is weak, explain exactly why it is weak. "
            "Give one concrete experiment-oriented next test, not generic advice like 'do more research'. "
            "Do not mention market size or statistics unless they were provided in the input. "
            "Be detailed enough to stand alone, but avoid filler.\n\n"
            "Use this structure:\n"
            "Overall Verdict:\n"
            "Final Analysis:\n"
            "Key Advantages:\n"
            "Finalized Risks:\n"
            "Biggest Constraint:\n"
            "Most Plausible Wedge:\n"
            "Best Next Test:"
        ),
        expected_output=(
            "A detailed final verdict with Overall Verdict, Final Analysis, Key Advantages, Finalized Risks, Biggest Constraint, Most Plausible Wedge, and Best Next Test sections."
        ),
        agent=verdict_agent,
    )

    crew = Crew(
        agents=[verdict_agent],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()
    return str(result)


def main():
    print("Multi-Agent Startup Evaluator")
    print("--------------------------------")
    print("Workflow:")
    print("1. Independent specialist branches")
    print("2. Shared risk critique")
    print("3. Revised specialist branches")
    print("4. Final verdict")
    print()
    print(f"Using model: {MODEL_NAME}")
    print()

    idea = prompt_startup_idea()
    state = create_state(idea)
    agents = create_specialist_agents()
    risk_agent = create_risk_agent()
    verdict_agent = create_verdict_agent()

    print()
    print("Startup idea recorded.")
    print()

    state["initial_analyses"] = run_initial_specialist_branches(state["idea"], agents)

    print("Initial branch stage finished.")
    print()
    print("Market Output:")
    print(state["initial_analyses"]["market"])
    print()
    print("Competitor Output:")
    print(state["initial_analyses"]["competitor"])
    print()
    print("Business Model Output:")
    print(state["initial_analyses"]["business_model"])
    print()

    print("Running shared risk critique...")
    print()
    state["risk_critique"] = run_risk_critique(
        state["idea"],
        state["initial_analyses"],
        risk_agent,
    )

    print("Shared risk critique complete.")
    print()
    print("Risk Critique:")
    print(state["risk_critique"])
    print()

    state["revised_analyses"] = run_revised_specialist_branches(
        state["idea"],
        agents,
        state["initial_analyses"],
        state["risk_critique"],
    )

    print("Revision stage finished.")
    print()
    print("Revised Market Output:")
    print(state["revised_analyses"]["market"])
    print()
    print("Revised Competitor Output:")
    print(state["revised_analyses"]["competitor"])
    print()
    print("Revised Business Model Output:")
    print(state["revised_analyses"]["business_model"])
    print()

    print("Running final verdict...")
    print()
    state["final_verdict"] = run_final_verdict(
        state["idea"],
        state["revised_analyses"],
        verdict_agent,
    )

    print("Final verdict complete.")
    print()
    print("Final Verdict:")
    print(state["final_verdict"])


if __name__ == "__main__":
    main()
