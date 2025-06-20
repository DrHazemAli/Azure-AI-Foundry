# Module 02: Getting Started - Code Samples

This directory contains practical code samples for Module 02: Getting Started with Azure AI Foundry. These samples demonstrate the fundamental concepts and provide working implementations across multiple programming languages.

## Sample Applications

### 1. Azure AI Foundry Setup and Authentication
**Purpose**: Demonstrates how to set up and authenticate with Azure AI Foundry
**Languages**: C#, Python, JavaScript, Java
**Key Concepts**: Authentication, project configuration, connection management

### 2. First Chat Completion
**Purpose**: Build your first AI application using Azure AI Foundry
**Languages**: C#, Python, JavaScript, Java
**Key Concepts**: Model interaction, prompt engineering, response handling

### 3. Error Handling and Retry Logic
**Purpose**: Implement robust error handling and retry mechanisms
**Languages**: C#, Python, JavaScript, Java
**Key Concepts**: Exception handling, retry policies, logging

## Prerequisites

Before running these samples, ensure you have:

- ✅ Azure subscription with Azure AI Foundry access
- ✅ Azure AI Foundry project created
- ✅ Appropriate development environment set up
- ✅ Required SDKs and dependencies installed

## Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/DrHazemAli/Azure-AI-Foundry.git
cd Azure-AI-Foundry/Samples/Module02-Getting-Started

# Choose your preferred language directory
cd CSharp  # or Python, JavaScript, Java
```

### 2. Configure Environment
Copy the sample configuration and update with your values:

```bash
# Copy environment template
cp .env.example .env

# Edit with your Azure AI Foundry details
# - Project endpoint
# - API keys
# - Model deployments
```

### 3. Install Dependencies
Follow the language-specific setup instructions in each directory.

### 4. Run Samples
Each sample includes detailed instructions for execution and testing.

## Sample Structure

```
Module02-Getting-Started/
├── README.md                          # This file
├── CSharp/                            # C# samples
│   ├── AzureAIFoundrySetup/          # Setup and authentication
│   ├── FirstChatCompletion/          # Basic chat completion
│   ├── ErrorHandling/                # Error handling patterns
│   └── README.md                     # C# specific instructions
├── Python/                           # Python samples
│   ├── azure_ai_foundry_setup/      # Setup and authentication
│   ├── first_chat_completion/       # Basic chat completion
│   ├── error_handling/              # Error handling patterns
│   └── README.md                    # Python specific instructions
├── JavaScript/                      # JavaScript/TypeScript samples
│   ├── azure-ai-foundry-setup/     # Setup and authentication
│   ├── first-chat-completion/      # Basic chat completion
│   ├── error-handling/             # Error handling patterns
│   └── README.md                   # JavaScript specific instructions
├── Java/                           # Java samples
│   ├── AzureAIFoundrySetup/        # Setup and authentication
│   ├── FirstChatCompletion/        # Basic chat completion
│   ├── ErrorHandling/              # Error handling patterns
│   └── README.md                   # Java specific instructions
└── shared/                         # Shared resources
    ├── sample-data/                # Sample data files
    ├── configurations/             # Configuration templates
    └── documentation/              # Additional documentation
```

## Key Learning Outcomes

By working through these samples, you will learn:

### 🔧 **Technical Skills**
- Azure AI Foundry SDK setup and configuration
- Authentication patterns and security best practices
- Model interaction and API usage
- Error handling and resilience patterns
- Logging and monitoring implementation

### 🏗️ **Development Practices**
- Environment configuration and management
- Code organization and structure
- Testing and debugging techniques
- Documentation and code comments
- Version control best practices

### 🚀 **Azure AI Foundry Specifics**
- Project types and selection criteria
- Model deployment and management
- Connection and endpoint configuration
- Cost optimization strategies
- Performance monitoring and optimization

## Sample Descriptions

### 1. Azure AI Foundry Setup and Authentication

#### **What You'll Build**
A foundational application that demonstrates:
- Azure AI Foundry project connection
- Authentication using different methods
- Configuration management
- Connection validation

#### **Key Features**
- Multiple authentication patterns (managed identity, service principal, API key)
- Environment-based configuration
- Connection testing and validation
- Error handling for authentication failures

#### **Learning Focus**
- Understanding Azure AI Foundry authentication
- Security best practices
- Configuration management
- Environment setup

### 2. First Chat Completion

#### **What You'll Build**
A simple but complete chat application that demonstrates:
- Model selection and deployment
- Prompt engineering basics
- Response handling and parsing
- Conversation context management

#### **Key Features**
- Interactive chat interface
- Multiple model support (GPT-4, GPT-3.5)
- System message configuration
- Response streaming (where supported)
- Conversation history management

#### **Learning Focus**
- Model interaction patterns
- Prompt engineering fundamentals
- Response processing
- User experience considerations

### 3. Error Handling and Retry Logic

#### **What You'll Build**
A robust application framework that demonstrates:
- Comprehensive error handling
- Retry policies and backoff strategies
- Logging and monitoring
- Graceful degradation

#### **Key Features**
- Custom exception types
- Exponential backoff retry logic
- Circuit breaker pattern
- Comprehensive logging
- Health check endpoints

#### **Learning Focus**
- Production-ready error handling
- Resilience patterns
- Monitoring and observability
- Performance optimization

## Environment Configuration

### Required Environment Variables

All samples use environment variables for configuration:

```bash
# Azure AI Foundry Configuration
AZURE_AI_FOUNDRY_ENDPOINT=https://your-project.cognitiveservices.azure.com/
AZURE_AI_FOUNDRY_API_KEY=your-api-key-here

