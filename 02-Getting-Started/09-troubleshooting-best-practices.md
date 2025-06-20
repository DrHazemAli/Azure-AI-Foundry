# Troubleshooting and Best Practices

## Overview

This final lesson in the Getting Started module covers essential troubleshooting techniques, common issues, and best practices for developing and maintaining Azure AI Foundry applications.

## Learning Objectives

- Identify and resolve common Azure AI Foundry issues
- Implement debugging strategies and diagnostic tools
- Follow development and deployment best practices
- Establish maintenance and monitoring procedures
- Understand security and compliance requirements
- Create documentation and knowledge management systems

## Prerequisites

- Completed monitoring and optimization (Lesson 08)
- Experience with Azure AI Foundry application development
- Understanding of software development lifecycle concepts

---

## 1. Common Issues and Solutions

### Authentication and Access Issues

**Problem: Authentication Failed Errors**
```python
# Common authentication issues and solutions

class AuthenticationTroubleshooter:
    @staticmethod
    def diagnose_auth_issue(error_message: str) -> dict:
        """Diagnose authentication issues based on error message."""
        
        issues = {
            "401 Unauthorized": {
                "cause": "Invalid or expired credentials",
                "solutions": [
                    "Verify API key is correct and active",
                    "Check if key has been regenerated recently",
                    "Ensure proper authentication method is used",
                    "Verify endpoint URL is correct"
                ],
                "commands": [
                    "az account show",
                    "az cognitiveservices account keys list --name <service-name> --resource-group <rg-name>"
                ]
            },
            "403 Forbidden": {
                "cause": "Insufficient permissions",
                "solutions": [
                    "Check user/service principal permissions",
                    "Verify resource access policies",
                    "Ensure proper RBAC roles assigned",
                    "Check network access rules"
                ],
                "commands": [
                    "az role assignment list --assignee <user-id>",
                    "az cognitiveservices account show --name <service-name>"
                ]
            },
            "Key not found": {
                "cause": "Missing or incorrect environment variables",
                "solutions": [
                    "Set AZURE_AI_FOUNDRY_API_KEY environment variable",
                    "Set AZURE_AI_FOUNDRY_ENDPOINT environment variable",
                    "Check .env file configuration",
                    "Verify environment variable loading"
                ],
                "commands": [
                    "echo $AZURE_AI_FOUNDRY_API_KEY",
                    "echo $AZURE_AI_FOUNDRY_ENDPOINT"
                ]
            }
        }
        
        for error_pattern, details in issues.items():
            if error_pattern.lower() in error_message.lower():
                return details
        
        return {
            "cause": "Unknown authentication issue",
            "solutions": [
                "Check Azure portal for service status",
                "Verify all configuration settings",
                "Review Azure AI Foundry documentation",
                "Contact support if issue persists"
            ]
        }

    @staticmethod
    def test_authentication():
        """Test authentication configuration."""
        
        import os
        from azure.identity import DefaultAzureCredential, ClientSecretCredential
        
        checks = []
        
        # Check environment variables
        endpoint = os.getenv('AZURE_AI_FOUNDRY_ENDPOINT')
        api_key = os.getenv('AZURE_AI_FOUNDRY_API_KEY')
        
        checks.append({
            "test": "Environment Variables",
            "passed": bool(endpoint and api_key),
            "details": f"Endpoint: {'✓' if endpoint else '✗'}, API Key: {'✓' if api_key else '✗'}"
        })
        
        # Test credential creation
        try:
            credential = DefaultAzureCredential()
            checks.append({
                "test": "Default Credential",
                "passed": True,
                "details": "Successfully created DefaultAzureCredential"
            })
        except Exception as e:
            checks.append({
                "test": "Default Credential", 
                "passed": False,
                "details": str(e)
            })
        
        return checks

# Example usage
troubleshooter = AuthenticationTroubleshooter()
auth_results = troubleshooter.test_authentication()

for result in auth_results:
    status = "✅" if result["passed"] else "❌"
    print(f"{status} {result['test']}: {result['details']}")
```

