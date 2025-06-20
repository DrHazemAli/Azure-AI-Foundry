# Lesson 2: Development Workflows and Methodologies

## Learning Objectives

By the end of this lesson, you will be able to:
- Implement agile development methodologies for AI projects
- Design effective sprint planning and backlog management processes
- Establish code review and quality assurance workflows
- Create testing strategies specific to AI applications
- Set up documentation and knowledge management systems
- Manage AI model development lifecycle within agile frameworks

## Overview

Developing AI applications requires specialized workflows that account for the unique challenges of machine learning development, model testing, and iterative improvement. This lesson explores proven methodologies and workflows specifically adapted for Azure AI Foundry projects.

---

## 1. Agile Methodologies for AI Development

### AI-Adapted Scrum Framework

Traditional Scrum needs adaptation for AI development due to the experimental nature of machine learning and the uncertainty in AI project outcomes.

#### AI Scrum Components

**Roles:**
- **Product Owner**: Defines business requirements and AI success metrics
- **AI Scrum Master**: Facilitates AI-specific ceremonies and removes blockers
- **Development Team**: Includes AI engineers, data scientists, and traditional developers
- **AI Ethics Officer**: Ensures responsible AI practices (for larger teams)

**Artifacts:**
- **Product Backlog**: User stories with AI-specific acceptance criteria
- **Sprint Backlog**: Includes model experiments and data tasks
- **AI Model Registry**: Tracks model versions and performance metrics
- **Experiment Log**: Documents AI experiments and results

#### Sprint Structure for AI Projects

```
Sprint Planning (Day 1)
├── Story Estimation with AI Uncertainty
├── Experiment Planning
├── Data Requirements Review
└── Model Performance Goals

Sprint Development (Days 2-13)
├── Week 1: Data Preparation & Model Development
├── Week 2: Testing, Validation & Integration
└── Continuous: Experiment Tracking

Sprint Review (Day 14)
├── Demo Working Features
├── Review Model Performance
├── Stakeholder Feedback
└── Ethics and Bias Review

Sprint Retrospective (Day 14)
├── Technical Challenges Review
├── Data Quality Issues
├── Model Performance Analysis
└── Process Improvements
```

### Kanban for AI Projects

Kanban can be particularly effective for AI projects due to the iterative and experimental nature of the work.

#### AI Kanban Board Structure

```
Backlog → Data Prep → Modeling → Testing → Integration → Done
    ↓         ↓          ↓         ↓           ↓        ↓
 Stories   Data      Model    Model      Code     Released
           Ready     Ready    Valid     Ready     Features
```

#### Kanban Metrics for AI

```python
class AIKanbanMetrics:
    def __init__(self):
        self.metrics = {
            "lead_time": [],
            "cycle_time": [],
            "model_accuracy": [],
            "experiment_success_rate": [],
            "data_quality_score": []
        }
    
    def track_story_completion(self, story_id: str, start_time: datetime, 
                             end_time: datetime, model_accuracy: float):
        """Track completion metrics for AI stories"""
        lead_time = (end_time - start_time).total_seconds() / 3600  # hours
        self.metrics["lead_time"].append(lead_time)
        self.metrics["model_accuracy"].append(model_accuracy)
    
    def calculate_velocity(self, sprint_stories: List[dict]) -> dict:
        """Calculate AI-specific velocity metrics"""
        completed_stories = len([s for s in sprint_stories if s["status"] == "done"])
        avg_accuracy = sum([s["model_accuracy"] for s in sprint_stories if s.get("model_accuracy")]) / len(sprint_stories)
        
        return {
            "stories_completed": completed_stories,
            "average_model_accuracy": avg_accuracy,
            "experiments_conducted": len([s for s in sprint_stories if s["type"] == "experiment"])
        }
```

---

## 2. Sprint Planning for AI Projects

### Story Types for AI Development

#### Traditional User Stories
```
As a [user type], I want [functionality] so that [business value]

Example:
As a customer service agent, I want an AI assistant that can 
suggest responses to customer inquiries so that I can respond 
faster and more accurately.
```

#### AI Experiment Stories
```
As a [team], we want to [experiment] to [learn/validate]

Example:
As the development team, we want to experiment with different 
temperature settings for our chat model to determine the optimal 
balance between creativity and accuracy.
```

#### Data Stories
```
As a [stakeholder], we need [data capability] to [enable AI functionality]

Example:
As the product team, we need historical customer conversation 
data to train our sentiment analysis model for customer support.
```

