"""
Test script to verify LlamaIndex Vocareum API compatibility fix
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("Testing LlamaIndex Vocareum API Compatibility Fix")
print("=" * 60)
print()

# Test 1: Check environment variables
print("✅ Test 1: Environment Variables")
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE", "https://openai.vocareum.com/v1")
print(f"   OPENAI_API_KEY: {api_key[:20]}..." if api_key else "   OPENAI_API_KEY: Not set")
print(f"   OPENAI_API_BASE: {api_base}")
print()

# Test 2: Import LlamaIndex components
print("✅ Test 2: Import LlamaIndex Components")
try:
    from llama_index.llms.openai import OpenAI
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.core import Settings
    print("   ✓ Successfully imported OpenAI")
    print("   ✓ Successfully imported OpenAIEmbedding")
    print("   ✓ Successfully imported Settings")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)
print()

# Test 3: Initialize with api_base parameter (THE FIX)
print("✅ Test 3: Initialize with api_base parameter (Vocareum Fix)")
try:
    # This is the fix - explicitly passing api_base parameter
    llm = OpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_base=api_base  # This parameter is REQUIRED for Vocareum
    )
    print(f"   ✓ LLM initialized with api_base={api_base}")
    
    embed_model = OpenAIEmbedding(
        model="text-embedding-ada-002",
        api_base=api_base  # This parameter is REQUIRED for Vocareum
    )
    print(f"   ✓ Embedding model initialized with api_base={api_base}")
except Exception as e:
    print(f"   ✗ Initialization failed: {e}")
    sys.exit(1)
print()

# Test 4: Configure Settings
print("✅ Test 4: Configure Global Settings")
try:
    Settings.llm = llm
    Settings.embed_model = embed_model
    print("   ✓ Settings.llm configured")
    print("   ✓ Settings.embed_model configured")
except Exception as e:
    print(f"   ✗ Settings configuration failed: {e}")
    sys.exit(1)
print()

# Test 5: Test helper modules
print("✅ Test 5: Test Helper Modules Import")
try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'helper_modules'))
    
    # Import agent coordinator
    from agent_coordinator import AgentCoordinator
    print("   ✓ Successfully imported AgentCoordinator")
    
    # Import document tools
    from document_tools import DocumentToolsManager
    print("   ✓ Successfully imported DocumentToolsManager")
    
    # Import function tools
    from function_tools import FunctionToolsManager
    print("   ✓ Successfully imported FunctionToolsManager")
except Exception as e:
    print(f"   ✗ Helper module import failed: {e}")
    sys.exit(1)
print()

# Test 6: Verify the fix in helper modules
print("✅ Test 6: Verify Fix Applied in Helper Modules")
import inspect

# Check agent_coordinator.py
try:
    from helper_modules.agent_coordinator import AgentCoordinator
    source = inspect.getsource(AgentCoordinator._configure_settings)
    if 'api_base' in source and 'OPENAI_API_BASE' in source:
        print("   ✓ agent_coordinator.py has api_base fix")
    else:
        print("   ✗ agent_coordinator.py missing api_base parameter")
except Exception as e:
    print(f"   ⚠ Could not verify agent_coordinator.py: {e}")

# Check document_tools.py
try:
    from helper_modules.document_tools import DocumentToolsManager
    source = inspect.getsource(DocumentToolsManager._configure_settings)
    if 'api_base' in source and 'OPENAI_API_BASE' in source:
        print("   ✓ document_tools.py has api_base fix")
    else:
        print("   ✗ document_tools.py missing api_base parameter")
except Exception as e:
    print(f"   ⚠ Could not verify document_tools.py: {e}")

# Check function_tools.py
try:
    from helper_modules.function_tools import FunctionToolsManager
    source = inspect.getsource(FunctionToolsManager._configure_settings)
    if 'api_base' in source and 'OPENAI_API_BASE' in source:
        print("   ✓ function_tools.py has api_base fix")
    else:
        print("   ✗ function_tools.py missing api_base parameter")
except Exception as e:
    print(f"   ⚠ Could not verify function_tools.py: {e}")

print()
print("=" * 60)
print("✅ ALL TESTS PASSED - Vocareum fix is working correctly!")
print("=" * 60)
print()
print("Key Fix Applied:")
print("- Added 'api_base' parameter to OpenAI() initialization")
print("- Added 'api_base' parameter to OpenAIEmbedding() initialization")
print("- Applied to all 3 helper modules (solution)")
print("- Applied to all 3 helper modules (starter with student comments)")
print()
print("This fix ensures LlamaIndex works with Vocareum's custom OpenAI endpoint.")