### Network and Connectivity Issues

**Problem: Connection Timeouts and Network Errors**
```python
import asyncio
import aiohttp
import time
from typing import Dict, List
import socket

class NetworkDiagnostics:
    @staticmethod
    async def test_endpoint_connectivity(endpoint: str) -> Dict:
        """Test connectivity to Azure AI Foundry endpoint."""
        
        results = {
            "endpoint": endpoint,
            "dns_resolution": False,
            "tcp_connection": False,
            "http_response": False,
            "latency_ms": None,
            "errors": []
        }
        
        try:
            # Test DNS resolution
            import urllib.parse
            parsed = urllib.parse.urlparse(endpoint)
            hostname = parsed.hostname
            
            socket.gethostbyname(hostname)
            results["dns_resolution"] = True
            
        except Exception as e:
            results["errors"].append(f"DNS resolution failed: {e}")
        
        try:
            # Test HTTP connectivity
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    results["http_response"] = True
                    results["tcp_connection"] = True
                    results["latency_ms"] = (time.time() - start_time) * 1000
                    results["status_code"] = response.status
                    
        except asyncio.TimeoutError:
            results["errors"].append("Connection timeout")
        except aiohttp.ClientError as e:
            results["errors"].append(f"HTTP client error: {e}")
        except Exception as e:
            results["errors"].append(f"Connection error: {e}")
        
        return results
    
    @staticmethod
    def check_firewall_rules():
        """Check common firewall and network issues."""
        
        checks = [
            {
                "description": "Outbound HTTPS (443) access",
                "required": "Access to *.cognitiveservices.azure.com on port 443",
                "check_command": "telnet <endpoint> 443"
            },
            {
                "description": "Corporate proxy settings",
                "required": "Configure proxy if behind corporate firewall",
                "check_command": "echo $HTTP_PROXY && echo $HTTPS_PROXY"
            },
            {
                "description": "DNS resolution",
                "required": "Resolve Azure service DNS names",
                "check_command": "nslookup <your-service>.cognitiveservices.azure.com"
            }
        ]
        
        return checks

# Usage example
async def diagnose_network_issues():
    diagnostics = NetworkDiagnostics()
    
    endpoint = "https://your-service.cognitiveservices.azure.com"
    results = await diagnostics.test_endpoint_connectivity(endpoint)
    
    print(f"Connectivity Test for {endpoint}:")
    print(f"✅ DNS Resolution: {results['dns_resolution']}")
    print(f"✅ TCP Connection: {results['tcp_connection']}")
    print(f"✅ HTTP Response: {results['http_response']}")
    
    if results['latency_ms']:
        print(f"🚀 Latency: {results['latency_ms']:.2f}ms")
    
    if results['errors']:
        print("❌ Errors:")
        for error in results['errors']:
            print(f"   - {error}")

# Run diagnostics
# asyncio.run(diagnose_network_issues())
```

### Model and Response Issues

