# Advanced Tool Usage Examples

This document provides comprehensive examples of sophisticated tool-calling patterns and configurations for the Enhanced DeepAgent Generator.

## Example 1: Multi-Tool Research Agent

### Configuration
```yaml
name: "MultiToolResearchAgent"
description: "An advanced research agent that can search the web, analyze code, and generate comprehensive reports with multi-tool coordination"
reasoning_type: "plan-and-execute"
memory_type: "vector"
security_level: "high"
include_monitoring: true
tools:
  - browser_navigate
  - browser_snapshot
  - browser_evaluate
  - codebase_search
  - search_files
  - read_file
  - write_to_file
  - execute_command
```

### Generated Agent Features
- **Sophisticated Tool Selection**: Automatically selects tools based on research requirements
- **Tool Chaining**: Coordinates multiple tools in sequence (search → analyze → write)
- **Security Validation**: High security level with input sanitization and audit logging
- **Performance Monitoring**: Tracks tool usage and execution times
- **Error Recovery**: Automatic retry logic with exponential backoff

### Usage Example
```python
from agent import MultiToolResearchAgent

agent = MultiToolResearchAgent()

# Complex research task requiring multiple tools
result = agent.run("""
Research the latest LangChain features and create a comprehensive report.
1. Search for recent LangChain documentation and examples
2. Analyze code patterns and best practices  
3. Generate a detailed report with findings
""")

print(f"Research completed: {result['success']}")
print(f"Tools used: {result['tool_usage']}")
```

## Example 2: Secure Data Analysis Agent

### Configuration
```yaml
name: "SecureDataAnalyzer"
description: "A secure data analysis agent with controlled file access and audit logging for sensitive data processing"
reasoning_type: "react"
memory_type: "buffer"
security_level: "maximum"
include_monitoring: true
tools:
  - read_file
  - search_files
  - execute_command
  - write_to_file
  - list_files
```

### Security Features
- **Path Validation**: Restricted file access with directory traversal prevention
- **Command Filtering**: Whitelisted commands only (ls, cat, grep, head, tail)
- **Audit Logging**: All operations logged to `agent_audit.log`
- **Input Sanitization**: Comprehensive input validation and sanitization
- **Sandboxing**: Maximum security with AppArmor integration (Docker mode)

### Usage Example
```python
from agent import SecureDataAnalyzer

agent = SecureDataAnalyzer()

# Secure data analysis with audit trail
result = agent.run("""
Analyze the CSV files in the ./data directory and generate a summary report.
Only access files in the allowed directories and log all operations.
""")

# Check audit log for security events
with open('agent_audit.log', 'r') as f:
    audit_entries = f.readlines()
    for entry in audit_entries:
        if "AUDIT:" in entry:
            print(f"Security event: {entry}")
```

## Example 3: Web Automation Agent

### Configuration
```yaml
name: "WebAutomationAgent"
description: "An autonomous web automation agent that can navigate websites, interact with elements, and extract information"
reasoning_type: "babyagi"
memory_type: "vector"
security_level: "medium"
include_monitoring: true
tools:
  - browser_navigate
  - browser_snapshot
  - browser_evaluate
  - browser_click
  - browser_type
  - search_files
  - write_to_file
```

### Autonomous Features
- **Goal-Oriented**: BabyAGI pattern for autonomous task generation and execution
- **Web Interaction**: Full browser automation capabilities
- **Content Extraction**: JavaScript evaluation for dynamic content
- **State Management**: Vector memory for maintaining context across sessions
- **Self-Improvement**: Learns from previous interactions

### Usage Example
```python
from agent import WebAutomationAgent

agent = WebAutomationAgent()

# Autonomous web research task
result = agent.run("""
Research and compare pricing for cloud hosting providers.
Navigate to provider websites, extract pricing information, 
and create a comparison report.
""")

# Agent will automatically:
# 1. Plan the research strategy
# 2. Navigate to multiple provider websites
# 3. Extract pricing data using browser tools
# 4. Generate and save comparison report
```

## Example 4: Code Analysis and Refactoring Agent

### Configuration
```yaml
name: "CodeRefactoringAgent"
description: "An intelligent code analysis agent that can search codebases, identify patterns, and suggest refactoring"
reasoning_type: "plan-and-execute"
memory_type: "vector"
security_level: "high"
include_monitoring: true
tools:
  - codebase_search
  - search_files
  - list_code_definition_names
  - read_file
  - apply_diff
  - write_to_file
  - execute_command
```

### Analysis Capabilities
- **Semantic Search**: Understands code structure and patterns
- **Definition Extraction**: Identifies classes, functions, and interfaces
- **Pattern Recognition**: Finds code smells and anti-patterns
- **Automated Refactoring**: Suggests and applies code improvements
- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, C++