### AI Sprint Planning Process

```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class StoryType(Enum):
    FEATURE = "feature"
    EXPERIMENT = "experiment"
    DATA = "data"
    INFRASTRUCTURE = "infrastructure"

@dataclass
class AIStory:
    id: str
    title: str
    story_type: StoryType
    description: str
    acceptance_criteria: List[str]
    estimated_effort: int  # story points
    model_accuracy_target: Optional[float] = None
    data_requirements: Optional[List[str]] = None
    experiment_hypothesis: Optional[str] = None
    
    def is_ready_for_sprint(self) -> bool:
        """Check if story meets Definition of Ready for AI projects"""
        basic_ready = (
            bool(self.description) and 
            bool(self.acceptance_criteria) and 
            self.estimated_effort > 0
        )
        
        if self.story_type == StoryType.EXPERIMENT:
            return basic_ready and bool(self.experiment_hypothesis)
        elif self.story_type == StoryType.FEATURE and self.model_accuracy_target:
            return basic_ready and bool(self.data_requirements)
        
        return basic_ready

class AISprintPlanning:
    def __init__(self, team_capacity: int, sprint_length: int = 14):
        self.team_capacity = team_capacity
        self.sprint_length = sprint_length
        self.velocity_history = []
    
    def plan_sprint(self, backlog: List[AIStory]) -> List[AIStory]:
        """Plan sprint considering AI-specific factors"""
        ready_stories = [story for story in backlog if story.is_ready_for_sprint()]
        
        # Prioritize stories based on AI project needs
        prioritized_stories = self._prioritize_stories(ready_stories)
        
        # Select stories for sprint considering capacity and dependencies
        sprint_stories = self._select_stories_for_sprint(prioritized_stories)
        
        return sprint_stories
    
    def _prioritize_stories(self, stories: List[AIStory]) -> List[AIStory]:
        """Prioritize stories with AI-specific considerations"""
        # Priority order: Data → Infrastructure → Experiments → Features
        priority_order = {
            StoryType.DATA: 1,
            StoryType.INFRASTRUCTURE: 2,
            StoryType.EXPERIMENT: 3,
            StoryType.FEATURE: 4
        }
        
        return sorted(stories, key=lambda s: priority_order[s.story_type])
    
    def _select_stories_for_sprint(self, stories: List[AIStory]) -> List[AIStory]:
        """Select stories that fit in sprint capacity"""
        selected_stories = []
        total_effort = 0
        
        for story in stories:
            if total_effort + story.estimated_effort <= self.team_capacity:
                selected_stories.append(story)
                total_effort += story.estimated_effort
            else:
                break
        
        return selected_stories
```

### Definition of Ready for AI Stories

Before including a story in a sprint, ensure it meets these criteria:

#### For Feature Stories:
- [ ] Clear business value defined
- [ ] Acceptance criteria include performance metrics
- [ ] Data requirements identified and available
- [ ] Model performance targets defined
- [ ] Ethical considerations reviewed

#### For Experiment Stories:
- [ ] Clear hypothesis stated
- [ ] Success/failure criteria defined
- [ ] Required data identified
- [ ] Experiment design reviewed
- [ ] Time-boxed duration set

#### For Data Stories:
- [ ] Data sources identified
- [ ] Data quality requirements defined
- [ ] Privacy and compliance requirements reviewed
- [ ] Data access permissions secured
- [ ] Data pipeline design approved

---

## 3. Code Review Workflows for AI Projects

### AI-Specific Code Review Checklist

#### Model Code Review Checklist

```python
class AICodeReviewChecklist:
    """Automated checks for AI code reviews"""
    
    @staticmethod
    def check_model_configuration(config: dict) -> List[str]:
        """Validate model configuration"""
        issues = []
        
        # Check for hardcoded values
        if not config.get("temperature"):
            issues.append("Temperature not configured")
        
        # Check for reasonable parameter ranges
        if config.get("temperature", 0) > 2.0:
            issues.append("Temperature too high (>2.0)")
        
        # Check for required parameters
        required_params = ["model", "max_tokens", "temperature"]
        for param in required_params:
            if param not in config:
                issues.append(f"Missing required parameter: {param}")
        
        return issues
    
    @staticmethod
    def check_data_handling(code: str) -> List[str]:
        """Check for proper data handling practices"""
        issues = []
        
        # Check for PII handling
        if "personal" in code.lower() and "encrypt" not in code.lower():
            issues.append("Potential PII handling without encryption")
        
        # Check for data validation
        if "input" in code and "validate" not in code:
            issues.append("Input validation may be missing")
        
        return issues
    
    @staticmethod
    def check_error_handling(code: str) -> List[str]:
        """Validate error handling patterns"""
        issues = []
        
        # Check for try-catch blocks around AI calls
        if "ai_client" in code and "try:" not in code:
            issues.append("AI client calls should be wrapped in try-catch")
        
        # Check for timeout handling
        if "timeout" not in code and "ai_client" in code:
            issues.append("Consider adding timeout handling for AI calls")
        
        return issues
```

