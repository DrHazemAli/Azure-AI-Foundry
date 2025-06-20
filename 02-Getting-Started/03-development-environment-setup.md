# Development Environment Setup

## Overview

This lesson guides you through setting up a complete development environment for Azure AI Foundry development across multiple programming languages and platforms.

## Learning Objectives

- Set up development environments for Python, C#, JavaScript, and Java
- Configure Azure AI Foundry SDKs and dependencies
- Set up proper authentication for development
- Configure development tools and IDEs
- Implement best practices for local development

## Prerequisites

- Completed Azure AI Foundry setup (Lesson 02)
- Basic programming knowledge in your chosen language
- Administrator access to your development machine

---

## 1. Python Development Setup

### Python Installation and Virtual Environment

```bash
# Install Python 3.8 or later
python3 --version

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install Azure AI Foundry SDK
pip install azure-ai-projects
pip install azure-ai-inference
pip install azure-identity
pip install python-dotenv
```

### Python Configuration

Create `.env` file:
```bash
AZURE_AI_FOUNDRY_ENDPOINT=https://your-ai-foundry.cognitiveservices.azure.com
AZURE_AI_FOUNDRY_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

---

## 2. C# Development Setup

### .NET Installation

```bash
# Install .NET 8 SDK
dotnet --version

# Create console application
dotnet new console -n AzureAIFoundryDev
cd AzureAIFoundryDev

# Add packages
dotnet add package Azure.AI.Projects
dotnet add package Azure.AI.Inference
dotnet add package Azure.Identity
```

---

## 3. JavaScript Development Setup

### Node.js Setup

```bash
# Install Node.js LTS
node --version
npm --version

# Create project
mkdir azure-ai-foundry-js
cd azure-ai-foundry-js
npm init -y

# Install packages
npm install @azure/ai-projects
npm install @azure/ai-inference
npm install @azure/identity
```

---

## 4. Authentication Setup

### Azure CLI Authentication

```bash
# Install and login
az login
az account set --subscription "your-subscription-id"
```

### Environment Variables

Create secure environment configuration for your chosen platform with proper authentication credentials.

---

## 5. IDE Configuration

### Visual Studio Code

Install recommended extensions:
- Azure Account
- Python/C#/JavaScript extensions
- Azure AI Foundry extension (if available)

---

## Summary

You now have a complete development environment configured for Azure AI Foundry development with proper authentication and tooling.

## Next Steps

- Create your first AI project (Lesson 04)
- Explore the Azure AI Foundry portal interface
- Build your first application

---

*This lesson is part of the Azure AI Foundry Zero-to-Hero course.* 