# Authentication (choose one)
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id

# Model Configuration
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Optional: Logging and Monitoring
LOG_LEVEL=INFO
ENABLE_TELEMETRY=true
```

### Configuration Templates

Each language directory includes:
- `.env.example` - Template for environment variables
- `appsettings.json` (C#) - Application configuration
- `config.py` (Python) - Configuration management
- `config.js` (JavaScript) - Configuration utilities
- `application.properties` (Java) - Spring Boot configuration

## Testing and Validation

### Unit Tests
Each sample includes unit tests demonstrating:
- Authentication testing
- Model interaction mocking
- Error condition simulation
- Configuration validation

### Integration Tests
Integration tests verify:
- End-to-end functionality
- Azure AI Foundry connectivity
- Model deployment validation
- Performance benchmarks

### Manual Testing
Manual testing guides for:
- Interactive testing scenarios
- User acceptance testing
- Performance validation
- Security verification

## Troubleshooting

### Common Issues

#### **Authentication Errors**
```
Error: Unauthorized (401)
```
**Solutions**:
- Verify API key or managed identity configuration
- Check Azure AI Foundry project permissions
- Validate endpoint URL format
- Ensure proper Azure CLI login (for DefaultAzureCredential)

#### **Model Not Found**
```
Error: Model deployment not found
```
**Solutions**:
- Verify model deployment name in Azure portal
- Check model availability in your region
- Ensure proper model permissions
- Validate API version compatibility

#### **Quota Exceeded**
```
Error: Rate limit exceeded
```
**Solutions**:
- Implement retry logic with exponential backoff
- Request quota increase in Azure portal
- Optimize request frequency
- Consider model selection for better quota utilization

#### **Network Connectivity**
```
Error: Connection timeout
```
**Solutions**:
- Check network connectivity to Azure
- Verify firewall and proxy settings
- Test with different network connection
- Check Azure service status

### Debugging Tips

#### **Enable Detailed Logging**
```bash
# Set environment variable for detailed logging
export LOG_LEVEL=DEBUG
export AZURE_LOG_LEVEL=DEBUG
```

#### **Test Connectivity**
```bash
# Test basic connectivity to Azure AI Foundry
curl -H "Authorization: Bearer $AZURE_AI_FOUNDRY_API_KEY" \
     "$AZURE_AI_FOUNDRY_ENDPOINT/models"
```

#### **Validate Configuration**
Each sample includes configuration validation utilities to help identify setup issues.

## Performance Considerations

### Optimization Strategies

#### **Connection Pooling**
- Reuse HTTP connections
- Implement connection pooling
- Configure appropriate timeouts

#### **Caching**
- Cache model responses for repeated queries
- Implement intelligent cache invalidation
- Consider distributed caching for scale

#### **Batch Processing**
- Batch multiple requests when possible
- Implement queue-based processing
- Use asynchronous patterns

#### **Resource Management**
- Monitor token usage and costs
- Implement request throttling
- Optimize prompt length and structure

## Security Best Practices

### Authentication Security
- Use managed identities in production
- Rotate API keys regularly
- Implement least privilege access
- Monitor authentication logs

### Data Protection
- Encrypt sensitive data at rest and in transit
- Implement proper data retention policies
- Use Azure Key Vault for secrets management
- Follow GDPR and compliance requirements

### Network Security
- Use private endpoints where possible
- Implement network security groups
- Configure Azure Firewall rules
- Monitor network traffic

## Next Steps

After completing these samples:

1. **Explore Advanced Features**: Move to Module 03 for advanced project management
2. **Build Custom Applications**: Apply learnings to your specific use cases
3. **Implement Production Patterns**: Add monitoring, scaling, and deployment automation
4. **Join the Community**: Participate in Azure AI Foundry community discussions

## Additional Resources

### Documentation
- [Azure AI Foundry SDK Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview)
- [Azure AI Foundry Best Practices](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/best-practices)
- [Azure AI Foundry Troubleshooting](https://learn.microsoft.com/en-us/azure/ai-foundry/troubleshooting)

### Community
- [Azure AI Foundry Tech Community](https://techcommunity.microsoft.com/t5/azure-ai-foundry/ct-p/AzureAIFoundry)
- [Azure AI Foundry GitHub Samples](https://github.com/Azure-Samples/azureai-samples)
- [Azure AI Foundry Stack Overflow](https://stackoverflow.com/questions/tagged/azure-ai-foundry)

### Training
- [Microsoft Learn: Azure AI Foundry](https://learn.microsoft.com/en-us/training/paths/azure-ai-foundry/)
- [Azure AI Foundry Workshop Materials](https://github.com/microsoft/azure-ai-foundry-workshop)

---

*These samples are designed to provide practical, working examples that you can adapt for your own applications. Each sample includes comprehensive documentation, error handling, and best practices to help you build production-ready AI applications with Azure AI Foundry.* 