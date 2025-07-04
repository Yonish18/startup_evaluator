# startup_evaluator
A system that evaluates a startup/idea using multi-agent LLMs put together using CrewAI

Founder Lens:

Takes some basic information about a startup idea form the user and than runs a multi agent system orchestered by CrewAI employing different LLMs like ChatGPT and Claude to do an in-depth analysis of the idea.

Using a multi agent system, we can simulate a "discussion" between the LLM agents where each one of them specialises in a specific role in analysing some aspect of the startup idea. This wil create an automatic feedback loop and give an extremely well p[olished output to the user.]

Initially Planned Agents:

Market Agent: Checks product market fit and researches other markets that might alternatively be good for the product

Competition Agent: Researches competition in the market and evaluates differentiating factors of the idea

Feasibility Agent: Assesses the technical and operational feasibility of building and scaling the product given limited resources.

Verdict Agent: Synthesizes insights from other agents and delivers a final recommendation: **Build**, **Pivot**, or **Don't Build**, with reasoning.


inputs that we can expect form the user:

  "startup_name": "VoxSynth",
  "one_liner": "AI-powered tool to generate custom vocal tracks for music producers",
  "problem": "It's hard and expensive for indie musicians to hire real vocalists",
  "solution": "We use generative AI to create realistic vocals in various styles",
  "target_users": "Indie music producers, content creators, hobbyists",
  "tech_stack_or_claims": "We use diffusion-based voice generation models",
  "revenue_model": "Subscription and pay-per-track model",
  "competitive_edge": "Customization, voice library, fast turnaround",
  "founder_background": "Ex-Google DeepMind + Berklee College of Music"