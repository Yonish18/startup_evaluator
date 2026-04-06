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
        goal="Study customer demand, target users, and market need for a startup idea.",
        backstory="You look at whether people actually want this and who the best customers would be.",
        llm=MODEL_NAME,
        verbose=False,
        allow_delegation=False,
    )

    competitor_agent = Agent(
        role="Competitor Analyst",
        goal="Study competitors, alternatives, and what makes a startup idea different.",
        backstory="You compare the idea to existing products and point out where it may struggle or stand out.",
        llm=MODEL_NAME,
        verbose=False,
        allow_delegation=False,
    )

    business_model_agent = Agent(
        role="Business Model Analyst",
        goal="Study how a startup idea could make money and whether the model looks realistic.",
        backstory="You focus on pricing, customers, costs, and whether the business can grow in a practical way.",
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
        goal="Critique multiple startup analyses and point out weak assumptions, gaps, and major risks.",
        backstory="You review other analyses together and look for what they missed, overstated, or did not prove well.",
        llm=MODEL_NAME,
        verbose=False,
        allow_delegation=False,
    )
    return risk_agent


def create_verdict_agent():
    verdict_agent = Agent(
        role="Verdict Analyst",
        goal="Combine revised startup analyses into one final clear conclusion.",
        backstory="You read the final revised branch outputs together and turn them into one practical startup evaluation.",
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
            "Keep the response short and structured with these sections:\n"
            "Analysis:\n"
            "Assumptions:\n"
            "Risks:\n"
            "Confidence:"
        ),
        expected_output=(
            "A short structured analysis with Analysis, Assumptions, Risks, and Confidence sections."
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
        "market demand, customers, and adoption",
    )
    state["market"] = market_output
    print("Market analysis complete.")
    print()

    competitor_output = run_specialist_analysis(
        agents["competitor"],
        idea,
        "competition, substitutes, and differentiation",
    )
    state["competitor"] = competitor_output
    print("Competitor analysis complete.")
    print()

    business_model_output = run_specialist_analysis(
        agents["business_model"],
        idea,
        "business model, pricing, and scalability",
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
            "Focus on weak assumptions, missing information, contradictions, blind spots, and major risks.\n\n"
            "Keep the response short and structured with these sections:\n"
            "Main Weaknesses:\n"
            "Questionable Assumptions:\n"
            "Missing Evidence or Gaps:\n"
            "Biggest Risks:"
        ),
        expected_output=(
            "One short shared critique with Main Weaknesses, Questionable Assumptions, Missing Evidence or Gaps, and Biggest Risks sections."
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
            "Keep the response short and structured with these sections:\n"
            "Analysis:\n"
            "Assumptions:\n"
            "Risks:\n"
            "Confidence:"
        ),
        expected_output=(
            "A revised short structured analysis with Analysis, Assumptions, Risks, and Confidence sections."
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
        "market demand, customers, and adoption",
        initial_analyses["market"],
        risk_critique,
    )
    revised["market"] = market_revision
    print("Market revision complete.")
    print()

    competitor_revision = run_specialist_revision(
        agents["competitor"],
        idea,
        "competition, substitutes, and differentiation",
        initial_analyses["competitor"],
        risk_critique,
    )
    revised["competitor"] = competitor_revision
    print("Competitor revision complete.")
    print()

    business_model_revision = run_specialist_revision(
        agents["business_model"],
        idea,
        "business model, pricing, and scalability",
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
            "Combine them into one final conclusion.\n\n"
            "Keep the response short and structured with these sections:\n"
            "Overall Verdict:\n"
            "Why It Could Work:\n"
            "Main Concerns:\n"
            "Suggested Next Step:"
        ),
        expected_output=(
            "A short final verdict with Overall Verdict, Why It Could Work, Main Concerns, and Suggested Next Step sections."
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
