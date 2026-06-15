from pydantic import BaseModel

class Recommendation(BaseModel):
    title: str
    popularity_score: int
    final_score: int