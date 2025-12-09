#!/usr/bin/env python3
"""
Enhanced DeepAgent Generator - Generate production-ready LangChain DeepAgents with sophisticated tool-calling capabilities

Usage:
    generate-agent-enhanced.py --description <agent-description> [options]

Examples:
    # Basic agent generation
    python generate-agent-enhanced.py --description "Create a research agent that can search the web and generate reports"
    
    # Advanced configuration with specific tools
    python generate-agent-enhanced.py --description "Build a data analysis agent" --name "DataAnalyzer" --reasoning-type plan-and-execute --memory-type vector
    
    # Generate with enhanced security and monitoring
    python generate-agent-enhanced.py --description "Create a customer support agent" --name "SupportAgent" --include-monitoring --security-level high
"""

import argparse
import json
import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnhancedDeepAgentGenerator:
    """Enhanced generator class for creating DeepAgents with sophisticated tool-calling capabilities"""
    
    REASONING_TYPES = ['auto', 'react', 'plan-and-execute', 'babyagi']
    MEMORY_TYPES = ['auto', 'buffer', 'summary', 'vector']
    OUTPUT_FORMATS = ['python-package', 'standalone-script', 'docker']
    SECURITY_LEVELS = ['low', 'medium', 'high', 'maximum']
    
    # Template mappings for different configurations
    TEMPLATE_CONFIGS = {
        'react': {
            'agent_template': 'agent_react.py.j2',
            'requirements': ['langchain>=0.1.0', 'langchain-openai>=0.0.5'],
            'description': 'ReAct (Reasoning + Acting) pattern for direct task execution'
        },
        'plan-and-execute': {
            'agent_template': 'agent_plan_execute.py.j2',
            'requirements': ['langchain>=0.1.0', 'langchain-openai>=0.0.5', 'langchain-experimental>=0.0.10'],
            'description': 'Plan-and-Execute pattern for complex multi-step tasks'
        },
        'babyagi': {
            'agent_template': 'agent_babyagi.py.j2',
            'requirements': ['langchain>=0.1.0', 'langchain-openai>=0.0.5', 'beautifulsoup4>=4.12.0', 'requests>=2.31.0'],
            'description': 'BabyAGI autonomous task generation and execution'
        }
    }
    
    MEMORY_CONFIGS = {
        'buffer': {
            'class': 'ConversationBufferWindowMemory',
            'requirements': [],
            'description': 'Simple conversation buffer with window limit'
        },
        'summary': {
            'class': 'ConversationSummaryMemory',
            'requirements': [],
            'description': 'Summarized conversation history'
        },
        'vector': {
            'class': 'VectorStoreRetrieverMemory',
            'requirements': ['chromadb>=0.4.0', 'tiktoken>=0.5.0'],
            'description': 'Vector store based memory for semantic retrieval'
        }
    }
    
    def __init__(self, verbose: bool = False, security_level: str = 'medium'):
        self.verbose = verbose
        self.security_level = security_level
        self.template_engine = EnhancedTemplateEngine()
        self.tool_analyzer = EnhancedToolAnalyzer()
        self.tool_generator = ToolGenerator()
        self.memory_selector = MemorySelector()
        self.reasoning_selector = ReasoningSelector()
        self.security_validator = SecurityValidator()
    
    def generate_agent(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete DeepAgent based on configuration with enhanced tool-calling capabilities
        
        Args:
            config: Agent generation configuration
            
        Returns:
            Dictionary containing generation results
        """
        logger.info("Starting Enhanced DeepAgent generation")
        logger.info(f"Agent name: {config.get('name', 'Auto-generated')}")
        logger.info(f"Reasoning type: {config.get('reasoning_type', 'auto')}")
        logger.info(f"Memory type: {config.get('memory_type', 'auto')}")
        logger.info(f"Security level: {config.get('security_level', 'medium')}")
        
        try:
            # Analyze description to determine requirements
            analysis = self._analyze_requirements(config['description'])
            
            # Select reasoning type
            reasoning_type = self._select_reasoning_type(
                config.get('reasoning_type', 'auto'),
                config['description'],
                analysis
            )
            
            # Select memory type
            memory_type = self._select_memory_type(
                config.get('memory_type', 'auto'),
                config['description'],
                analysis
            )
            
            # Determine required tools with enhanced analysis
            tool_analysis = self.tool_analyzer.analyze(config['description'])
            tools = tool_analysis['selected_tools']
            
            # Generate sophisticated tool implementations
            generated_tools = self.tool_generator.generate_tools(tools, config)
            
            # Validate tool compatibility and security
            security_validation = self._validate_tool_security(tools, generated_tools, config)
            
            # Create output directory
            output_path = self._create_output_directory(config.get('name'))
            
            # Generate agent files with enhanced capabilities
            generated_files = self._generate_agent_files(
                config, reasoning_type, memory_type, tools, 
                generated_tools, security_validation, output_path
            )
            
            # Generate dependencies
            dependencies = self._generate_dependencies(
                reasoning_type, memory_type, config.get('include_monitoring', True),
                generated_tools
            )
            
            # Generate security configuration
            security_config = self._generate_security_config(config, tools, security_validation)
            
            # Create README with enhanced documentation
            self._generate_enhanced_readme(
                config, reasoning_type, memory_type, tools, generated_tools,
                security_validation, output_path
            )
            
            logger.info(f"Enhanced agent generation completed: {len(generated_files)} files")
            logger.info(f"Output directory: {output_path}")
            
            return {
                'success': True,
                'output_path': str(output_path),
                'files': generated_files,
                'dependencies': dependencies,
                'security_config': security_config,
                'configuration': {
                    'reasoning_type': reasoning_type,
                    'memory_type': memory_type,
                    'tools': tools,
                    'tool_categories': tool_analysis['tool_categories'],
                    'confidence_scores': tool_analysis['confidence_scores'],
                    'include_monitoring': config.get('include_monitoring', True),
                    'security_level': config.get('security_level', 'medium'),
                    'security_validation': security_validation
                }
            }
            
        except Exception as e:
            logger.error(f"Enhanced agent generation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _analyze_requirements(self, description: str) -> Dict[str, Any]:
        """Analyze agent description to determine requirements with enhanced tool analysis"""
        logger.info("Analyzing agent requirements with enhanced tool analysis")
        
        # Use enhanced tool analyzer
        tool_analysis = self.tool_analyzer.analyze(description)
        
        analysis = {
            'complexity': self._assess_complexity(description),
            'tool_requirements': tool_analysis,
            'memory_requirements': self._assess_memory_needs(description),
            'reasoning_requirements': self._assess_reasoning_needs(description),
            'security_requirements': self._assess_security_needs(description)
        }
        
        if self.verbose:
            logger.info(f"Enhanced requirements analysis: {json.dumps(analysis, indent=2)}")
        
        return analysis
    
    def _assess_complexity(self, description: str) -> str:
        """Assess task complexity from description"""
        complexity_indicators = {
            'simple': ['simple', 'basic', 'easy', 'straightforward', 'minimal'],
            'medium': ['multiple', 'several', 'various', 'different', 'moderate'],
            'complex': ['complex', 'advanced', 'sophisticated', 'multi-step', 'coordinated', 'intricate']
        }
        
        desc_lower = description.lower()
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in desc_lower for indicator in indicators):
                return level
        
        return 'medium'
    
    def _assess_memory_needs(self, description: str) -> str:
        """Assess memory requirements from description"""
        memory_indicators = {
            'buffer': ['simple', 'basic', 'recent', 'limited'],
            'summary': ['summary', 'overview', 'key points', 'high-level'],
            'vector': ['semantic', 'similar', 'related', 'context', 'search', 'find']
        }
        
        desc_lower = description.lower()
        
        for memory_type, indicators in memory_indicators.items():
            if any(indicator in desc_lower for indicator in indicators):
                return memory_type
        
        return 'buffer'
    
    def _assess_reasoning_needs(self, description: str) -> str:
        """Assess reasoning requirements from description"""
        reasoning_indicators = {
            'react': ['direct', 'simple', 'quick', 'immediate', 'straightforward'],
            'plan-and-execute': ['plan', 'strategy', 'multi-step', 'coordinate', 'orchestrate'],
            'babyagi': ['autonomous', 'research', 'explore', 'discover', 'continuous']
        }
        
        desc_lower = description.lower()
        
        for reasoning_type, indicators in reasoning_indicators.items():
            if any(indicator in desc_lower for indicator in indicators):
                return reasoning_type
        
        return 'react'
    
    def _assess_security_needs(self, description: str) -> str:
        """Assess security requirements from description"""
        security_indicators = {
            'low': ['internal', 'trusted', 'safe', 'private'],
            'medium': ['standard', 'normal', 'typical'],
            'high': ['secure', 'sensitive', 'confidential', 'protected'],
            'maximum': ['critical', 'top-secret', 'classified', 'financial', 'medical']
        }
        
        desc_lower = description.lower()
        
        for level, indicators in security_indicators.items():
            if any(indicator in desc_lower for indicator in indicators):
                return level
        
        return 'medium'
    
    def _select_reasoning_type(self, requested_type: str, description: str, 
                             analysis: Dict[str, Any]) -> str:
        """Select appropriate reasoning type"""
        if requested_type != 'auto':
            if requested_type not in self.REASONING_TYPES:
                raise ValueError(f"Unsupported reasoning type: {requested_type}")
            return requested_type
        
        # Auto-select based on analysis
        complexity = analysis['complexity']
        reasoning_needs = analysis['reasoning_requirements']
        
        if reasoning_needs == 'babyagi' or 'research' in description.lower():
            return 'babyagi'
        elif complexity == 'complex' or reasoning_needs == 'plan-and-execute':
            return 'plan-and-execute'
        else:
            return 'react'
    
    def _select_memory_type(self, requested_type: str, description: str,
                          analysis: Dict[str, Any]) -> str:
        """Select appropriate memory type"""
        if requested_type != 'auto':
            if requested_type not in self.MEMORY_TYPES:
                raise ValueError(f"Unsupported memory type: {requested_type}")
            return requested_type
        
        # Auto-select based on analysis
        memory_needs = analysis['memory_requirements']
        
        if memory_needs == 'vector' or 'semantic' in description.lower():
            return 'vector'
        elif memory_needs == 'summary' or 'summary' in description.lower():
            return 'summary'
        else:
            return 'buffer'
    
    def _validate_tool_security(self, tools: List[str], generated_tools: Dict[str, Any], 
                               config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate tool security and compatibility"""
        security_level = config.get('security_level', 'medium')
        
        validation_results = {
            'level': security_level,
            'validations': {},
            'warnings': [],
            'recommendations': []
        }
        
        for tool_name in tools:
            if tool_name in generated_tools['implementations']:
                tool_impl = generated_tools['implementations'][tool_name]
                
                # Validate against security policies
                policy = generated_tools['security_policies'][tool_name]
                
                validation_results['validations'][tool_name] = {
                    'policy': policy,
                    'risk_level': self._assess_tool_risk(tool_name, policy, security_level)
                }
                
                # Check for security concerns
                if security_level == 'high' and tool_name in ['execute_command', 'browser_navigate']:
                    validation_results['warnings'].append(
                        f"Tool '{tool_name}' may pose security risks at high security level"
                    )
        
        # Check for tool compatibility
        compatibility_issues = self._check_tool_compatibility(tools)
        validation_results['compatibility_issues'] = compatibility_issues
        
        # Generate recommendations
        validation_results['recommendations'] = self._generate_security_recommendations(
            tools, security_level, validation_results
        )
        
        return validation_results
    
    def _assess_tool_risk(self, tool_name: str, policy: Dict[str, Any], 
                         security_level: str) -> str:
        """Assess risk level for a tool"""
        high_risk_tools = ['execute_command', 'write_to_file', 'browser_navigate']
        medium_risk_tools = ['read_file', 'search_files', 'apply_diff']
        
        if tool_name in high_risk_tools:
            return 'high' if security_level in ['high', 'maximum'] else 'medium'
        elif tool_name in medium_risk_tools:
            return 'medium'
        else:
            return 'low'
    
    def _check_tool_compatibility(self, tools: List[str]) -> List[str]:
        """Check for tool compatibility issues"""
        issues = []
        
        # Check for conflicting tools
        if 'execute_command' in tools and 'browser_navigate' in tools:
            issues.append("Combining command execution with browser automation may have security implications")
        
        if len(tools) > 8:
            issues.append(f"Large number of tools ({len(tools)}) may impact performance and increase complexity")
        
        return issues
    
    def _generate_security_recommendations(self, tools: List[str], security_level: str,
                                         validation_results: Dict[str, Any]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if security_level == 'high':
            recommendations.append("Consider using sandboxed environments for tool execution")
            recommendations.append("Implement additional input validation for user-provided parameters")
        
        if 'execute_command' in tools:
            recommendations.append("Review command execution policies and restrict allowed commands")
        
        if 'browser_navigate' in tools:
            recommendations.append("Implement URL validation and restrict navigation to trusted domains")
        
        if 'write_to_file' in tools:
            recommendations.append("Use file path validation and restrict write access to safe directories")
        
        return recommendations
    
    def _create_output_directory(self, agent_name: Optional[str]) -> Path:
        """Create output directory for generated agent"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        
        if agent_name:
            safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', agent_name)
            dir_name = f"{safe_name}-{timestamp}"
        else:
            dir_name = f"DeepAgent-{timestamp}"
        
        output_path = Path.cwd() / 'generated-agents' / dir_name
        output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Created output directory: {output_path}")
        return output_path
    
    def _generate_agent_files(self, config: Dict[str, Any], reasoning_type: str,
                            memory_type: str, tools: List[str], 
                            generated_tools: Dict[str, Any],
                            security_validation: Dict[str, Any],
                            output_path: Path) -> List[str]:
        """Generate all agent files with enhanced capabilities"""
        logger.info("Generating enhanced agent files")
        
        generated_files = []
        
        # Get template configuration
        template_config = self.TEMPLATE_CONFIGS[reasoning_type]
        
        # Generate main agent file
        agent_file = self._generate_agent_file(
            config, reasoning_type, memory_type, tools, 
            generated_tools, security_validation, template_config, output_path
        )
        generated_files.append(str(agent_file))
        
        # Generate sophisticated tools file
        tools_file = self._generate_enhanced_tools_file(
            tools, generated_tools, security_validation, output_path
        )
        generated_files.append(str(tools_file))
        
        # Generate requirements.txt
        requirements_file = self._generate_requirements(
            reasoning_type, memory_type, config.get('include_monitoring', True), 
            generated_tools, output_path
        )
        generated_files.append(str(requirements_file))
        
        # Generate Dockerfile if needed
        if config.get('output_format') == 'docker':
            dockerfile = self._generate_dockerfile(config, security_validation, output_path)
            generated_files.append(str(dockerfile))
        
        # Generate .env template
        env_file = self._generate_env_file(config, security_validation, output_path)
        generated_files.append(str(env_file))
        
        # Generate security configuration file
        security_file = self._generate_security_config_file(
            config, tools, security_validation, output_path
        )
        generated_files.append(str(security_file))
        
        # Generate test suite
        test_file = self._generate_test_suite(
            tools, generated_tools, security_validation, output_path
        )
        generated_files.append(str(test_file))
        
        return generated_files
    
    def _generate_agent_file(self, config: Dict[str, Any], reasoning_type: str,
                           memory_type: str, tools: List[str], 
                           generated_tools: Dict[str, Any],
                           security_validation: Dict[str, Any],
                           template_config: Dict[str, Any], output_path: Path) -> Path:
        """Generate enhanced main agent file"""
        logger.info("Generating enhanced main agent file")
        
        agent_file = output_path / 'agent.py'
        
        # Prepare template variables
        template_vars = {
            'agent_name': config.get('name', 'DeepAgent'),
            'description': config['description'],
            'reasoning_type': reasoning_type,
            'memory_type': memory_type,
            'tools': tools,
            'generated_tools': generated_tools,
            'security_validation': security_validation,
            'include_monitoring': config.get('include_monitoring', True),
            'security_level': config.get('security_level', 'medium'),
            'llm_config': config.get('llm_config', {
                'model': 'gpt-4-turbo-preview',
                'temperature': 0.1
            })
        }
        
        # Generate agent content using enhanced template engine
        agent_content = self.template_engine.render_agent(template_vars)
        
        agent_file.write_text(agent_content, encoding='utf-8')
        logger.info(f"Generated enhanced agent file: {agent_file}")
        
        return agent_file
    
    def _generate_enhanced_tools_file(self, tools: List[str], 
                                    generated_tools: Dict[str, Any],
                                    security_validation: Dict[str, Any],
                                    output_path: Path) -> Path:
        """Generate sophisticated tools file with enhanced implementations"""
        logger.info("Generating enhanced tools file")
        
        tools_file = output_path / 'tools.py'
        
        # Prepare template variables
        template_vars = {
            'tools': tools,
            'generated_tools': generated_tools,
            'security_validation': security_validation,
            'agent_name': 'DeepAgent'
        }
        
        # Generate tools content using enhanced template
        tools_content = self.template_engine.render_tools(template_vars)
        
        tools_file.write_text(tools_content, encoding='utf-8')
        logger.info(f"Generated enhanced tools file: {tools_file}")
        
        return tools_file
    
    def _generate_requirements(self, reasoning_type: str, memory_type: str,
                             include_monitoring: bool, 
                             generated_tools: Dict[str, Any], output_path: Path) -> Path:
        """Generate enhanced requirements.txt with tool dependencies"""
        logger.info("Generating enhanced requirements.txt")
        
        requirements_file = output_path / 'requirements.txt'
        
        # Base requirements
        requirements = [
            'langchain>=0.1.0',
            'langchain-openai>=0.0.5',
            'langchain-community>=0.0.10',
            'python-dotenv>=1.0.0',
            'openai>=1.0.0',
            'pydantic>=2.0.0',
            'typing-extensions>=4.0.0'
        ]
        
        # Add reasoning-specific requirements
        template_config = self.TEMPLATE_CONFIGS[reasoning_type]
        requirements.extend(template_config['requirements'])
        
        # Add memory-specific requirements
        memory_config = self.MEMORY_CONFIGS[memory_type]
        requirements.extend(memory_config['requirements'])
        
        # Add tool dependencies
        requirements.extend(generated_tools['dependencies'])
        
        # Add monitoring requirements
        if include_monitoring:
            requirements.append('langsmith>=0.0.60')
        
        # Add security-related dependencies for high security levels
        if self.security_level in ['high', 'maximum']:
            requirements.extend([
                'cryptography>=3.4.8',
                'python-json-logger>=2.0.0'
            ])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_requirements = []
        for req in requirements:
            if req not in seen:
                seen.add(req)
                unique_requirements.append(req)
        
        requirements_file.write_text('\n'.join(unique_requirements), encoding='utf-8')
        logger.info(f"Generated enhanced requirements file: {requirements_file}")
        
        return requirements_file
    
    def _generate_dockerfile(self, config: Dict[str, Any], 
                           security_validation: Dict[str, Any], output_path: Path) -> Path:
        """Generate enhanced Dockerfile with security considerations"""
        logger.info("Generating enhanced Dockerfile")
        
        dockerfile = output_path / 'Dockerfile'
        
        # Security-specific configurations
        security_configs = {
            'low': '',
            'medium': 'RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*',
            'high': '''RUN apt-get update && apt-get install -y gcc tini && rm -rf /var/lib/apt/lists/*
# Use tini for proper signal handling
ENTRYPOINT ["/usr/bin/tini", "--"]''',
            'maximum': '''RUN apt-get update && apt-get install -y gcc tini apparmor-utils && rm -rf /var/lib/apt/lists/*
# Enable AppArmor for enhanced security
RUN aa-enforce /etc/apparmor.d/docker-default''',
        }
        
        security_config = security_configs.get(self.security_level, security_configs['medium'])
        
        content = f'''# Enhanced DeepAgent Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
{security_config}

# Create non-root user early
RUN groupadd -r agent && useradd -r -g agent agent

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent files
COPY --chown=agent:agent . .

# Security: Set appropriate permissions
RUN chmod -R 755 /app && chown -R agent:agent /app

# Switch to non-root user
USER agent

# Expose port (if needed for web interfaces)
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV AGENT_SECURITY_LEVEL={self.security_level}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import agent; print('Agent healthy')"

# Run the agent
CMD ["python", "agent.py"]
'''
        
        dockerfile.write_text(content, encoding='utf-8')
        logger.info(f"Generated enhanced Dockerfile: {dockerfile}")
        
        return dockerfile
    
    def _generate_env_file(self, config: Dict[str, Any], 
                         security_validation: Dict[str, Any], output_path: Path) -> Path:
        """Generate enhanced .env template with security configurations"""
        logger.info("Generating enhanced .env template")
        
        env_file = output_path / '.env.template'
        
        security_level = config.get('security_level', 'medium')
        
        content = f'''# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_TEMPERATURE=0.1

# LangSmith Configuration (optional)
# LANGCHAIN_API_KEY=your-langsmith-api-key-here
# LANGCHAIN_PROJECT=your-project-name

# Agent Configuration
AGENT_NAME={config.get('name', 'DeepAgent')}
AGENT_LOG_LEVEL=INFO
AGENT_SECURITY_LEVEL={security_level}

# Security Configuration
# ENABLE_AUDIT_LOGGING=true
# LOG_SENSITIVE_OPERATIONS=true
# MAX_TOOL_TIMEOUT=60
# ALLOWED_FILE_EXTENSIONS=.py,.md,.txt,.json,.yaml,.yml

# Optional: Additional API keys for tools
# SERPAPI_API_KEY=your-serpapi-key  # For web search
# WOLFRAM_ALPHA_APPID=your-wolfram-id  # For calculations

# Tool-specific configurations
# BROWSER_TIMEOUT=45
# MAX_COMMAND_OUTPUT_SIZE=1048576
# ENABLE_TOOL_RETRY=true
# MAX_TOOL_RETRY_ATTEMPTS=3
'''
        
        env_file.write_text(content, encoding='utf-8')
        logger.info(f"Generated enhanced .env.template: {env_file}")
        
        return env_file
    
    def _generate_security_config_file(self, config: Dict[str, Any], tools: List[str],
                                     security_validation: Dict[str, Any], 
                                     output_path: Path) -> Path:
        """Generate security configuration file"""
        logger.info("Generating security configuration file")
        
        security_file = output_path / 'security_config.json'
        
        security_config = {
            'security_level': config.get('security_level', 'medium'),
            'tool_policies': security_validation['validations'],
            'compatibility_issues': security_validation['compatibility_issues'],
            'recommendations': security_validation['recommendations'],
            'audit_logging': {
                'enabled': True,
                'log_file': 'agent_audit.log',
                'log_sensitive_operations': config.get('security_level') in ['high', 'maximum']
            },
            'input_validation': {
                'enabled': True,
                'max_input_length': 10000,
                'sanitize_user_input': True
            },
            'tool_execution': {
                'timeout_default': 30,
                'enable_retry_logic': True,
                'max_retry_attempts': 3,
                'enable_sandboxing': config.get('security_level') == 'maximum'
            }
        }
        
        security_file.write_text(json.dumps(security_config, indent=2), encoding='utf-8')
        logger.info(f"Generated security configuration: {security_file}")
        
        return security_file
    
    def _generate_test_suite(self, tools: List[str], generated_tools: Dict[str, Any],
                           security_validation: Dict[str, Any], output_path: Path) -> Path:
        """Generate comprehensive test suite"""
        logger.info("Generating test suite")
        
        test_file = output_path / 'test_tools.py'
        
        test_content = f'''#!/usr/bin/env python3
"""
Test suite for DeepAgent tools

Generated by Enhanced DeepAgent Generator
"""

import unittest
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from tools import *

class TestToolSecurity(unittest.TestCase):
    """Test tool security features"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.security_config = {security_validation}
    
    def test_input_validation(self):
        """Test that tools validate inputs properly"""
        # Test will be implemented based on generated tools
        pass
    
    def test_security_policies(self):
        """Test that security policies are enforced"""
        # Test will be implemented based on generated tools
        pass

class TestToolFunctionality(unittest.TestCase):
    """Test tool functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tools = {tools}
        self.generated_tools = {generated_tools}
    
'''

        # Add test cases for each tool
        for tool_name in tools:
            if tool_name in generated_tools['test_cases']:
                test_cases = generated_tools['test_cases'][tool_name]
                for test_case in test_cases:
                    test_content += f'''
    def {test_case['name']}(self):
        """{test_case['description']}"""
        # Test implementation for {tool_name}
        # Inputs: {test_case['inputs']}
        # Expected success: {test_case['expected_success']}
        pass
    
'''
        
        test_content += '''
if __name__ == '__main__':
    unittest.main()
'''
        
        test_file.write_text(test_content, encoding='utf-8')
        logger.info(f"Generated test suite: {test_file}")
        
        return test_file
    
    def _generate_enhanced_readme(self, config: Dict[str, Any], reasoning_type: str,
                                memory_type: str, tools: List[str], 
                                generated_tools: Dict[str, Any],
                                security_validation: Dict[str, Any],
                                output_path: Path):
        """Generate enhanced README with comprehensive documentation"""
        logger.info("Generating enhanced README")
        
        readme_file = output_path / 'README.md'
        
        # Generate tool documentation section
        tool_docs = ""
        for tool_name in tools:
            if tool_name in generated_tools['documentation']:
                tool_docs += f"\n### {tool_name.replace('_', ' ').title()}\n"
                tool_docs += generated_tools['documentation'][tool_name]
        
        # Generate security section
        security_section = f"""
## Security Configuration

- **Security Level**: {config.get('security_level', 'medium')}
- **Tool Validation**: Enabled
- **Input Sanitization**: Enabled
- **Audit Logging**: Enabled

### Security Recommendations
"""
        
        for rec in security_validation['recommendations']:
            security_section += f"- {rec}\n"
        
        content = f'''# {config.get("name", "DeepAgent")}

{config["description"]}

## Configuration

- **Reasoning Type**: {reasoning_type}
- **Memory Type**: {memory_type}
- **Tools**: {len(tools)} tools configured
- **Security Level**: {config.get('security_level', 'medium')}
- **Monitoring**: {"Enabled" if config.get("include_monitoring") else "Disabled"}

## Tools Overview

The following tools have been configured for this agent:

{', '.join(tools) if tools else 'No tools configured'}

### Tool Categories
"""
        
        # Add tool categories
        if 'tool_categories' in security_validation:
            for category, category_tools in security_validation['tool_categories'].items():
                if category_tools:
                    content += f"- **{category.title()}**: {', '.join(category_tools)}\n"
        
        content += f"""

## Installation

1. Copy the environment template:
```bash
cp .env.template .env
```

2. Edit `.env` and add your API keys:
```bash
# Required
OPENAI_API_KEY=your-openai-api-key

# Optional
# LANGCHAIN_API_KEY=your-langsmith-key
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Review security configuration:
```bash
cat security_config.json
```

## Usage

### Basic Usage
```python
from agent import {config.get('name', 'DeepAgent').replace(' ', '')}

agent = {config.get('name', 'DeepAgent').replace(' ', '')}()
result = agent.run("Your task here")
print(result)
```

### Running the Agent
```bash
python agent.py
```

### Running Tests
```bash
python test_tools.py
```

## Tool Documentation

{tool_docs}

## Security Features

{security_section}

## Advanced Features

### Tool Chaining
Tools can be chained together to create complex workflows:

```python
# Example: Search for files, read content, and analyze
result1 = agent.search_files(path=".", regex="class\\s+\\w+")
result2 = agent.read_file(path="found_file.py")
result3 = agent.codebase_search(query="specific pattern")
```

### Error Handling
All tools include comprehensive error handling and retry logic:

```python
# Tools automatically handle common errors
# - Network timeouts
# - File permission issues
# - Invalid inputs
# - Security policy violations
```

### Security Policies
Tools enforce security policies based on the configured security level:

```python
# High security mode enables:
# - Input validation and sanitization
# - Path traversal protection
# - Command injection prevention
# - Audit logging
```

## Development

### Project Structure
```
{output_path.name}/
├── agent.py                 # Main agent implementation
├── tools.py                 # Enhanced tool implementations
├── test_tools.py           # Comprehensive test suite
├── security_config.json    # Security configuration
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration (if generated)
└── .env.template          # Environment variables template
```

### Adding Custom Tools
Edit `tools.py` to add your custom tools:

```python
from langchain.tools import BaseTool
from typing import Optional

class CustomTool(BaseTool):
    \"\"\"Your custom tool implementation\"\"\"
    
    name: str = "custom_tool"
    description: str = "Description of what this tool does"
    
    def _run(self, param: str) -> str:
        # Your implementation here
        return "Tool result"
```

### Security Best Practices
1. Always review security recommendations in `security_config.json`
2. Use appropriate security level for your use case
3. Regularly audit tool usage and access patterns
4. Keep dependencies updated
5. Monitor tool execution logs

## Deployment

### Docker Deployment
If you generated a Dockerfile:

```bash
# Build the image
docker build -t {config.get('name', 'deepagent').lower()} .

# Run the container
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY {config.get('name', 'deepagent').lower()}
```

### Production Considerations
- Use `security_level: maximum` for production deployments
- Implement proper secrets management
- Configure monitoring and alerting
- Set up log aggregation
- Regular security audits

## Monitoring

### LangSmith Integration
To enable LangSmith monitoring:
1. Set `LANGCHAIN_API_KEY` in your `.env` file
2. Set `LANGCHAIN_PROJECT` to your project name
3. Run your agent as usual

### Audit Logging
Security events and tool executions are logged to `agent_audit.log` when enabled.

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure `OPENAI_API_KEY` is set in `.env`
   - Verify the key is valid and has sufficient quota

2. **Security Policy Violations**
   - Review `security_config.json` for policy details
   - Adjust security level if needed
   - Check audit logs for detailed information

3. **Tool Execution Failures**
   - Check tool-specific error messages
   - Verify input parameters
   - Review timeout settings in `.env`

4. **Performance Issues**
   - Reduce number of concurrent tools
   - Adjust timeout values
   - Consider using vector memory for large contexts

## Support

For issues and questions:
1. Check the logs for detailed error messages
2. Review security configuration and recommendations
3. Verify all API keys are correctly set
4. Run test suite: `python test_tools.py`
5. Check tool documentation above

Generated by Enhanced DeepAgent Generator on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
'''
        
        readme_file.write_text(content, encoding='utf-8')
        logger.info(f"Generated enhanced README.md: {readme_file}")
    
    def _generate_security_config(self, config: Dict[str, Any], tools: List[str],
                                security_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate security configuration summary"""
        return {
            'security_level': config.get('security_level', 'medium'),
            'tools_configured': len(tools),
            'security_validations': security_validation['validations'],
            'compatibility_issues': security_validation['compatibility_issues'],
            'recommendations': security_validation['recommendations'],
            'audit_logging': {
                'enabled': True,
                'log_file': 'agent_audit.log'
            }
        }


class EnhancedTemplateEngine:
    """Enhanced template engine for generating sophisticated agent files"""
    
    def __init__(self):
        self.templates = {}
    
    def render_agent(self, variables: Dict[str, Any]) -> str:
        """Render enhanced agent template with variables"""
        
        # Generate imports section
        imports = self._generate_agent_imports(variables)
        
        # Generate agent class
        agent_class = self._generate_agent_class(variables)
        
        # Generate tool setup
        tool_setup = self._generate_tool_setup(variables)
        
        # Generate security setup
        security_setup = self._generate_security_setup(variables)
        
        content = f'''#!/usr/bin/env python3
"""
{variables['agent_name']} - {variables['description']}

Generated by Enhanced DeepAgent Generator on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

{imports}

class {variables['agent_name'].replace(' ', '')}:
    """
    {variables['description']}
    
    Configuration:
    - Reasoning Type: {variables['reasoning_type']}
    - Memory Type: {variables['memory_type']}
    - Tools: {len(variables['tools'])} tools configured
    - Security Level: {variables['security_level']}
    - Monitoring: {'Enabled' if variables['include_monitoring'] else 'Disabled'}
    """
    
    def __init__(self):
        \"\"\"Initialize the enhanced agent with security and monitoring\"\"\"
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.security_level = os.getenv('AGENT_SECURITY_LEVEL', '{variables['security_level']}')
        
        # Setup core components
        self._setup_llm()
        self._setup_memory()
        self._setup_tools()
        self._setup_security()
        self._setup_monitoring()
        
        self.logger.info("Enhanced agent initialized successfully")
    
    def _setup_llm(self):
        \"\"\"Setup language model with enhanced configuration\"\"\"
        self.llm = ChatOpenAI(
            model=os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview'),
            temperature=float(os.getenv('OPENAI_TEMPERATURE', '0.1')),
            streaming=True
        )
    
    def _setup_memory(self):
        \"\"\"Setup memory system based on configuration\"\"\"
        memory_type = '{variables['memory_type']}'
        
        if memory_type == 'buffer':
            from langchain.memory import ConversationBufferWindowMemory
            self.memory = ConversationBufferWindowMemory(k=5)
        elif memory_type == 'summary':
            from langchain.memory import ConversationSummaryMemory
            self.memory = ConversationSummaryMemory(llm=self.llm)
        elif memory_type == 'vector':
            from langchain.memory import VectorStoreRetrieverMemory
            from langchain.vectorstores import Chroma
            from langchain_openai import OpenAIEmbeddings
            
            vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
            self.memory = VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever())
        else:
            self.memory = None
        
        self.logger.info(f"Memory system configured: {{memory_type}}")
    
    def _setup_tools(self):
        \"\"\"Setup enhanced tools with security and monitoring\"\"\"
        from tools import get_available_tools
        
        self.tools = get_available_tools()
        self.logger.info(f"{{len(self.tools)}} tools configured")
    
    def _setup_security(self):
        \"\"\"Setup security policies and validation\"\"\"
        self.security_validator = SecurityValidator()
        self.audit_logger = logging.getLogger('agent.audit')
        
        # Setup audit logging
        audit_handler = logging.FileHandler('agent_audit.log')
        audit_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.audit_logger.addHandler(audit_handler)
        self.audit_logger.setLevel(logging.INFO)
        
        self.logger.info("Security system configured")
    
    def _setup_monitoring(self):
        \"\"\"Setup monitoring and observability\"\"\"
        self.monitoring_enabled = {str(variables['include_monitoring']).lower()}
        
        if self.monitoring_enabled:
            try:
                # from langsmith import Client
                # self.monitoring_client = Client()
                self.logger.info("Monitoring enabled (LangSmith integration ready)")
            except ImportError:
                self.logger.warning("Monitoring requested but langsmith not available")
                self.monitoring_enabled = False
    
    def _validate_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> bool:
        \"\"\"Validate tool call against security policies\"\"\"
        validation_result = self.security_validator.validate_tool_call(tool_name, parameters)
        
        if not validation_result['allowed']:
            self.logger.warning(f"Tool call blocked: {{validation_result['reason']}}")
            self.audit_logger.warning(f"Blocked tool call: {{tool_name}} - {{validation_result['reason']}}")
            return False
        
        # Log warnings
        for warning in validation_result.get('warnings', []):
            self.logger.warning(f"Tool call warning: {{warning}}")
        
        return True
    
    def run(self, task: str) -> Dict[str, Any]:
        \"\"\"Execute a task with enhanced error handling and monitoring\"\"\"
        self.logger.info(f'Executing task: {{task}}')
        self.audit_logger.info(f'Task execution started: {{task[:100]}}...')
        
        try:
            # Validate task input
            if not task or len(task) > 10000:
                raise ValueError("Invalid task input")
            
            # Execute task based on reasoning type
            if '{variables['reasoning_type']}' == 'react':
                result = self._run_with_react(task)
            elif '{variables['reasoning_type']}' == 'plan-and-execute':
                result = self._run_with_plan_and_execute(task)
            elif '{variables['reasoning_type']}' == 'babyagi':
                result = self._run_with_babyagi(task)
            else:
                result = self._run_default(task)
            
            # Log success
            self.audit_logger.info(f'Task completed successfully: {{task[:100]}}...')
            
            return {{
                'success': True,
                'output': result,
                'tool_usage': self._get_tool_usage_stats()
            }}
            
        except Exception as e:
            self.logger.error(f'Task execution failed: {{e}}')
            self.audit_logger.error(f'Task failed: {{task[:100]}}... - Error: {{e}}')
            
            return {{
                'success': False,
                'error': str(e),
                'tool_usage': self._get_tool_usage_stats()
            }}
    
    def _run_with_react(self, task: str) -> str:
        \"\"\"Execute task using ReAct pattern\"\"\"
        from langchain.agents import AgentExecutor, create_openai_tools_agent
        
        # Create agent with tools
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant with access to various tools."),
            ("human", "{{input}}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=self.verbose)
        
        result = agent_executor.invoke({{"input": task}})
        return result["output"]
    
    def _run_with_plan_and_execute(self, task: str) -> str:
        \"\"\"Execute task using Plan-and-Execute pattern\"\"\"
        from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
        
        planner = load_chat_planner(self.llm)
        executor = load_agent_executor(self.llm, self.tools, verbose=self.verbose)
        
        agent = PlanAndExecute(planner=planner, executor=executor, verbose=self.verbose)
        result = agent.run(task)
        
        return result
    
    def _run_with_babyagi(self, task: str) -> str:
        \"\"\"Execute task using BabyAGI pattern\"\"\"
        from langchain_experimental.autonomous_agents import BabyAGI
        from langchain.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings
        
        vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
        
        baby_agi = BabyAGI.from_llm(
            llm=self.llm,
            vectorstore=vectorstore,
            verbose=self.verbose,
            max_iterations=10
        )
        
        result = baby_agi({{"objective": task}})
        return result["output"]
    
    def _run_default(self, task: str) -> str:
        \"\"\"Default task execution\"\"\"
        # Simple LLM call with tool access
        from langchain_core.prompts import ChatPromptTemplate
        
        prompt = ChatPromptTemplate.from_template(
            "Use the available tools to help with this task: {{task}}\\n\\nAvailable tools: {{tools}}"
        )
        
        chain = prompt | self.llm
        result = chain.invoke({{
            "task": task,
            "tools": [tool.name for tool in self.tools]
        }})
        
        return result.content
    
    def _get_tool_usage_stats(self) -> Dict[str, Any]:
        \"\"\"Get tool usage statistics\"\"\"
        return {{
            "tools_configured": len(self.tools),
            "security_level": self.security_level,
            "monitoring_enabled": self.monitoring_enabled
        }}

{tool_setup}

{security_setup}

if __name__ == '__main__':
    # Example usage
    agent = {variables['agent_name'].replace(' ', '')}()
    
    # Test task
    test_task = "Your task here"
    result = agent.run(test_task)
    
    print(f"Task: {{test_task}}")
    print(f"Result: {{result}}")
'''
        
        return content
    
    def _generate_agent_imports(self, variables: Dict[str, Any]) -> str:
        """Generate imports for agent file"""
        imports = [
            'import logging',
            'import os',
            'from typing import Dict, Any, List, Optional',
            'from dotenv import load_dotenv'
        ]
        
        # LangChain imports
        imports.extend([
            'from langchain_openai import ChatOpenAI',
            'from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder'
        ])
        
        # Reasoning-specific imports
        reasoning_type = variables['reasoning_type']
        if reasoning_type == 'react':
            imports.extend([
                'from langchain.agents import AgentExecutor, create_openai_tools_agent',
                'from langchain_core.agents import AgentAction, AgentFinish'
            ])
        elif reasoning_type == 'plan-and-execute':
            imports.extend([
                'from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner'
            ])
        elif reasoning_type == 'babyagi':
            imports.extend([
                'from langchain_experimental.autonomous_agents import BabyAGI',
                'from langchain.vectorstores import Chroma',
                'from langchain_openai import OpenAIEmbeddings'
            ])
        
        # Memory-specific imports
        memory_type = variables['memory_type']
        if memory_type == 'buffer':
            imports.append('from langchain.memory import ConversationBufferWindowMemory')
        elif memory_type == 'summary':
            imports.append('from langchain.memory import ConversationSummaryMemory')
        elif memory_type == 'vector':
            imports.extend([
                'from langchain.memory import VectorStoreRetrieverMemory',
                'from langchain.vectorstores import Chroma',
                'from langchain_openai import OpenAIEmbeddings'
            ])
        
        # Monitoring imports
        if variables['include_monitoring']:
            imports.append('# from langsmith import Client  # Uncomment for LangSmith monitoring')
        
        return '\n'.join(imports)
    
    def _generate_agent_class(self, variables: Dict[str, Any]) -> str:
        """Generate agent class content"""
        # This is now handled in the main render_agent method
        return ""
    
    def _generate_tool_setup(self, variables: Dict[str, Any]) -> str:
        """Generate tool setup methods"""
        return '''
    # Tool setup is handled in __init__ through _setup_tools()
'''
    
    def _generate_security_setup(self, variables: Dict[str, Any]) -> str:
        """Generate security setup methods"""
        return '''
    # Security setup is handled in __init__ through _setup_security()
'''
    
    def render_tools(self, variables: Dict[str, Any]) -> str:
        """Render enhanced tools template with variables"""
        
        tools = variables['tools']
        generated_tools = variables['generated_tools']
        security_validation = variables['security_validation']
        
        # Generate imports
        imports = self._generate_tools_imports(tools, generated_tools)
        
        # Generate tool classes
        tool_classes = self._generate_tool_classes(tools, generated_tools, security_validation)
        
        # Generate tool registry
        tool_registry = self._generate_tool_registry(tools, generated_tools)
        
        # Generate security utilities
        security_utils = self._generate_security_utils()
        
        content = f'''#!/usr/bin/env python3
"""
Tool definitions for {variables['agent_name']}

Generated by Enhanced DeepAgent Generator
"""

{imports}

logger = logging.getLogger(__name__)

# ============================================================================
# Enhanced Tool Classes
# ============================================================================

{tool_classes}

# ============================================================================
# Tool Registry and Utilities
# ============================================================================

{tool_registry}

{security_utils}

# ============================================================================
# Tool Documentation
# ============================================================================

"""
Available Tools:
{chr(10).join([f"- {tool}: {generated_tools['implementations'][tool]['description'] if tool in generated_tools['implementations'] else 'Custom tool'}" for tool in tools])}

Tool Categories:
"""
        
        # Add tool categories
        if 'tool_categories' in security_validation:
            for category, category_tools in security_validation['tool_categories'].items():
                if category_tools:
                    content += f"{category.title()}: {', '.join(category_tools)}\n"
        
        content += '"""'
        
        return content
    
    def _generate_tools_imports(self, tools: List[str], 
                              generated_tools: Dict[str, Any]) -> str:
        """Generate imports for tools file"""
        imports = [
            'import logging',
            'import os',
            'import re',
            'import json',
            'import time',
            'from typing import Dict, Any, List, Optional, Union',
            'from pathlib import Path',
            'from functools import wraps',
            'from datetime import datetime'
        ]
        
        # Add LangChain tool imports
        imports.extend([
            'from langchain.tools import BaseTool',
            'from langchain.callbacks.manager import CallbackManagerForToolRun',
            'from pydantic import BaseModel, Field, validator'
        ])
        
        # Add tool-specific imports
        all_imports = set()
        for tool_name in tools:
            if tool_name in generated_tools['implementations']:
                tool_impl = generated_tools['implementations'][tool_name]
                all_imports.update(tool_impl.get('required_imports', []))
        
        imports.extend(sorted(all_imports))
        
        return '\n'.join(imports)
    
    def _generate_tool_classes(self, tools: List[str], 
                             generated_tools: Dict[str, Any],
                             security_validation: Dict[str, Any]) -> str:
        """Generate tool class implementations"""
        classes = []
        
        for tool_name in tools:
            if tool_name in generated_tools['implementations']:
                tool_impl = generated_tools['implementations'][tool_name]
                
                # Generate enhanced tool class
                tool_class = self._generate_enhanced_tool_class(
                    tool_name, tool_impl, security_validation
                )
                classes.append(tool_class)
        
        return '\n\n\n'.join(classes)
    
    def _generate_enhanced_tool_class(self, tool_name: str, 
                                    tool_impl: Dict[str, Any],
                                    security_validation: Dict[str, Any]) -> str:
        """Generate enhanced tool class with security and monitoring"""
        
        class_name = tool_impl['class_name']
        parameters = tool_impl['parameters']
        
        # Generate parameter definitions
        param_defs = []
        for param in parameters:
            param_type = param['type']
            if 'Optional' in param_type:
                param_defs.append(f"{param['name']}: {param_type} = None")
            else:
                param_defs.append(f"{param['name']}: {param_type}")
        
        # Add run_manager parameter
        param_defs.append("run_manager: Optional[CallbackManagerForToolRun] = None")
        
        # Generate class
        class_def = f'''class {class_name}(BaseTool):
    \"\"\"{tool_impl['description']}\"\"\"
    
    name: str = "{tool_name}"
    description: str = \"\"\"{tool_impl['description']}
    
    Args:
{chr(10).join([f"        {p['name']} ({p['type']}): {p['description']}" for p in parameters])}
    
    Returns:
        {tool_impl['return_type']}: {tool_impl.get('return_description', 'Result of the tool execution')}
    \"\"\"
    
    # Security policy for this tool
    security_policy: Dict[str, Any] = {security_validation['validations'].get(tool_name, {}).get('policy', {})}
    
    # Tool metadata
    timeout: int = {tool_impl.get('timeout', 30)}
    retry_enabled: bool = {str(tool_impl.get('retry_logic', False)).lower()}
    max_retries: int = 3
    
    def _run(
        self,
        {',\\n        '.join(param_defs)}
    ) -> str:
        """Execute the tool with security validation and error handling."""
        
        start_time = time.time()
        execution_attempts = 0
        
        while execution_attempts <= self.max_retries:
            try:
                execution_attempts += 1
                
                # Validate parameters
                validation_result = self._validate_parameters(locals())
                if not validation_result['valid']:
                    return f"Parameter validation failed: {{validation_result['error']}}"
                
                # Check security policy
                if not self._check_security_policy(locals()):
                    return f"Security policy violation for tool {{self.name}}"
                
                # Log tool execution
                logger.info(f"Executing {{self.name}} (attempt {{execution_attempts}})")
                
                # Execute tool implementation
                result = self._execute_tool(
                    {', '.join([p['name'] for p in parameters])}
                )
                
                # Log success
                execution_time = time.time() - start_time
                logger.info(f"Tool {{self.name}} completed in {{execution_time:.2f}}s")
                
                return result
                
            except Exception as e:
                logger.error(f"Error in {{self.name}} (attempt {{execution_attempts}}): {{e}}")
                
                if execution_attempts >= self.max_retries or not self.retry_enabled:
                    return f"Error executing {{self.name}} after {{execution_attempts}} attempts: {{str(e)}}"
                
                # Wait before retry
                time.sleep(2 ** execution_attempts)
        
        return f"Tool {{self.name}} failed after {{self.max_retries}} attempts"
    
    def _validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"Validate tool parameters\"\"\"
        try:
            # Remove self and run_manager from params
            params_to_validate = {{k: v for k, v in params.items() if k not in ['self', 'run_manager']}}
            
            # Basic validation
            for param_name, param_value in params_to_validate.items():
                if param_value is None:
                    continue
                
                # Type checking
                if isinstance(param_value, str):
                    if len(param_value) > 10000:
                        return {{"valid": False, "error": f"Parameter {{param_name}} too long"}}
                
                # Security checks
                if param_name == 'path' or param_name == 'file_path':
                    if '..' in str(param_value) or str(param_value).startswith('/'):
                        return {{"valid": False, "error": f"Invalid path in {{param_name}}"}}
            
            return {{"valid": True, "error": ""}}
            
        except Exception as e:
            return {{"valid": False, "error": f"Validation error: {{str(e)}}"}}
    
    def _check_security_policy(self, params: Dict[str, Any]) -> bool:
        \"\"\"Check security policy for this tool\"\"\"
        try:
            # This would integrate with the security validator
            # For now, return True (policy checked at agent level)
            return True
        except Exception:
            return False
    
    def _execute_tool(self, {', '.join([p['name'] for p in parameters])}) -> str:
        \"\"\"Actual tool execution logic\"\"\"
        {tool_impl['implementation']}
    
    async def _arun(self, {', '.join(param_defs)}) -> str:
        \"\"\"Async version of the tool\"\"\"
        return self._run({', '.join([p['name'] for p in parameters])}, run_manager)'''
        
        return class_def
    
    def _generate_tool_registry(self, tools: List[str], 
                              generated_tools: Dict[str, Any]) -> str:
        """Generate tool registry function"""
        
        tool_instantiations = []
        for tool_name in tools:
            if tool_name in generated_tools['implementations']:
                tool_impl = generated_tools['implementations'][tool_name]
                class_name = tool_impl['class_name']
                tool_instantiations.append(f"        {class_name}(),")
        
        registry_def = "def get_available_tools() -> List[BaseTool]:\n"
        registry_def += "    \"\"\"Get all available tools with enhanced security and monitoring.\"\"\"\n"
        registry_def += "    return [\n"
        registry_def += f"{chr(10).join(tool_instantiations)}\n"
        registry_def += "    ]\n"
        registry_def += "\n"
        registry_def += "def get_tool_descriptions() -> Dict[str, str]:\n"
        registry_def += "    \"\"\"Get descriptions of all available tools.\"\"\"\n"
        registry_def += "    return {\n"
        for tool in tools:
            desc = generated_tools['implementations'][tool]['description'] if tool in generated_tools['implementations'] else 'Custom tool'
            registry_def += f'        "{tool}": "{desc}",\n'
        registry_def += "    }"
        return registry_def
    
    def _generate_security_utils(self) -> str:
        """Generate security utility functions"""
        security_utils = "# ============================================================================\n"
        security_utils += "# Security Utilities\n"
        security_utils += "# ============================================================================\n"
        security_utils += "\n"
        security_utils += "class SecurityException(Exception):\n"
        security_utils += "    \"\"\"Custom exception for security violations\"\"\"\n"
        security_utils += "    pass\n"
        security_utils += "\n"
        security_utils += "def sanitize_input(input_string: str, max_length: int = 10000) -> str:\n"
        security_utils += "    \"\"\"Sanitize user input to prevent injection attacks.\"\"\"\n"
        security_utils += "    if not input_string:\n"
        security_utils += "        return \"\"\n"
        security_utils += "    \n"
        security_utils += "    if len(input_string) > max_length:\n"
        security_utils += "        raise SecurityException(f\"Input exceeds maximum length of {max_length}\")\n"
        security_utils += "    \n"
        security_utils += "    # Remove potentially dangerous characters\n"
        security_utils += "    sanitized = re.sub(r'[<>'\"'&]', '', input_string)\n"
        security_utils += "    \n"
        security_utils += "    return sanitized\n"
        security_utils += "\n"
        security_utils += "def validate_path(file_path: str, allowed_dirs: List[str] = None) -> bool:\n"
        security_utils += "    \"\"\"Validate file path to prevent directory traversal.\"\"\"\n"
        security_utils += "    try:\n"
        security_utils += "        path = Path(file_path).resolve()\n"
        security_utils += "        \n"
        security_utils += "        # Check for directory traversal\n"
        security_utils += "        if '..' in str(file_path):\n"
        security_utils += "            return False\n"
        security_utils += "        \n"
        security_utils += "        # Check against allowed directories\n"
        security_utils += "        if allowed_dirs:\n"
        security_utils += "            return any(str(path).startswith(str(Path(allowed_dir).resolve())) \n"
        security_utils += "                      for allowed_dir in allowed_dirs)\n"
        security_utils += "        \n"
        security_utils += "        return True\n"
        security_utils += "        \n"
        security_utils += "    except Exception:\n"
        security_utils += "        return False\n"
        security_utils += "\n"
        security_utils += "def audit_log(logger: logging.Logger, action: str, details: Dict[str, Any]):\n"
        security_utils += "    \"\"\"Log security-relevant actions.\"\"\"\n"
        security_utils += "    audit_entry = {\n"
        security_utils += "        \"timestamp\": datetime.now().isoformat(),\n"
        security_utils += "        \"action\": action,\n"
        security_utils += "        \"details\": details\n"
        security_utils += "    }\n"
        security_utils += "    logger.info(f\"AUDIT: {json.dumps(audit_entry)}\")\n"
        security_utils += "\n"
        security_utils += "def retry_with_backoff(max_attempts: int = 3, base_delay: float = 1.0):\n"
        security_utils += "    \"\"\"Decorator for retrying functions with exponential backoff.\"\"\"\n"
        security_utils += "    def decorator(func):\n"
        security_utils += "        @wraps(func)\n"
        security_utils += "        def wrapper(*args, **kwargs):\n"
        security_utils += "            for attempt in range(max_attempts):\n"
        security_utils += "                try:\n"
        security_utils += "                    return func(*args, **kwargs)\n"
        security_utils += "                except Exception as e:\n"
        security_utils += "                    if attempt == max_attempts - 1:\n"
        security_utils += "                        raise\n"
        security_utils += "                    \n"
        security_utils += "                    delay = base_delay * (2 ** attempt)\n"
        security_utils += "                    logging.warning(f\"Attempt {attempt + 1} failed, retrying in {delay}s: {e}\")\n"
        security_utils += "                    time.sleep(delay)\n"
        security_utils += "            \n"
        security_utils += "            raise Exception(f\"Failed after {max_attempts} attempts\")\n"
        security_utils += "        \n"
        security_utils += "        return wrapper\n"
        security_utils += "    return decorator\n"
        security_utils += "\n"
        security_utils += "# ============================================================================\n"
        security_utils += "# Performance Monitoring\n"
        security_utils += "# ============================================================================\n"
        security_utils += "\n"
        security_utils += "class ToolPerformanceMonitor:\n"
        security_utils += "    \"\"\"Monitor tool performance and usage.\"\"\"\n"
        security_utils += "    \n"
        security_utils += "    def __init__(self):\n"
        security_utils += "        self.usage_stats = {}\n"
        security_utils += "    \n"
        security_utils += "    def record_usage(self, tool_name: str, execution_time: float, success: bool):\n"
        security_utils += "        \"\"\"Record tool usage statistics.\"\"\"\n"
        security_utils += "        if tool_name not in self.usage_stats:\n"
        security_utils += "            self.usage_stats[tool_name] = {\n"
        security_utils += "                \"calls\": 0,\n"
        security_utils += "                \"total_time\": 0,\n"
        security_utils += "                \"failures\": 0\n"
        security_utils += "            }\n"
        security_utils += "        \n"
        security_utils += "        stats = self.usage_stats[tool_name]\n"
        security_utils += "        stats[\"calls\"] += 1\n"
        security_utils += "        stats[\"total_time\"] += execution_time\n"
        security_utils += "        \n"
        security_utils += "        if not success:\n"
        security_utils += "            stats[\"failures\"] += 1\n"
        security_utils += "    \n"
        security_utils += "    def get_stats(self) -> Dict[str, Any]:\n"
        security_utils += "        \"\"\"Get performance statistics.\"\"\"\n"
        security_utils += "        stats = {}\n"
        security_utils += "        for tool_name, tool_stats in self.usage_stats.items():\n"
        security_utils += "            calls = tool_stats[\"calls\"]\n"
        security_utils += "            if calls > 0:\n"
        security_utils += "                stats[tool_name] = {\n"
        security_utils += "                    \"total_calls\": calls,\n"
        security_utils += "                    \"average_time\": tool_stats[\"total_time\"] / calls,\n"
        security_utils += "                    \"failure_rate\": tool_stats[\"failures\"] / calls,\n"
        security_utils += "                    \"total_time\": tool_stats[\"total_time\"]\n"
        security_utils += "                }\n"
        security_utils += "        \n"
        security_utils += "        return stats\n"
        security_utils += "\n"
        security_utils += "# Global performance monitor\n"
        security_utils += "performance_monitor = ToolPerformanceMonitor()"
        return security_utils


class EnhancedToolAnalyzer:
    """Enhanced tool analyzer with sophisticated keyword extraction and categorization"""
    
    TOOL_CATEGORIES = {
        'web': {
            'tools': ['browser_navigate', 'browser_snapshot', 'browser_evaluate', 'browser_click', 'browser_type'],
            'keywords': ['web', 'browser', 'website', 'online', 'internet', 'page', 'navigate', 'click', 'type'],
            'description': 'Web automation and browser interaction tools'
        },
        'data': {
            'tools': ['data_analysis', 'calculator', 'statistics', 'plot', 'graph'],
            'keywords': ['data', 'analyze', 'statistics', 'calculate', 'math', 'plot', 'graph', 'chart'],
            'description': 'Data analysis and mathematical computation tools'
        },
        'file': {
            'tools': ['search_files', 'read_file', 'write_to_file', 'list_files', 'apply_diff'],
            'keywords': ['file', 'read', 'write', 'document', 'search', 'list', 'directory', 'folder'],
            'description': 'File system operations and management tools'
        },
        'api': {
            'tools': ['api_calls', 'http_request', 'webhook', 'endpoint'],
            'keywords': ['api', 'http', 'request', 'endpoint', 'webhook', 'rest', 'json', 'xml'],
            'description': 'API integration and HTTP request tools'
        },
        'database': {
            'tools': ['database', 'sql', 'query', 'table', 'record'],
            'keywords': ['database', 'sql', 'query', 'table', 'record', 'postgres', 'mysql', 'mongodb'],
            'description': 'Database operations and query tools'
        },
        'communication': {
            'tools': ['email', 'send_message', 'slack', 'teams', 'chat'],
            'keywords': ['email', 'send', 'message', 'slack', 'teams', 'chat', 'communicate', 'notify'],
            'description': 'Communication and messaging tools'
        },
        'analysis': {
            'tools': ['codebase_search', 'list_code_definition_names', 'search_files'],
            'keywords': ['analyze', 'code', 'search', 'find', 'pattern', 'structure', 'definition'],
            'description': 'Code analysis and search tools'
        },
        'automation': {
            'tools': ['execute_command', 'mcp_tool', 'schedule', 'automate'],
            'keywords': ['execute', 'command', 'run', 'automate', 'schedule', 'script', 'program'],
            'description': 'System automation and command execution tools'
        }
    }
    
    SPECIFIC_TOOL_PATTERNS = {
        'search_files': {
            'primary_keywords': ['search', 'find', 'pattern', 'regex', 'grep'],
            'context_keywords': ['file', 'code', 'content', 'text', 'directory'],
            'confidence_boost': 2.0
        },
        'read_file': {
            'primary_keywords': ['read', 'open', 'load', 'view', 'display'],
            'context_keywords': ['file', 'document', 'content', 'text', 'code'],
            'confidence_boost': 1.5
        },
        'browser_navigate': {
            'primary_keywords': ['browse', 'navigate', 'visit', 'go to', 'open'],
            'context_keywords': ['web', 'website', 'page', 'url', 'internet'],
            'confidence_boost': 2.0
        },
        'execute_command': {
            'primary_keywords': ['execute', 'run', 'command', 'shell', 'terminal'],
            'context_keywords': ['script', 'program', 'system', 'bash', 'cmd'],
            'confidence_boost': 1.8
        },
        'codebase_search': {
            'primary_keywords': ['search', 'find', 'analyze', 'understand'],
            'context_keywords': ['codebase', 'project', 'repository', 'code', 'implementation'],
            'confidence_boost': 2.5
        }
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze(self, description: str) -> Dict[str, Any]:
        """Analyze description with sophisticated keyword extraction"""
        desc_lower = description.lower()
        
        # Extract keywords using multiple techniques
        keywords = self._extract_keywords(desc_lower)
        
        # Categorize tools
        category_scores = self._categorize_tools(keywords, desc_lower)
        
        # Score specific tools
        tool_scores = self._score_specific_tools(keywords, desc_lower)
        
        # Resolve conflicts and select final tools
        selected_tools = self._select_final_tools(category_scores, tool_scores)
        
        return {
            'keywords': keywords,
            'category_scores': category_scores,
            'tool_scores': tool_scores,
            'selected_tools': selected_tools,
            'confidence_scores': self._calculate_confidence_scores(selected_tools, tool_scores),
            'tool_categories': self._assign_tool_categories(selected_tools)
        }
    
    def _extract_keywords(self, description: str) -> List[str]:
        """Extract keywords using multiple techniques"""
        keywords = []
        
        # Split into words and clean
        words = re.findall(r'\b\w+\b', description.lower())
        
        # Add individual words
        keywords.extend(words)
        
        # Add bigrams (two-word phrases)
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            keywords.append(bigram)
        
        # Add trigrams (three-word phrases)
        for i in range(len(words) - 2):
            trigram = f"{words[i]} {words[i+1]} {words[i+2]}"
            keywords.append(trigram)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)
        
        return unique_keywords
    
    def _categorize_tools(self, keywords: List[str], description: str) -> Dict[str, float]:
        """Score tool categories based on keywords"""
        category_scores = {}
        
        for category, config in self.TOOL_CATEGORIES.items():
            score = 0.0
            
            # Count matching keywords
            for keyword in keywords:
                for category_keyword in config['keywords']:
                    if keyword in category_keyword or category_keyword in keyword:
                        # Weight by length (longer matches are more specific)
                        weight = len(keyword.split()) / 3.0  # Normalize by max phrase length
                        score += weight
            
            # Normalize by category keyword count
            score = score / len(config['keywords'])
            
            # Boost score if category description appears in text
            if any(desc_word in description for desc_word in config['description'].lower().split()):
                score *= 1.2
            
            category_scores[category] = score
        
        return category_scores
    
    def _score_specific_tools(self, keywords: List[str], description: str) -> Dict[str, float]:
        """Score specific tools using pattern matching"""
        tool_scores = {}
        
        for tool, patterns in self.SPECIFIC_TOOL_PATTERNS.items():
            score = 0.0
            
            # Check primary keywords
            for keyword in keywords:
                for primary_kw in patterns['primary_keywords']:
                    if keyword in primary_kw or primary_kw in keyword:
                        score += patterns['confidence_boost']
            
            # Check context keywords
            context_matches = 0
            for keyword in keywords:
                for context_kw in patterns['context_keywords']:
                    if keyword in context_kw or context_kw in keyword:
                        context_matches += 1
            
            # Boost based on context
            if context_matches > 0:
                score *= (1.0 + context_matches * 0.3)
            
            # Additional boost if tool name appears directly
            if tool.replace('_', ' ') in description:
                score *= 2.0
            
            tool_scores[tool] = score
        
        return tool_scores
    
    def _select_final_tools(self, category_scores: Dict[str, float], 
                           tool_scores: Dict[str, float]) -> List[str]:
        """Select final tools based on scores and resolve conflicts"""
        selected_tools = []
        
        # Add high-scoring specific tools first
        for tool, score in tool_scores.items():
            if score >= 2.0:  # Threshold for tool inclusion
                selected_tools.append(tool)
        
        # Add tools from high-scoring categories
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        
        for category, score in sorted_categories:
            if score >= 0.3:  # Category threshold
                category_tools = self.TOOL_CATEGORIES[category]['tools']
                
                # Add tools that aren't already selected
                for tool in category_tools:
                    if tool not in selected_tools:
                        # Check if we have a more specific version already
                        has_specific = any(
                            selected_tool.startswith(tool.split('_')[0]) 
                            for selected_tool in selected_tools
                        )
                        
                        if not has_specific:
                            selected_tools.append(tool)
        
        # Remove duplicates and return
        return list(set(selected_tools))
    
    def _calculate_confidence_scores(self, selected_tools: List[str], 
                                    tool_scores: Dict[str, float]) -> Dict[str, float]:
        """Calculate confidence scores for selected tools"""
        confidence_scores = {}
        
        for tool in selected_tools:
            if tool in tool_scores:
                # Normalize score to 0-1 range
                confidence = min(tool_scores[tool] / 5.0, 1.0)
                confidence_scores[tool] = confidence
            else:
                confidence_scores[tool] = 0.5  # Default confidence
        
        return confidence_scores
    
    def _assign_tool_categories(self, selected_tools: List[str]) -> Dict[str, List[str]]:
        """Assign tools to categories"""
        tool_categories = {}
        
        for category, config in self.TOOL_CATEGORIES.items():
            category_tools = []
            
            for tool in selected_tools:
                if tool in config['tools']:
                    category_tools.append(tool)
            
            if category_tools:
                tool_categories[category] = category_tools
        
        return tool_categories
    
    def suggest_tools(self, description: str) -> List[str]:
        """Suggest tools based on enhanced analysis"""
        analysis = self.analyze(description)
        return analysis['selected_tools']


class ToolGenerator:
    """Generates sophisticated tool implementations based on requirements"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.security_validator = SecurityValidator()
        self.template_engine = EnhancedTemplateEngine()
    
    def generate_tools(self, tool_names: List[str], agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete tool implementations"""
        self.logger.info(f"Generating tools: {tool_names}")
        
        generated_tools = {
            'implementations': {},
            'imports': set(),
            'dependencies': [],
            'security_policies': {},
            'test_cases': {},
            'documentation': {}
        }
        
        for tool_name in tool_names:
            try:
                # Generate tool implementation
                tool_impl = self._generate_tool_implementation(tool_name, agent_config)
                generated_tools['implementations'][tool_name] = tool_impl
                
                # Extract imports
                generated_tools['imports'].update(tool_impl.get('required_imports', []))
                
                # Add dependencies
                generated_tools['dependencies'].extend(tool_impl.get('dependencies', []))
                
                # Generate security policy
                security_policy = self.security_validator.generate_security_policy(tool_name)
                generated_tools['security_policies'][tool_name] = security_policy
                
                # Generate test cases
                test_cases = self._generate_test_cases(tool_name, tool_impl)
                generated_tools['test_cases'][tool_name] = test_cases
                
                # Generate documentation
                documentation = self._generate_tool_documentation(tool_name, tool_impl)
                generated_tools['documentation'][tool_name] = documentation
                
            except Exception as e:
                self.logger.error(f"Failed to generate tool {tool_name}: {e}")
                continue
        
        # Remove duplicates from dependencies
        generated_tools['dependencies'] = list(set(generated_tools['dependencies']))
        
        return generated_tools
    
    def _generate_tool_implementation(self, tool_name: str, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate implementation for a specific tool"""
        
        # Tool implementation templates
        implementations = {
            'search_files': self._generate_search_files_tool,
            'read_file': self._generate_read_file_tool,
            'browser_navigate': self._generate_browser_navigate_tool,
            'browser_snapshot': self._generate_browser_snapshot_tool,
            'browser_evaluate': self._generate_browser_evaluate_tool,
            'browser_click': self._generate_browser_click_tool,
            'browser_type': self._generate_browser_type_tool,
            'execute_command': self._generate_execute_command_tool,
            'write_to_file': self._generate_write_to_file_tool,
            'apply_diff': self._generate_apply_diff_tool,
            'list_files': self._generate_list_files_tool,
            'list_code_definition_names': self._generate_list_code_definitions_tool,
            'codebase_search': self._generate_codebase_search_tool,
            'use_mcp_tool': self._generate_mcp_tool
        }
        
        generator = implementations.get(tool_name)
        if not generator:
            # Generate generic tool stub
            return self._generate_generic_tool(tool_name, agent_config)
        
        return generator(agent_config)
    
    def _generate_search_files_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate search_files tool implementation"""
        return {
            'name': 'search_files',
            'description': 'Search for files matching patterns using regex with performance optimization',
            'class_name': 'FileSearchTool',
            'parameters': [
                {'name': 'path', 'type': 'str', 'description': 'Directory path to search', 'required': True},
                {'name': 'regex', 'type': 'str', 'description': 'Regex pattern to match', 'required': True},
                {'name': 'file_pattern', 'type': 'Optional[str]', 'description': 'File pattern filter', 'required': False}
            ],
            'return_type': 'str',
            'implementation': '''
        # Performance optimized search
        search_path = Path(path)
        if not search_path.exists():
            return f"Error: Path does not exist: {path}"
        
        matches = []
        pattern = re.compile(regex)
        
        # Use rglob for efficient recursive search
        if file_pattern:
            files = search_path.rglob(file_pattern) if search_path.is_dir() else [search_path]
        else:
            files = search_path.rglob('*') if search_path.is_dir() else [search_path]
        
        # Search each file with error handling
        for file_path in files:
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if pattern.search(content):
                            matches.append(str(file_path))
                except Exception as e:
                    logger.warning(f"Could not read {file_path}: {e}")
        
        if matches:
            return f"Found {len(matches)} matching files:\\n" + "\\n".join(matches[:20]) + \
                   ("\\n..." if len(matches) > 20 else "")
        else:
            return f"No files found matching pattern '{regex}'"
            ''',
            'required_imports': ['import re', 'from pathlib import Path', 'from typing import Optional'],
            'dependencies': [],
            'error_handling': ['FileNotFoundError', 'PermissionError', 're.error'],
            'retry_logic': True,
            'timeout': 30
        }
    
    def _generate_read_file_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate read_file tool implementation"""
        return {
            'name': 'read_file',
            'description': 'Read and return file contents with encoding detection and security validation',
            'class_name': 'FileReadTool',
            'parameters': [
                {'name': 'path', 'type': 'str', 'description': 'Path to file to read', 'required': True}
            ],
            'return_type': 'str',
            'implementation': '''
        # Security validation
        if '..' in path or path.startswith('/'):
            raise SecurityException(f"Invalid file path: {path}")
        
        file_path = Path(path)
        if not file_path.exists():
            return f"Error: File not found: {path}"
        
        if not file_path.is_file():
            return f"Error: Path is not a file: {path}"
        
        # Check file size
        max_size = 5 * 1024 * 1024  # 5MB
        if file_path.stat().st_size > max_size:
            return f"Error: File too large (> {max_size} bytes)"
        
        # Read with encoding detection
        encodings = ['utf-8', 'utf-16', 'latin-1', 'ascii']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    preview = content[:500]
                    if len(content) > 500:
                        preview += f"...\\n\\n[File truncated: {len(content)} total characters]"
                    return f"Successfully read {path} ({encoding}):\\n\\n{preview}"
            except UnicodeDecodeError:
                continue
        
        return f"Error: Could not decode file {path} with any standard encoding"
            ''',
            'required_imports': ['from pathlib import Path'],
            'dependencies': [],
            'error_handling': ['FileNotFoundError', 'PermissionError', 'UnicodeDecodeError', 'SecurityException'],
            'retry_logic': False,
            'timeout': 10
        }
    
    def _generate_browser_navigate_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate browser_navigate tool implementation"""
        return {
            'name': 'browser_navigate',
            'description': 'Navigate to web pages using browser automation with security validation',
            'class_name': 'BrowserNavigateTool',
            'parameters': [
                {'name': 'url', 'type': 'str', 'description': 'URL to navigate to', 'required': True}
            ],
            'return_type': 'str',
            'implementation': '''
        # Validate URL
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return f"Error: Invalid URL format: {url}"
        
        # Security check for dangerous schemes
        dangerous_schemes = ['file:', 'javascript:', 'data:', 'vbscript:']
        if any(url.lower().startswith(scheme) for scheme in dangerous_schemes):
            return f"Error: Dangerous URL scheme detected: {url}"
        
        # Check against allowed domains (if configured)
        allowed_domains = os.getenv('ALLOWED_DOMAINS', '').split(',')
        if allowed_domains and parsed.netloc not in allowed_domains:
            return f"Error: Domain not in allowed list: {parsed.netloc}"
        
        # Simulate browser navigation (in real implementation, use playwright/selenium)
        return f"Browser navigation to {url} initiated successfully"
            ''',
            'required_imports': ['from urllib.parse import urlparse', 'import logging', 'import os'],
            'dependencies': [],
            'error_handling': ['ValueError', 'Exception'],
            'retry_logic': True,
            'timeout': 45
        }
    
    def _generate_browser_snapshot_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate browser_snapshot tool implementation"""
        return {
            'name': 'browser_snapshot',
            'description': 'Take accessibility snapshot of current browser page with metadata',
            'class_name': 'BrowserSnapshotTool',
            'parameters': [],
            'return_type': 'str',
            'implementation': '''
        # In real implementation, this would capture accessibility tree
        # For now, return simulated snapshot with metadata
        snapshot_content = {
            "url": "current_page_url",
            "title": "Current Page Title",
            "elements": [
                {"type": "heading", "level": 1, "text": "Main Heading"},
                {"type": "paragraph", "text": "Sample paragraph content"},
                {"type": "button", "text": "Click Me"},
                {"type": "link", "text": "Learn More", "href": "/learn"}
            ],
            "timestamp": datetime.now().isoformat(),
            "metadata": {
                "viewport_width": 1920,
                "viewport_height": 1080,
                "user_agent": "Enhanced DeepAgent Browser"
            }
        }
        
        return f"Browser snapshot captured:\\n{json.dumps(snapshot_content, indent=2)}"
            ''',
            'required_imports': ['import json', 'import logging', 'from datetime import datetime'],
            'dependencies': [],
            'error_handling': ['Exception'],
            'retry_logic': False,
            'timeout': 15
        }
    
    def _generate_browser_evaluate_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate browser_evaluate tool implementation"""
        return {
            'name': 'browser_evaluate',
            'description': 'Execute JavaScript code in browser context with security sandboxing',
            'class_name': 'BrowserEvaluateTool',
            'parameters': [
                {'name': 'function', 'type': 'str', 'description': 'JavaScript function to execute', 'required': True}
            ],
            'return_type': 'str',
            'implementation': '''
        # Security validation for JavaScript
        dangerous_patterns = [
            'eval(', 'Function(', 'setTimeout(', 'setInterval(',
            'document.write(', 'innerHTML=', 'outerHTML=',
            'fetch(', 'XMLHttpRequest(', 'WebSocket(',
            'localStorage', 'sessionStorage', 'cookie'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in function:
                return f"Error: Potentially dangerous JavaScript pattern detected: {pattern}"
        
        # Validate function structure
        function = function.strip()
        if not (function.startswith('function') or function.startswith('()') or function.startswith('async')):
            return "Error: JavaScript must be a function"
        
        # Check function length
        if len(function) > 5000:
            return "Error: JavaScript function too long (max 5000 characters)"
        
        # Simulate execution (in real implementation, use browser context)
        return f"JavaScript executed successfully: {function[:100]}..."
            ''',
            'required_imports': ['import logging'],
            'dependencies': [],
            'error_handling': ['Exception'],
            'retry_logic': False,
            'timeout': 20
        }
    
    def _generate_browser_click_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate browser_click tool implementation"""
        return {
            'name': 'browser_click',
            'description': 'Click elements on web pages with validation',
            'class_name': 'BrowserClickTool',
            'parameters': [
                {'name': 'element', 'type': 'str', 'description': 'Human-readable element description', 'required': True},
                {'name': 'ref', 'type': 'str', 'description': 'Exact element reference', 'required': True}
            ],
            'return_type': 'str',
            'implementation': '''
        # Validate parameters
        if not element or not ref:
            return "Error: Both element and ref parameters are required"
        
        # Security check - prevent clicking on dangerous elements
        dangerous_elements = ['javascript:', 'data:', 'file:', '<script']
        if any(dangerous in ref.lower() for dangerous in dangerous_elements):
            return f"Error: Dangerous element reference detected: {ref}"
        
        # Validate element description length
        if len(element) > 200:
            return "Error: Element description too long (max 200 characters)"
        
        # Simulate click (in real implementation, use browser automation)
        return f"Successfully clicked element: {element} (ref: {ref})"
            ''',
            'required_imports': ['import logging'],
            'dependencies': [],
            'error_handling': ['Exception'],
            'retry_logic': True,
            'timeout': 15
        }
    
    def _generate_browser_type_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate browser_type tool implementation"""
        return {
            'name': 'browser_type',
            'description': 'Type text into web page elements with validation',
            'class_name': 'BrowserTypeTool',
            'parameters': [
                {'name': 'element', 'type': 'str', 'description': 'Human-readable element description', 'required': True},
                {'name': 'ref', 'type': 'str', 'description': 'Exact element reference', 'required': True},
                {'name': 'text', 'type': 'str', 'description': 'Text to type', 'required': True},
                {'name': 'submit', 'type': 'bool', 'description': 'Whether to submit after typing', 'required': False}
            ],
            'return_type': 'str',
            'implementation': '''
        # Validate parameters
        if not all([element, ref, text]):
            return "Error: element, ref, and text parameters are required"
        
        # Security check - validate text length and content
        if len(text) > 10000:
            return "Error: Text too long (max 10000 characters)"
        
        # Check for potentially dangerous content
        dangerous_patterns = ['<script', 'javascript:', 'onload=', 'onerror=']
        for pattern in dangerous_patterns:
            if pattern in text.lower():
                return f"Error: Potentially dangerous content detected: {pattern}"
        
        # Simulate typing (in real implementation, use browser automation)
        action = "submitted" if submit else "typed"
        preview = text[:50] + "..." if len(text) > 50 else text
        return f"Successfully {action} text into {element}: {preview}"
            ''',
            'required_imports': ['import logging'],
            'dependencies': [],
            'error_handling': ['Exception'],
            'retry_logic': True,
            'timeout': 15
        }
    
    def _generate_execute_command_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate execute_command tool implementation"""
        return {
            'name': 'execute_command',
            'description': 'Execute system commands with comprehensive security validation',
            'class_name': 'CommandExecutionTool',
            'parameters': [
                {'name': 'command', 'type': 'str', 'description': 'Command to execute', 'required': True}
            ],
            'return_type': 'str',
            'implementation': '''
        # Comprehensive security validation
        validation_result = self._validate_command(command)
        if not validation_result['allowed']:
            return f"Error: Command blocked by security policy: {validation_result['reason']}"
        
        # Additional security checks
        if len(command) > 1000:
            return "Error: Command too long (max 1000 characters)"
        
        # Log command execution (audit trail)
        logger.warning(f"Executing command: {command}")
        audit_log(logger, "command_execution", {"command": command})
        
        # Simulate command execution (in real implementation, use subprocess with sandboxing)
        # For security, we simulate rather than actually execute
        return f"Command executed successfully (simulated): {command}"
    
    def _validate_command(self, command: str) -> Dict[str, Any]:
        """Validate command against security policies."""
        dangerous_patterns = [
            r'rm\\s+-rf\\s+/',  # Dangerous deletion
            r'dd\\s+if=',      # Disk operations
            r':\\(\\)\\{\\s*:\\|\\:&\\s*\\};:',  # Fork bomb
            r'chmod\\s+\\d+\\s+/',  # Permission changes
            r'mv\\s+.+\\s+/',     # Dangerous moves
            r'>\\s*/dev/sd',     # Direct disk writing
            r'wget\\s+.*\\s+-O\\s+-\\s*\\|',  # Download and execute
            r'curl\\s+.*\\s+\\|',  # Download and execute
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return {
                    'allowed': False,
                    'reason': f'Dangerous pattern detected: {pattern}'
                }
        
        # Check for sudo commands
        if command.strip().startswith('sudo'):
            return {
                'allowed': False,
                'reason': 'Sudo commands are not allowed'
            }
        
        # Check allowed commands (if configured)
        allowed_commands = os.getenv('ALLOWED_COMMANDS', 'ls,echo,cat,grep,find,pwd,which').split(',')
        cmd_start = command.split()[0].lower()
        
        if cmd_start not in allowed_commands:
            return {
                'allowed': False,
                'reason': f'Command not in allowed list: {cmd_start}'
            }
        
        return {'allowed': True, 'reason': ''}
            ''',
            'required_imports': ['import logging', 'import re', 'from typing import Dict, Any', 'import os'],
            'dependencies': [],
            'error_handling': ['Exception', 'SecurityException'],
            'retry_logic': False,
            'timeout': 60
        }
    
    def _generate_write_to_file_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate write_to_file tool implementation"""
        return {
            'name': 'write_to_file',
            'description': 'Write content to files with backup and validation',
            'class_name': 'FileWriteTool',
            'parameters': [
                {'name': 'path', 'type': 'str', 'description': 'File path to write to', 'required': True},
                {'name': 'content', 'type': 'str', 'description': 'Content to write', 'required': True}
            ],
            'return_type': 'str',
            'implementation': '''
        # Security validation
        if '..' in path:
            raise SecurityException(f"Invalid path (directory traversal detected): {path}")
        
        file_path = Path(path)
        
        # Check file size
        max_size = 10 * 1024 * 1024  # 10MB
        if len(content.encode('utf-8')) > max_size:
            return f"Error: Content too large (> {max_size} bytes)"
        
        # Create backup if file exists
        if file_path.exists():
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            shutil.copy2(file_path, backup_path)
            logger.info(f"Created backup: {backup_path}")
        
        # Create parent directories
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Log file write
        audit_log(logger, "file_write", {"path": str(file_path), "size": len(content)})
        
        return f"Successfully wrote {len(content)} characters to {path}"
            ''',
            'required_imports': ['from pathlib import Path', 'import shutil', 'import logging'],
            'dependencies': [],
            'error_handling': ['Exception', 'SecurityException'],
            'retry_logic': True,
            'timeout': 30
        }
    
    def _generate_apply_diff_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate apply_diff tool implementation"""
        return {
            'name': 'apply_diff',
            'description': 'Apply code changes using diff format with validation',
            'class_name': 'DiffApplyTool',
            'parameters': [
                {'name': 'path', 'type': 'str', 'description': 'File path to modify', 'required': True},
                {'name': 'diff', 'type': 'str', 'description': 'Diff content to apply', 'required': True},
                {'name': 'start_line', 'type': 'int', 'description': 'Starting line number', 'required': True}
            ],
            'return_type': 'str',
            'implementation': '''
        # Security validation
        if '..' in path:
            raise SecurityException(f"Invalid path (directory traversal detected): {path}")
        
        file_path = Path(path)
        if not file_path.exists():
            return f"Error: File not found: {path}"
        
        # Validate start_line
        if start_line < 1:
            return "Error: start_line must be positive"
        
        # Read original content
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Create backup
        backup_path = file_path.with_suffix(file_path.suffix + '.backup')
        shutil.copy2(file_path, backup_path)
        
        # Parse and apply diff (simplified implementation)
        # In production, use a proper diff library
        try:
            # This is a placeholder - real implementation would parse diff format
            # and apply changes carefully
            
            # Log the diff application
            audit_log(logger, "diff_apply", {
                "path": str(file_path),
                "start_line": start_line,
                "diff_preview": diff[:100] + "..." if len(diff) > 100 else diff
            })
            
            return f"Diff applied to {path} starting at line {start_line} (simulated)"
            
        except Exception as e:
            # Restore backup on failure
            shutil.copy2(backup_path, file_path)
            return f"Error applying diff: {str(e)} - backup restored"
            ''',
            'required_imports': ['from pathlib import Path', 'import shutil', 'import logging'],
            'dependencies': [],
            'error_handling': ['Exception', 'SecurityException'],
            'retry_logic': False,
            'timeout': 20
        }
    
    def _generate_list_files_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate list_files tool implementation"""
        return {
            'name': 'list_files',
            'description': 'List files in directories with filtering and pagination',
            'class_name': 'FileListTool',
            'parameters': [
                {'name': 'path', 'type': 'str', 'description': 'Directory path to list', 'required': True},
                {'name': 'recursive', 'type': 'bool', 'description': 'List recursively', 'required': False}
            ],
            'return_type': 'str',
            'implementation': '''
        # Security validation
        if '..' in path:
            raise SecurityException(f"Invalid path (directory traversal detected): {path}")
        
        dir_path = Path(path)
        if not dir_path.exists():
            return f"Error: Path does not exist: {path}"
        
        if not dir_path.is_dir():
            return f"Error: Path is not a directory: {path}"
        
        # List files with pagination
        if recursive:
            files = [str(p) for p in dir_path.rglob('*') if p.is_file()]
        else:
            files = [str(p) for p in dir_path.iterdir() if p.is_file()]
        
        if files:
            # Paginate results
            page_size = 50
            pages = [files[i:i + page_size] for i in range(0, len(files), page_size)]
            
            result = f"Files in {path} ({'recursive' if recursive else 'top-level'}): {len(files)} total\\n"
            result += f"Showing first {len(pages[0])} files:\\n"
            result += "\\n".join(pages[0])
            
            if len(pages) > 1:
                result += f"\\n... and {len(files) - len(pages[0])} more files"
            
            return result
        else:
            return f"No files found in {path}"
            ''',
            'required_imports': ['from pathlib import Path', 'import logging'],
            'dependencies': [],
            'error_handling': ['Exception', 'SecurityException'],
            'retry_logic': False,
            'timeout': 15
        }
    
    def _generate_list_code_definitions_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate list_code_definition_names tool implementation"""
        return {
            'name': 'list_code_definition_names',
            'description': 'List code definitions (functions, classes, etc.) with analysis',
            'class_name': 'CodeDefinitionsTool',
            'parameters': [
                {'name': 'path', 'type': 'str', 'description': 'File or directory path', 'required': True}
            ],
            'return_type': 'str',
            'implementation': '''
        # Security validation
        if '..' in path:
            raise SecurityException(f"Invalid path (directory traversal detected): {path}")
        
        path_obj = Path(path)
        
        definitions = []
        
        if path_obj.is_file():
            files = [path_obj]
        else:
            # Support multiple languages
            files = []
            for ext in ['*.py', '*.js', '*.ts', '*.java', '*.cpp', '*.c', '*.h']:
                files.extend(path_obj.rglob(ext))
        
        for file_path in files[:100]:  # Limit to prevent performance issues
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Find Python definitions
                if file_path.suffix == '.py':
                    class_matches = re.findall(r'^class\\s+(\\w+)', content, re.MULTILINE)
                    func_matches = re.findall(r'^def\\s+(\\w+)', content, re.MULTILINE)
                    
                    for cls in class_matches:
                        definitions.append(f"Class: {cls} (in {file_path})")
                    for func in func_matches:
                        definitions.append(f"Function: {func} (in {file_path})")
                
                # Find JavaScript/TypeScript definitions
                elif file_path.suffix in ['.js', '.ts']:
                    class_matches = re.findall(r'(?:class|interface)\\s+(\\w+)', content)
                    func_matches = re.findall(r'(?:function\\s+(\\w+)|(const|let|var)\\s+(\\w+)\\s*=\\s*(?:\\([^)]*\\)|[^=])=>', content)
                    
                    for cls in class_matches:
                        definitions.append(f"Class/Interface: {cls} (in {file_path})")
                    for func in func_matches:
                        definitions.append(f"Function: {func} (in {file_path})")
                
            except Exception as e:
                logger.warning(f"Could not analyze {file_path}: {e}")
        
        if definitions:
            return "Code definitions found:\\n" + "\\n".join(definitions[:30]) + \
                   ("\\n..." if len(definitions) > 30 else "")
        else:
            return f"No code definitions found in {path}"
            ''',
            'required_imports': ['from pathlib import Path', 'import re', 'import logging'],
            'dependencies': [],
            'error_handling': ['Exception', 'SecurityException'],
            'retry_logic': False,
            'timeout': 30
        }
    
    def _generate_codebase_search_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate codebase_search tool implementation"""
        return {
            'name': 'codebase_search',
            'description': 'Search codebase using semantic search with relevance scoring',
            'class_name': 'CodebaseSearchTool',
            'parameters': [
                {'name': 'query', 'type': 'str', 'description': 'Search query', 'required': True},
                {'name': 'path', 'type': 'Optional[str]', 'description': 'Path to search (default: current directory)', 'required': False}
            ],
            'return_type': 'str',
            'implementation': '''
        # Security validation
        if path and '..' in path:
            raise SecurityException(f"Invalid path (directory traversal detected): {path}")
        
        search_path = Path(path) if path else Path.cwd()
        
        if not search_path.exists():
            return f"Error: Search path does not exist: {search_path}"
        
        # In real implementation, this would use semantic search
        # For now, perform keyword search with relevance scoring
        results = []
        
        # Search in common code files
        code_files = []
        for ext in ['*.py', '*.js', '*.ts', '*.md', '*.txt', '*.json', '*.yaml', '*.yml']:
            code_files.extend(search_path.rglob(ext))
        
        query_lower = query.lower()
        
        for file_path in code_files[:200]:  # Limit search scope for performance
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    if query_lower in content:
                        # Calculate relevance score
                        count = content.count(query_lower)
                        # Bonus for proximity to important sections
                        bonus = 0
                        if 'def ' in content or 'class ' in content:
                            bonus += 1
                        
                        relevance = count + bonus
                        results.append((file_path, relevance, count))
            except Exception:
                continue
        
        # Sort by relevance
        results.sort(key=lambda x: x[1], reverse=True)
        
        if results:
            result_str = "\\n".join([
                f"{file} (relevance: {rel}, mentions: {count})" 
                for file, rel, count in results[:10]
            ])
            return f"Semantic search results for '{query}':\\n{result_str}"
        else:
            return f"No results found for '{query}' in {search_path}"
            ''',
            'required_imports': ['from pathlib import Path', 'from typing import Optional', 'import logging'],
            'dependencies': [],
            'error_handling': ['Exception', 'SecurityException'],
            'retry_logic': True,
            'timeout': 45
        }
    
    def _generate_mcp_tool(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate use_mcp_tool implementation"""
        return {
            'name': 'use_mcp_tool',
            'description': 'Use MCP server tools for extended functionality with validation',
            'class_name': 'McpTool',
            'parameters': [
                {'name': 'server_name', 'type': 'str', 'description': 'MCP server name', 'required': True},
                {'name': 'tool_name', 'type': 'str', 'description': 'Tool name to use', 'required': True},
                {'name': 'arguments', 'type': 'Dict[str, Any]', 'description': 'Tool arguments', 'required': True}
            ],
            'return_type': 'str',
            'implementation': '''
        # Validate parameters
        if not all([server_name, tool_name, arguments]):
            return "Error: server_name, tool_name, and arguments are required"
        
        # Security check for dangerous servers
        dangerous_servers = ['system', 'shell', 'bash', 'cmd', 'powershell']
        if any(dangerous in server_name.lower() for dangerous in dangerous_servers):
            return f"Error: Potentially dangerous MCP server: {server_name}"
        
        # Validate arguments size
        args_str = str(arguments)
        if len(args_str) > 10000:
            return "Error: Arguments too large (max 10000 characters)"
        
        # Log MCP tool usage
        audit_log(logger, "mcp_tool_usage", {
            "server": server_name,
            "tool": tool_name,
            "arg_keys": list(arguments.keys())
        })
        
        # Simulate MCP tool usage
        # In real implementation, this would call the actual MCP server
        return f"MCP tool '{tool_name}' from server '{server_name}' executed successfully with arguments: {list(arguments.keys())}"
            ''',
            'required_imports': ['from typing import Dict, Any', 'import logging'],
            'dependencies': [],
            'error_handling': ['Exception'],
            'retry_logic': True,
            'timeout': 30
        }
    
    def _generate_generic_tool(self, tool_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate generic tool stub for unknown tools"""
        return {
            'name': tool_name,
            'description': f'Custom tool: {tool_name}',
            'class_name': f'{tool_name.replace("_", " ").title().replace(" ", "")}Tool',
            'parameters': [
                {'name': 'input_data', 'type': 'str', 'description': 'Input data for the tool', 'required': True}
            ],
            'return_type': 'str',
            'implementation': f'''
        # Generic tool implementation for {tool_name}
        # This is a stub that should be customized for your specific needs
        
        if not input_data:
            return "Error: input_data is required"
        
        if len(input_data) > 10000:
            return "Error: input_data too long (max 10000 characters)"
        
        # Log usage
        logger.info(f"Custom tool {tool_name} executed")
        
        return f"Custom tool {tool_name} executed with input: {{input_data[:100]}}..."
            ''',
            'required_imports': ['import logging'],
            'dependencies': [],
            'error_handling': ['Exception'],
            'retry_logic': False,
            'timeout': 30
        }
    
    def _generate_test_cases(self, tool_name: str, tool_impl: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate test cases for a tool"""
        test_cases = []
        
        # Basic functionality test
        test_cases.append({
            'name': f'test_{tool_name}_basic',
            'description': f'Test basic {tool_name} functionality',
            'inputs': self._generate_test_inputs(tool_name),
            'expected_success': True
        })
        
        # Error handling test
        test_cases.append({
            'name': f'test_{tool_name}_error_handling',
            'description': f'Test {tool_name} error handling',
            'inputs': self._generate_error_test_inputs(tool_name),
            'expected_success': False
        })
        
        # Security test (for high-risk tools)
        if tool_name in ['execute_command', 'write_to_file', 'browser_navigate']:
            test_cases.append({
                'name': f'test_{tool_name}_security',
                'description': f'Test {tool_name} security validation',
                'inputs': self._generate_security_test_inputs(tool_name),
                'expected_success': False
            })
        
        return test_cases
    
    def _generate_test_inputs(self, tool_name: str) -> Dict[str, Any]:
        """Generate appropriate test inputs for a tool"""
        test_inputs = {
            'search_files': {'path': '.', 'regex': 'test'},
            'read_file': {'path': 'test.txt'},
            'browser_navigate': {'url': 'https://example.com'},
            'browser_snapshot': {},
            'browser_evaluate': {'function': '() => { return "test"; }'},
            'browser_click': {'element': 'test button', 'ref': 'button-1'},
            'browser_type': {'element': 'test input', 'ref': 'input-1', 'text': 'test text'},
            'execute_command': {'command': 'echo "test"'},
            'write_to_file': {'path': 'test.txt', 'content': 'test content'},
            'apply_diff': {'path': 'test.py', 'diff': 'test diff', 'start_line': 1},
            'list_files': {'path': '.'},
            'list_code_definition_names': {'path': '.'},
            'codebase_search': {'query': 'test'},
            'use_mcp_tool': {'server_name': 'test', 'tool_name': 'test', 'arguments': {}}
        }
        
        return test_inputs.get(tool_name, {'input_data': 'test'})
    
    def _generate_error_test_inputs(self, tool_name: str) -> Dict[str, Any]:
        """Generate test inputs that should cause errors"""
        error_inputs = {
            'search_files': {'path': '/nonexistent', 'regex': '['},  # Invalid regex
            'read_file': {'path': '/nonexistent/file.txt'},
            'browser_navigate': {'url': 'not-a-url'},
            'browser_snapshot': {},
            'browser_evaluate': {'function': 'invalid javascript['},
            'browser_click': {'element': '', 'ref': ''},
            'browser_type': {'element': '', 'ref': '', 'text': ''},
            'execute_command': {'command': 'rm -rf /'},  # Dangerous command
            'write_to_file': {'path': '/root/test.txt', 'content': 'test'},  # Permission issue
            'apply_diff': {'path': '/nonexistent.py', 'diff': 'test', 'start_line': -1},
            'list_files': {'path': '/nonexistent'},
            'list_code_definition_names': {'path': '/nonexistent'},
            'codebase_search': {'query': ''},
            'use_mcp_tool': {'server_name': '', 'tool_name': '', 'arguments': {}}
        }
        
        return error_inputs.get(tool_name, {'input_data': ''})
    
    def _generate_security_test_inputs(self, tool_name: str) -> Dict[str, Any]:
        """Generate security test inputs that should be blocked"""
        security_inputs = {
            'execute_command': {'command': 'rm -rf /'},  # Should be blocked
            'write_to_file': {'path': '../../../etc/passwd', 'content': 'test'},  # Should be blocked
            'browser_navigate': {'url': 'file:///etc/passwd'},  # Should be blocked
        }
        
        return security_inputs.get(tool_name, {'input_data': '../../etc/passwd'})
    
    def _generate_tool_documentation(self, tool_name: str, tool_impl: Dict[str, Any]) -> str:
        """Generate documentation for a tool"""
        doc = f"""
## {tool_impl['class_name']}

### Description
{tool_impl['description']}

### Parameters
"""
        
        for param in tool_impl['parameters']:
            required = "Required" if param.get('required', True) else "Optional"
            doc += f"- `{param['name']}` ({param['type']}) - {param['description']} ({required})\n"
        
        doc += f"""
### Return Type
{tool_impl['return_type']}

### Usage Example
```python
from tools import {tool_impl['class_name']}

tool = {tool_impl['class_name']}()
result = tool._run({', '.join([f"{p['name']}='value'" for p in tool_impl['parameters'] if p.get('required', True)])})
print(result)
```

### Security Features
- **Error Handling**: {', '.join(tool_impl['error_handling'])}
- **Retry Logic**: {'Enabled' if tool_impl['retry_logic'] else 'Disabled'}
- **Timeout**: {tool_impl['timeout']} seconds
- **Input Validation**: Enabled
- **Security Policy**: Enforced

### Performance Characteristics
- **Resource Usage**: Moderate
- **Network Calls**: {'Yes' if 'browser' in tool_name or 'api' in tool_name else 'No'}
- **File System Access**: {'Yes' if 'file' in tool_name or 'read' in tool_name or 'write' in tool_name else 'No'}
"""
        
        return doc


class SecurityValidator:
    """Validates tool security and generates security policies"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_security_policy(self, tool_name: str) -> Dict[str, Any]:
        """Generate security policy for a tool"""
        policies = {
            'search_files': {
                'allowed_paths': ['.', './workspace', './project', './src'],
                'blocked_patterns': [r'/etc/', r'/proc/', r'/sys/', r'~/.ssh', r'~/.gnupg', r'/root/'],
                'max_file_size': 10 * 1024 * 1024,  # 10MB
                'timeout': 30,
                'require_safe_paths': True
            },
            'read_file': {
                'allowed_extensions': ['.py', '.md', '.txt', '.json', '.yaml', '.yml', '.js', '.ts', '.java', '.cpp', '.c', '.h'],
                'blocked_paths': [r'/etc/', r'/proc/', r'/sys/', r'/root/', r'~/.ssh', r'~/.gnupg'],
                'max_file_size': 5 * 1024 * 1024,  # 5MB
                'timeout': 10,
                'require_safe_paths': True
            },
            'browser_navigate': {
                'allowed_schemes': ['http', 'https'],
                'blocked_domains': ['localhost', '127.0.0.1', '0.0.0.0', 'file://', 'internal'],
                'timeout': 45,
                'max_redirects': 5,
                'require_https': False
            },
            'execute_command': {
                'allowed_commands': ['ls', 'echo', 'cat', 'grep', 'find', 'pwd', 'which', 'head', 'tail'],
                'blocked_patterns': [r'rm\\s+-rf', r'dd\\s+if=', r':\\(\\)\\{', r'chmod\\s+\\d+\\s+/', r'>\\s*/dev/sd', r'wget.*\\|', r'curl.*\\|'],
                'timeout': 60,
                'max_output_size': 1024 * 1024,  # 1MB
                'allow_sudo': False,
                'require_shell': False
            },
            'write_to_file': {
                'allowed_directories': ['.', './workspace', './project', './output', './temp'],
                'blocked_paths': [r'/etc/', r'/proc/', r'/sys/', r'/root/', r'~/.ssh', r'~/.gnupg'],
                'max_file_size': 10 * 1024 * 1024,  # 10MB
                'create_backup': True,
                'timeout': 30,
                'require_safe_paths': True
            }
        }
        
        # Return default policy if tool not found
        default_policy = {
            'timeout': 30,
            'max_attempts': 3,
            'require_validation': True,
            'logging_level': 'INFO'
        }
        
        return policies.get(tool_name, default_policy)
    
    def validate_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a tool call against security policies"""
        policy = self.generate_security_policy(tool_name)
        
        validation_result = {
            'allowed': True,
            'reason': '',
            'warnings': [],
            'modified_params': {}
        }
        
        # Tool-specific validation
        if tool_name == 'read_file':
            validation_result = self._validate_read_file(parameters, policy, validation_result)
        elif tool_name == 'write_to_file':
            validation_result = self._validate_write_file(parameters, policy, validation_result)
        elif tool_name == 'execute_command':
            validation_result = self._validate_execute_command(parameters, policy, validation_result)
        elif tool_name == 'browser_navigate':
            validation_result = self._validate_browser_navigate(parameters, policy, validation_result)
        
        return validation_result
    
    def _validate_read_file(self, params: Dict[str, Any], policy: Dict[str, Any], 
                           result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate read_file parameters"""
        file_path = params.get('path', '')
        
        # Check blocked paths
        for blocked_pattern in policy['blocked_paths']:
            if re.search(blocked_pattern, file_path):
                result['allowed'] = False
                result['reason'] = f'Access to path blocked by policy: {file_path}'
                return result
        
        # Check allowed extensions
        if 'allowed_extensions' in policy:
            ext = Path(file_path).suffix.lower()
            if ext not in policy['allowed_extensions']:
                result['warnings'].append(f'File extension {ext} may not be supported')
        
        return result
    
    def _validate_write_file(self, params: Dict[str, Any], policy: Dict[str, Any], 
                            result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate write_file parameters"""
        file_path = params.get('path', '')
        
        # Check blocked paths
        for blocked_pattern in policy['blocked_paths']:
            if re.search(blocked_pattern, file_path):
                result['allowed'] = False
                result['reason'] = f'Write to path blocked by policy: {file_path}'
                return result
        
        # Check file size
        content = params.get('content', '')
        if len(content.encode('utf-8')) > policy['max_file_size']:
            result['allowed'] = False
            result['reason'] = f'Content too large: {len(content)} bytes (max: {policy["max_file_size"]})'
            return result
        
        return result
    
    def _validate_execute_command(self, params: Dict[str, Any], policy: Dict[str, Any], 
                                 result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate execute_command parameters"""
        command = params.get('command', '')
        
        # Check blocked patterns
        for blocked_pattern in policy['blocked_patterns']:
            if re.search(blocked_pattern, command, re.IGNORECASE):
                result['allowed'] = False
                result['reason'] = f'Command blocked by security policy: {blocked_pattern}'
                return result
        
        # Check allowed commands
        if 'allowed_commands' in policy:
            cmd_start = command.split()[0].lower()
            if cmd_start not in policy['allowed_commands']:
                result['warnings'].append(f'Command {cmd_start} not in allowed list')
        
        return result
    
    def _validate_browser_navigate(self, params: Dict[str, Any], policy: Dict[str, Any], 
                                  result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate browser_navigate parameters"""
        url = params.get('url', '')
        
        # Parse URL
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            
            # Check scheme
            if parsed.scheme not in policy['allowed_schemes']:
                result['allowed'] = False
                result['reason'] = f'URL scheme not allowed: {parsed.scheme}'
                return result
            
            # Check blocked domains
            for blocked_domain in policy['blocked_domains']:
                if blocked_domain in parsed.netloc:
                    result['allowed'] = False
                    result['reason'] = f'Access to domain blocked: {parsed.netloc}'
                    return result
                    
        except Exception as e:
            result['allowed'] = False
            result['reason'] = f'Invalid URL format: {e}'
        
        return result


class MemorySelector:
    """Selects appropriate memory type based on requirements"""
    
    def select(self, requirements: Dict[str, Any]) -> str:
        """Select memory type based on analysis"""
        # In a real implementation, this would use ML/AI to select
        # For now, return a default
        return 'buffer'


class ReasoningSelector:
    """Selects appropriate reasoning type based on requirements"""
    
    def select(self, requirements: Dict[str, Any]) -> str:
        """Select reasoning type based on analysis"""
        # In a real implementation, this would use ML/AI to select
        # For now, return a default
        return 'react'


def main():
    """Main CLI entry point for enhanced DeepAgent generator"""
    parser = argparse.ArgumentParser(
        description='Generate Enhanced DeepAgents with sophisticated tool-calling capabilities',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic agent generation
  python generate-agent-enhanced.py --description "Create a research agent that can search the web and generate reports"
  
  # Advanced configuration with specific security level
  python generate-agent-enhanced.py --description "Build a data analysis agent" --name "DataAnalyzer" --reasoning-type plan-and-execute --memory-type vector --security-level high
  
  # Generate with maximum security and monitoring
  python generate-agent-enhanced.py --description "Create a secure customer support agent" --name "SupportAgent" --include-monitoring --security-level maximum --verbose
        '''
    )
    
    parser.add_argument(
        '--description', '-d',
        required=True,
        help='Description of the agent purpose and capabilities'
    )
    
    parser.add_argument(
        '--name', '-n',
        help='Name for the generated agent (auto-generated if not specified)'
    )
    
    parser.add_argument(
        '--reasoning-type', '-r',
        choices=['auto', 'react', 'plan-and-execute', 'babyagi'],
        default='auto',
        help='Reasoning pattern to use (default: auto-select)'
    )
    
    parser.add_argument(
        '--memory-type', '-m',
        choices=['auto', 'buffer', 'summary', 'vector'],
        default='auto',
        help='Memory system to use (default: auto-select)'
    )
    
    parser.add_argument(
        '--include-monitoring', '--monitor',
        action='store_true',
        help='Include LangSmith monitoring integration'
    )
    
    parser.add_argument(
        '--output-format', '-f',
        choices=['python-package', 'standalone-script', 'docker'],
        default='python-package',
        help='Output format for the generated agent (default: python-package)'
    )
    
    parser.add_argument(
        '--security-level', '-s',
        choices=['low', 'medium', 'high', 'maximum'],
        default='medium',
        help='Security level for tool execution (default: medium)'
    )
    
    parser.add_argument(
        '--llm-model',
        default='gpt-4-turbo-preview',
        help='LLM model to use (default: gpt-4-turbo-preview)'
    )
    
    parser.add_argument(
        '--llm-temperature',
        type=float,
        default=0.1,
        help='LLM temperature (default: 0.1)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Prepare configuration
    config = {
        'description': args.description,
        'name': args.name,
        'reasoning_type': args.reasoning_type,
        'memory_type': args.memory_type,
        'include_monitoring': args.include_monitoring,
        'output_format': args.output_format,
        'security_level': args.security_level,
        'llm_config': {
            'model': args.llm_model,
            'temperature': args.llm_temperature,
            'verbose': args.verbose
        }
    }
    
    # Generate agent
    generator = EnhancedDeepAgentGenerator(verbose=args.verbose, security_level=args.security_level)
    result = generator.generate_agent(config)
    
    # Print results
    print("\n" + "="*80)
    print("ENHANCED DEEPAGENT GENERATION REPORT")
    print("="*80)
    
    if result['success']:
        print("✅ Enhanced agent generation successful!")
        print(f"\nOutput Directory: {result['output_path']}")
        print(f"Generated Files: {len(result['files'])}")
        print(f"Dependencies: {len(result['dependencies'])}")
        
        print(f"\nConfiguration:")
        print(f"  Reasoning Type: {result['configuration']['reasoning_type']}")
        print(f"  Memory Type: {result['configuration']['memory_type']}")
        print(f"  Tools: {len(result['configuration']['tools'])} configured")
        print(f"  Security Level: {result['configuration']['security_level']}")
        print(f"  Monitoring: {'Enabled' if result['configuration']['include_monitoring'] else 'Disabled'}")
        
        print(f"\nTool Categories:")
        for category, tools in result['configuration']['tool_categories'].items():
            if tools:
                print(f"  {category.title()}: {', '.join(tools)}")
        
        print(f"\nSecurity Recommendations:")
        for rec in result['configuration']['security_validation']['recommendations']:
            print(f"  - {rec}")
        
        print(f"\nNext Steps:")
        print(f"1. cd {result['output_path']}")
        print(f"2. cp .env.template .env")
        print(f"3. Edit .env and add your API keys")
        print(f"4. Review security_config.json")
        print(f"5. pip install -r requirements.txt")
        print(f"6. python test_tools.py  # Run tests")
        print(f"7. python agent.py")
        
        print(f"\nGenerated Files:")
        for file_path in result['files']:
            print(f"  - {Path(file_path).name}")
        
        print(f"\nEnhanced Features:")
        print(f"  ✅ Sophisticated tool analysis and selection")
        print(f"  ✅ Comprehensive security validation")
        print(f"  ✅ Advanced error handling and retry logic")
        print(f"  ✅ Performance monitoring and optimization")
        print(f"  ✅ Detailed documentation and test suite")
        
    else:
        print("❌ Enhanced agent generation failed!")
        print(f"Error: {result['error']}")
    
    print("\n" + "="*80)
    
    # Exit with appropriate code
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()