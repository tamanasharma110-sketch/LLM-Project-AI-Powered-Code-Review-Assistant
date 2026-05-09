import streamlit as st
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from code_analyzer import CodeAnalyzer

st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for code highlighting
st.markdown("""
<style>
.code-block {
    background-color: #1e1e1e;
    border-radius: 8px;
    padding: 16px;
    overflow-x: auto;
}
.severity-error { color: #ff6b6b; font-weight: bold; }
.severity-warning { color: #ffd93d; }
.severity-suggestion { color: #6bcb77; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_analyzer():
    return CodeAnalyzer()


def render_code(code: str) -> str:
    """Syntax highlight Python code."""
    formatter = HtmlFormatter(style="monokai", noclasses=True)
    return highlight(code, PythonLexer(), formatter)


def main():
    st.title("🔍 AI Code Review Assistant")
    st.markdown("Analyze Python code for bugs, security issues, and improvements")
    
    analyzer = get_analyzer()
    
    # Sidebar for options
    with st.sidebar:
        st.header("Analysis Options")
        
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Full Review", "Security Scan", "Explain Code", "Refactor", "Generate Tests", "Generate Docs"]
        )
        
        if analysis_type == "Full Review":
            focus_areas = st.multiselect(
                "Focus Areas",
                ["bugs", "security", "performance", "style", "best practices"],
                default=["bugs", "style"]
            )
        
        if analysis_type == "Explain Code":
            level = st.select_slider(
                "Explanation Level",
                options=["beginner", "intermediate", "advanced"],
                value="intermediate"
            )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Input Code")
        code = st.text_area(
            "Paste your Python code here",
            height=400,
            placeholder="def example():\n    pass"
        )
        
        analyze_btn = st.button("🚀 Analyze", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("📊 Analysis Results")
        
        if analyze_btn and code.strip():
            with st.spinner("Analyzing code..."):
                try:
                    if analysis_type == "Full Review":
                        result = analyzer.review_code(code, focus_areas)
                        
                        # Score display
                        score_color = "green" if result.overall_score >= 7 else "orange" if result.overall_score >= 4 else "red"
                        st.metric("Overall Score", f"{result.overall_score}/10")
                        
                        # Summary
                        st.markdown(f"**Summary:** {result.summary}")
                        
                        # Strengths
                        if result.strengths:
                            with st.expander("✅ Strengths", expanded=True):
                                for strength in result.strengths:
                                    st.markdown(f"- {strength}")
                        
                        # Issues
                        if result.issues:
                            with st.expander(f"⚠️ Issues ({len(result.issues)})", expanded=True):
                                for issue in result.issues:
                                    severity_class = f"severity-{issue.severity}"
                                    st.markdown(f"""
                                    **<span class='{severity_class}'>[{issue.severity.upper()}]</span> {issue.category}** 
                                    {f'(Line {issue.line_number})' if issue.line_number else ''}
                                    
                                    {issue.description}
                                    
                                    💡 **Suggestion:** {issue.suggestion}
                                    """, unsafe_allow_html=True)
                                    
                                    if issue.code_fix:
                                        st.code(issue.code_fix, language="python")
                                    st.divider()
                        
                        # Improved code
                        if result.improved_code:
                            with st.expander("✨ Improved Code"):
                                st.code(result.improved_code, language="python")
                    
                    elif analysis_type == "Security Scan":
                        result = analyzer.security_scan(code)
                        st.markdown(f"**Security Score:** {result.overall_score}/10")
                        st.markdown(result.summary)
                        
                        for issue in result.issues:
                            st.error(f"**{issue.category}**: {issue.description}")
                            st.info(f"Fix: {issue.suggestion}")
                    
                    elif analysis_type == "Explain Code":
                        explanation = analyzer.explain_code(code, level)
                        st.markdown(explanation)
                    
                    elif analysis_type == "Refactor":
                        refactored = analyzer.suggest_refactor(code)
                        st.markdown(refactored)
                    
                    elif analysis_type == "Generate Tests":
                        tests = analyzer.generate_tests(code)
                        st.code(tests, language="python")
                    
                    elif analysis_type == "Generate Docs":
                        docs = analyzer.generate_docs(code)
                        st.markdown(docs)
                
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
        
        elif analyze_btn:
            st.warning("Please enter some code to analyze.")


if __name__ == "__main__":
    main()
