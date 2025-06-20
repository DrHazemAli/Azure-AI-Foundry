# Azure AI Foundry Portal Walkthrough

## Overview

This lesson provides a comprehensive walkthrough of the Azure AI Foundry portal interface, helping you navigate the platform effectively and understand all available features and tools.

## Learning Objectives

- Navigate the Azure AI Foundry portal interface
- Understand the main sections and their purposes
- Learn to use the project dashboard and management tools
- Explore the model catalog and deployment options
- Understand monitoring and analytics features
- Master the development and collaboration tools

## Prerequisites

- Completed Azure AI Foundry setup (Lesson 02)
- Created your first AI project (Lesson 04)
- Basic familiarity with Azure portal navigation

---

## 1. Portal Overview and Navigation

### 1.1 Main Navigation Structure

The Azure AI Foundry portal is organized into several key sections:

**Primary Navigation:**
- **Home**: Dashboard and quick access to projects
- **Projects**: Manage AI projects and applications
- **Models**: Browse and deploy models from the catalog
- **Data**: Manage datasets and knowledge bases
- **Compute**: Configure and manage compute resources
- **Security**: Access control and compliance settings
- **Monitoring**: Performance metrics and usage analytics

### 1.2 Getting Started Dashboard

Upon login, you'll see the main dashboard featuring:

```yaml
Dashboard Components:
  Recent Projects: Quick access to recently used projects
  Getting Started: Guided tutorials and setup wizards
  Resource Usage: Current consumption and limits
  System Status: Service health and announcements
  Quick Actions: Common tasks and shortcuts
```

**Key Features:**
- **Project Cards**: Visual representation of your projects with status indicators
- **Usage Metrics**: Real-time consumption data and cost tracking
- **Recommendations**: AI-driven suggestions for optimization and features
- **News & Updates**: Latest features and announcements

---

## 2. Project Management Interface

### 2.1 Project Dashboard

Each project has its own dedicated dashboard with:

**Overview Section:**
```yaml
Project Information:
  Name: Your project name
  Type: Chat Application / Content Generation / Multi-Agent
  Status: Active / Development / Deployed
  Created: Creation date and time
  Last Modified: Recent activity timestamp
  Resource Usage: Current consumption metrics
```

**Quick Stats:**
- Total requests processed
- Average response time
- Error rate percentage
- Cost summary (current month)

### 2.2 Project Settings

Access project configuration through the Settings tab:

**General Settings:**
- Project name and description
- Project type and category
- Tags and metadata
- Sharing and collaboration settings

**Resource Configuration:**
- Compute allocation and scaling
- Storage limits and data retention
- Network and security settings
- Integration endpoints

**Access Control:**
- User permissions and roles
- API key management
- Service principal configuration
- Audit logging settings

---

## 3. Model Catalog and Management

### 3.1 Browsing the Model Catalog

The Models section provides access to 1,900+ models:

**Model Categories:**
```yaml
Foundation Models:
  GPT-4 Turbo: Advanced language understanding and generation
  GPT-3.5 Turbo: Cost-effective language processing
  Claude 3: Anthropic's advanced reasoning model
  Gemini Pro: Google's multimodal AI model

Specialized Models:
  Code Generation: GitHub Copilot, CodeT5, StarCoder
  Image Generation: DALL-E 3, Stable Diffusion, Midjourney
  Vision Models: GPT-4 Vision, Florence, CLIP
  Speech Models: Whisper, Azure Speech Services

Open Source Models:
  Llama 2: Meta's open-source language model
  Mistral: European AI lab's efficient models
  Phi-3: Microsoft's small language models
  Code Llama: Specialized for code generation
```

**Model Information Panel:**
- Model description and capabilities
- Performance benchmarks
- Pricing information
- Usage examples and documentation
- Community ratings and reviews

### 3.2 Deploying Models

**Deployment Options:**
1. **Serverless Deployment**: Pay-per-use model access
2. **Dedicated Deployment**: Reserved capacity for consistent performance
3. **Bring Your Own Compute**: Deploy on your Azure resources

**Deployment Wizard:**
```yaml
Step 1: Select Model
  Choose from catalog or custom model
  Review model specifications
  Check compatibility requirements

Step 2: Configure Deployment
  Deployment name and description
  Compute resources and scaling
  Geographic region selection
  Performance tier selection

Step 3: Security and Access
  Authentication methods
  Network access controls
  Data encryption settings
  Compliance requirements

Step 4: Review and Deploy
  Configuration summary
  Cost estimation
  Deployment timeline
  Monitoring setup
```

---

## 4. Data Management Interface

### 4.1 Dataset Management

The Data section helps you manage training and inference data:

**Data Sources:**
- **Upload**: Direct file upload from local machine
- **Azure Storage**: Connect to existing Azure Storage accounts
- **GitHub**: Import from code repositories
- **Web URLs**: Fetch data from web sources
- **APIs**: Connect to external data services

**Supported Formats:**
```yaml
Text Data:
  - JSON, JSONL
  - CSV, TSV
  - TXT, MD
  - XML, YAML

Multimedia:
  - Images (PNG, JPG, WEBP)
  - Audio (WAV, MP3, M4A)
  - Video (MP4, AVI, MOV)
  - Documents (PDF, DOCX, PPTX)
```

### 4.2 Data Processing Tools

**Data Preparation:**
- **Cleaning**: Remove duplicates, handle missing values
- **Transformation**: Format conversion and normalization
- **Validation**: Quality checks and schema validation
- **Annotation**: Label data for supervised learning

**Data Quality Metrics:**
- Completeness percentage
- Consistency score
- Accuracy assessment
- Privacy compliance status

