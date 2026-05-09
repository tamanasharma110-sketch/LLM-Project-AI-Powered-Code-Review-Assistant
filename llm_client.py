import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class CodeIssue(BaseModel):
    line_number: Optional[int]
    severity: str  # "error", "warning", "suggestion"
    category: str  # "bug", "security", "style", "performance"
    description: str
    suggestion: str
    code_fix: Optional[str]


class CodeReviewResponse(BaseModel):
    summary: str
    issues: list[CodeIssue]
    overall_score: int  # 1-10
    strengths: list[str]
    improved_code: Optional[str]


def get_completion(messages: list, temperature: float = 0.3) -> str:
    """Basic completion without structured output."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=temperature,
        max_tokens=2000
    )
    return response.choices[0].message.content


def get_structured_review(messages: list) -> CodeReviewResponse:
    """Get structured code review using function calling."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    
    import json
    data = json.loads(response.choices[0].message.content)
    return CodeReviewResponse(**data)
