#!/usr/bin/env python3
"""
Multi-Tool Coordination Examples

This script demonstrates how multiple tools work together in complex workflows,
showing coordination patterns and data flow between tools.

Examples include:
1. Web research and code analysis pipeline
2. Data extraction, analysis, and reporting workflow
3. File processing and validation chain
4. Error recovery and fallback patterns
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.generate_agent_enhanced import EnhancedDeepAgentGenerator


class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class ToolResult:
    """Result from tool execution"""
    tool_name: str
    success: bool
    data: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    retry_count: int = 0


class MultiToolWorkflow:
    """Orchestrates multiple tools in complex workflows"""
    
    def __init__(self, agent_config: Dict[str, Any]):
        self.config = agent_config
        self.workflow_steps = []
        self.results = []
        self.generator = EnhancedDeepAgentGenerator()
        
    def add_step(self, tool_name: str, params: Dict[str, Any], 
                 fallback_tool: Optional[str] = None,
                 retry_on_failure: bool = True,
                 max_retries: int = 3):
        """Add a workflow step"""
        self.workflow_steps.append({
            'tool_name': tool_name,
            'params': params,
            'fallback_tool': fallback_tool,
            'retry_on_failure': retry_on_failure,
            'max_retries': max_retries,
            'status': WorkflowStatus.PENDING
        })
    
    def execute_step(self, step: Dict[str, Any]) -> ToolResult:
        """Execute a single workflow step"""
        tool_name = step['tool_name']
        params = step['params']
        
        print(f"  → Executing {tool_name}...")
        start_time = time.time()
        
        try:
            # Simulate tool execution (in real implementation, this would call actual tools)
            result = self._simulate_tool_execution(tool_name, params)
            
            execution_time = time.time() - start_time
            
            return ToolResult(
                tool_name=tool_name,
                success=True,
                data=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            return ToolResult(
                tool_name=tool_name,
                success=False,
                data=None,
                error=str(e),
                execution_time=execution_time
            )
    
    def _simulate_tool_execution(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """Simulate tool execution for demonstration"""
        # This would be replaced with actual tool calls in production
        
        simulation_results = {
            'search_files': {
                'files': ['src/main.py', 'src/utils.py', 'tests/test_main.py'],
                'count': 3,
                'pattern': params.get('regex', '.*')
            },
            'read_file': {
                'content': 'def main():\n    print("Hello World")\n\nif __name__ == "__main__":\n    main()',
                'lines': 5,
                'encoding': 'utf-8'
            },
            'codebase_search': {
                'matches': [
                    {'file': 'src/main.py', 'line': 10, 'content': 'class DataProcessor:'},
                    {'file': 'src/utils.py', 'line': 25, 'content': 'def process_data(data):'}
                ],
                'total_matches': 2
            },
            'browser_navigate': {
                'url': params.get('url', 'https://example.com'),
                'status': 200,
                'title': 'Example Domain',
                'content_length': 1256
            },
            'browser_snapshot': {
                'elements': 45,
                'forms': 2,
                'links': 15,
                'title': 'Example Domain'
            },
            'data_analysis': {
                'mean': 42.5,
                'median': 40.0,
                'std_dev': 12.3,
                'sample_size': 100
            },
            'write_to_file': {
                'success': True,
                'path': params.get('path', 'output.txt'),
                'bytes_written': len(params.get('content', ''))
            },
            'execute_command': {
                'command': params.get('command', ''),
                'return_code': 0,
                'stdout': 'Command executed successfully',
                'stderr': ''
            }
        }
        
        return simulation_results.get(tool_name, {'status': 'simulated', 'tool': tool_name})
    
    def execute_workflow(self) -> List[ToolResult]:
        """Execute the complete workflow"""
        print(f"\n🚀 Starting workflow with {len(self.workflow_steps)} steps...")
        
        for i, step in enumerate(self.workflow_steps, 1):
            print(f"\n📋 Step {i}/{len(self.workflow_steps)}: {step['tool_name']}")
            
            retry_count = 0
            max_retries = step['max_retries']
            
            while retry_count <= max_retries:
                result = self.execute_step(step)
                result.retry_count = retry_count
                
                if result.success:
                    print(f"  ✅ Success ({result.execution_time:.2f}s)")
                    self.results.append(result)
                    break
                else:
                    retry_count += 1
                    
                    if retry_count <= max_retries and step['retry_on_failure']:
                        print(f"  ⚠️  Failed (attempt {retry_count}/{max_retries}): {result.error}")
                        time.sleep(2  ** retry_count)  # Exponential backoff
                    else:
                        # Try fallback tool if available
                        if step['fallback_tool']:
                            print(f"  🔄 Trying fallback: {step['fallback_tool']}")
                            fallback_step = step.copy()
                            fallback_step['tool_name'] = step['fallback_tool']
                            fallback_result = self.execute_step(fallback_step)
                            
                            if fallback_result.success:
                                print(f"  ✅ Fallback succeeded ({fallback_result.execution_time:.2f}s)")
                                self.results.append(fallback_result)
                                break
                        
                        print(f"  ❌ Failed after {retry_count} attempts: {result.error}")
                        self.results.append(result)
                        break
        
        print(f"\n📊 Workflow completed: {sum(1 for r in self.results if r.success)}/{len(self.results)} steps successful")
        return self.results
    
    def get_workflow_report(self) -> Dict[str, Any]:
        """Generate comprehensive workflow report"""
        successful = sum(1 for r in self.results if r.success)
        total = len(self.results)
        
        return {
            'workflow_name': self.config.get('name', 'Unnamed Workflow'),
            'total_steps': total,
            'successful_steps': successful,
            'failed_steps': total - successful,
            'success_rate': successful / total if total > 0 else 0,
            'total_execution_time': sum(r.execution_time for r in self.results),
            'average_execution_time': sum(r.execution_time for r in self.results) / total if total > 0 else 0,
            'steps': [
                {
                    'tool_name': r.tool_name,
                    'success': r.success,
                    'execution_time': r.execution_time,
                    'retry_count': r.retry_count,
                    'error': r.error
                }
                for r in self.results
            ]
        }


def example_web_research_pipeline():
    """
    Example 1: Web research and code analysis pipeline
    
    Workflow:
    1. Navigate to documentation website
    2. Extract page content
    3. Search for code examples in repository
    4. Analyze and compare implementations
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Web Research & Code Analysis Pipeline")
    print("="*60)
    
    # Configure agent
    config = {
        'name': 'WebResearchPipeline',
        'description': 'Research web documentation and analyze related code',
        'reasoning_type': 'plan-and-execute',
        'memory_type': 'buffer',
        'security_level': 'medium',
        'include_monitoring': True
    }
    
    # Create workflow
    workflow = MultiToolWorkflow(config)
    
    # Add workflow steps
    workflow.add_step(
        tool_name='browser_navigate',
        params={'url': 'https://docs.example.com/api'},
        retry_on_failure=True,
        max_retries=3
    )
    
    workflow.add_step(
        tool_name='browser_snapshot',
        params={'verbose': True},
        fallback_tool='browser_evaluate',
        retry_on_failure=True,
        max_retries=2
    )
    
    workflow.add_step(
        tool_name='search_files',
        params={
            'path': './src',
            'regex': 'def\\s+\\w+.*api',
            'file_pattern': '*.py'
        },
        retry_on_failure=True,
        max_retries=3
    )
    
    workflow.add_step(
        tool_name='read_file',
        params={'path': './src/api_client.py'},
        fallback_tool='codebase_search',
        retry_on_failure=True,
        max_retries=2
    )
    
    # Execute workflow
    results = workflow.execute_workflow()
    
    # Generate report
    report = workflow.get_workflow_report()
    print(f"\n📈 Workflow Report:")
    print(json.dumps(report, indent=2))
    
    return results, report


