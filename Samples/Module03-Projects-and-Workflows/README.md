# Module 03: Projects and Workflows - Code Samples

This directory contains comprehensive code samples demonstrating advanced project management, development workflows, and deployment strategies for Azure AI Foundry applications.

## Overview

The samples in this module showcase enterprise-grade patterns and practices for managing complex AI projects, including:

- **Project Architecture Patterns** - Microservices, monolithic, and hybrid architectures
- **Development Workflows** - Agile methodologies adapted for AI development
- **Team Collaboration** - Code sharing, branching strategies, and role-based access
- **CI/CD Pipelines** - Automated testing, validation, and deployment for AI
- **Environment Management** - Multi-environment configuration and Infrastructure as Code
- **Security & Governance** - Data protection, compliance, and audit frameworks
- **Monitoring & Optimization** - Performance tracking and cost optimization
- **Advanced Deployments** - Blue-green, canary releases, and A/B testing

## Sample Projects

### 1. Enterprise AI Architecture Template
**Directory**: `enterprise-ai-template/`
**Language**: Python, Terraform, YAML
**Description**: Complete enterprise-grade project template with microservices architecture, CI/CD pipelines, and multi-environment deployment.

**Features**:
- Microservices architecture with API gateway
- Docker containerization and Kubernetes deployment
- Azure DevOps CI/CD pipelines
- Infrastructure as Code with Terraform
- Comprehensive monitoring and logging
- Security and compliance frameworks

### 2. Advanced Deployment Manager
**Directory**: `deployment-manager/`
**Language**: Python
**Description**: Implementation of blue-green deployments, canary releases, and A/B testing for AI models.

**Features**:
- Blue-green deployment automation
- Canary release with automated rollback
- A/B testing framework for model comparison
- Traffic routing and load balancing
- Performance validation and monitoring

### 3. AI Project Governance Framework
**Directory**: `governance-framework/`
**Language**: Python, YAML
**Description**: Comprehensive governance framework including data lineage, compliance tracking, and audit trails.

**Features**:
- Data classification and lineage tracking
- GDPR compliance management
- Security policy enforcement
- Audit trail generation
- Risk assessment automation

### 4. Multi-Environment Configuration System
**Directory**: `config-management/`
**Language**: Python, YAML, JSON
**Description**: Hierarchical configuration management system for multiple environments with secret management.

**Features**:
- Environment-specific configuration
- Azure Key Vault integration
- Configuration validation
- Secret rotation and management
- Infrastructure as Code templates

### 5. AI Monitoring and Optimization Suite
**Directory**: `monitoring-suite/`
**Language**: Python, Grafana
**Description**: Comprehensive monitoring solution with performance optimization recommendations.

**Features**:
- Custom metrics collection for AI applications
- Real-time alerting and notification
- Performance baseline establishment
- Cost optimization analysis
- Automated optimization recommendations

## Prerequisites

### Required Software
- **Python 3.11+**
- **Docker Desktop**
- **Azure CLI 2.50+**
- **Terraform 1.5+**
- **kubectl** (for Kubernetes samples)
- **Git**

### Azure Resources
- **Azure Subscription** with Contributor access
- **Azure AI Foundry** workspace
- **Azure DevOps** organization (for CI/CD samples)
- **Azure Key Vault** (for secrets management)
- **Azure Monitor** (for observability)

### Development Tools
- **Visual Studio Code** with extensions:
  - Azure Tools
  - Python
  - Docker
  - Terraform
  - Kubernetes

## Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd Samples/Module03-Projects-and-Workflows

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Azure Authentication
```bash
# Login to Azure
az login

# Set default subscription
az account set --subscription "your-subscription-id"

# Create service principal for automation
az ad sp create-for-rbac --name "ai-foundry-automation" \
  --role contributor \
  --scopes /subscriptions/your-subscription-id
```

### 3. Setup Environment Variables
```bash
# Copy environment template
cp .env.template .env

# Edit .env file with your values
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_AI_FOUNDRY_ENDPOINT="your-ai-foundry-endpoint"
```

### 4. Run Sample Projects

