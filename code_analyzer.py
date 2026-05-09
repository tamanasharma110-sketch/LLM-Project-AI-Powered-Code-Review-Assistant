from llm_client import get_completion, get_structured_review, CodeReviewResponse
from prompts.review_prompt import build_review_prompt
from prompts.security_prompt import build_security_prompt
from prompts.explain_prompt import build_explain_prompt


class CodeAnalyzer:
    """Orchestrates different types of code analysis."""
    
    def __init__(self):
        self.history = []
    
    def review_code(
        self, 
        code: str, 
        focus_areas: list[str] = None
    ) -> CodeReviewResponse:
        """Perform comprehensive code review."""
        messages = build_review_prompt(code, focus_areas)
        result = get_structured_review(messages)
        
        self.history.append({
            "type": "review",
            "code": code,
            "result": result
        })
        
        return result
    
    def security_scan(self, code: str) -> CodeReviewResponse:
        """Focused security vulnerability analysis."""
        messages = build_security_prompt(code)
        return get_structured_review(messages)
    
    def explain_code(self, code: str, level: str = "intermediate") -> str:
        """Generate educational explanation of code."""
        messages = build_explain_prompt(code, level)
        return get_completion(messages, temperature=0.5)
    
    def suggest_refactor(self, code: str) -> str:
        """Suggest refactoring improvements."""
        messages = [
            {
                "role": "system",
                "content": "You are a refactoring expert. Suggest improvements "
                          "focusing on readability, maintainability, and SOLID principles. "
                          "Show the refactored code with explanations."
            },
            {
                "role": "user",
                "content": f"Refactor this code:\n\n```python\n{code}\n```"
            }
        ]
        return get_completion(messages, temperature=0.4)
    
    def generate_tests(self, code: str) -> str:
        """Generate unit tests for the code."""
        messages = [
            {
                "role": "system",
                "content": "You are a testing expert. Generate comprehensive pytest "
                          "unit tests covering normal cases, edge cases, and error handling. "
                          "Include docstrings explaining what each test verifies."
            },
            {
                "role": "user",
                "content": f"Generate tests for:\n\n```python\n{code}\n```"
            }
        ]
        return get_completion(messages, temperature=0.3)
    
    def generate_docs(self, code: str) -> str:
        """Generate documentation for the code."""
        messages = [
            {
                "role": "system",
                "content": "Generate clear documentation including: "
                          "module docstring, function/class docstrings (Google style), "
                          "type hints, and a brief README section explaining usage."
            },
            {
                "role": "user",
                "content": f"Document this code:\n\n```python\n{code}\n```"
            }
        ]
        return get_completion(messages, temperature=0.3)

