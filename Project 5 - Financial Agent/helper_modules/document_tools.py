"""
Document Tools Module - Company-specific 10-K filing analysis tools

This module provides document analysis capabilities for Apple, Google, and Tesla
10-K SEC filings using LlamaIndex vector indexing for semantic search.

Learning Objectives:
- Understand document processing with LlamaIndex
- Create vector indices for semantic search  
- Build QueryEngineTool objects for document analysis
- Configure LLM and embedding models

Your Task: Complete the missing implementations marked with YOUR CODE HERE

Key Concepts:
1. LlamaIndex Settings: Configure global LLM and embedding models
2. Document Processing: Load PDFs and split into chunks
3. Vector Indexing: Create searchable vector representations
4. Query Engines: Enable natural language querying
5. Tool Creation: Wrap engines in QueryEngineTool objects
"""

import logging
import os
from pathlib import Path
from typing import List

# LlamaIndex imports
from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.core.tools import QueryEngineTool
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Environment setup
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class DocumentToolsManager:
    """Manager for all document analysis tools"""
    
    def __init__(self, companies: List[str] = None, verbose: bool = False):
        """Initialize document tools manager
        
        Args:
            companies: List of company symbols (default: ["AAPL", "GOOGL", "TSLA"])
            verbose: Whether to print detailed progress information
        """
        self.companies = companies if companies is not None else ["AAPL", "GOOGL", "TSLA"]
        self.verbose = verbose
        self.project_root = Path.cwd()  # Use current working directory
        self.documents_dir = self.project_root / "data" / "10k_documents"
        
        # Company metadata
        self.company_info = {
            "AAPL": {"name": "Apple Inc.", "sector": "Technology"},
            "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology"},
            "TSLA": {"name": "Tesla Inc.", "sector": "Automotive"}
        }
        
        # Storage for tools
        self.document_tools = []
        
        self._configure_settings()
        
        if self.verbose:
            print("✅ Document Tools Manager Initialized")
    
    def _configure_settings(self):
        """Configure LlamaIndex settings with OpenAI models
        
        TODO: Set up the global LlamaIndex settings for LLM and embeddings
        
        Requirements:
        - Use OpenAI LLM with "gpt-3.5-turbo" model and temperature=0
        - Use OpenAI embeddings with "text-embedding-ada-002" model
        - Set these on Settings.llm and Settings.embed_model
        
        IMPORTANT NOTE FOR VOCAREUM:
        LlamaIndex requires the api_base parameter to work with Vocareum's OpenAI endpoint.
        Get the base URL from environment: os.getenv("OPENAI_API_BASE", "https://openai.vocareum.com/v1")
        Pass it as api_base parameter to both OpenAI() and OpenAIEmbedding() constructors.
        
        Hint: All necessary imports are already provided at the top of this file.
        """
        # YOUR CODE HERE
        base_url = os.getenv("OPENAI_API_BASE", "https://openai.vocareum.com/v1")

        llm = OpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_base=base_url,
        )

        embed_model = OpenAIEmbedding(
            model="text-embedding-ada-002",
            api_base=base_url,
        )

        Settings.llm = llm
        Settings.embed_model = embed_model
    
    def build_document_tools(self):
        """Build document query engines for each company
        
        Process each company's 10-K filing to create a searchable vector index
        and wrap it in a QueryEngineTool for the agent to use.
        
        Returns:
            List of QueryEngineTool objects for document analysis
        """
        if self.verbose:
            print("📄 Building document tools...")
        
        # Clear existing tools first to avoid duplicates
        self.document_tools = []
        
        # TODO: Create a text splitter for chunking documents
        # YOUR CODE HERE
        
        splitter = SentenceSplitter(
            chunk_size=1024,
            chunk_overlap=200,
        )

        for company in self.companies:
            # Determine company name for tool description
            company_name = self.company_info[company]["name"].split()[0].lower()
            if company == "GOOGL":
                company_name = "google"
            
            # Create tool name
            tool_name = f"{company}_10k_filing_tool"
            
            # Determine PDF path
            pdf_path = self.documents_dir / f"{company}_10K_2024.pdf"
            
            # Check if PDF exists
            if not pdf_path.exists():
                if self.verbose:
                    print(f"   ❌ PDF not found for {company}: {pdf_path}")
                continue
            
            try:
                # TODO: Implement document processing pipeline
                # YOUR CODE HERE
                # - Load the PDF document
                reader = SimpleDirectoryReader(input_files=[str(pdf_path)])
                documents = reader.load_data()

                # Add metadata at document level
                for doc in documents:
                    doc.metadata = doc.metadata or {}
                    doc.metadata.update({
                        "company_symbol": company,
                        "company_name": self.company_info[company]["name"],
                        "sector": self.company_info[company]["sector"],
                        "document_type": "10-K",
                        "filing_year": "2024",
                        "source_file": pdf_path.name,
                    })

                # - Split into chunks/nodes
                nodes = splitter.get_nodes_from_documents(documents)

                # - Add metadata (company info, document type)
                for node in nodes:
                    node.metadata = node.metadata or {}
                    node.metadata.update({
                        "company_symbol": company,
                        "company_name": self.company_info[company]["name"],
                        "sector": self.company_info[company]["sector"],
                        "document_type": "10-K",
                        "filing_year": "2024",
                        "source_file": pdf_path.name,
                    })

                # - Build vector index
                index = VectorStoreIndex(nodes)

                # - Create query engine
                query_engine = index.as_query_engine(
                    similarity_top_k=5
                )

                # - Wrap in QueryEngineTool with descriptive name and description
                description = (
                    f"Use this tool to answer questions about "
                    f"{self.company_info[company]['name']}'s 2024 Form 10-K filing."
                )

                tool = QueryEngineTool.from_defaults(
                    query_engine=query_engine,
                    name=tool_name,
                    description=description,
                )

                self.document_tools.append(tool)
                
                if self.verbose:
                    print(f"   ✅ {company} tool created: {tool_name}")
                    
            except Exception as e:
                if self.verbose:
                    print(f"   ❌ Error building {company} tool: {e}")
        
        # Return the built tools
        return self.document_tools
    
    def get_tools(self):
        """Get all document tools
        
        Returns:
            List of QueryEngineTool objects
        """
        return self.document_tools
    
    def query_tool(self, tool_name: str, question: str) -> str:
        """Query a specific document tool by name
        
        Args:
            tool_name: Name of the tool to query
            question: Question to ask the tool
            
        Returns:
            String response from the tool
        """
        for tool in self.document_tools:
            if tool.metadata.name == tool_name:
                result = tool.query_engine.query(question)
                return str(result)
        return f"Tool {tool_name} not found"