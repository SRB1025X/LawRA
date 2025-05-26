from crewai import Task
from agents import (
    document_analyst,
    keyword_generator,
    legal_search_agent,
    citation_chain_agent,
    relevance_scorer,
    citation_formatter,
    output_assembler
)

# Task 1: Analyze base legal document and extract arguments
document_analysis_task = Task(
    description="""
Analyze the provided legal document to extract key arguments and identify any new research angles or interpretations.
""",
    expected_output="""
A structured summary of all primary and secondary legal arguments extracted from the PDF document.
""",
    agent=document_analyst,
    max_iterations=2
)

# Task 2: Generate search keywords
keyword_generation_task = Task(
    description="""
Generate precise and context-aware keyword combinations based on extracted legal arguments for legal and academic research.
""",
    expected_output="""
List of keyword combinations categorized by statute, case type, issue, and jurisdiction.
""",
    agent=keyword_generator,
    context=[document_analysis_task],
    max_iterations=2
)

# Task 3: Conduct repository search
search_task = Task(
    description="""
Use the generated keyword combinations to search across 4 fixed URLs and legal databases for case law, statutes, and papers.
""",
    expected_output="""
A compiled list of documents, cases, and legal papers retrieved with URLs or sources noted.
""",
    agent=legal_search_agent,
    context=[keyword_generation_task],
    max_iterations=2
)

# Task 4: Extract and expand citation network
citation_parsing_task = Task(
    description="""
Parse the citations found in retrieved sources and follow them recursively to uncover foundational legal materials.
""",
    expected_output="""
Extended set of legal materials discovered through citation tracing, with metadata and source links.
""",
    agent=citation_chain_agent,
    context=[search_task],
    max_iterations=2
)

# Task 5: Score relevance and authority
relevance_scoring_task = Task(
    description="""
Score and rank all sources for relevance, legal authority, and jurisdictional accuracy.
""",
    expected_output="""
Ranked list of sources with relevance scores, authority indicators, and brief justifications.
""",
    agent=relevance_scorer,
    context=[citation_parsing_task],
    max_iterations=2
)

# Task 6: Format citations
formatting_task = Task(
    description="""
Format all citations from top-ranked sources using the Bluebook citation style.
""",
    expected_output="""
A formatted list of citations in proper Bluebook style.
""",
    agent=citation_formatter,
    context=[relevance_scoring_task],
    max_iterations=2
)

# Task 7: Compile final output
assembly_task = Task(
    description="""
Assemble the top legal arguments, source rankings, and formatted citations into a final structured report.
""",
    expected_output="""
Final compiled legal research output in a structured format suitable for academic or legal reference.
""",
    agent=output_assembler,
    context=[formatting_task],
    max_iterations=2,
    output_file="legal_final_output.txt"
)