def example_data_analysis_workflow():
    """
    Example 2: Data extraction, analysis, and reporting workflow
    
    Workflow:
    1. Extract data from multiple files
    2. Perform statistical analysis
    3. Generate visualizations
    4. Create comprehensive report
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Data Analysis & Reporting Workflow")
    print("="*60)
    
    # Configure agent
    config = {
        'name': 'DataAnalysisWorkflow',
        'description': 'Extract data, analyze, and generate reports',
        'reasoning_type': 'react',
        'memory_type': 'vector',
        'security_level': 'high',
        'include_monitoring': True
    }
    
    # Create workflow
    workflow = MultiToolWorkflow(config)
    
    # Add workflow steps
    workflow.add_step(
        tool_name='search_files',
        params={
            'path': './data',
            'regex': '.*\\.(csv|json|xml)$',
            'file_pattern': '*.*'
        },
        retry_on_failure=True,
        max_retries=3
    )
    
    workflow.add_step(
        tool_name='read_file',
        params={'path': './data/sales_data.csv'},
        retry_on_failure=True,
        max_retries=2
    )
    
    workflow.add_step(
        tool_name='data_analysis',
        params={
            'data_source': 'sales_data.csv',
            'analysis_type': 'descriptive_statistics'
        },
        retry_on_failure=True,
        max_retries=3
    )
    
    workflow.add_step(
        tool_name='write_to_file',
        params={
            'path': './reports/analysis_report.md',
            'content': '# Data Analysis Report\n\n## Summary\nAnalysis completed successfully.\n\n## Key Findings\n- Average: 42.5\n- Median: 40.0\n- Std Dev: 12.3\n'
        },
        retry_on_failure=True,
        max_retries=2
    )
    
    # Execute workflow
    results = workflow.execute_workflow()
    
    # Generate report
    report = workflow.get_workflow_report()
    print(f"\n📈 Workflow Report:")
    print(json.dumps(report, indent=2))
    
    return results, report


def example_file_processing_chain():
    """
    Example 3: File processing and validation chain
    
    Workflow:
    1. List files in directory
    2. Validate file formats
    3. Process valid files
    4. Generate validation report
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: File Processing & Validation Chain")
    print("="*60)
    
    # Configure agent
    config = {
        'name': 'FileProcessingChain',
        'description': 'Process and validate files with error handling',
        'reasoning_type': 'plan-and-execute',
        'memory_type': 'buffer',
        'security_level': 'medium',
        'include_monitoring': True
    }
    
    # Create workflow
    workflow = MultiToolWorkflow(config)
    
    # Add workflow steps
    workflow.add_step(
        tool_name='list_files',
        params={
            'path': './documents',
            'recursive': True
        },
        retry_on_failure=True,
        max_retries=2
    )
    
    workflow.add_step(
        tool_name='search_files',
        params={
            'path': './documents',
            'regex': '\\.(pdf|docx|txt)$',
            'file_pattern': '*.*'
        },
        retry_on_failure=True,
        max_retries=3
    )
    
    # Simulate processing each file
    for i in range(3):
        workflow.add_step(
            tool_name='read_file',
            params={'path': f'./documents/file_{i}.txt'},
            fallback_tool='execute_command',
            retry_on_failure=True,
            max_retries=2
        )
    
    workflow.add_step(
        tool_name='write_to_file',
        params={
            'path': './reports/validation_report.json',
            'content': json.dumps({
                'processed_files': 3,
                'valid_files': 3,
                'errors': 0,
                'timestamp': time.time()
            }, indent=2)
        },
        retry_on_failure=True,
        max_retries=2
    )
    
    # Execute workflow
    results = workflow.execute_workflow()
    
    # Generate report
    report = workflow.get_workflow_report()
    print(f"\n📈 Workflow Report:")
    print(json.dumps(report, indent=2))
    
    return results, report