#### Enterprise AI Template
```bash
cd enterprise-ai-template
./deploy.sh dev  # Deploy to development environment
```

#### Deployment Manager
```bash
cd deployment-manager
python main.py --deploy-model chat-assistant --version 2.0.0
```

#### Governance Framework
```bash
cd governance-framework
python governance_manager.py --scan-data-assets --generate-report
```

## Sample Architecture

### Enterprise AI Template Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Azure AI Foundry Project                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Chat Service│  │Embedding Svc│  │ Vision Svc  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                 │                 │               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              API Gateway / Load Balancer               │ │
│  └─────────────────────────────────────────────────────────┘ │
│         │                 │                 │               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Metrics   │  │   Logging   │  │  Security   │         │
│  │ Collection  │  │ Aggregation │  │ Monitoring  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                     Azure Infrastructure                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Key Vault │  │  App Insights│  │  Log Analytics│       │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### CI/CD Pipeline Flow
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Source    │───▶│   Build     │───▶│    Test     │
│   Control   │    │   Stage     │    │   Stage     │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Unit Tests │    │Model Validation│ │Integration  │
│  Code Quality│    │Performance Test│ │   Tests     │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Deploy    │───▶│   Staging   │───▶│ Production  │
│  to Staging │    │ Validation  │    │ Deployment  │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Key Features Demonstrated

### 1. Project Architecture Patterns

**Microservices Architecture** (`enterprise-ai-template/services/`)
- Independent service deployments
- API gateway pattern
- Service mesh communication
- Distributed monitoring

**Configuration Management** (`config-management/`)
- Environment-specific settings
- Secret management integration
- Configuration validation
- Hierarchical overrides

### 2. Development Workflows

**Agile AI Development** (`workflows/agile/`)
- Sprint planning for AI projects
- User story templates for AI features
- Definition of Done for AI deliverables
- Velocity tracking for AI teams

**Code Review Process** (`workflows/code-review/`)
- AI-specific review checklists
- Automated quality gates
- Model validation requirements
- Security compliance checks

### 3. CI/CD Automation

**Pipeline Templates** (`pipelines/`)
- Multi-stage build pipelines
- Model validation stages
- Security scanning integration
- Deployment automation

**Testing Frameworks** (`testing/`)
- Unit tests for AI components
- Integration tests for model APIs
- Performance benchmarking
- Bias and fairness testing

### 4. Deployment Strategies

**Blue-Green Deployment** (`deployment-manager/blue_green.py`)
```python
# Example usage
deployment_manager = BlueGreenDeploymentManager(azure_client)

result = await deployment_manager.deploy_new_version(
    model_name="chat-assistant",
    model_version="2.0.0",
    model_config={
        "temperature": 0.7,
        "max_tokens": 1000
    }
)

if result["success"]:
    print(f"Deployment successful: {result['endpoint']}")
else:
    print(f"Deployment failed: {result['error']}")
```

**Canary Release** (`deployment-manager/canary.py`)
```python
# Example canary configuration
canary_config = CanaryConfiguration(
    model_name="summarizer",
    canary_version="1.5.0",
    baseline_version="1.4.2",
    canary_traffic_percentage=20,
    success_criteria={
        "error_rate": 0.05,  # Max 5% increase
        "response_time": 0.10,  # Max 10% increase
        "user_satisfaction": 0.02  # Max 2% decrease
    },
    rollout_duration_minutes=120,
    evaluation_interval_minutes=10
)

canary_manager = CanaryReleaseManager(traffic_router, monitoring)
canary_id = await canary_manager.start_canary_release(canary_config)
```

### 5. Monitoring and Observability

**Custom Metrics** (`monitoring-suite/metrics.py`)
```python
# AI-specific metrics collection
metrics_collector = AIMetricsCollector(monitoring_system)

# Track model performance
session_id = await metrics_collector.track_model_request(
    "chat-assistant", 
    {"input_tokens": 150}
)

await metrics_collector.complete_model_request(
    session_id,
    {"output_tokens": 200},
    error=None
)

# Get performance report
report = metrics_collector.get_model_performance_report(
    "chat-assistant", 
    time_range=3600
)
```

