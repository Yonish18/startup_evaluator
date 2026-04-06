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

    print()
    print("Workflow scaffold initialized.")
    print("Startup idea recorded:")
    print(state["idea"])


if __name__ == "__main__":
    main()