def example_error_recovery_patterns():
    """
    Example 4: Error recovery and fallback patterns
    
    Workflow:
    1. Attempt primary operation (may fail)
    2. Use fallback method on failure
    3. Implement retry with exponential backoff
    4. Log all errors for analysis
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Error Recovery & Fallback Patterns")
    print("="*60)
    
    # Configure agent
    config = {
        'name': 'ErrorRecoveryDemo',
        'description': 'Demonstrate error recovery and fallback mechanisms',
        'reasoning_type': 'react',
        'memory_type': 'buffer',
        'security_level': 'high',
        'include_monitoring': True
    }
    
    # Create workflow
    workflow = MultiToolWorkflow(config)
    
    # Step 1: Primary operation that might fail
    workflow.add_step(
        tool_name='browser_navigate',
        params={'url': 'https://unreliable-website.com'},
        fallback_tool='execute_command',
        retry_on_failure=True,
        max_retries=3
    )
    
    # Step 2: Fallback to API if web fails
    workflow.add_step(
        tool_name='execute_command',
        params={'command': 'curl -s https://api.example.com/data'},
        retry_on_failure=True,
        max_retries=2
    )
    
    # Step 3: Try multiple file access methods
    workflow.add_step(
        tool_name='read_file',
        params={'path': './nonexistent_file.txt'},
        fallback_tool='search_files',
        retry_on_failure=True,
        max_retries=2
    )
    
    # Step 4: Final fallback to generic search
    workflow.add_step(
        tool_name='search_files',
        params={
            'path': '.',
            'regex': 'backup.*\\.txt$'
        },
        retry_on_failure=False,  # No retry for final fallback
        max_retries=0
    )
    
    # Execute workflow
    results = workflow.execute_workflow()
    
    # Generate report
    report = workflow.get_workflow_report()
    print(f"\n📈 Workflow Report:")
    print(json.dumps(report, indent=2))
    
    # Show recovery statistics
    recoveries = sum(1 for r in results if r.retry_count > 0 and r.success)
    fallbacks_used = sum(1 for step, result in zip(workflow.workflow_steps, results) 
                        if step.get('fallback_tool') and result.success)
    
    print(f"\n🔄 Recovery Statistics:")
    print(f"  - Successful recoveries: {recoveries}")
    print(f"  - Fallbacks used: {fallbacks_used}")
    print(f"  - Total retries: {sum(r.retry_count for r in results)}")
    
    return results, report


def example_parallel_execution():
    """
    Example 5: Parallel tool execution
    
    Workflow:
    1. Execute multiple independent tools in parallel
    2. Aggregate results
    3. Process aggregated data
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Parallel Tool Execution")
    print("="*60)
    
    # Configure agent
    config = {
        'name': 'ParallelExecutionDemo',
        'description': 'Execute multiple tools in parallel and aggregate results',
        'reasoning_type': 'plan-and-execute',
        'memory_type': 'buffer',
        'security_level': 'medium',
        'include_monitoring': True
    }
    
    # Create workflow
    workflow = MultiToolWorkflow(config)
    
    # Add parallel execution steps (simulated)
    parallel_tools = [
        ('search_files', {'path': './src', 'regex': '.*\\.py$', 'file_pattern': '*.py'}),
        ('search_files', {'path': './tests', 'regex': '.*\\.py$', 'file_pattern': '*.py'}),
        ('search_files', {'path': './docs', 'regex': '.*\\.(md|txt)$', 'file_pattern': '*.*'})
    ]
    
    for tool_name, params in parallel_tools:
        workflow.add_step(
            tool_name=tool_name,
            params=params,
            retry_on_failure=True,
            max_retries=2
        )
    
    # Add aggregation step
    workflow.add_step(
        tool_name='write_to_file',
        params={
            'path': './reports/parallel_results.json',
            'content': json.dumps({
                'parallel_executions': len(parallel_tools),
                'total_files_found': 150,
                'execution_time': 3.2,
                'efficiency': '85%'
            }, indent=2)
        },
        retry_on_failure=True,
        max_retries=2
    )
    
    # Execute workflow
    results = workflow.execute_workflow()
    
    # Generate report
    report = workflow.get_workflow_report()
    print(f"\n📈 Workflow Report:")
    print(json.dumps(report, indent=2))
    
    # Show parallel execution benefits
    sequential_time = sum(r.execution_time for r in results)
    parallel_time = max(r.execution_time for r in results[:-1]) + results[-1].execution_time
    
    print(f"\n⚡ Parallel Execution Benefits:")
    print(f"  - Sequential time: {sequential_time:.2f}s")
    print(f"  - Parallel time: {parallel_time:.2f}s")
    print(f"  - Time saved: {sequential_time - parallel_time:.2f}s ({((sequential_time - parallel_time) / sequential_time * 100):.1f}%)")
    
    return results, report


