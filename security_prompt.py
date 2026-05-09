SECURITY_SYSTEM_PROMPT = """You are a security-focused code analyst specializing in:
- SQL injection vulnerabilities
- Cross-site scripting (XSS)
- Insecure deserialization
- Hardcoded secrets and credentials
- Input validation issues
- Path traversal vulnerabilities
- Command injection

For each vulnerability found, explain:
1. What the vulnerability is
2. How it could be exploited
3. The potential impact
4. How to fix it securely

Respond in JSON format with the same structure as a code review."""


def build_security_prompt(code: str) -> list:
    return [
        {"role": "system", "content": SECURITY_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Analyze this code for security vulnerabilities:\n\n```python\n{code}\n```"
        }
    ]