#### Code Review Process

```yaml
# .github/pull_request_template.md
## AI Code Review Checklist

### Model Changes
- [ ] Model configuration is externalized
- [ ] Parameter ranges are validated
- [ ] Performance metrics are logged
- [ ] Error handling is comprehensive

### Data Handling
- [ ] PII is properly handled
- [ ] Input validation is implemented
- [ ] Data privacy requirements met
- [ ] Data lineage is documented

### Testing
- [ ] Unit tests for AI components
- [ ] Integration tests with mock data
- [ ] Model performance tests
- [ ] Bias and fairness tests

### Documentation
- [ ] Model behavior documented
- [ ] API changes documented
- [ ] Deployment notes updated
- [ ] Ethical considerations noted

### Performance
- [ ] Resource usage optimized
- [ ] Caching implemented where appropriate
- [ ] Rate limiting considered
- [ ] Monitoring and alerting updated
```

### Automated Code Quality Checks

```python
# ai_code_quality.py
import ast
import re
from typing import List, Dict

class AICodeQualityChecker:
    def __init__(self):
        self.checks = [
            self._check_hardcoded_secrets,
            self._check_model_configuration,
            self._check_error_handling,
            self._check_logging,
            self._check_data_validation
        ]
    
    def analyze_file(self, file_path: str) -> Dict[str, List[str]]:
        """Analyze a Python file for AI-specific quality issues"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        results = {}
        for check in self.checks:
            issues = check(content)
            if issues:
                results[check.__name__] = issues
        
        return results
    
    def _check_hardcoded_secrets(self, content: str) -> List[str]:
        """Check for hardcoded API keys or secrets"""
        issues = []
        patterns = [
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'password\s*=\s*["\'][^"\']+["\']'
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f"Potential hardcoded secret found: {pattern}")
        
        return issues
    
    def _check_model_configuration(self, content: str) -> List[str]:
        """Check for proper model configuration"""
        issues = []
        
        # Check if temperature is configurable
        if "temperature" in content and "config" not in content:
            issues.append("Temperature should be configurable")
        
        # Check for model name configuration
        if '"gpt-' in content:
            issues.append("Model name should be configurable, not hardcoded")
        
        return issues
    
    def _check_error_handling(self, content: str) -> List[str]:
        """Check for proper error handling"""
        issues = []
        
        # Check for bare except clauses
        if re.search(r'except\s*:', content):
            issues.append("Avoid bare except clauses")
        
        # Check for AI client error handling
        if "ai_client" in content and "except" not in content:
            issues.append("AI client calls should have error handling")
        
        return issues
    
    def _check_logging(self, content: str) -> List[str]:
        """Check for proper logging"""
        issues = []
        
        if "import logging" not in content and "logger" in content:
            issues.append("Logging module not imported")
        
        if "ai_client" in content and "logger" not in content:
            issues.append("AI operations should be logged")
        
        return issues
    
    def _check_data_validation(self, content: str) -> List[str]:
        """Check for data validation"""
        issues = []
        
        if "request" in content and "validate" not in content:
            issues.append("Input validation may be missing")
        
        return issues

# Usage in CI/CD pipeline
def run_ai_quality_checks(file_paths: List[str]) -> bool:
    """Run AI code quality checks in CI/CD"""
    checker = AICodeQualityChecker()
    all_passed = True
    
    for file_path in file_paths:
        if file_path.endswith('.py'):
            issues = checker.analyze_file(file_path)
            if issues:
                print(f"Issues found in {file_path}:")
                for check_name, check_issues in issues.items():
                    for issue in check_issues:
                        print(f"  - {issue}")
                all_passed = False
    
    return all_passed
```

---

