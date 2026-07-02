# Pitch to Valorant Lobby

Submit your startup idea and get roasted by 5 Valorant agents acting as VCs.

## Agents
- **Jett** — evaluates market growth and 10x potential
- **Viper** — hunts competitors and market saturation  
- **Reyna** — tears apart product logic and technical feasibility
- **Sova** — finds failed startups that tried the same thing
- **Sage** — synthesizes everything into a final lobby verdict

## Stack
- LLM: Groq (openai/gpt-oss-120b)
- Search: DuckDuckGo (real-time web search)
- Orchestration: asyncio parallel execution
- Backend: FastAPI (coming soon)
- Frontend: HTML/CSS/JS (coming soon)

## Architecture
4 agents run in parallel → outputs fed to Sage → final JSON verdict