---

## 5. Development and Testing Tools

### 5.1 Playground Interface

The Playground provides an interactive environment for testing:

**Chat Playground:**
```yaml
Features:
  System Message: Configure AI behavior and personality
  Temperature: Control response creativity (0.0 - 2.0)
  Max Tokens: Limit response length
  Top P: Nuclear sampling parameter
  Frequency Penalty: Reduce repetitive content
  Presence Penalty: Encourage topic diversity
```

**Testing Scenarios:**
- Single-turn conversations
- Multi-turn dialogue flows
- Function calling demonstrations
- Custom prompt templates
- A/B testing different configurations

### 5.2 Code Generation and SDK Explorer

**Code Samples:**
The portal automatically generates code in multiple languages:

```python
# Python Example
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

client = ChatCompletionsClient(
    endpoint="your-endpoint",
    credential=DefaultAzureCredential()
)

response = client.complete(
    messages=[{"role": "user", "content": "Hello!"}],
    model="gpt-4"
)
```

```csharp
// C# Example
using Azure.AI.Inference;
using Azure.Identity;

var client = new ChatCompletionsClient(
    new Uri("your-endpoint"),
    new DefaultAzureCredential()
);

var response = await client.CompleteAsync(
    new ChatCompletionsOptions
    {
        DeploymentName = "gpt-4",
        Messages = { new ChatRequestUserMessage("Hello!") }
    }
);
```

---

## 6. Monitoring and Analytics

### 6.1 Real-time Monitoring Dashboard

**Key Metrics Displayed:**
```yaml
Performance Metrics:
  Requests per Second: Current API call rate
  Average Latency: Response time metrics
  Success Rate: Percentage of successful requests
  Error Rate: Failed request percentage

Usage Analytics:
  Total Requests: Cumulative API calls
  Unique Users: Active user count
  Peak Usage Times: Traffic patterns
  Geographic Distribution: Request origins

Cost Analytics:
  Current Month Spend: Running total costs
  Daily Burn Rate: Average daily expenses
  Cost per Request: Unit economics
  Budget Utilization: Spending vs. allocated budget
```

### 6.2 Advanced Analytics

**Custom Dashboards:**
- Create personalized monitoring views
- Configure alert thresholds and notifications
- Export data for external analysis
- Set up automated reports

**Log Analytics:**
- Request/response logging
- Error tracking and debugging
- Performance profiling
- Security audit trails

---

## 7. Collaboration and Sharing

### 7.1 Team Management

**User Roles and Permissions:**
```yaml
Owner:
  - Full project control
  - User management
  - Billing access
  - Resource configuration

Contributor:
  - Model deployment
  - Data management
  - Application development
  - Testing and debugging

Viewer:
  - Read-only access
  - Monitor dashboards
  - Export data
  - Generate reports
```

### 7.2 Sharing and Publishing

**Project Sharing Options:**
- **Internal Sharing**: Within your organization
- **External Sharing**: With specific email addresses
- **Public Gallery**: Showcase to the community
- **Marketplace**: Commercial distribution

**Export Capabilities:**
- Project templates
- Model configurations
- Training datasets
- Documentation packages

---

## 8. Advanced Features

### 8.1 Multi-Agent Orchestration

**Agent Management Interface:**
```yaml
Agent Configuration:
  Agent Roles: Define specialized functions
  Communication Protocols: A2A messaging setup
  Workflow Definition: Orchestration patterns
  Error Handling: Fallback strategies
```

**Visual Workflow Designer:**
- Drag-and-drop agent composition
- Flow control and decision points
- Real-time execution monitoring
- Debug and troubleshooting tools

### 8.2 Model Router and Optimization

**Router Configuration:**
- Model selection criteria
- Load balancing strategies
- Cost optimization rules
- Performance targets

**A/B Testing Framework:**
- Split traffic configuration
- Performance comparison metrics
- Statistical significance testing
- Automated winner selection

---

## 9. Integration and API Management

### 9.1 API Gateway

**Endpoint Management:**
- Custom domain configuration
- Rate limiting and quotas
- Authentication and authorization
- Request/response transformation

**API Documentation:**
- Interactive API explorer
- Code samples in multiple languages
- SDK documentation
- Testing tools

### 9.2 Webhook and Event Integration

**Event Types:**
```yaml
Model Events:
  - Deployment completed
  - Model performance alerts
  - Usage threshold exceeded
  - Error rate spike

Project Events:
  - User added/removed
  - Configuration changes
  - Resource scaling
  - Cost budget alerts
```

---

## 10. Mobile and Responsive Experience

### 10.1 Mobile Portal Access

**Mobile-Optimized Features:**
- Project status monitoring
- Usage alerts and notifications
- Quick model testing
- Team collaboration tools

**Mobile App (if available):**
- Push notifications
- Offline access to documentation
- Voice-to-text testing
- Camera integration for vision models

---

## Summary

The Azure AI Foundry portal provides a comprehensive interface for managing AI projects, from initial development to production deployment. Key areas include:

- **Project Management**: Centralized control of AI applications
- **Model Catalog**: Access to 1,900+ models
- **Development Tools**: Playground, testing, and code generation
- **Monitoring**: Real-time analytics and performance tracking
- **Collaboration**: Team management and sharing capabilities
- **Integration**: APIs, webhooks, and external connections

## Next Steps

- Explore the playground to test different models and configurations
- Set up monitoring and alerts for your projects
- Invite team members and configure collaboration settings
- Review the model catalog for advanced use cases (Lesson 06)

---

*This lesson is part of the Azure AI Foundry Zero-to-Hero course.* 