## 4. Testing Strategies for AI Applications

### AI Testing Pyramid

```
                    /\
                   /  \
                  /    \
                 /  E2E  \     ← End-to-End AI Workflow Tests
                /________\
               /          \
              /Integration  \   ← Model Integration Tests
             /______________\
            /                \
           /   Unit Tests     \  ← Component Unit Tests
          /____________________\
```

### Unit Testing for AI Components

```python
import pytest
from unittest.mock import Mock, AsyncMock
from azure.ai.inference.models import ChatCompletions, ChatChoice, ChatMessage

class TestAIService:
    @pytest.fixture
    def mock_ai_client(self):
        """Mock Azure AI client for testing"""
        client = Mock()
        
        # Mock successful response
        mock_response = Mock(spec=ChatCompletions)
        mock_choice = Mock(spec=ChatChoice)
        mock_message = Mock(spec=ChatMessage)
        mock_message.content = "Test AI response"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        client.complete = AsyncMock(return_value=mock_response)
        return client
    
    @pytest.fixture
    def ai_service(self, mock_ai_client):
        """Create AI service with mocked dependencies"""
        return ConversationService(mock_ai_client, Mock())
    
    @pytest.mark.asyncio
    async def test_process_valid_message(self, ai_service, mock_ai_client):
        """Test processing a valid message"""
        message = "Hello, how are you?"
        
        result = await ai_service.process_message(message)
        
        assert result is not None
        assert "Test AI response" in str(result)
        mock_ai_client.complete.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_empty_message(self, ai_service):
        """Test handling of empty message"""
        with pytest.raises(ValueError, match="Message cannot be empty"):
            await ai_service.process_message("")
    
    @pytest.mark.asyncio
    async def test_ai_client_error_handling(self, ai_service, mock_ai_client):
        """Test error handling when AI client fails"""
        mock_ai_client.complete.side_effect = Exception("AI service unavailable")
        
        with pytest.raises(AIServiceException):
            await ai_service.process_message("Test message")

# Model Performance Tests
class TestModelPerformance:
    @pytest.mark.asyncio
    async def test_response_time(self, ai_service):
        """Test that AI responses are within acceptable time limits"""
        import time
        
        start_time = time.time()
        await ai_service.process_message("Quick test message")
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 5.0, f"Response time {response_time}s exceeds 5s limit"
    
    @pytest.mark.asyncio
    async def test_response_quality_metrics(self, ai_service):
        """Test response quality metrics"""
        test_messages = [
            "What is the weather like?",
            "How do I reset my password?",
            "Can you help me with billing?"
        ]
        
        for message in test_messages:
            response = await ai_service.process_message(message)
            
            # Check response length
            assert len(response) > 10, "Response too short"
            assert len(response) < 1000, "Response too long"
            
            # Check for harmful content (basic check)
            harmful_keywords = ["hate", "violence", "illegal"]
            response_lower = response.lower()
            assert not any(keyword in response_lower for keyword in harmful_keywords)
```

### Integration Testing

```python
import pytest
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

class TestAIIntegration:
    @pytest.fixture(scope="session")
    def ai_client(self):
        """Real AI client for integration tests"""
        endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT_TEST")
        return ChatCompletionsClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_real_ai_conversation(self, ai_client):
        """Test actual AI conversation"""
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is 2+2?"}
        ]
        
        response = await ai_client.complete({
            "model": "gpt-4",
            "messages": messages,
            "max_tokens": 100
        })
        
        assert response is not None
        assert len(response.choices) > 0
        assert "4" in response.choices[0].message.content
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_conversation_flow(self, ai_client):
        """Test multi-turn conversation"""
        conversation_service = ConversationService(ai_client, InMemoryStorage())
        
        # First message
        response1 = await conversation_service.start_conversation(
            "Hello, my name is John"
        )
        assert "John" in response1 or "hello" in response1.lower()
        
        # Follow-up message
        response2 = await conversation_service.continue_conversation(
            "What is my name?"
        )
        assert "John" in response2
```

### Load Testing for AI Services