### Usage Example
```python
from agent import CodeRefactoringAgent

agent = CodeRefactoringAgent()

# Complex code analysis and refactoring task
result = agent.run("""
Analyze the codebase in ./src for code quality issues:
1. Find functions with high complexity
2. Identify duplicate code patterns
3. Suggest refactoring improvements
4. Apply safe refactoring to 3 most critical issues
""")

print(f"Analysis complete. Check the generated refactoring report.")
```

## Example 5: Multi-Agent Coordination System

### Configuration
```yaml
name: "CoordinatorAgent"
description: "A coordination agent that manages multiple specialized agents for complex workflows"
reasoning_type: "plan-and-execute"
memory_type: "vector"
security_level: "high"
include_monitoring: true
tools:
  - use_mcp_tool
  - execute_command
  - write_to_file
  - search_files
```

### Coordination Features
- **MCP Integration**: Uses MCP servers for specialized tools
- **Workflow Orchestration**: Coordinates multiple agents and tools
- **Result Aggregation**: Combines outputs from different agents
- **Error Propagation**: Handles failures across the agent network
- **Performance Tracking**: Monitors entire workflow execution

### Usage Example
```python
from agent import CoordinatorAgent

coordinator = CoordinatorAgent()

# Multi-agent workflow coordination
result = coordinator.run("""
Coordinate a complex data processing workflow:
1. Use data extraction agent to gather information
2. Use analysis agent to process the data
3. Use reporting agent to generate insights
4. Save final report and notify stakeholders
""")

# Coordinator manages the entire workflow across multiple agents
print(f"Workflow completed with {len(result['tool_usage'])} tool executions")
```

## Tool Performance Benchmarking

### Benchmarking Script
```python
#!/usr/bin/env python3
"""
Tool Performance Benchmarking for Enhanced DeepAgent
"""

import time
import json
from typing import Dict, Any
from tools import get_available_tools, performance_monitor

def benchmark_tool_performance():
    """Benchmark all available tools"""
    tools = get_available_tools()
    benchmark_results = {}
    
    print(f"Starting performance benchmark for {len(tools)} tools...")
    
    for tool in tools:
        print(f"Benchmarking {tool.name}...")
        
        # Warm-up runs
        for _ in range(3):
            try:
                tool._run(test_input="benchmark")
            except:
                pass
        
        # Benchmark runs
        execution_times = []
        success_count = 0
        
        for i in range(10):
            start_time = time.time()
            try:
                result = tool._run(test_input=f"benchmark_run_{i}")
                execution_time = time.time() - start_time
                execution_times.append(execution_time)
                success_count += 1
            except Exception as e:
                execution_time = time.time() - start_time
                execution_times.append(execution_time)
                print(f"  Error: {e}")
        
        # Calculate statistics
        if execution_times:
            avg_time = sum(execution_times) / len(execution_times)
            min_time = min(execution_times)
            max_time = max(execution_times)
            success_rate = success_count / len(execution_times)
            
            benchmark_results[tool.name] = {
                "average_time": avg_time,
                "min_time": min_time,
                "max_time": max_time,
                "success_rate": success_rate,
                "total_runs": len(execution_times)
            }
            
            print(f"  Average time: {avg_time:.3f}s")
            print(f"  Success rate: {success_rate:.1%}")
    
    # Save results
    with open('benchmark_results.json', 'w') as f:
        json.dump(benchmark_results, f, indent=2)
    
    print(f"Benchmark complete. Results saved to benchmark_results.json")
    return benchmark_results

def analyze_performance_bottlenecks():
    """Analyze performance bottlenecks from monitoring data"""
    stats = performance_monitor.get_stats()
    
    print("Performance Analysis:")
    print("=" * 50)
    
    slow_tools = []
    failing_tools = []
    
    for tool_name, tool_stats in stats.items():
        if tool_stats["average_time"] > 5.0:  # Tools slower than 5 seconds
            slow_tools.append((tool_name, tool_stats["average_time"]))
        
        if tool_stats["failure_rate"] > 0.1:  # Tools with >10% failure rate
            failing_tools.append((tool_name, tool_stats["failure_rate"]))
    
    if slow_tools:
        print("\nSlow Tools ( > 5s average):")
        for tool, avg_time in sorted(slow_tools, key=lambda x: x[1], reverse=True):
            print(f"  - {tool}: {avg_time:.2f}s average")
    
    if failing_tools:
        print("\nHigh Failure Rate Tools (> 10%):")
        for tool, failure_rate in sorted(failing_tools, key=lambda x: x[1], reverse=True):
            print(f"  - {tool}: {failure_rate:.1%} failure rate")
    
    return {
        "slow_tools": slow_tools,
        "failing_tools": failing_tools,
        "all_stats": stats
    }

if __name__ == "__main__":
    # Run benchmarks
    benchmark_results = benchmark_tool_performance()
    
    # Analyze performance
    analysis = analyze_performance_bottlenecks()
    
    # Print recommendations
    print("\nPerformance Recommendations:")
    print("=" * 50)
    
    if analysis["slow_tools"]:
        print("- Consider increasing timeout for slow tools")
        print("- Implement caching for frequently used tools")
        print("- Optimize tool implementations")
    
    if analysis["failing_tools"]:
        print("- Review error handling in failing tools")
        print("- Add retry logic with exponential backoff")
        print("- Validate inputs before tool execution")
```

