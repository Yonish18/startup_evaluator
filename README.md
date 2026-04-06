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
- `Analysis`
- `Assumptions`
- `Risks`
- `Confidence`

The risk agent returns short text with:
- `Main Weaknesses`
- `Questionable Assumptions`
- `Missing Evidence or Gaps`
- `Biggest Risks`

The verdict agent returns short text with:
- `Overall Verdict`
- `Why It Could Work`
- `Main Concerns`
- `Suggested Next Step`

## Run
1. Install dependencies:
   `pip install -r requirements.txt`
2. Make sure `OPENAI_API_KEY` is set in your environment
3. Run:
   `python main.py`

## Notes
- The workflow is designed as branch -> critique -> revision -> synthesis
- The Python code runs these stages sequentially for simplicity
- There is no API, no RAG, no vector database, and no external retrieval
