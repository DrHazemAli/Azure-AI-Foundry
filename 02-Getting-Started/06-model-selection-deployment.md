# Model Selection and Deployment

## Overview

This lesson covers the essential aspects of selecting and deploying AI models in Azure AI Foundry, including understanding model capabilities, deployment strategies, and optimization techniques.

## Learning Objectives

- Understand the model catalog and available options
- Learn model selection criteria and best practices
- Master deployment strategies and configurations
- Implement model optimization and monitoring
- Understand cost management and scaling

## Prerequisites

- Completed Azure AI Foundry portal walkthrough (Lesson 05)
- Understanding of basic AI/ML concepts
- Familiarity with your specific use case requirements

---

## 1. Understanding the Model Ecosystem

### Available Model Categories

**Foundation Models (1,900+ available):**

**Language Models:**
- **GPT-4 Turbo**: Advanced reasoning, coding, analysis (128k tokens)
- **GPT-3.5 Turbo**: General language tasks (16k tokens)
- **Claude 3**: Safe AI, constitutional AI (200k tokens)
- **Gemini Pro**: Multimodal understanding (32k tokens)

**Specialized Models:**
- **Code Generation**: GitHub Copilot, CodeT5, StarCoder
- **Vision Models**: GPT-4 Vision, Florence, CLIP
- **Audio Models**: Whisper, Azure Speech
- **Embedding Models**: text-embedding-ada-002, text-embedding-3

### Model Selection Criteria

**Performance Considerations:**
- Accuracy on your specific task
- Response time requirements
- Context length needs
- Multimodal capabilities

**Cost Factors:**
- Token pricing (input vs. output)
- Compute requirements
- Volume discounts
- Hidden costs (data transfer, storage)

**Operational Requirements:**
- Availability and SLA
- Security and compliance
- Geographic deployment
- SDK compatibility

---

## 2. Model Evaluation and Testing

### Using the Playground for Evaluation

```python
import asyncio
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

class ModelEvaluator:
    def __init__(self, endpoint: str):
        self.client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
    
    async def evaluate_model(self, model_name: str, test_cases: list):
        """Evaluate a model against test cases."""
        results = []
        
        for test_case in test_cases:
            try:
                response = await self.client.complete(
                    messages=[
                        {"role": "system", "content": test_case["system"]},
                        {"role": "user", "content": test_case["input"]}
                    ],
                    model=model_name,
                    max_tokens=test_case.get("max_tokens", 1000),
                    temperature=test_case.get("temperature", 0.7)
                )
                
                result = {
                    "test_case": test_case["name"],
                    "input": test_case["input"],
                    "output": response.choices[0].message.content,
                    "tokens_used": response.usage.total_tokens,
                    "success": True
                }
                
            except Exception as e:
                result = {
                    "test_case": test_case["name"],
                    "input": test_case["input"],
                    "error": str(e),
                    "success": False
                }
            
            results.append(result)
        
        return results

# Example test cases
test_cases = [
    {
        "name": "General Q&A",
        "system": "You are a helpful assistant.",
        "input": "What is the capital of France?",
        "max_tokens": 100
    },
    {
        "name": "Code Generation",
        "system": "You are a coding assistant.",
        "input": "Write a Python function to calculate factorial",
        "max_tokens": 200
    }
]
```

---

## 3. Deployment Strategies

### Deployment Types

**1. Serverless Deployment (Pay-per-use)**
- **Pricing**: Pay per token/request
- **Scaling**: Automatic, shared infrastructure
- **Best For**: Development, testing, low-volume apps

**2. Dedicated Deployment (Reserved Capacity)**
- **Pricing**: Reserved capacity pricing
- **Scaling**: Predictable, dedicated resources
- **Best For**: Production, high-volume, latency-sensitive apps

**3. Bring Your Own Compute (BYOC)**
- **Pricing**: Your Azure compute costs
- **Scaling**: Full control over infrastructure
- **Best For**: Maximum control, compliance requirements

### Deployment Configuration

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