```python
import asyncio
import time
from typing import List
import statistics

class AILoadTester:
    def __init__(self, ai_service, concurrent_users: int = 10):
        self.ai_service = ai_service
        self.concurrent_users = concurrent_users
        self.results = []
    
    async def run_load_test(self, duration_seconds: int = 60) -> dict:
        """Run load test for specified duration"""
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        # Start concurrent users
        user_tasks = []
        for i in range(self.concurrent_users):
            task = asyncio.create_task(
                self._simulate_user(f"user_{i}", end_time)
            )
            user_tasks.append(task)
        
        # Wait for all users to complete
        await asyncio.gather(*user_tasks)
        
        return self._calculate_metrics()
    
    async def _simulate_user(self, user_id: str, end_time: float):
        """Simulate a single user's interactions"""
        test_messages = [
            "Hello, how are you?",
            "What can you help me with?",
            "Tell me a joke",
            "What is the weather like?",
            "How do I reset my password?"
        ]
        
        message_index = 0
        
        while time.time() < end_time:
            try:
                message = test_messages[message_index % len(test_messages)]
                
                start = time.time()
                response = await self.ai_service.process_message(message)
                end = time.time()
                
                self.results.append({
                    "user_id": user_id,
                    "response_time": end - start,
                    "success": True,
                    "timestamp": start
                })
                
                message_index += 1
                
                # Wait before next request
                await asyncio.sleep(1)
                
            except Exception as e:
                self.results.append({
                    "user_id": user_id,
                    "response_time": None,
                    "success": False,
                    "error": str(e),
                    "timestamp": time.time()
                })
    
    def _calculate_metrics(self) -> dict:
        """Calculate performance metrics"""
        successful_requests = [r for r in self.results if r["success"]]
        failed_requests = [r for r in self.results if not r["success"]]
        
        if not successful_requests:
            return {"error": "No successful requests"}
        
        response_times = [r["response_time"] for r in successful_requests]
        
        return {
            "total_requests": len(self.results),
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "success_rate": len(successful_requests) / len(self.results),
            "avg_response_time": statistics.mean(response_times),
            "median_response_time": statistics.median(response_times),
            "p95_response_time": self._percentile(response_times, 0.95),
            "p99_response_time": self._percentile(response_times, 0.99),
            "requests_per_second": len(successful_requests) / 60
        }
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile"""
        sorted_data = sorted(data)
        index = int(percentile * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]

# Usage
async def run_ai_load_test():
    ai_service = ConversationService(ai_client, storage)
    load_tester = AILoadTester(ai_service, concurrent_users=20)
    
    print("Starting load test...")
    metrics = await load_tester.run_load_test(duration_seconds=120)
    
    print(f"Load test results:")
    print(f"Success rate: {metrics['success_rate']:.2%}")
    print(f"Average response time: {metrics['avg_response_time']:.2f}s")
    print(f"P95 response time: {metrics['p95_response_time']:.2f}s")
    print(f"Requests per second: {metrics['requests_per_second']:.2f}")
```

---

## 5. Documentation and Knowledge Management

### AI Project Documentation Structure

```
docs/
├── architecture/
│   ├── system-overview.md
│   ├── ai-model-architecture.md
│   ├── data-flow-diagrams.md
│   └── security-architecture.md
├── api/
│   ├── endpoints.md
│   ├── request-response-schemas.md
│   ├── authentication.md
│   └── rate-limits.md
├── models/
│   ├── model-cards/
│   │   ├── chat-model-v1.md
│   │   ├── sentiment-model-v2.md
│   │   └── template.md
│   ├── training-data.md
│   ├── evaluation-metrics.md
│   └── bias-testing.md
├── deployment/
│   ├── environment-setup.md
│   ├── deployment-guide.md
│   ├── monitoring-setup.md
│   └── troubleshooting.md
├── development/
│   ├── coding-standards.md
│   ├── testing-guidelines.md
│   ├── review-process.md
│   └── contribution-guide.md
└── ethics/
    ├── ai-ethics-guidelines.md
    ├── bias-mitigation.md
    ├── privacy-compliance.md
    └── responsible-ai-checklist.md
```

### Model Card Template

