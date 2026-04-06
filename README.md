# Multi-Agent Startup Evaluator

## Overview
A simple terminal-based CrewAI prototype that evaluates a startup idea using a staged multi-agent workflow.

## Agents
- Market Agent: analyzes demand and customers
- Competitor Agent: analyzes existing solutions
- Business Model Agent: analyzes monetization and scalability
- Risk Agent: critiques assumptions and identifies weaknesses
- Verdict Agent: combines all outputs into a final decision

## Workflow
1. User inputs a startup idea
2. Market, Competitor, and Business Model agents analyze it as independent branches
3. Risk agent receives all 3 branch outputs together and writes one shared critique
4. Each specialist revises only its own analysis using that shared critique
5. Verdict agent receives all 3 revised outputs together and produces the final summary

## Output Format
The specialist agents return short text with:
- `Core Judgment`
- `Key Assumptions`
- `Key Risks`
- `Most Important Unknown`
- `Confidence`

The risk agent returns short text with:
- `Main Weaknesses`
- `Contradictions or Tensions`
- `Questionable Assumptions`
- `Biggest Failure Risks`

The verdict agent returns the final user-facing summary with:
- `Overall Verdict`
- `Final Analysis`
- `Key Advantages`
- `Finalized Risks`
- `Biggest Constraint`
- `Most Plausible Wedge`
- `Best Next Test`

## Project Structure
- `main.py`: active terminal-based CrewAI startup evaluator
- `requirements.txt`: Python dependencies
- `.env.example`: safe template for local environment variables
- `examples/TestStartup.txt`: sample startup idea for manual testing
- `unused/legacy/`: old experiments, API/Docker files, and placeholders kept for reference

## Run
1. Install dependencies:
   `pip install -r requirements.txt`
2. Copy the example environment file:
   `cp .env.example .env`
3. Open `.env` and replace `your-openai-api-key-here` with your real OpenAI API key
4. Run:
   `python main.py`

The `.env` file is ignored by git, so your real API key should stay local.
To use a different model, change `OPENAI_MODEL_NAME` in `.env`.

## Notes
- The workflow is designed as branch -> critique -> revision -> synthesis
- The Python code runs these stages sequentially for simplicity
- There is no API, no RAG, no vector database, and no external retrieval