class ModelDeploymentManager:
    def __init__(self, endpoint: str, project_id: str):
        self.client = AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential()
        )
        self.project_id = project_id
    
    async def deploy_serverless_model(self, model_name: str):
        """Deploy model in serverless mode."""
        deployment_config = {
            "model_name": model_name,
            "deployment_name": f"{model_name}-serverless",
            "deployment_type": "serverless",
            "scaling_config": {
                "min_instances": 0,
                "max_instances": 10,
                "target_utilization": 70
            }
        }
        
        try:
            deployment = await self.client.create_deployment(
                project_id=self.project_id,
                **deployment_config
            )
            
            return {
                "status": "success",
                "deployment_id": deployment.deployment_id,
                "endpoint": deployment.endpoint_url
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
```

---

## 4. Model Router and Load Balancing

### Intelligent Model Router

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict

class RoutingStrategy(Enum):
    COST_OPTIMIZED = "cost_optimized"
    PERFORMANCE_OPTIMIZED = "performance_optimized"
    BALANCED = "balanced"

@dataclass
class ModelEndpoint:
    name: str
    endpoint_url: str
    cost_per_token: float
    avg_latency_ms: float
    current_load: float

class ModelRouter:
    def __init__(self, strategy: RoutingStrategy = RoutingStrategy.BALANCED):
        self.strategy = strategy
        self.endpoints: List[ModelEndpoint] = []
    
    def add_endpoint(self, endpoint: ModelEndpoint):
        """Add a model endpoint to the router."""
        self.endpoints.append(endpoint)
    
    def route_request(self, request_context: Dict) -> ModelEndpoint:
        """Route request to optimal model endpoint."""
        
        if self.strategy == RoutingStrategy.COST_OPTIMIZED:
            return min(self.endpoints, key=lambda ep: ep.cost_per_token)
        elif self.strategy == RoutingStrategy.PERFORMANCE_OPTIMIZED:
            available = [ep for ep in self.endpoints if ep.current_load < 0.8]
            return min(available or self.endpoints, key=lambda ep: ep.avg_latency_ms)
        else:  # BALANCED
            def score_endpoint(ep: ModelEndpoint) -> float:
                cost_score = 1.0 / (ep.cost_per_token + 0.001)
                perf_score = 1.0 / (ep.avg_latency_ms + 1)
                load_score = 1.0 - ep.current_load
                return (cost_score * 0.3 + perf_score * 0.4 + load_score * 0.3)
            
            return max(self.endpoints, key=score_endpoint)
```

---

## 5. Cost Optimization Strategies

### Cost Monitoring and Analysis

```python
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class CostMetrics:
    total_cost: float
    cost_by_model: Dict[str, float]
    tokens_consumed: int
    cost_per_token: float

class CostOptimizer:
    def __init__(self):
        self.cost_history = []
    
    def analyze_usage_patterns(self, usage_data: List[Dict]) -> Dict:
        """Analyze usage patterns for optimization opportunities."""
        
        # Model efficiency analysis
        model_efficiency = {}
        for record in usage_data:
            model = record['model']
            if model not in model_efficiency:
                model_efficiency[model] = {'total_cost': 0, 'total_tokens': 0}
            
            model_efficiency[model]['total_cost'] += record['cost']
            model_efficiency[model]['total_tokens'] += record['tokens']
        
        # Calculate cost per token for each model
        for model, data in model_efficiency.items():
            data['cost_per_token'] = (data['total_cost'] / data['total_tokens'] 
                                    if data['total_tokens'] > 0 else 0)
        
        return {
            'model_efficiency': model_efficiency,
            'total_cost': sum(r['cost'] for r in usage_data),
            'total_tokens': sum(r['tokens'] for r in usage_data),
            'total_requests': len(usage_data)
        }
    
    def recommend_optimizations(self, analysis: Dict) -> List[Dict]:
        """Generate cost optimization recommendations."""
        recommendations = []
        
        # Model switching recommendations
        models_by_efficiency = sorted(
            analysis['model_efficiency'].items(),
            key=lambda x: x[1]['cost_per_token']
        )
        
        if len(models_by_efficiency) > 1:
            most_efficient = models_by_efficiency[0]
            least_efficient = models_by_efficiency[-1]
            
            if (least_efficient[1]['cost_per_token'] > 
                most_efficient[1]['cost_per_token'] * 1.5):
                recommendations.append({
                    'type': 'model_switch',
                    'description': f"Consider switching from {least_efficient[0]} to {most_efficient[0]}",
                    'potential_savings': ((least_efficient[1]['cost_per_token'] - 
                                         most_efficient[1]['cost_per_token']) * 
                                        least_efficient[1]['total_tokens'])
                })
        
        return recommendations
```

---

## Summary

This lesson covered comprehensive model selection and deployment strategies:

- **Model Ecosystem**: Understanding 1,900+ available models and their capabilities
- **Evaluation**: Testing frameworks and evaluation methodologies
- **Deployment Types**: Serverless, dedicated, and BYOC options
- **Model Router**: Intelligent routing and load balancing
- **Cost Optimization**: Monitoring, analysis, and optimization strategies

## Next Steps

- Implement model evaluation for your specific use case
- Deploy your first production model with monitoring
- Configure cost optimization strategies
- Explore advanced features and customization (Lesson 07)

---

*This lesson is part of the Azure AI Foundry Zero-to-Hero course.* 