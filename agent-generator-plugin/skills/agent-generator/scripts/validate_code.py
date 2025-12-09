#!/usr/bin/env python3
"""
Code Validator - AST-based security and syntax validation for generated agents.

Ensures generated code is:
- Syntactically correct
- Free of dangerous patterns (eval, exec, etc.)
- Uses only allowed imports
"""

import ast
import sys
from typing import Tuple, List
from dataclasses import dataclass

@dataclass
class ValidationResult:
    """Result of code validation."""
    valid: bool
    errors: List[str]
    warnings: List[str]
    imports_found: List[str]

class SecurityValidator(ast.NodeVisitor):
    """Validates code for security issues."""
    
    # Forbidden function calls at module level
    FORBIDDEN_CALLS = {
        'eval', 'exec', 'compile', '__import__',
        'open', 'file', 'input', 'raw_input',
        'system', 'popen', 'subprocess',
    }
    
    # Allowed import modules (packages)
    ALLOWED_IMPORTS = {
        'langgraph', 'langchain', 'langchain_core', 'langchain_community',
        'pydantic', 'deepagents',
        'json', 'os', 'sys', 'asyncio', 'logging', 'typing',
        'datetime', 'dataclasses', 'functools', 'itertools',
        'pathlib', 'tempfile', 'shutil',
        'requests', 'aiohttp', 'redis',
        'tenacity', 'dotenv',
    }
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.imports = []
        self.in_function_def = False
        self.depth = 0
    
    def visit_Call(self, node: ast.Call):
        """Check function calls."""
        if isinstance(node.func, ast.Name):
            # Only block bare function calls (not methods)
            if node.func.id in self.FORBIDDEN_CALLS:
                self.errors.append(
                    f"Line {node.lineno}: Forbidden function call: {node.func.id}"
                )
        # Note: Don't block method calls (e.g., agent.compile()) - these are safe
        
        self.generic_visit(node)
    
    def visit_Import(self, node: ast.Import):
        """Check import statements."""
        for alias in node.names:
            module = alias.name.split('.')[0]
            self.imports.append(alias.name)
            
            if module not in self.ALLOWED_IMPORTS:
                self.errors.append(
                    f"Line {node.lineno}: Unauthorized import: {alias.name}"
                )
        
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Check from...import statements."""
        if node.module:
            module = node.module.split('.')[0]
            self.imports.append(node.module)
            
            if module not in self.ALLOWED_IMPORTS:
                self.errors.append(
                    f"Line {node.lineno}: Unauthorized import from: {node.module}"
                )
        
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Track function definitions."""
        old_in_func = self.in_function_def
        self.in_function_def = True
        
        self.generic_visit(node)
        
        self.in_function_def = old_in_func
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Track async function definitions."""
        self.visit_FunctionDef(node)

def validate_python_code(code: str) -> ValidationResult:
    """
    Validate Python code for security and correctness.
    
    Returns:
        ValidationResult with validation status, errors, warnings, and imports
    """
    errors = []
    warnings = []
    imports = []
    
    # 1. Syntax validation
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return ValidationResult(
            valid=False,
            errors=[f"Syntax error at line {e.lineno}: {e.msg}"],
            warnings=[],
            imports_found=[]
        )
    
    # 2. Security validation
    validator = SecurityValidator()
    validator.visit(tree)
    
    errors.extend(validator.errors)
    warnings.extend(validator.warnings)
    imports = validator.imports
    
    # 3. Code quality checks
    lines = code.split("\n")
    
    # Check for hardcoded API keys
    for i, line in enumerate(lines, 1):
        if any(key in line for key in ['api_key = "', 'token = "', 'password = "']):
            if not any(substring in line for substring in ['os.getenv', 'environ.get']):
                warnings.append(
                    f"Line {i}: Potential hardcoded secret detected. Use os.getenv() instead."
                )
    
    # Check for print instead of logging
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('print(') and not any(
            exclude in line for exclude in ['logging', '__name__', 'argparse']
        ):
            warnings.append(
                f"Line {i}: Use logging instead of print() for production code"
            )
    
    # Check imports are present
    if not imports:
        warnings.append("No imports detected - code may be incomplete")
    
    # Final status
    valid = len(errors) == 0
    
    return ValidationResult(
        valid=valid,
        errors=errors,
        warnings=warnings,
        imports_found=imports
    )

def format_validation_report(result: ValidationResult) -> str:
    """Format validation result as readable report."""
    lines = []
    
    if result.valid:
        lines.append("✓ Code validation PASSED")
    else:
        lines.append("✗ Code validation FAILED")
    
    if result.errors:
        lines.append("\nERRORS:")
        for error in result.errors:
            lines.append(f"  • {error}")
    
    if result.warnings:
        lines.append("\nWARNINGS:")
        for warning in result.warnings:
            lines.append(f"  ⚠ {warning}")
    
    if result.imports_found:
        lines.append(f"\nImports found: {', '.join(set(result.imports_found))}")
    
    return "\n".join(lines)

if __name__ == "__main__":
    # Test with sample code
    test_code = """
import os
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

api_key = os.getenv("API_KEY")

def safe_tool(query: str) -> str:
    return "result"

agent = create_react_agent(
    model="gpt-4",
    tools=[safe_tool],
    prompt="test"
)
"""
    
    result = validate_python_code(test_code)
    print(format_validation_report(result))
    
    # Test with bad code
    print("\n" + "="*50 + "\n")
    
    bad_code = """
import os
eval("malicious_code()")
api_key = "hardcoded_secret_here"
"""
    
    result = validate_python_code(bad_code)
    print(format_validation_report(result))
