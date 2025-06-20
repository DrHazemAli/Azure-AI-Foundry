# Lesson 6: Project Types and Structure

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand the two types of Azure AI Foundry projects
- Compare Foundry projects vs Hub-based projects
- Choose the appropriate project type for your use case
- Understand project structure and organization
- Plan resource allocation and team collaboration

## Overview

Azure AI Foundry supports two distinct project types, each designed for different use cases and organizational needs. Understanding these project types is crucial for making the right architectural decisions for your AI initiatives.

## Project Types Overview

### Foundry Projects
A **Foundry project** is built on an Azure AI Foundry resource and provides a simplified, streamlined approach to AI development. This project type is designed for teams that want to focus on building AI agents and applications without complex infrastructure management.

### Hub-Based Projects
A **hub-based project** is hosted by an Azure AI Foundry hub and provides access to advanced enterprise features, Azure Machine Learning capabilities, and comprehensive MLOps tools.

## Detailed Comparison

### Foundry Projects

#### **Core Characteristics**
- Built on Azure AI Foundry resource
- Lightweight setup and management
- Focused on AI agent development
- Simplified project structure
- Ideal for rapid prototyping and development

#### **Key Features**
- ✅ **Agents (GA)**: Full production support for AI agents
- ✅ **AI Foundry API**: Native support for cross-model operations
- ✅ **Azure OpenAI Models**: Direct access to GPT-4, DALL-E, Whisper
- ✅ **Partner Models**: Marketplace models from Stability, Bria, Cohere
- ✅ **Open Source Models**: HuggingFace and community models
- ✅ **Project Files**: Direct file upload and experimentation
- ✅ **Evaluations**: Model and application evaluation tools
- ✅ **Playground**: Interactive testing environment
- ✅ **Prompt Flow**: Workflow orchestration
- ✅ **Content Understanding**: Built-in content analysis

#### **Dependencies**
- **Minimal Azure dependencies**: No additional storage or key vault requirements
- **Simplified billing**: Pay-as-you-go model
- **Reduced complexity**: Fewer moving parts to manage

### Hub-Based Projects

#### **Core Characteristics**
- Hosted by Azure AI Foundry hub
- Enterprise-grade features and governance
- Integration with Azure Machine Learning
- Advanced MLOps capabilities
- Comprehensive resource management

#### **Key Features**
- ✅ **Agents (Preview)**: Preview support for AI agents
- ✅ **Project-level isolation**: Secure file and output separation
- ✅ **Evaluations**: Advanced evaluation frameworks
- ✅ **Playground**: Full testing capabilities
- ✅ **Azure ML Integration**: Complete MLOps lifecycle
- ✅ **Enterprise Governance**: Advanced security and compliance
- ✅ **Custom ML Models**: Full model training and deployment
- ✅ **Advanced Networking**: VNet integration and private endpoints

#### **Dependencies**
- **Azure Storage Account**: Required for artifacts and data
- **Azure Key Vault**: Required for secrets management
- **Azure Container Registry**: Optional for custom containers
- **Application Insights**: Optional for monitoring

## Feature Comparison Matrix

| **Capability** | **Foundry Project** | **Hub-Based Project** |
|---|---|---|
| **Agents** | ✅ (GA) | ✅ (Preview only) |
| **AI Foundry API** | ✅ (Native support) | Available via connections |
| **Azure OpenAI Models** | ✅ | Available via connections |
| **Partner Models** | ✅ | Available via connections |
| **Open Source Models** | ✅ | ❌ |
| **Evaluations** | ✅ | ✅ |
| **Playground** | ✅ | ✅ |
| **Prompt Flow** | ✅ | ❌ |
| **Content Understanding** | ✅ | ❌ |
| **Project Files** | ✅ | ❌ |
| **Project-level Isolation** | ✅ | ✅ |
| **Azure ML Integration** | ❌ | ✅ |
| **Custom Model Training** | ❌ | ✅ |
| **Advanced Networking** | ❌ | ✅ |
| **Enterprise Governance** | Basic | Advanced |

## Project Structure and Organization

### Foundry Project Structure

