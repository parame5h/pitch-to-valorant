from pydantic import BaseModel



class AgentOutput(BaseModel):
    agent: str
    verdict: str
    score: int
    reasoning: str
    sources: list[str]

class AggregateOutput(BaseModel):
    agent: str
    verdict: str
    lobby_score: int
    reasoning: str
    sources: list[str]


class PitchRequest(BaseModel):
    pitch: str


class AnalysisResponse(BaseModel):
    jett: AgentOutput
    viper: AgentOutput
    reyna: AgentOutput
    sova: AgentOutput
    sage: AggregateOutput