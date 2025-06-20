using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Identity;
using Azure.AI.Inference;
using Azure.AI.Inference.Models;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace FirstChatCompletion;

/// <summary>
/// Simple chat completion application demonstrating Azure AI Foundry basics
/// </summary>
public class Program
{
    private static ILogger<Program>? _logger;
    private static IConfiguration? _configuration;

    public static async Task Main(string[] args)
    {
        Console.WriteLine("🤖 Azure AI Foundry - First Chat Completion Demo");
        Console.WriteLine("=" * 50);

        try
        {
            // Setup configuration
            _configuration = new ConfigurationBuilder()
                .AddJsonFile("appsettings.json", optional: true)
                .AddEnvironmentVariables()
                .AddUserSecrets<Program>()
                .Build();

            // Setup logging
            using var loggerFactory = LoggerFactory.Create(builder =>
                builder.AddConsole().SetMinimumLevel(LogLevel.Information));
            _logger = loggerFactory.CreateLogger<Program>();

            _logger.LogInformation("Starting Azure AI Foundry chat completion demo");

            // Create and run chat application
            var chatApp = new SimpleChatApp(_configuration, _logger);
            await chatApp.RunAsync();

            _logger.LogInformation("Demo completed successfully");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Error: {ex.Message}");
            _logger?.LogError(ex, "Demo failed with error");
        }
    }
}

/// <summary>
/// Simple chat application using Azure AI Foundry
/// </summary>
public class SimpleChatApp
{
    private readonly IConfiguration _configuration;
    private readonly ILogger _logger;
    private readonly ChatCompletionsClient _chatClient;
    private readonly List<ChatRequestMessage> _conversationHistory;
    private readonly string _deploymentName;

    public SimpleChatApp(IConfiguration configuration, ILogger logger)
    {
        _configuration = configuration;
        _logger = logger;
        _conversationHistory = new List<ChatRequestMessage>();
        
        // Get configuration values
        var endpoint = _configuration["AzureAIFoundry:Endpoint"] ?? 
                      Environment.GetEnvironmentVariable("AZURE_AI_FOUNDRY_ENDPOINT");
        var apiKey = _configuration["AzureAIFoundry:ApiKey"] ?? 
                    Environment.GetEnvironmentVariable("AZURE_AI_FOUNDRY_API_KEY");
        
        _deploymentName = _configuration["AzureOpenAI:DeploymentName"] ?? 
                         Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME") ?? 
                         "gpt-4";

        if (string.IsNullOrEmpty(endpoint))
            throw new InvalidOperationException("Azure AI Foundry endpoint is required");

        // Initialize chat client
        TokenCredential credential;
        if (!string.IsNullOrEmpty(apiKey))
        {
            credential = new AzureKeyCredential(apiKey) as TokenCredential ?? new DefaultAzureCredential();
        }
        else
        {
            credential = new DefaultAzureCredential();
        }

        _chatClient = new ChatCompletionsClient(new Uri(endpoint), credential);

        // Add system message
        _conversationHistory.Add(new ChatRequestSystemMessage(
            "You are a helpful AI assistant powered by Azure AI Foundry. " +
            "You provide accurate, helpful, and friendly responses to user queries. " +
            "Keep your responses concise but informative."
        ));

        _logger.LogInformation("SimpleChatApp initialized with deployment: {DeploymentName}", _deploymentName);
    }

    public async Task RunAsync()
    {
        Console.WriteLine("\n🤖 Simple AI Chat Assistant");
        Console.WriteLine("Type your message and press Enter to chat.");
        Console.WriteLine("Type 'quit', 'exit', or 'q' to end the conversation.");
        Console.WriteLine("Type 'clear' to clear conversation history.");
        Console.WriteLine("Type 'help' for more commands.");
        Console.WriteLine("-" * 50);

        // Test connection first
        if (!await TestConnectionAsync())
        {
            Console.WriteLine("❌ Failed to connect to Azure AI Foundry. Please check your configuration.");
            return;
        }

        Console.WriteLine("✅ Connected to Azure AI Foundry successfully!");
        Console.WriteLine($"📝 Using model deployment: {_deploymentName}");

        while (true)
        {
            try
            {
                Console.Write("\n👤 You: ");
                var userInput = Console.ReadLine()?.Trim();

                if (string.IsNullOrEmpty(userInput))
                    continue;

                // Handle commands
                if (userInput.ToLower() is "quit" or "exit" or "q")
                {
                    Console.WriteLine("👋 Goodbye! Thanks for chatting.");
                    break;
                }

                if (userInput.ToLower() == "clear")
                {
                    ClearConversation();
                    Console.WriteLine("🧹 Conversation history cleared.");
                    continue;
                }

                if (userInput.ToLower() == "help")
                {
                    ShowHelp();
                    continue;
                }

                if (userInput.ToLower() == "history")
                {
                    ShowConversationHistory();
                    continue;
                }

                // Send message and get response
                var response = await SendMessageAsync(userInput);
                Console.WriteLine($"🤖 Assistant: {response}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error: {ex.Message}");
                _logger.LogError(ex, "Error processing user input");
            }
        }
    }

    private async Task<bool> TestConnectionAsync()
    {
        try
        {
            var testMessages = new List<ChatRequestMessage>
            {
                new ChatRequestSystemMessage("You are a helpful assistant."),
                new ChatRequestUserMessage("Say 'Connection test successful' in 3 words or less.")
            };

            var options = new ChatCompletionsOptions(_deploymentName, testMessages)
            {
                MaxTokens = 10,
                Temperature = 0.0f
            };

            var response = await _chatClient.GetChatCompletionsAsync(options);
            return response?.Value?.Choices?.Count > 0;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Connection test failed");
            return false;
        }
    }

