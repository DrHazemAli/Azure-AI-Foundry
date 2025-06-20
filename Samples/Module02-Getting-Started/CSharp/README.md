# C# Samples - Module 02: Getting Started

This directory contains C# samples for getting started with Azure AI Foundry using .NET 8.0+.

## Prerequisites

- .NET 8.0 SDK or later
- Azure AI Foundry project with appropriate permissions
- Visual Studio 2022 or VS Code with C# extension

## Quick Start

### 1. Setup Development Environment

```bash
# Verify .NET installation
dotnet --version

# Clone and navigate to C# samples
cd Samples/Module02-Getting-Started/CSharp
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

Each sample includes a `.csproj` file with required dependencies:

```bash
# Navigate to specific sample directory
cd AzureAIFoundrySetup

# Restore packages
dotnet restore

# Build project
dotnet build

# Run sample
dotnet run
```

## Available Samples

### 1. AzureAIFoundrySetup
**Purpose**: Demonstrates Azure AI Foundry setup and authentication patterns
**Key Features**:
- Multiple authentication methods
- Configuration management
- Connection validation
- Environment setup

### 2. FirstChatCompletion
**Purpose**: Basic chat completion application
**Key Features**:
- Simple chat interface
- Model interaction
- Response handling
- Conversation management

### 3. ErrorHandling
**Purpose**: Robust error handling and retry logic
**Key Features**:
- Exception handling patterns
- Retry policies
- Logging and monitoring
- Graceful degradation

## Common Commands

```bash
# Run with specific configuration
dotnet run --configuration Release

# Run with environment variables
AZURE_AI_FOUNDRY_ENDPOINT="your-endpoint" dotnet run

# Run tests
dotnet test

# Clean build artifacts
dotnet clean
```

## Troubleshooting

### Authentication Issues
- Ensure proper API key configuration
- Verify Azure CLI login for DefaultAzureCredential
- Check Azure AD permissions

### Package Issues
- Clear NuGet cache: `dotnet nuget locals all --clear`
- Restore packages: `dotnet restore --force`
- Update packages: `dotnet add package PackageName`

---

*These C# samples demonstrate production-ready patterns for Azure AI Foundry development.* 