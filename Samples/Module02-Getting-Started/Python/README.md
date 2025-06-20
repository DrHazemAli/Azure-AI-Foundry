# Python Samples - Module 02: Getting Started

This directory contains Python samples for getting started with Azure AI Foundry using the Azure AI SDK.

## Prerequisites

- Python 3.8 or later
- pip package manager
- Azure AI Foundry project with appropriate permissions
- VS Code with Python extension or preferred Python IDE

## Quick Start

### 1. Setup Development Environment

```bash
# Verify Python installation
python --version

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Clone and navigate to Python samples
cd Samples/Module02-Getting-Started/Python
```

### 2. Configure Environment

Create a `.env` file in each sample directory:

```bash
AZURE_AI_FOUNDRY_ENDPOINT=https://your-project.cognitiveservices.azure.com/
AZURE_AI_FOUNDRY_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 3. Install Dependencies

Each sample includes a `requirements.txt` file with required dependencies:

```bash
# Navigate to specific sample directory
cd azure_ai_foundry_setup

# Install packages
pip install -r requirements.txt

# Run sample
python main.py
```

## Available Samples

### 1. azure_ai_foundry_setup
**Purpose**: Demonstrates Azure AI Foundry setup and authentication patterns
**Key Features**:
- Multiple authentication methods (API key, managed identity, service principal, default credential)
- Configuration management and validation
- Connection testing and validation
- Comprehensive error handling and logging

### 2. first_chat_completion
**Purpose**: Complete chat application with advanced features
**Key Features**:
- Interactive chat interface with command support
- Conversation context management
- Streaming and non-streaming responses
- Cost tracking and optimization
- Error handling and retry logic
- Conversation export and statistics

### 3. error_handling
**Purpose**: Robust error handling and retry logic patterns
**Key Features**:
- Exception handling patterns
- Retry policies with exponential backoff
- Circuit breaker pattern implementation
- Comprehensive logging and monitoring
- Health check service
- Custom exception types

## Sample Structure

```
Python/
├── README.md                          # This file
├── azure_ai_foundry_setup/           # Setup and authentication
│   ├── main.py                       # Main demo script
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment template
│   └── README.md                     # Sample-specific instructions
├── first_chat_completion/            # Complete chat application
│   ├── main.py                       # Comprehensive chat app (766 lines)
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment template
│   └── README.md                     # Sample-specific instructions
└── error_handling/                   # Error handling patterns
    ├── main.py                       # Error handling demo
    ├── requirements.txt              # Python dependencies
    ├── .env.example                  # Environment template
    └── README.md                     # Sample-specific instructions
```

## Common Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Run sample
python main.py

# Run with debugging
python -m pdb main.py

# Run tests (if available)
python -m pytest

# Format code
black *.py

# Check code quality
flake8 *.py
```

## Environment Configuration

### Using .env files
Create a `.env` file in each sample directory:

```bash
# Azure AI Foundry Configuration
AZURE_AI_FOUNDRY_ENDPOINT=https://your-project.cognitiveservices.azure.com/
AZURE_AI_FOUNDRY_API_KEY=your-api-key

# Authentication (choose one)
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id

# Model Configuration
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Optional: Application Settings
LOG_LEVEL=INFO
MAX_TOKENS=1000
TEMPERATURE=0.7
```

### Using environment variables
```bash
# Set environment variables
export AZURE_AI_FOUNDRY_ENDPOINT="your-endpoint"
export AZURE_AI_FOUNDRY_API_KEY="your-api-key"
python main.py
```

## Dependencies

All samples use these core dependencies:

```txt
# Azure AI Foundry SDK
azure-ai-projects>=1.0.0b2
azure-ai-inference>=1.0.0b2
azure-identity>=1.15.0

# Utilities
python-dotenv>=1.0.0
asyncio>=3.4.3
```