```
Foundry Project
├── Models & Deployments
│   ├── Azure OpenAI models
│   ├── Partner marketplace models
│   └── Open source models
├── Agents
│   ├── Agent templates
│   ├── Custom agents
│   └── Multi-agent workflows
├── Data & Files
│   ├── Project files
│   ├── Knowledge bases
│   └── Data connections
├── Evaluations
│   ├── Model evaluations
│   ├── Agent performance
│   └── A/B testing
└── Settings
    ├── Access control
    ├── API keys
    └── Integrations
```

### Hub-Based Project Structure

```
Hub-Based Project
├── Hub Resources (Shared)
│   ├── Connections
│   ├── Compute resources
│   ├── Security policies
│   └── Shared datasets
├── Project Resources (Isolated)
│   ├── Models & Deployments
│   ├── Experiments
│   ├── Pipelines
│   └── Endpoints
├── Data Assets
│   ├── Datasets
│   ├── Data stores
│   └── Feature stores
├── ML Components
│   ├── Environments
│   ├── Custom models
│   └── Training jobs
└── Governance
    ├── Access policies
    ├── Compliance tracking
    └── Audit logs
```

## Use Case Guidelines

### Choose Foundry Projects When:

#### **Agent-Focused Development**
- Building conversational AI agents
- Developing task automation agents
- Creating customer service bots
- Implementing AI assistants

#### **Rapid Prototyping**
- Quick proof-of-concept development
- Startup or small team projects
- Time-to-market pressure
- Limited infrastructure requirements

#### **Model Exploration**
- Testing multiple foundation models
- Comparing model capabilities
- Prompt engineering and optimization
- Educational and learning projects

#### **Simplified Operations**
- Minimal DevOps requirements
- Small development teams
- Limited compliance requirements
- Cost-conscious projects

### Choose Hub-Based Projects When:

#### **Enterprise Requirements**
- Large organization with governance needs
- Regulatory compliance requirements
- Advanced security and networking
- Multi-team collaboration

#### **Advanced ML Workflows**
- Custom model training and fine-tuning
- Complex MLOps pipelines
- Data science experimentation
- Research and development

#### **Integration Needs**
- Existing Azure ML investments
- Complex data pipeline requirements
- Enterprise data governance
- Advanced monitoring and observability

#### **Scale and Performance**
- High-volume production workloads
- Advanced resource management
- Cost optimization requirements
- Performance monitoring needs

## Project Creation and Setup

### Creating a Foundry Project

#### **Prerequisites**
- Azure subscription with Owner permissions
- Basic understanding of AI/ML concepts
- Clear use case definition

#### **Setup Process**
1. **Navigate to Azure AI Foundry portal**
2. **Select "Create new project"**
3. **Choose "Azure AI Foundry resource"**
4. **Configure basic settings**:
   - Project name
   - Resource group
   - Region selection
5. **Review and create**

#### **Post-Creation Steps**
- Configure authentication
- Set up data connections
- Import or create initial datasets
- Define access policies

### Creating a Hub-Based Project

#### **Prerequisites**
- Azure subscription with appropriate permissions
- Understanding of Azure ML concepts
- Enterprise governance requirements
- Resource planning completed

#### **Setup Process**
1. **Create or select an existing hub**
2. **Configure hub-level resources**:
   - Storage accounts
   - Key vault
   - Container registry
   - Networking settings
3. **Create project within hub**
4. **Configure project-specific settings**

#### **Post-Creation Steps**
- Set up compute resources
- Configure data connections
- Implement security policies
- Establish MLOps pipelines

## Resource Management and Sharing

### Foundry Project Resources

#### **Resource Isolation**
- Each project has its own resource boundary
- No sharing between projects by default
- Simplified resource management
- Direct billing per project

#### **Sharing Mechanisms**
- API endpoints can be shared
- Model deployments can be exposed
- Limited cross-project integration
- Manual coordination required

### Hub-Based Project Resources

#### **Hub-Level Sharing**
- **Connections**: Shared across all projects in hub
- **Compute**: Shared capacity with quota allocation
- **Security**: Centralized policies and controls
- **Data**: Shared data stores and feature stores

#### **Project-Level Isolation**
- **Experiments**: Isolated per project
- **Models**: Project-specific deployments
- **Artifacts**: Separate storage containers
- **Access**: Project-specific permissions

## Team Collaboration Models

### Foundry Project Collaboration

#### **Small Team Model**
- 2-5 developers per project
- Shared access to all project resources
- Simple role-based access control
- Direct communication and coordination

