from crewai import Crew
from agents import (
    document_analyst,
    keyword_generator,
    legal_search_agent,
    citation_chain_agent,
    relevance_scorer,
    citation_formatter,
    output_assembler,
    process_agent_output
)
from tasks import (
    document_analysis_task,
    keyword_generation_task,
    search_task,
    citation_parsing_task,
    relevance_scoring_task,
    formatting_task,
    assembly_task
)
import logging
import time
from typing import Optional
from utils import extract_text_from_pdf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('legal_research.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_legal_research(pdf_path: str) -> Optional[str]:
    start_time = time.time()
    logger.info("Starting legal research process")

    try:
        # Extract text from the PDF
        logger.info(f"Extracting content from PDF: {pdf_path}")
        pdf_text = extract_text_from_pdf(pdf_path)
        logger.info("PDF text extraction complete")

        # Inject the extracted text into the initial document analysis task
        document_analysis_task.description += f"\n\n[Source: PDF Document]\n{pdf_text[:5000]}..."

        # Set up Crew with the new agents and tasks
        crew = Crew(
            agents=[
                document_analyst,
                keyword_generator,
                legal_search_agent,
                citation_chain_agent,
                relevance_scorer,
                citation_formatter,
                output_assembler
            ],
            tasks=[
                document_analysis_task,
                keyword_generation_task,
                search_task,
                citation_parsing_task,
                relevance_scoring_task,
                formatting_task,
                assembly_task
            ],
            max_rpm=20,
            max_iterations=2,
            verbose=False,
            sequential=True
        )

        logger.info("Crew initialized, starting task execution")
        task_output = crew.kickoff()

        if task_output:
            process_agent_output(task_output)
            execution_time = time.time() - start_time
            logger.info(f"Legal research completed successfully in {execution_time:.2f} seconds")
            return task_output
        else:
            logger.error("No output generated from crew")
            return None

    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Error in legal research after {execution_time:.2f} seconds: {str(e)}", exc_info=True)
        return None

def main(pdf_path):
    print("\nStarting Legal Research Process...")
    print("=" * 50)

    output = run_legal_research(pdf_path)

    if output:
        print("\nLegal Research Output:")
        print("=" * 50)
        print(output)
        print("=" * 50)
        print("\nOutput has been saved to:")
        print("- legal_research_extracted.txt (Research phase)")
        print("- legal_memo_output_final.txt (Analysis phase)")
        print("- legal_research.log (Process logs)")
    else:
        print("\nError: Research process failed. Check legal_research.log for details.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python crew.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    main(pdf_path)