    private async Task<string> SendMessageAsync(string userMessage)
    {
        // Add user message to conversation
        _conversationHistory.Add(new ChatRequestUserMessage(userMessage));

        try
        {
            // Create chat completion options
            var options = new ChatCompletionsOptions(_deploymentName, _conversationHistory)
            {
                MaxTokens = 1000,
                Temperature = 0.7f,
                FrequencyPenalty = 0.0f,
                PresencePenalty = 0.0f
            };

            // Get response from Azure AI Foundry
            var response = await _chatClient.GetChatCompletionsAsync(options);

            if (response?.Value?.Choices?.Count > 0)
            {
                var assistantMessage = response.Value.Choices[0].Message.Content;
                
                // Add assistant response to conversation history
                _conversationHistory.Add(new ChatRequestAssistantMessage(assistantMessage));

                // Keep conversation history manageable (limit to last 20 messages)
                if (_conversationHistory.Count > 21) // 1 system message + 20 conversation messages
                {
                    // Remove oldest user/assistant pairs, but keep system message
                    _conversationHistory.RemoveRange(1, 2);
                }

                // Log usage information if available
                if (response.Value.Usage != null)
                {
                    _logger.LogInformation(
                        "Token usage - Prompt: {PromptTokens}, Completion: {CompletionTokens}, Total: {TotalTokens}",
                        response.Value.Usage.PromptTokens,
                        response.Value.Usage.CompletionTokens,
                        response.Value.Usage.TotalTokens
                    );
                }

                return assistantMessage ?? "No response received.";
            }
            else
            {
                return "❌ No response received from the model.";
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting chat completion");
            
            // Remove the user message from history since we couldn't process it
            if (_conversationHistory.Count > 0 && 
                _conversationHistory[^1] is ChatRequestUserMessage)
            {
                _conversationHistory.RemoveAt(_conversationHistory.Count - 1);
            }

            return $"❌ Sorry, I encountered an error: {ex.Message}";
        }
    }

    private void ClearConversation()
    {
        // Keep only the system message
        var systemMessage = _conversationHistory.FirstOrDefault(m => m is ChatRequestSystemMessage);
        _conversationHistory.Clear();
        
        if (systemMessage != null)
        {
            _conversationHistory.Add(systemMessage);
        }

        _logger.LogInformation("Conversation history cleared");
    }

    private void ShowHelp()
    {
        Console.WriteLine("\n🆘 Available Commands:");
        Console.WriteLine("• help     - Show this help message");
        Console.WriteLine("• clear    - Clear conversation history");
        Console.WriteLine("• history  - Show conversation statistics");
        Console.WriteLine("• quit/exit/q - Exit the application");
        Console.WriteLine("\n💡 Tips:");
        Console.WriteLine("• The assistant remembers your conversation context");
        Console.WriteLine("• Conversation history is automatically managed");
        Console.WriteLine("• All interactions are logged for debugging");
    }

    private void ShowConversationHistory()
    {
        var userMessages = _conversationHistory.Count(m => m is ChatRequestUserMessage);
        var assistantMessages = _conversationHistory.Count(m => m is ChatRequestAssistantMessage);
        var totalMessages = _conversationHistory.Count - 1; // Exclude system message

        Console.WriteLine("\n📊 Conversation Statistics:");
        Console.WriteLine($"• Total messages: {totalMessages}");
        Console.WriteLine($"• User messages: {userMessages}");
        Console.WriteLine($"• Assistant messages: {assistantMessages}");
        Console.WriteLine($"• Model deployment: {_deploymentName}");
    }
}

/// <summary>
/// Configuration helper for chat application settings
/// </summary>
public class ChatAppConfig
{
    public string Endpoint { get; set; } = string.Empty;
    public string? ApiKey { get; set; }
    public string DeploymentName { get; set; } = "gpt-4";
    public int MaxTokens { get; set; } = 1000;
    public float Temperature { get; set; } = 0.7f;
    public int MaxConversationLength { get; set; } = 20;

    public static ChatAppConfig FromConfiguration(IConfiguration configuration)
    {
        return new ChatAppConfig
        {
            Endpoint = configuration["AzureAIFoundry:Endpoint"] ?? 
                      Environment.GetEnvironmentVariable("AZURE_AI_FOUNDRY_ENDPOINT") ?? 
                      string.Empty,
            ApiKey = configuration["AzureAIFoundry:ApiKey"] ?? 
                    Environment.GetEnvironmentVariable("AZURE_AI_FOUNDRY_API_KEY"),
            DeploymentName = configuration["AzureOpenAI:DeploymentName"] ?? 
                           Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME") ?? 
                           "gpt-4",
            MaxTokens = int.TryParse(configuration["ChatApp:MaxTokens"], out var maxTokens) ? maxTokens : 1000,
            Temperature = float.TryParse(configuration["ChatApp:Temperature"], out var temperature) ? temperature : 0.7f,
            MaxConversationLength = int.TryParse(configuration["ChatApp:MaxConversationLength"], out var maxLength) ? maxLength : 20
        };
    }

    public void Validate()
    {
        if (string.IsNullOrEmpty(Endpoint))
            throw new InvalidOperationException("Azure AI Foundry endpoint is required");

        if (!Uri.TryCreate(Endpoint, UriKind.Absolute, out _))
            throw new InvalidOperationException("Invalid Azure AI Foundry endpoint URL");

        if (MaxTokens <= 0)
            throw new InvalidOperationException("MaxTokens must be positive");

        if (Temperature < 0.0f || Temperature > 2.0f)
            throw new InvalidOperationException("Temperature must be between 0.0 and 2.0");
    }
} 