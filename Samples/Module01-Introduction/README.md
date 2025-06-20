# Module 01 - Introduction Sample

This sample demonstrates the basic concepts and capabilities of Azure AI Foundry, including model access, chat completions, and conversation management.

## What This Sample Demonstrates

- **Azure AI Foundry Connection**: How to connect to Azure AI Foundry using the C# SDK
- **Authentication**: Using DefaultAzureCredential for secure authentication
- **Chat Completions**: Basic chat completion functionality with Azure OpenAI models
- **System Messages**: Using system messages to control AI behavior and expertise
- **Conversation Context**: Maintaining context across multiple exchanges
- **Error Handling**: Proper error handling and user feedback
- **Best Practices**: Following Azure AI Foundry development best practices

## Prerequisites

Before running this sample, ensure you have:

1. **Azure Subscription**: An active Azure subscription
2. **Azure AI Foundry Project**: A project created in Azure AI Foundry
3. **Model Deployment**: At least one model deployed (e.g., gpt-4o-mini)
4. **.NET 8.0**: .NET 8.0 SDK installed on your machine
5. **Azure CLI**: Azure CLI installed and authenticated (`az login`)

## Setup Instructions

### 1. Clone or Download the Sample

```bash
# If you're cloning the entire course repository
git clone https://github.com/DrHazemAli/Azure-AI-Foundry.git
cd Azure-AI-Foundry/Samples/Module01-Introduction
```

### 2. Set Environment Variables

Set the required environment variable for your Azure AI Foundry project:

#### Windows (Command Prompt)
```cmd
set AZURE_AI_PROJECT_ENDPOINT=https://your-project-name.aiservices.azure.com
```

#### Windows (PowerShell)
```powershell
$env:AZURE_AI_PROJECT_ENDPOINT="https://your-project-name.aiservices.azure.com"
```

#### macOS/Linux (Bash)
```bash
export AZURE_AI_PROJECT_ENDPOINT="https://your-project-name.aiservices.azure.com"
```

### 3. Authenticate with Azure

Ensure you're authenticated with Azure CLI:

```bash
az login
```

### 4. Install Dependencies

Restore the NuGet packages:

```bash
dotnet restore
```

### 5. Run the Sample

```bash
dotnet run
```

## Configuration Options

### Model Deployment Name

By default, the sample uses `gpt-4o-mini`. If you have a different model deployed, you can modify the `ModelDeploymentName` constant in `Program.cs`:

```csharp
private static readonly string ModelDeploymentName = "your-model-deployment-name";
```

### Project Endpoint

The sample reads the project endpoint from the `AZURE_AI_PROJECT_ENDPOINT` environment variable. You can also hardcode it in `Program.cs` for testing:

```csharp
private static readonly string ProjectEndpoint = "https://your-project-name.aiservices.azure.com";
```

## Sample Output

When you run the sample successfully, you should see output similar to:

```
=== Azure AI Foundry - Module 01 Introduction Sample ===

🔗 Connecting to Azure AI Foundry...
✅ Connected successfully!

📝 Demonstrating Basic Chat Completion
=====================================
🤖 Sending request to Azure AI Foundry...
✨ Response: Azure AI Foundry is Microsoft's comprehensive platform for building, deploying, and managing AI applications and agents at enterprise scale...
📊 Token Usage - Prompt: 15, Completion: 85, Total: 100

🎭 Demonstrating System Message Usage
====================================
🤖 Sending request with system message...
✨ Response: Azure AI Foundry provides robust multi-agent orchestration capabilities through several key features...

💬 Demonstrating Conversation Context
====================================
🤖 First exchange...
✨ AI: The main benefits of using Azure AI Foundry include...

🤖 Second exchange (with context)...
✨ AI: Regarding the agent orchestration benefit I mentioned earlier...

📋 Conversation Summary:
- Total messages in conversation: 5
- The AI maintained context between exchanges
- System message guided the AI's expertise domain

=== Sample completed successfully! ===

Press any key to exit...
```

## Key Concepts Demonstrated

### 1. Authentication with DefaultAzureCredential

```csharp
var credential = new DefaultAzureCredential();
var client = new ChatCompletionsClient(new Uri(ProjectEndpoint), credential);
```

The `DefaultAzureCredential` class provides a simplified authentication experience by trying multiple authentication methods in order:
- Environment variables
- Managed Identity
- Visual Studio
- Azure CLI
- Interactive browser

### 2. Basic Chat Completion

```csharp
var requestOptions = new ChatCompletionsOptions()
{
    Messages = { new ChatRequestUserMessage("Your question here") },
    Model = ModelDeploymentName,
    MaxTokens = 200,
    Temperature = 0.7f
};

Response<ChatCompletions> response = await client.CompleteAsync(requestOptions);
```

### 3. System Messages for Behavior Control

```csharp
var requestOptions = new ChatCompletionsOptions()
{
    Messages =
    {
        new ChatRequestSystemMessage("You are a helpful AI assistant specializing in Azure cloud services..."),
        new ChatRequestUserMessage("Your question here")
    },
    // ... other options
};
```

### 4. Conversation Context Management

```csharp
var messages = new List<ChatRequestMessage>
{
    new ChatRequestSystemMessage("System instructions..."),
    new ChatRequestUserMessage("First question")
};

// Get first response and add to history
var firstResponse = await GetChatResponse(client, messages);
messages.Add(new ChatRequestAssistantMessage(firstResponse));

// Continue conversation with context
messages.Add(new ChatRequestUserMessage("Follow-up question"));
var secondResponse = await GetChatResponse(client, messages);
```

## Troubleshooting

### Common Issues

1. **Authentication Error**: Ensure you're logged in with Azure CLI (`az login`)
2. **Endpoint Error**: Verify your project endpoint URL is correct
3. **Model Not Found**: Ensure you have a model deployed in your Azure AI Foundry project
4. **Permission Error**: Verify you have appropriate permissions to access the Azure AI Foundry project

### Getting Help

If you encounter issues:

1. Check the [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
2. Verify your Azure AI Foundry project setup in the [Azure AI Foundry Portal](https://ai.azure.com)
3. Check the [Azure AI Foundry SDK Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview)

## Next Steps

After running this sample successfully:

1. Explore the other modules in this course
2. Try modifying the system messages to change AI behavior
3. Experiment with different temperature and max token settings
4. Add your own conversation scenarios

## Additional Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Azure AI Foundry SDK Reference](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/ai.inference-readme)
- [Azure Identity Documentation](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/identity-readme)

---

*This sample is part of the Azure AI Foundry Zero-to-Hero Course. For the complete course, visit the [course repository](https://github.com/DrHazemAli/Azure-AI-Foundry).* 