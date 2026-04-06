from crewai import Agent, Crew, Task


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
        verbose=False,
        allow_delegation=False,
    )

    competitor_agent = Agent(
        role="Competitor Analyst",
        goal="Study competitors, alternatives, and what makes a startup idea different.",
        backstory="You compare the idea to existing products and point out where it may struggle or stand out.",
        verbose=False,
        allow_delegation=False,
    )

    business_model_agent = Agent(
        role="Business Model Analyst",
        goal="Study how a startup idea could make money and whether the model looks realistic.",
        backstory="You focus on pricing, customers, costs, and whether the business can grow in a practical way.",
        verbose=False,
        allow_delegation=False,
    )

    return {
        "market": market_agent,
        "competitor": competitor_agent,
        "business_model": business_model_agent,
    }


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


def main():
    print("Multi-Agent Startup Evaluator")
    print("--------------------------------")
    print("Workflow:")
    print("1. Independent specialist branches")
    print("2. Shared risk critique")
    print("3. Revised specialist branches")
    print("4. Final verdict")
    print()

    idea = prompt_startup_idea()
    state = create_state(idea)
    agents = create_specialist_agents()

    print()
    print("Startup idea recorded.")
    print()

    state["initial_analyses"] = run_initial_specialist_branches(state["idea"], agents)

    print("Initial branch stage finished.")
    print("Later stages are not added yet.")
    print()
    print("Market Output:")
    print(state["initial_analyses"]["market"])
    print()
    print("Competitor Output:")
    print(state["initial_analyses"]["competitor"])
    print()
    print("Business Model Output:")
    print(state["initial_analyses"]["business_model"])


if __name__ == "__main__":
    main()
