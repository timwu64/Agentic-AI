"""
Test Function Tools Module - Educational Testing Framework

This test file helps you verify your FunctionToolsManager implementation step by step.
Run this file to check your progress and get helpful debugging hints.

Usage: python tests/test_function_tools.py

The tests are designed to:
1. Check each function tool individually
2. Provide specific error messages and hints
3. Help you understand what went wrong and how to fix it
4. Build confidence as you progress through the implementation

Test Categories:
- Configuration Tests: Verify LLM setup and database connection
- Database Tool Tests: Check SQL generation and execution
- Market Data Tool Tests: Verify API integration and data fetching
- PII Protection Tool Tests: Check privacy protection functionality
- Integration Tests: End-to-end tool functionality verification
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

try:
    from helper_modules.function_tools import FunctionToolsManager
    from llama_index.core import Settings
    from llama_index.llms.openai import OpenAI
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.core.tools import FunctionTool
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Hint: Make sure you're running this from the starter_code directory")
    print("💡 Hint: Check that all required packages are installed: pip install -r requirements.txt")
    sys.exit(1)


class FunctionToolsTest:
    """Educational test framework for FunctionToolsManager"""

    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.verbose = True

    def print_test_header(self, test_name: str):
        """Print a formatted test header"""
        print(f"\n{'='*60}")
        print(f"🧪 Testing: {test_name}")
        print(f"{'='*60}")

    def print_success(self, message: str):
        """Print a success message"""
        print(f"✅ {message}")
        self.tests_passed += 1

    def print_failure(self, message: str, hint: str = None):
        """Print a failure message with optional hint"""
        print(f"❌ {message}")
        if hint:
            print(f"💡 Hint: {hint}")
        self.tests_failed += 1

    def print_summary(self):
        """Print test summary"""
        total = self.tests_passed + self.tests_failed
        print(f"\n{'='*60}")
        print("📊 Test Summary")
        print(f"{'='*60}")
        print(f"✅ Passed: {self.tests_passed}/{total}")
        print(f"❌ Failed: {self.tests_failed}/{total}")

        if self.tests_failed == 0:
            print("\n🎉 Congratulations! All tests passed!")
            print("🎯 Your FunctionToolsManager implementation is working correctly!")
            print("🚀 You're ready to move on to agent_coordinator.py")
        else:
            print("\n🔧 Keep working! Fix the failing tests and run again.")
            print("📚 Read the hints carefully - they'll guide you to the solution.")

    def test_environment_setup(self):
        """Test if environment is properly configured"""
        self.print_test_header("Environment Setup")

        # Check OpenAI API key
        if not os.getenv("OPENAI_API_KEY"):
            self.print_failure(
                "OpenAI API key not found",
                "Set OPENAI_API_KEY in your .env file or environment variables",
            )
            return False
        self.print_success("OpenAI API key configured")

        # Check database file
        db_path = project_root / "data" / "financial.db"
        if not db_path.exists():
            self.print_failure(
                "Database file not found",
                "Make sure financial.db exists in the data directory. Run build_database.py first.",
            )
            return False
        self.print_success("Database file found")

        return True

    def test_initialization(self):
        """Test FunctionToolsManager initialization"""
        self.print_test_header("FunctionToolsManager Initialization")

        try:
            manager = FunctionToolsManager(verbose=False)
            self.print_success("FunctionToolsManager created successfully")

            # Check database path
            if hasattr(manager, "db_path") and manager.db_path.exists():
                self.print_success("Database path properly set")
            else:
                self.print_failure(
                    "Database path not properly configured",
                    "Make sure self.db_path points to the financial.db file",
                )

            # Check schema
            if hasattr(manager, "db_schema") and len(manager.db_schema) > 100:
                self.print_success("Database schema loaded")
            else:
                self.print_failure(
                    "Database schema not properly loaded",
                    "Check that _get_database_schema() returns detailed schema information",
                )

            # Check function_tools list
            if hasattr(manager, "function_tools") and isinstance(manager.function_tools, list):
                self.print_success("Function tools list initialized")
            else:
                self.print_failure(
                    "Function tools list not properly initialized",
                    "Make sure self.function_tools = [] in __init__",
                )

            return manager

        except Exception as e:
            self.print_failure(
                f"Failed to create FunctionToolsManager: {e}",
                "Check your __init__ method implementation",
            )
            return None

    def test_configuration(self, manager):
        """Test LlamaIndex settings configuration"""
        self.print_test_header("LlamaIndex Configuration")

        if manager is None:
            self.print_failure("Cannot test configuration - manager not created", "Fix initialization first")
            return False

        # Check if LLM is configured
        if hasattr(manager, "llm") and manager.llm is not None:
            if isinstance(manager.llm, OpenAI):
                self.print_success("OpenAI LLM configured correctly")
            else:
                self.print_failure(
                    f"LLM is not OpenAI type. Got: {type(manager.llm)}",
                    "Use self.llm = OpenAI(model='gpt-3.5-turbo', temperature=0)",
                )
        else:
            self.print_failure(
                "self.llm not configured",
                "Implement _configure_settings() method to set self.llm",
            )

        # Check Settings configuration
        if hasattr(Settings, "llm") and Settings.llm is not None:
            self.print_success("Settings.llm configured")
        else:
            self.print_failure(
                "Settings.llm not configured",
                "Set Settings.llm = self.llm in _configure_settings()",
            )

        return True

    def test_create_function_tools(self, manager):
        """Test function tools creation"""
        self.print_test_header("Creating Function Tools")

        if manager is None:
            self.print_failure("Cannot test tool creation - manager not created", "Fix initialization first")
            return None

        try:
            tools = manager.create_function_tools()

            if tools is None:
                self.print_failure(
                    "create_function_tools() returned None",
                    "Make sure to return self.function_tools at the end of the method",
                )
                return None

            if not isinstance(tools, list):
                self.print_failure(
                    f"create_function_tools() should return a list, got: {type(tools)}",
                    "Return self.function_tools which should be a list",
                )
                return None

            expected_count = 3
            if len(tools) == expected_count:
                self.print_success(f"Created {expected_count} function tools")
            else:
                self.print_failure(
                    f"Expected {expected_count} tools, got {len(tools)}",
                    "Make sure all 3 tools are created: database_query_tool, finance_market_search_tool, pii_protection_tool",
                )

            for i, tool in enumerate(tools):
                if isinstance(tool, FunctionTool):
                    self.print_success(f"Tool {i+1} is correct FunctionTool type")
                else:
                    self.print_failure(
                        f"Tool {i+1} is not a FunctionTool, got: {type(tool)}",
                        "Use FunctionTool.from_defaults() to create tools",
                    )

            expected_names = ["database_query_tool", "finance_market_search_tool", "pii_protection_tool"]
            actual_names = [tool.metadata.name for tool in tools if hasattr(tool, "metadata")]

            for expected_name in expected_names:
                if expected_name in actual_names:
                    self.print_success(f"Found tool: {expected_name}")
                else:
                    self.print_failure(
                        f"Missing tool: {expected_name}",
                        f"Make sure to create FunctionTool with name='{expected_name}'",
                    )

            for tool in tools:
                if hasattr(tool, "metadata") and hasattr(tool.metadata, "description"):
                    if len(tool.metadata.description) > 30:
                        self.print_success(f"Tool {tool.metadata.name} has proper description")
                    else:
                        self.print_failure(
                            f"Tool {tool.metadata.name} has insufficient description",
                            "Provide a detailed description explaining what the tool does",
                        )
                else:
                    self.print_failure(
                        "Tool missing metadata or description",
                        "Make sure FunctionTool.from_defaults() includes name and description",
                    )

            return tools

        except Exception as e:
            self.print_failure(
                f"Error creating function tools: {e}",
                "Check your create_function_tools() implementation. Make sure all YOUR CODE HERE sections are completed.",
            )
            return None

    def test_database_tool_basic(self, tools):
        """Test basic database tool functionality"""
        self.print_test_header("Database Tool Basic Functionality")

        if not tools:
            self.print_failure("No tools available for testing", "Fix tool creation first")
            return False

        db_tool = next((t for t in tools if hasattr(t, "metadata") and t.metadata.name == "database_query_tool"), None)
        if db_tool is None:
            self.print_failure("Database tool not found", "Make sure database_query_tool has the correct name")
            return False

        try:
            result = db_tool.call("Show me all customers")

            if "not implemented" in result.lower():
                self.print_failure("Database tool not implemented yet", "Complete database_query_tool implementation")
            elif "error" in result.lower():
                self.print_failure(
                    f"Database tool returned error: {result[:120]}...",
                    "Check your SQL generation and DB execution",
                )
            else:
                self.print_success("Database tool executed without errors")

        except Exception as e:
            self.print_failure(
                f"Error calling database tool: {e}",
                "Check that database_query_tool function is callable and returns a string",
            )

        return True

    def test_market_tool_basic(self, tools):
        """Test basic market data tool functionality"""
        self.print_test_header("Market Data Tool Basic Functionality")

        if not tools:
            self.print_failure("No tools available for testing", "Fix tool creation first")
            return False

        market_tool = next(
            (t for t in tools if hasattr(t, "metadata") and t.metadata.name == "finance_market_search_tool"),
            None,
        )
        if market_tool is None:
            self.print_failure("Market tool not found", "Make sure finance_market_search_tool has the correct name")
            return False

        try:
            result = market_tool.call("What is Apple's stock price?")

            if "not implemented" in result.lower():
                self.print_failure("Market tool not implemented yet", "Complete finance_market_search_tool implementation")
            elif "error" in result.lower() and "not implemented" not in result.lower():
                self.print_failure(
                    f"Market tool returned error: {result[:120]}...",
                    "Check Yahoo Finance API integration and error handling",
                )
            else:
                self.print_success("Market tool executed without errors")

        except Exception as e:
            self.print_failure(
                f"Error calling market tool: {e}",
                "Check that finance_market_search_tool function is callable and returns a string",
            )

        return True

    def test_pii_tool_basic(self, tools):
        """Test basic PII protection tool functionality"""
        self.print_test_header("PII Protection Tool Basic Functionality")

        if not tools:
            self.print_failure("No tools available for testing", "Fix tool creation first")
            return False

        pii_tool = next((t for t in tools if hasattr(t, "metadata") and t.metadata.name == "pii_protection_tool"), None)
        if pii_tool is None:
            self.print_failure("PII tool not found", "Make sure pii_protection_tool has the correct name")
            return False

        try:
            test_data = "Customer: John Doe, Email: john@example.com"
            # FunctionTool.call passes args positionally; keep 2 args here
            result = pii_tool.call(test_data, "['name', 'email']")

            if result == test_data:
                self.print_failure(
                    "PII tool returned unchanged data",
                    "Implement PII masking logic inside pii_protection_tool",
                )
            else:
                self.print_success("PII tool modified the input data (masking applied)")

        except Exception as e:
            self.print_failure(
                f"Error calling PII tool: {e}",
                "Check that pii_protection_tool signature matches (database_results, column_names)",
            )

        return True

    def test_get_tools_method(self, manager):
        """Test the get_tools method"""
        self.print_test_header("Get Tools Method")

        if manager is None:
            self.print_failure("Cannot test get_tools - manager not created", "Fix initialization first")
            return False

        try:
            tools = manager.get_tools()
            if isinstance(tools, list):
                self.print_success("get_tools() returns a list")
            else:
                self.print_failure(
                    f"get_tools() should return a list, got: {type(tools)}",
                    "Return self.function_tools from get_tools() method",
                )
        except Exception as e:
            self.print_failure(
                f"Error calling get_tools(): {e}",
                "Make sure get_tools() method is implemented correctly",
            )

        return True

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting FunctionToolsManager Testing Framework")
        print("📋 This will test your implementation step by step")

        if not self.test_environment_setup():
            print("\n⚠️  Environment issues detected. Please fix before continuing.")
            self.print_summary()
            return

        manager = self.test_initialization()
        self.test_configuration(manager)

        tools = self.test_create_function_tools(manager)

        self.test_database_tool_basic(tools)
        self.test_market_tool_basic(tools)
        self.test_pii_tool_basic(tools)

        self.test_get_tools_method(manager)
        self.print_summary()


def main():
    tester = FunctionToolsTest()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
