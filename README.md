# Multi-Agent Startup Evaluator 

## Overview
A simple multi-agent system that evaluates a startup idea using multiple specialized agents and a critique loop.

## Agents
- Market Agent: analyzes demand and customers
- Competitor Agent: analyzes existing solutions
- Business Model Agent: analyzes monetization and scalability
- Risk Agent: critiques assumptions and identifies weaknesses
- Verdict Agent: combines all outputs into a final decision

## Workflow
1. User inputs a startup idea
2. Market, Competitor, and Business Model agents analyze it
3. Risk agent critiques their outputs
4. Specialist agents revise based on critique
5. Verdict agent produces final summary

## Output Format
Each agent returns:
```json
{
  "analysis": "...",
  "assumptions": ["..."],
  "risks": ["..."],
  "confidence": "low | medium | high"
}