**Problem: Poor Model Performance or Unexpected Responses**
```python
from dataclasses import dataclass
from typing import List, Dict, Any
import json

@dataclass
class ModelDiagnostic:
    test_name: str
    input_prompt: str
    expected_behavior: str
    actual_response: str
    parameters: Dict[str, Any]
    passed: bool
    issues: List[str]

class ModelTroubleshooter:
    def __init__(self):
        self.diagnostic_tests = [
            {
                "name": "Basic Functionality",
                "prompt": "What is 2 + 2?",
                "expected": "Should return 4 or simple arithmetic",
                "parameters": {"temperature": 0.1, "max_tokens": 50}
            },
            {
                "name": "System Message Adherence",
                "prompt": "What's your role?",
                "expected": "Should reflect configured system message",
                "parameters": {"temperature": 0.3, "max_tokens": 100}
            },
            {
                "name": "Context Handling",
                "prompt": "Remember this number: 42. What number did I just tell you?",
                "expected": "Should remember and return 42",
                "parameters": {"temperature": 0.1, "max_tokens": 50}
            },
            {
                "name": "Response Length Control",
                "prompt": "Explain machine learning",
                "expected": "Should respect max_tokens limit",
                "parameters": {"temperature": 0.7, "max_tokens": 100}
            }
        ]
    
    async def run_diagnostics(self, ai_client) -> List[ModelDiagnostic]:
        """Run comprehensive model diagnostics."""
        
        results = []
        
        for test in self.diagnostic_tests:
            try:
                response = await ai_client.send_message(
                    test["prompt"],
                    **test["parameters"]
                )
                
                # Analyze response
                issues = self._analyze_response(response, test)
                
                diagnostic = ModelDiagnostic(
                    test_name=test["name"],
                    input_prompt=test["prompt"],
                    expected_behavior=test["expected"],
                    actual_response=response,
                    parameters=test["parameters"],
                    passed=len(issues) == 0,
                    issues=issues
                )
                
                results.append(diagnostic)
                
            except Exception as e:
                diagnostic = ModelDiagnostic(
                    test_name=test["name"],
                    input_prompt=test["prompt"],
                    expected_behavior=test["expected"],
                    actual_response="",
                    parameters=test["parameters"],
                    passed=False,
                    issues=[f"Exception: {str(e)}"]
                )
                results.append(diagnostic)
        
        return results
    
    def _analyze_response(self, response: str, test: Dict) -> List[str]:
        """Analyze response for potential issues."""
        
        issues = []
        
        # Check if response is empty
        if not response.strip():
            issues.append("Empty response received")
        
        # Check response length vs max_tokens
        if len(response.split()) > test["parameters"].get("max_tokens", 1000):
            issues.append("Response exceeds max_tokens limit")
        
        # Test-specific checks
        if test["name"] == "Basic Functionality":
            if "4" not in response:
                issues.append("Failed basic arithmetic test")
        
        elif test["name"] == "Context Handling":
            if "42" not in response:
                issues.append("Failed to maintain context")
        
        # Check for common response issues
        if "I'm sorry" in response and "error" in response.lower():
            issues.append("Model returned error message")
        
        if len(response) < 10:
            issues.append("Response too short, may indicate truncation")
        
        return issues
    
    def generate_troubleshooting_report(self, diagnostics: List[ModelDiagnostic]) -> str:
        """Generate a comprehensive troubleshooting report."""
        
        report = "# Azure AI Foundry Model Diagnostics Report\n\n"
        
        passed_tests = sum(1 for d in diagnostics if d.passed)
        total_tests = len(diagnostics)
        
        report += f"## Summary\n"
        report += f"- Tests Passed: {passed_tests}/{total_tests}\n"
        report += f"- Success Rate: {(passed_tests/total_tests)*100:.1f}%\n\n"
        
        for diagnostic in diagnostics:
            status = "✅ PASS" if diagnostic.passed else "❌ FAIL"
            report += f"## {diagnostic.test_name} - {status}\n\n"
            report += f"**Input:** {diagnostic.input_prompt}\n\n"
            report += f"**Expected:** {diagnostic.expected_behavior}\n\n"
            report += f"**Response:** {diagnostic.actual_response}\n\n"
            report += f"**Parameters:** {json.dumps(diagnostic.parameters, indent=2)}\n\n"
            
            if diagnostic.issues:
                report += "**Issues Found:**\n"
                for issue in diagnostic.issues:
                    report += f"- {issue}\n"
                report += "\n"
        
        # Add recommendations
        report += "## Recommendations\n\n"
        
        all_issues = [issue for d in diagnostics for issue in d.issues]
        
        if any("empty response" in issue.lower() for issue in all_issues):
            report += "- Check system message configuration\n"
            report += "- Verify prompt formatting\n"
            report += "- Increase max_tokens parameter\n\n"
        
        if any("context" in issue.lower() for issue in all_issues):
            report += "- Review conversation history management\n"
            report += "- Check message formatting and ordering\n\n"
        
        if any("exceeds" in issue.lower() for issue in all_issues):
            report += "- Adjust max_tokens parameter\n"
            report += "- Optimize prompt length\n\n"
        
        return report

# Usage example
# troubleshooter = ModelTroubleshooter()
# diagnostics = await troubleshooter.run_diagnostics(your_ai_client)
# report = troubleshooter.generate_troubleshooting_report(diagnostics)
# print(report)
```

