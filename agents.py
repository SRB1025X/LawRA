from crewai import Agent
from llm_config import GemmaLLM
from tools import search_tool, scraper_tool
import logging
from typing import Optional, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
import time
import json
from datetime import datetime
import os

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

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def create_llm_with_retry() -> GemmaLLM:
    try:
        logger.info("Initializing GemmaLLM instance...")
        llm = GemmaLLM(
            model_name="gemma3:1b",
            max_tokens=1024,
            temperature=0.7,
            base_url="http://localhost:11434",
            use_gpu=False,
            request_timeout=180
        )
        logger.info("GemmaLLM instance initialized successfully")
        return llm
    except Exception as e:
        logger.error(f"Error creating LLM: {str(e)}")
        raise

# Create single LLM instance to be shared
try:
    llm_instance = create_llm_with_retry()
    logger.info("LLM instance created and ready for use")
except Exception as e:
    logger.error(f"Failed to create LLM instance: {str(e)}")
    raise

# Agent 1: Document Analyst Agent
document_analyst = Agent(
    llm=llm_instance,
    role="Document Analyst",
    goal="Extract the arguments from the base paper and new research angle",
    backstory="You specialize in understanding research papers and identifying core arguments, particularly for comparative and critical legal analysis.",
    allow_delegation=False,
    max_iterations=1,
    verbose=True,
)

# Agent 2: Keyword Generator Agent
keyword_generator = Agent(
    llm=llm_instance,
    role="Keyword Generator",
    goal="Generate precise keyword combinations from legal arguments",
    backstory="You are an expert in keyword engineering, used in legal research and database querying for pinpointing highly relevant academic and legal sources.",
    allow_delegation=False,
    max_iterations=1,
    verbose=True,
)

# Agent 3: Legal Search Agent
legal_search_agent = Agent(
    llm=llm_instance,
    role="Legal Search Agent",
    goal="Search repositories using generated keywords to find legally significant documents",
    backstory="You perform highly targeted searches across legal databases and repositories. You combine serper AI with custom scraping tools on four fixed URLs and collect all the data like citations, link and text.",
    tools=[search_tool, scraper_tool],
    allow_delegation=False,
    max_iterations=1,
    verbose=True,
)

# Agent 4: Citation Chain Agent
citation_chain_agent = Agent(
    llm=llm_instance,
    role="Citation Chain Extractor",
    goal="Parse citations from papers and recursively find deeper sources",
    backstory="You are an expert in tracking legal and academic citation networks to reveal foundational and precedent-setting documents.",
    allow_delegation=False,
    max_iterations=1,
    verbose=True,
)

# Agent 5: Relevance Scorer Agent
relevance_scorer = Agent(
    llm=llm_instance,
    role="Relevance Scorer",
    goal="Score and rank all retrieved sources based on relevance and legal authority",
    backstory="You apply objective relevance models and legal domain expertise to assign priority to sources based on citation count, recency, and jurisdiction relevance.",
    allow_delegation=False,
    max_iterations=1,
    verbose=True,
)

# Agent 6: Citation Formatter Agent
citation_formatter = Agent(
    llm=llm_instance,
    role="Citation Formatter",
    goal="Format all citations in proper Bluebook style",
    backstory="You are trained in the Bluebook citation system and ensure legal citations meet formatting standards for publications, courts, and academia.",
    allow_delegation=False,
    max_iterations=1,
    verbose=True,
)

# Agent 7: Output Assembler Agent
output_assembler = Agent(
    llm=llm_instance,
    role="Output Assembler",
    goal="Compile all processed outputs into a structured final format",
    backstory="You specialize in organizing research findings into logically structured and formatted deliverables for legal and academic use.",
    allow_delegation=False,
    max_iterations=1,
    verbose=True,
)

def process_agent_output(task_output):
    if not task_output:
        print("⚠️ No output received from the agent.")
        return

    # Safely convert CrewOutput to string
    cleaned_output = str(task_output).strip()

    cleaned_output = '\n'.join(
        line for line in cleaned_output.split('\n') if line.strip()
    )

    with open("legal_research_extracted.txt", "w") as f:
        f.write(cleaned_output)

    print("\n✅ Output saved to legal_research_extracted.txt")