```markdown
# Model Card: [Model Name] v[Version]

## Model Details
- **Model Name**: GPT-4 Chat Assistant
- **Version**: 1.2
- **Date**: 2024-01-15
- **Model Type**: Large Language Model
- **Architecture**: Transformer-based

## Intended Use
### Primary Use Cases
- Customer service chat assistance
- FAQ answering
- General conversation support

### Out-of-Scope Uses
- Medical diagnosis
- Legal advice
- Financial recommendations

## Training Data
### Data Sources
- Public conversation datasets
- Customer service transcripts (anonymized)
- FAQ databases

### Data Preprocessing
- PII removal and anonymization
- Content filtering for inappropriate material
- Quality scoring and filtering

## Evaluation
### Metrics
- Response Relevance: 85%
- Response Safety: 98%
- Response Helpfulness: 80%

### Test Data
- 10,000 customer service conversations
- 5,000 FAQ pairs
- Safety evaluation dataset

## Ethical Considerations
### Bias Testing
- Tested for demographic bias
- Evaluated for fairness across user groups
- Regular bias monitoring in production

### Limitations
- May generate plausible but incorrect information
- Limited knowledge cutoff date
- Cannot access real-time information

## Deployment
### Environment
- Azure AI Foundry
- Model Endpoint: [endpoint-url]
- Authentication: Azure AD

### Monitoring
- Response quality metrics
- Usage analytics
- Safety monitoring
```

### Automated Documentation

```python
import ast
import inspect
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class APIEndpoint:
    path: str
    method: str
    description: str
    parameters: List[Dict]
    responses: List[Dict]

class AIDocumentationGenerator:
    def __init__(self):
        self.endpoints = []
        self.models = []
    
    def generate_api_docs(self, app_module) -> str:
        """Generate API documentation from Flask/FastAPI app"""
        docs = "# AI Service API Documentation\n\n"
        
        # Extract endpoints
        for endpoint in self._extract_endpoints(app_module):
            docs += self._format_endpoint_docs(endpoint)
        
        return docs
    
    def generate_model_docs(self, model_config: Dict) -> str:
        """Generate model documentation"""
        docs = f"# Model Documentation: {model_config['name']}\n\n"
        
        docs += f"## Configuration\n"
        docs += f"- **Model**: {model_config.get('model', 'N/A')}\n"
        docs += f"- **Temperature**: {model_config.get('temperature', 'N/A')}\n"
        docs += f"- **Max Tokens**: {model_config.get('max_tokens', 'N/A')}\n\n"
        
        if "performance" in model_config:
            docs += f"## Performance Metrics\n"
            for metric, value in model_config["performance"].items():
                docs += f"- **{metric.title()}**: {value}\n"
        
        return docs
    
    def _extract_endpoints(self, app_module) -> List[APIEndpoint]:
        """Extract API endpoints from application module"""
        # This would be implemented based on your web framework
        # (Flask, FastAPI, etc.)
        pass
    
    def _format_endpoint_docs(self, endpoint: APIEndpoint) -> str:
        """Format endpoint documentation"""
        docs = f"## {endpoint.method.upper()} {endpoint.path}\n\n"
        docs += f"{endpoint.description}\n\n"
        
        if endpoint.parameters:
            docs += "### Parameters\n"
            for param in endpoint.parameters:
                docs += f"- **{param['name']}** ({param['type']}): {param['description']}\n"
            docs += "\n"
        
        if endpoint.responses:
            docs += "### Responses\n"
            for response in endpoint.responses:
                docs += f"- **{response['status']}**: {response['description']}\n"
            docs += "\n"
        
        return docs

# Usage in CI/CD
def generate_docs_in_pipeline():
    """Generate documentation as part of CI/CD pipeline"""
    generator = AIDocumentationGenerator()
    
    # Generate API docs
    api_docs = generator.generate_api_docs(app)
    with open("docs/api/generated-api-docs.md", "w") as f:
        f.write(api_docs)
    
    # Generate model docs
    model_config = load_model_config()
    model_docs = generator.generate_model_docs(model_config)
    with open("docs/models/generated-model-docs.md", "w") as f:
        f.write(model_docs)
```

---

## 6. AI Model Lifecycle Management

### Model Development Workflow