---

## 2. Debugging Strategies

### Comprehensive Logging and Debugging

```python
import logging
import json
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps

class DebugConfig:
    def __init__(self):
        self.log_level = logging.DEBUG
        self.log_requests = True
        self.log_responses = True
        self.log_errors = True
        self.log_performance = True
        self.sensitive_fields = ['api_key', 'password', 'token']

class AzureAIFoundryDebugger:
    def __init__(self, config: DebugConfig = None):
        self.config = config or DebugConfig()
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up comprehensive logging."""
        
        logger = logging.getLogger('azure_ai_foundry_debug')
        logger.setLevel(self.config.log_level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler
        file_handler = logging.FileHandler('azure_ai_foundry_debug.log')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
    
    def _sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove sensitive information from logged data."""
        
        if not isinstance(data, dict):
            return data
        
        sanitized = {}
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in self.config.sensitive_fields):
                sanitized[key] = "***REDACTED***"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_data(value)
            else:
                sanitized[key] = value
        
        return sanitized
    
    def debug_decorator(self, function_name: str = None):
        """Decorator for debugging function calls."""
        
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                func_name = function_name or func.__name__
                start_time = datetime.now()
                
                # Log function entry
                self.logger.debug(f"Entering {func_name}")
                
                if self.config.log_requests:
                    sanitized_kwargs = self._sanitize_data(kwargs)
                    self.logger.debug(f"Arguments: {json.dumps(sanitized_kwargs, default=str, indent=2)}")
                
                try:
                    result = await func(*args, **kwargs)
                    
                    # Log successful completion
                    duration = (datetime.now() - start_time).total_seconds()
                    
                    if self.config.log_performance:
                        self.logger.debug(f"{func_name} completed in {duration:.3f}s")
                    
                    if self.config.log_responses:
                        # Log response (truncated if too long)
                        response_str = str(result)
                        if len(response_str) > 500:
                            response_str = response_str[:500] + "... (truncated)"
                        self.logger.debug(f"Response: {response_str}")
                    
                    return result
                    
                except Exception as e:
                    duration = (datetime.now() - start_time).total_seconds()
                    
                    if self.config.log_errors:
                        self.logger.error(f"{func_name} failed after {duration:.3f}s: {str(e)}")
                        self.logger.error(f"Traceback: {traceback.format_exc()}")
                    
                    raise
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                func_name = function_name or func.__name__
                start_time = datetime.now()
                
                self.logger.debug(f"Entering {func_name}")
                
                try:
                    result = func(*args, **kwargs)
                    duration = (datetime.now() - start_time).total_seconds()
                    self.logger.debug(f"{func_name} completed in {duration:.3f}s")
                    return result
                    
                except Exception as e:
                    duration = (datetime.now() - start_time).total_seconds()
                    self.logger.error(f"{func_name} failed after {duration:.3f}s: {str(e)}")
                    raise
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        
        return decorator
    
    def log_request_response(self, request_data: Dict, response_data: Dict, duration_ms: float):
        """Log detailed request/response information."""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "duration_ms": duration_ms,
            "request": self._sanitize_data(request_data),
            "response": {
                "success": "error" not in response_data,
                "length": len(str(response_data.get("content", ""))),
                "tokens_used": response_data.get("usage", {}).get("total_tokens", 0)
            }
        }
        
        if "error" in response_data:
            log_entry["response"]["error"] = response_data["error"]
        
        self.logger.info(f"Request/Response: {json.dumps(log_entry, indent=2)}")
    
    def create_debug_session(self, session_id: str) -> 'DebugSession':
        """Create a debug session for tracking related operations."""
        return DebugSession(session_id, self)

class DebugSession:
    def __init__(self, session_id: str, debugger: AzureAIFoundryDebugger):
        self.session_id = session_id
        self.debugger = debugger
        self.start_time = datetime.now()
        self.operations = []
    
    def log_operation(self, operation: str, details: Dict[str, Any]):
        """Log an operation within this debug session."""
        
        operation_data = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": self.debugger._sanitize_data(details),
            "session_duration_s": (datetime.now() - self.start_time).total_seconds()
        }
        
        self.operations.append(operation_data)
        self.debugger.logger.debug(f"Session {self.session_id} - {operation}: {json.dumps(details, default=str)}")
    
    def export_session_log(self) -> str:
        """Export complete session log."""
        
        session_summary = {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "duration_s": (datetime.now() - self.start_time).total_seconds(),
            "operation_count": len(self.operations),
            "operations": self.operations
        }
        
        filename = f"debug_session_{self.session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(session_summary, f, indent=2, default=str)
        
        return filename

# Usage example
debugger = AzureAIFoundryDebugger()

# Use as decorator
@debugger.debug_decorator("send_ai_message")
async def send_message_with_debug(message: str):
    # Your AI client code here
    pass

# Use debug session
debug_session = debugger.create_debug_session("user_interaction_001")
debug_session.log_operation("user_message", {"message": "Hello", "user_id": "123"})
```

