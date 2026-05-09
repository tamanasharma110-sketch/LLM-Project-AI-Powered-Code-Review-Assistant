SYSTEM_PROMPT = """You are an expert Python code reviewer with deep knowledge of:
- Python best practices and PEP standards
- Common bugs and anti-patterns
- Security vulnerabilities (OWASP Top 10)
- Performance optimization
- Clean code principles

Analyze code thoroughly but fairly. Provide actionable feedback that helps 
developers learn and improve. Be specific about line numbers and provide 
concrete fixes.

Always respond with valid JSON matching this structure:
{
    "summary": "Brief overview of code quality",
    "issues": [
        {
            "line_number": 5,
            "severity": "warning",
            "category": "security",
            "description": "What the issue is",
            "suggestion": "How to fix it",
            "code_fix": "Corrected code snippet"
        }
    ],
    "overall_score": 7,
    "strengths": ["List of things done well"],
    "improved_code": "Full improved version if needed"
}"""


def build_review_prompt(code: str, focus_areas: list[str] = None) -> list:
    """Build the message list for code review."""
    
    focus_instruction = ""
    if focus_areas:
        focus_instruction = f"\n\nFocus especially on: {', '.join(focus_areas)}"
    
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user", 
            "content": f"Review this Python code:{focus_instruction}\n\n```python\n{code}\n```"
        }
    ]