**Performance Optimization** (`monitoring-suite/optimizer.py`)
```python
# Automated optimization recommendations
optimizer = PerformanceOptimizer(metrics_collector)

# Establish baseline
baseline = optimizer.establish_baseline("chat-assistant")

# Analyze performance degradation
analysis = optimizer.analyze_performance_degradation("chat-assistant")

if analysis["degradation_detected"]:
    for recommendation in analysis["recommendations"]:
        print(f"Recommendation: {recommendation.description}")
        print(f"Expected improvement: {recommendation.expected_improvement:.1%}")
```

### 6. Security and Governance

**Data Protection** (`governance-framework/data_protection.py`)
```python
# Data encryption and sanitization
data_protector = DataProtectionManager()

# Encrypt sensitive data
encrypted_data = data_protector.encrypt_sensitive_data({
    "user_id": "12345",
    "personal_data": "John Doe, john@example.com",
    "training_data": "sensitive content"
})

# Sanitize logs
sanitized_logs = data_protector.sanitize_logs(log_data)
```

**GDPR Compliance** (`governance-framework/gdpr.py`)
```python
# GDPR compliance management
gdpr_manager = GDPRComplianceManager(data_governance)

# Register personal data
gdpr_manager.register_personal_data(
    data_asset_id="customer-conversations",
    personal_data_types=["email", "name", "preferences"],
    lawful_basis="consent",
    retention_period=365
)

# Process data subject request
request_id = gdpr_manager.process_data_subject_request(
    request_type="access",
    data_subject_id="user123",
    details={"request_date": "2024-01-15"}
)
```

## Best Practices Demonstrated

### 1. Code Organization
- Clear separation of concerns
- Modular architecture with well-defined interfaces
- Comprehensive error handling and logging
- Configuration externalization

### 2. Testing Strategy
- Multi-level testing pyramid (unit, integration, E2E)
- AI-specific test cases (bias, fairness, performance)
- Automated test execution in CI/CD
- Test data management and versioning

### 3. Security Implementation
- Defense in depth security model
- Encryption at rest and in transit
- Secure secret management
- Regular security scanning and updates

### 4. Monitoring and Alerting
- Proactive monitoring with custom metrics
- Intelligent alerting with reduced noise
- Performance baseline establishment
- Automated optimization recommendations

### 5. Deployment Safety
- Zero-downtime deployment strategies
- Automated rollback mechanisms
- Progressive traffic shifting
- Comprehensive validation gates

## Troubleshooting

### Common Issues

**Authentication Errors**
```bash
# Verify Azure login
az account show

# Check service principal permissions
az role assignment list --assignee $AZURE_CLIENT_ID
```

**Deployment Failures**
```bash
# Check deployment logs
kubectl logs -f deployment/ai-service

# Verify resource quotas
az vm list-usage --location eastus2
```

**Configuration Issues**
```bash
# Validate configuration
python -m config_management.validator --env dev

# Test connectivity
python -m governance_framework.health_check
```

## Contributing

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/new-sample`
3. **Follow Coding Standards**: Use provided linting and formatting tools
4. **Add Tests**: Ensure comprehensive test coverage
5. **Update Documentation**: Include README updates and code comments
6. **Submit Pull Request**: With detailed description of changes

## Support and Resources

### Documentation
- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Azure DevOps Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/)

### Community
- [Azure AI Foundry Community](https://techcommunity.microsoft.com/t5/azure-ai-foundry/ct-p/AzureAIFoundry)
- [Azure Architecture Center](https://docs.microsoft.com/en-us/azure/architecture/)
- [MLOps Community](https://mlops.community/)

### Training Resources
- [Microsoft Learn - AI Engineering](https://docs.microsoft.com/en-us/learn/paths/azure-ai-engineer/)
- [Azure Architecture Patterns](https://docs.microsoft.com/en-us/azure/architecture/patterns/)
- [DevOps Best Practices](https://docs.microsoft.com/en-us/azure/devops/learn/)

---

*These samples demonstrate production-ready patterns and practices for enterprise AI development using Azure AI Foundry. Each sample includes comprehensive documentation, error handling, logging, and monitoring to serve as a reference for real-world implementations.* 