---

## 3. Development Best Practices

### Code Organization and Structure

```python
# Best practices for Azure AI Foundry application structure

"""
Recommended Project Structure:

azure_ai_app/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── client.py          # Azure AI Foundry client wrapper
│   │   ├── config.py          # Configuration management
│   │   └── exceptions.py      # Custom exceptions
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py    # Chat-specific logic
│   │   ├── prompt_service.py  # Prompt management
│   │   └── monitoring.py      # Monitoring and logging
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chat_models.py     # Data models
│   │   └── config_models.py   # Configuration models
│   └── utils/
│       ├── __init__.py
│       ├── validators.py      # Input validation
│       └── helpers.py         # Utility functions
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── config/
│   ├── development.yaml
│   ├── production.yaml
│   └── test.yaml
├── docs/
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
└── README.md
"""

# Example configuration management
from dataclasses import dataclass
from typing import Optional, Dict, Any
import os
import yaml

@dataclass
class AzureAIConfig:
    """Centralized configuration management."""
    
    # Azure AI Foundry settings
    endpoint: str
    api_key: Optional[str] = None
    deployment_name: str = "gpt-4"
    api_version: str = "2024-02-15-preview"
    
    # Application settings
    environment: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    
    # Performance settings
    max_tokens: int = 1000
    temperature: float = 0.7
    timeout_seconds: int = 30
    max_retries: int = 3
    
    # Security settings
    enable_content_filter: bool = True
    allowed_origins: list = None
    
    @classmethod
    def from_env(cls) -> 'AzureAIConfig':
        """Create configuration from environment variables."""
        return cls(
            endpoint=os.getenv('AZURE_AI_FOUNDRY_ENDPOINT', ''),
            api_key=os.getenv('AZURE_AI_FOUNDRY_API_KEY'),
            deployment_name=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
            environment=os.getenv('ENVIRONMENT', 'development'),
            debug=os.getenv('DEBUG', 'false').lower() == 'true',
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            max_tokens=int(os.getenv('MAX_TOKENS', '1000')),
            temperature=float(os.getenv('TEMPERATURE', '0.7')),
            timeout_seconds=int(os.getenv('TIMEOUT_SECONDS', '30')),
            max_retries=int(os.getenv('MAX_RETRIES', '3'))
        )
    
    @classmethod
    def from_yaml(cls, config_path: str) -> 'AzureAIConfig':
        """Create configuration from YAML file."""
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        return cls(**config_data)
    
    def validate(self) -> None:
        """Validate configuration settings."""
        if not self.endpoint:
            raise ValueError("Azure AI Foundry endpoint is required")
        
        if not self.api_key:
            raise ValueError("API key is required")
        
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")

# Example custom exceptions
class AzureAIFoundryError(Exception):
    """Base exception for Azure AI Foundry related errors."""
    pass

class AuthenticationError(AzureAIFoundryError):
    """Raised when authentication fails."""
    pass

class RateLimitError(AzureAIFoundryError):
    """Raised when rate limit is exceeded."""
    pass

class ValidationError(AzureAIFoundryError):
    """Raised when input validation fails."""
    pass

# Example client wrapper with best practices
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential
import asyncio
import logging

class AzureAIFoundryClient:
    """Production-ready Azure AI Foundry client wrapper."""
    
    def __init__(self, config: AzureAIConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Azure AI client with proper error handling."""
        try:
            if self.config.api_key:
                from azure.core.credentials import AzureKeyCredential
                credential = AzureKeyCredential(self.config.api_key)
            else:
                credential = DefaultAzureCredential()
            
            self._client = ChatCompletionsClient(
                endpoint=self.config.endpoint,
                credential=credential
            )
            
            self.logger.info("Azure AI Foundry client initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Azure AI client: {e}")
            raise AuthenticationError(f"Client initialization failed: {e}")
    
    async def send_message(self, message: str, **kwargs) -> str:
        """Send message with comprehensive error handling."""
        
        if not message.strip():
            raise ValidationError("Message cannot be empty")
        
        try:
            response = await self._client.complete(
                messages=[{"role": "user", "content": message}],
                model=self.config.deployment_name,
                max_tokens=kwargs.get('max_tokens', self.config.max_tokens),
                temperature=kwargs.get('temperature', self.config.temperature)
            )
            
            if response and response.choices:
                return response.choices[0].message.content
            else:
                raise AzureAIFoundryError("Empty response received")
                
        except Exception as e:
            self.logger.error(f"Message send failed: {e}")
            
            # Re-raise with appropriate exception type
            if "401" in str(e) or "authentication" in str(e).lower():
                raise AuthenticationError(f"Authentication failed: {e}")
            elif "429" in str(e) or "rate limit" in str(e).lower():
                raise RateLimitError(f"Rate limit exceeded: {e}")
            else:
                raise AzureAIFoundryError(f"Request failed: {e}")
```