def run_all_examples():
    """Run all multi-tool coordination examples"""
    print("\n" + "="*80)
    print("MULTI-TOOL COORDINATION EXAMPLES")
    print("="*80)
    
    examples = [
        example_web_research_pipeline,
        example_data_analysis_workflow,
        example_file_processing_chain,
        example_error_recovery_patterns,
        example_parallel_execution
    ]
    
    all_reports = []
    
    for example_func in examples:
        try:
            results, report = example_func()
            all_reports.append(report)
        except Exception as e:
            print(f"❌ Error running {example_func.__name__}: {e}")
    
    # Generate summary report
    print("\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80)
    
    total_workflows = len(all_reports)
    total_steps = sum(r['total_steps'] for r in all_reports)
    successful_steps = sum(r['successful_steps'] for r in all_reports)
    total_time = sum(r['total_execution_time'] for r in all_reports)
    
    print(f"📊 Summary Statistics:")
    print(f"  - Total workflows: {total_workflows}")
    print(f"  - Total steps: {total_steps}")
    print(f"  - Successful steps: {successful_steps}/{total_steps} ({successful_steps/total_steps*100:.1f}%)")
    print(f"  - Total execution time: {total_time:.2f}s")
    print(f"  - Average time per workflow: {total_time/total_workflows:.2f}s")
    
    # Save summary to file
    summary = {
        'timestamp': time.time(),
        'summary': {
            'total_workflows': total_workflows,
            'total_steps': total_steps,
            'successful_steps': successful_steps,
            'success_rate': successful_steps/total_steps if total_steps > 0 else 0,
            'total_execution_time': total_time,
            'average_time_per_workflow': total_time/total_workflows if total_workflows > 0 else 0
        },
        'workflows': all_reports
    }
    
    with open('reports/multi_tool_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Summary saved to: reports/multi_tool_summary.json")
    
    return all_reports


if __name__ == "__main__":
    # Create reports directory
    os.makedirs('reports', exist_ok=True)
    
    # Run all examples
    run_all_examples()
    
    print("\n✅ All multi-tool coordination examples completed!")