#### **Multi-Project Model**
- Multiple independent projects
- Limited cross-project dependencies
- Project-specific teams
- Coordination through external tools

### Hub-Based Project Collaboration

#### **Enterprise Hub Model**
- Central hub for organization/department
- Multiple projects under single governance
- Shared resources and policies
- Centralized administration

#### **Cross-Functional Teams**
- Data scientists, engineers, and analysts
- Shared datasets and compute resources
- Collaborative experimentation
- Integrated MLOps workflows

## Migration and Evolution

### Foundry to Hub-Based Migration

#### **When to Consider Migration**
- Outgrowing simple project structure
- Need for advanced MLOps capabilities
- Compliance requirements increase
- Team size and complexity grow

#### **Migration Approach**
- **Assessment**: Evaluate current project complexity
- **Planning**: Design target hub architecture
- **Preparation**: Set up hub infrastructure
- **Migration**: Move assets and reconfigure
- **Validation**: Test functionality and performance

### Hub-Based to Foundry Simplification

#### **When to Consider Simplification**
- Reduced complexity requirements
- Cost optimization needs
- Team size reduction
- Focus shift to agent development

#### **Simplification Process**
- **Evaluation**: Assess feature dependencies
- **Planning**: Design simplified architecture
- **Data Migration**: Extract essential assets
- **Reconfiguration**: Set up Foundry project
- **Testing**: Validate functionality

## Best Practices

### Project Type Selection

#### **Decision Framework**
1. **Assess team size and structure**
2. **Evaluate compliance requirements**
3. **Consider integration complexity**
4. **Plan for future growth**
5. **Analyze cost implications**

#### **Common Pitfalls**
- Over-engineering simple use cases
- Under-estimating enterprise requirements
- Ignoring future scalability needs
- Misaligning with organizational strategy

### Resource Planning

#### **Foundry Projects**
- Plan for model usage costs
- Consider data transfer requirements
- Account for agent scaling needs
- Monitor API usage patterns

#### **Hub-Based Projects**
- Plan compute resource allocation
- Design data architecture carefully
- Implement proper governance from start
- Consider networking requirements

### Governance and Security

#### **Foundry Projects**
- Implement basic access controls
- Monitor API usage and costs
- Secure sensitive data appropriately
- Plan for compliance requirements

#### **Hub-Based Projects**
- Design comprehensive governance framework
- Implement enterprise security policies
- Plan for audit and compliance
- Establish monitoring and alerting

## Cost Considerations

### Foundry Project Costs

#### **Primary Cost Drivers**
- Model inference costs (pay-per-use)
- Data storage and transfer
- Agent execution time
- API call volumes

#### **Cost Optimization**
- Efficient prompt design
- Model selection optimization
- Caching strategies
- Usage monitoring and alerts

### Hub-Based Project Costs

#### **Primary Cost Drivers**
- Compute resource provisioning
- Storage account costs
- Network data transfer
- Additional Azure services

#### **Cost Optimization**
- Right-sizing compute resources
- Implementing auto-scaling
- Optimizing data storage
- Monitoring resource utilization

## Summary

Understanding Azure AI Foundry project types is essential for successful AI implementation:

### **Key Decision Factors**
- **Team size and expertise**
- **Use case complexity**
- **Compliance requirements**
- **Integration needs**
- **Cost considerations**

### **Foundry Projects Excel At**
- Rapid AI agent development
- Simple, focused use cases
- Small team collaboration
- Cost-effective experimentation

### **Hub-Based Projects Excel At**
- Enterprise-grade governance
- Complex ML workflows
- Large team collaboration
- Advanced integration requirements

### **Migration Flexibility**
Both project types can evolve as your needs change, providing flexibility to start simple and scale up, or simplify complex implementations as requirements clarify.

## Next Steps

In the next lesson, we'll explore **Comparison with Other Platforms**, examining how Azure AI Foundry compares to alternatives like AWS Bedrock and Google Vertex AI, helping you understand the competitive landscape and unique value propositions.

## Additional Resources

- [Azure AI Foundry Project Types Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry#types-of-projects)
- [Hub Resources Overview](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/ai-resources)
- [Project Creation Guide](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/create-projects)
- [Azure AI Foundry Pricing](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/) 