### Testing Strategies

```python
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from src.core.client import AzureAIFoundryClient
from src.core.config import AzureAIConfig

class TestAzureAIFoundryClient:
    """Comprehensive test suite for Azure AI Foundry client."""
    
    @pytest.fixture
    def mock_config(self):
        """Create mock configuration for testing."""
        return AzureAIConfig(
            endpoint="https://test.cognitiveservices.azure.com",
            api_key="test_key",
            deployment_name="gpt-4-test",
            max_tokens=100,
            temperature=0.5
        )
    
    @pytest.fixture
    def mock_client(self, mock_config):
        """Create client with mocked Azure SDK."""
        with patch('src.core.client.ChatCompletionsClient'):
            client = AzureAIFoundryClient(mock_config)
            return client
    
    @pytest.mark.asyncio
    async def test_successful_message_send(self, mock_client):
        """Test successful message sending."""
        
        # Mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        
        mock_client._client.complete = AsyncMock(return_value=mock_response)
        
        # Test
        result = await mock_client.send_message("Test message")
        
        assert result == "Test response"
        mock_client._client.complete.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_empty_message_validation(self, mock_client):
        """Test validation of empty messages."""
        
        with pytest.raises(ValidationError):
            await mock_client.send_message("")
        
        with pytest.raises(ValidationError):
            await mock_client.send_message("   ")
    
    @pytest.mark.asyncio
    async def test_authentication_error_handling(self, mock_client):
        """Test authentication error handling."""
        
        mock_client._client.complete = AsyncMock(
            side_effect=Exception("401 Unauthorized")
        )
        
        with pytest.raises(AuthenticationError):
            await mock_client.send_message("Test message")
    
    @pytest.mark.asyncio
    async def test_rate_limit_error_handling(self, mock_client):
        """Test rate limit error handling."""
        
        mock_client._client.complete = AsyncMock(
            side_effect=Exception("429 Rate limit exceeded")
        )
        
        with pytest.raises(RateLimitError):
            await mock_client.send_message("Test message")
    
    def test_config_validation(self):
        """Test configuration validation."""
        
        # Valid config should not raise
        valid_config = AzureAIConfig(
            endpoint="https://test.cognitiveservices.azure.com",
            api_key="test_key"
        )
        valid_config.validate()  # Should not raise
        
        # Invalid endpoint should raise
        with pytest.raises(ValueError, match="endpoint is required"):
            invalid_config = AzureAIConfig(endpoint="", api_key="test_key")
            invalid_config.validate()
        
        # Invalid temperature should raise
        with pytest.raises(ValueError, match="temperature must be"):
            invalid_config = AzureAIConfig(
                endpoint="https://test.cognitiveservices.azure.com",
                api_key="test_key",
                temperature=3.0
            )
            invalid_config.validate()

# Integration tests
class TestAzureAIFoundryIntegration:
    """Integration tests requiring live Azure AI Foundry service."""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_live_service_connection(self):
        """Test connection to live Azure AI Foundry service."""
        
        # Skip if no live credentials
        config = AzureAIConfig.from_env()
        if not config.endpoint or not config.api_key:
            pytest.skip("Live credentials not available")
        
        client = AzureAIFoundryClient(config)
        
        # Test simple message
        response = await client.send_message("Hello, this is a test message.")
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_error_scenarios(self):
        """Test various error scenarios with live service."""
        
        # Test with invalid API key
        invalid_config = AzureAIConfig(
            endpoint="https://test.cognitiveservices.azure.com",
            api_key="invalid_key"
        )
        
        client = AzureAIFoundryClient(invalid_config)
        
        with pytest.raises(AuthenticationError):
            await client.send_message("Test message")

# Performance tests
class TestPerformance:
    """Performance and load testing."""
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, mock_client):
        """Test handling of concurrent requests."""
        
        # Mock successful responses
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        
        mock_client._client.complete = AsyncMock(return_value=mock_response)
        
        # Send 10 concurrent requests
        tasks = []
        for i in range(10):
            task = mock_client.send_message(f"Test message {i}")
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 10
        assert all(result == "Test response" for result in results)
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_response_time_benchmark(self, mock_client):
        """Benchmark response times."""
        
        import time
        
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        
        # Add small delay to simulate network latency
        async def mock_complete(*args, **kwargs):
            await asyncio.sleep(0.1)  # 100ms simulated latency
            return mock_response
        
        mock_client._client.complete = mock_complete
        
        start_time = time.time()
        result = await mock_client.send_message("Performance test")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert result == "Test response"
        assert response_time < 0.2  # Should complete within 200ms
```

---

## Summary

This final lesson in Module 02 covered essential troubleshooting and best practices:

- **Common Issues**: Authentication, network, and model performance problems
- **Debugging Strategies**: Comprehensive logging and diagnostic tools
- **Development Best Practices**: Code organization, configuration management, and error handling
- **Testing Strategies**: Unit, integration, and performance testing approaches

## Module 02 Completion

Congratulations! You have completed Module 02 - Getting Started with Azure AI Foundry. You now have:

- ✅ Set up Azure AI Foundry service and development environment
- ✅ Created your first AI application with proper configuration
- ✅ Learned navigation and portal features
- ✅ Mastered model selection and deployment strategies
- ✅ Implemented customization and configuration options
- ✅ Set up monitoring, optimization, and troubleshooting

## Next Steps

- **Module 03**: Projects and Workflows - Learn advanced project management
- **Module 04**: Service Overview - Deep dive into Azure AI Foundry services
- **Module 05**: SDK Guide - Master the Azure AI Foundry SDKs
- **Module 06**: Building AI Agents - Create sophisticated AI agents

---

*This lesson completes Module 02 of the Azure AI Foundry Zero-to-Hero course.* 