### Development Dependencies
```txt
# Testing
pytest>=7.0.0
pytest-asyncio>=0.21.0

# Code Quality
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0

# Documentation
sphinx>=7.0.0
```

## Virtual Environment Setup

### Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Verify activation
which python  # Should show path to .venv/bin/python
```

### Install dependencies:
```bash
# Install all dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install in editable mode for development
pip install -e .
```

## Troubleshooting

### Authentication Issues
- **API Key Problems**: Verify the key is correctly set in environment variables
- **DefaultAzureCredential**: Ensure Azure CLI login (`az login`) or managed identity is configured
- **Service Principal**: Check all three values (tenant_id, client_id, client_secret) are set

### Package Issues
- **Import Errors**: Ensure virtual environment is activated and dependencies installed
- **Version Conflicts**: Use `pip list` to check versions, create fresh virtual environment if needed
- **SSL Errors**: Update certificates or use `pip install --trusted-host pypi.org`

### Common Errors
- **ModuleNotFoundError**: Run `pip install -r requirements.txt`
- **Authentication failed**: Check credentials and Azure AD permissions
- **Connection timeout**: Verify network connectivity and firewall settings
- **Quota exceeded**: Check usage limits in Azure portal

## Code Quality and Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest test_authentication.py

# Run with verbose output
pytest -v
```

### Code Formatting
```bash
# Format code with black
black *.py

# Check formatting
black --check *.py

# Sort imports
isort *.py
```

### Type Checking
```bash
# Run mypy type checker
mypy main.py

# Check all Python files
mypy .
```

## Development Best Practices

### Code Organization
- Use dataclasses for configuration
- Implement proper error handling
- Add type hints for better IDE support
- Follow PEP 8 style guidelines

### Logging
- Use Python's logging module
- Set appropriate log levels
- Include structured logging for production

### Security
- Never commit API keys to version control
- Use environment variables for sensitive data
- Implement proper credential rotation
- Use Azure Key Vault for production secrets

### Performance
- Use async/await for I/O operations
- Implement connection pooling
- Cache responses when appropriate
- Monitor token usage and costs

## Advanced Features

### Async/Await Support
All samples support asynchronous operations:

```python
import asyncio
from azure.ai.inference import ChatCompletionsClient

async def main():
    client = ChatCompletionsClient(endpoint, credential)
    response = await client.complete(options)
    
asyncio.run(main())
```

### Context Managers
Use context managers for resource management:

```python
async with ChatCompletionsClient(endpoint, credential) as client:
    response = await client.complete(options)
```

### Error Handling Patterns
Implement comprehensive error handling:

```python
from azure.core.exceptions import HttpResponseError

try:
    response = await client.complete(options)
except HttpResponseError as e:
    if e.status_code == 429:  # Rate limited
        await asyncio.sleep(60)  # Wait and retry
    else:
        raise
```

## Next Steps

After completing these samples:

1. **Explore Advanced Features**: Move to Module 03 for advanced project management
2. **Build Custom Applications**: Apply learnings to your specific use cases
3. **Implement Production Patterns**: Add monitoring, scaling, and deployment automation
4. **Join the Community**: Participate in Azure AI Foundry community discussions

## Additional Resources

### Documentation
- [Azure AI Foundry Python SDK](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview)
- [Python SDK Reference](https://docs.microsoft.com/en-us/python/api/overview/azure/ai-foundry)
- [Azure Identity Library](https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme)

### Community
- [Python SDK GitHub Repository](https://github.com/Azure/azure-sdk-for-python)
- [Azure AI Foundry Samples](https://github.com/Azure-Samples/azureai-samples)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/azure-ai-foundry+python)

### Training
- [Microsoft Learn: Azure AI Foundry](https://learn.microsoft.com/en-us/training/paths/azure-ai-foundry/)
- [Python for Azure Developers](https://docs.microsoft.com/en-us/azure/developer/python/)

---

*These Python samples demonstrate best practices and production-ready patterns for Azure AI Foundry development.* 