```python
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
import json
from datetime import datetime

class ModelStage(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"
    RETIRED = "retired"

@dataclass
class ModelVersion:
    version: str
    stage: ModelStage
    config: Dict
    performance_metrics: Dict
    created_at: datetime
    deployed_at: Optional[datetime] = None
    retired_at: Optional[datetime] = None

class AIModelRegistry:
    def __init__(self):
        self.models = {}
        self.deployment_history = []
    
    def register_model(self, model_name: str, version: str, 
                      config: Dict, metrics: Dict) -> ModelVersion:
        """Register a new model version"""
        model_version = ModelVersion(
            version=version,
            stage=ModelStage.DEVELOPMENT,
            config=config,
            performance_metrics=metrics,
            created_at=datetime.utcnow()
        )
        
        if model_name not in self.models:
            self.models[model_name] = {}
        
        self.models[model_name][version] = model_version
        return model_version
    
    def promote_model(self, model_name: str, version: str, 
                     new_stage: ModelStage) -> bool:
        """Promote model to next stage"""
        if model_name not in self.models or version not in self.models[model_name]:
            return False
        
        model_version = self.models[model_name][version]
        
        # Validate promotion rules
        if not self._can_promote(model_version, new_stage):
            return False
        
        model_version.stage = new_stage
        
        if new_stage == ModelStage.PRODUCTION:
            model_version.deployed_at = datetime.utcnow()
            self._record_deployment(model_name, version)
        
        return True
    
    def _can_promote(self, model_version: ModelVersion, new_stage: ModelStage) -> bool:
        """Check if model can be promoted to new stage"""
        current_stage = model_version.stage
        
        # Define promotion rules
        promotion_rules = {
            ModelStage.DEVELOPMENT: [ModelStage.TESTING],
            ModelStage.TESTING: [ModelStage.STAGING],
            ModelStage.STAGING: [ModelStage.PRODUCTION],
            ModelStage.PRODUCTION: [ModelStage.RETIRED]
        }
        
        return new_stage in promotion_rules.get(current_stage, [])
    
    def _record_deployment(self, model_name: str, version: str):
        """Record deployment event"""
        deployment_record = {
            "model_name": model_name,
            "version": version,
            "deployed_at": datetime.utcnow(),
            "deployment_id": f"{model_name}-{version}-{int(datetime.utcnow().timestamp())}"
        }
        self.deployment_history.append(deployment_record)

class AIModelWorkflow:
    def __init__(self, model_registry: AIModelRegistry):
        self.registry = model_registry
    
    async def develop_model(self, model_name: str, config: Dict) -> str:
        """Develop and register new model version"""
        # Generate version number
        version = self._generate_version(model_name)
        
        # Train/configure model
        model = await self._create_model(config)
        
        # Evaluate model
        metrics = await self._evaluate_model(model, config)
        
        # Register in registry
        model_version = self.registry.register_model(
            model_name, version, config, metrics
        )
        
        return version
    
    async def _create_model(self, config: Dict):
        """Create/train model based on configuration"""
        # This would contain actual model creation logic
        # For Azure AI Foundry, this might involve configuring
        # model deployments and fine-tuning
        pass
    
    async def _evaluate_model(self, model, config: Dict) -> Dict:
        """Evaluate model performance"""
        # Run evaluation tests
        metrics = {
            "accuracy": 0.85,
            "response_time": 1.2,
            "safety_score": 0.98
        }
        return metrics
    
    def _generate_version(self, model_name: str) -> str:
        """Generate semantic version number"""
        existing_versions = list(self.registry.models.get(model_name, {}).keys())
        if not existing_versions:
            return "1.0.0"
        
        # Simple increment logic (in practice, use semantic versioning)
        latest_version = max(existing_versions)
        major, minor, patch = map(int, latest_version.split('.'))
        return f"{major}.{minor}.{patch + 1}"
```

---

## Summary

In this lesson, we've covered:

✅ **Agile Methodologies**: Adapting Scrum and Kanban for AI development with AI-specific ceremonies and artifacts
✅ **Sprint Planning**: Creating user stories, experiments, and data stories with proper acceptance criteria
✅ **Code Review Workflows**: Implementing AI-specific code review processes and automated quality checks
✅ **Testing Strategies**: Unit, integration, and load testing specifically designed for AI applications
✅ **Documentation**: Creating comprehensive documentation including model cards and API documentation
✅ **Model Lifecycle**: Managing AI model development, deployment, and retirement workflows

## Next Steps

In the next lesson, we'll explore **Team Collaboration and Code Management**, where you'll learn how to effectively manage code sharing, implement role-based access control, and coordinate cross-functional AI development teams.

## Additional Resources

- [Azure DevOps for AI Projects](https://docs.microsoft.com/en-us/azure/devops/)
- [MLOps Best Practices](https://docs.microsoft.com/en-us/azure/machine-learning/concept-model-management-and-deployment)
- [Agile AI Development](https://www.agilealliance.org/agile101/)
- [AI Model Cards](https://modelcards.withgoogle.com/about)

---

*This lesson provides the workflow foundation needed to develop AI applications efficiently and reliably in team environments.* 