## Error Handling Demonstrations

### Error Recovery Example
```python
from agent import EnhancedResearchAgent
import logging

# Configure detailed logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def demonstrate_error_handling():
    """Demonstrate comprehensive error handling"""
    
    agent = EnhancedResearchAgent()
    
    print("1. Testing network error recovery...")
    try:
        # Simulate network timeout
        result = agent.run("Search for information on a website that times out")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Handled error: {e}")
    
    print("\n2. Testing file access errors...")
    try:
        # Try to access non-existent file
        result = agent.run("Read the file /nonexistent/path/file.txt")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Handled error: {e}")
    
    print("\n3. Testing security policy violations...")
    try:
        # Try dangerous command
        result = agent.run("Execute command: rm -rf /")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Handled error: {e}")
    
    print("\n4. Testing tool retry logic...")
    # This will demonstrate automatic retry on transient failures
    result = agent.run("""
    Search for files with a pattern that might fail initially,
    but should succeed on retry.
    """)
    print(f"Retry result: {result['success']}")

if __name__ == "__main__":
    demonstrate_error_handling()
```

## Security Configuration Examples

### Maximum Security Configuration
```json
{
  "security_level": "maximum",
  "audit_logging": {
    "enabled": true,
    "log_file": "agent_audit.log",
    "log_sensitive_operations": true,
    "log_level": "INFO"
  },
  "input_validation": {
    "enabled": true,
    "max_input_length": 5000,
    "sanitize_user_input": true,
    "blocked_patterns": [
      "rm\\s+-rf",
      "dd\\s+if=",
      "eval\\(",
      "exec\\("
    ]
  },
  "tool_execution": {
    "timeout_default": 30,
    "enable_retry_logic": true,
    "max_retry_attempts": 3,
    "enable_sandboxing": true,
    "allowed_commands": [
      "ls",
      "echo",
      "cat",
      "grep",
      "head",
      "tail"
    ],
    "blocked_domains": [
      "localhost",
      "127.0.0.1",
      "internal"
    ]
  },
  "file_access": {
    "allowed_directories": [
      "./workspace",
      "./data",
      "./output"
    ],
    "blocked_paths": [
      "/etc/",
      "/proc/",
      "/sys/",
      "/root/"
    ],
    "allowed_extensions": [
      ".py",
      ".md",
      ".txt",
      ".json",
      ".csv"
    ]
  }
}
```

## Monitoring and Observability

### LangSmith Integration
```python
from agent import EnhancedAgent
from langsmith import Client

# Enable LangSmith monitoring
agent = EnhancedAgent()
agent.monitoring_enabled = True

# Configure LangSmith client
agent.monitoring_client = Client()

# All tool executions will be tracked
result = agent.run("Complex task with multiple tools")

# View traces in LangSmith dashboard
print("Check LangSmith dashboard for detailed execution traces")
```

### Custom Monitoring
```python
from tools import performance_monitor

def custom_monitoring_example():
    """Example of custom monitoring integration"""
    
    # Get performance stats
    stats = performance_monitor.get_stats()
    
    # Export metrics to Prometheus
    for tool_name, tool_stats in stats.items():
        print(f"Exporting metrics for {tool_name}:")
        print(f"  - calls_total: {tool_stats['total_calls']}")
        print(f"  - execution_time_average: {tool_stats['average_time']}")
        print(f"  - failure_rate: {tool_stats['failure_rate']}")
    
    # Alert on high failure rates
    for tool_name, tool_stats in stats.items():
        if tool_stats['failure_rate'] > 0.2:  # 20% failure rate
            print(f"ALERT: {tool_name} has high failure rate: {tool_stats['failure_rate']:.1%}")
```

These examples demonstrate the sophisticated tool-calling capabilities of the Enhanced DeepAgent Generator, including security, monitoring, performance optimization, and multi-tool coordination features.