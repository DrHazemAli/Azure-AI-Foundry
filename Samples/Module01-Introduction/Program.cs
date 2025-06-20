using Azure;
using Azure.Identity;
using Azure.AI.Inference;
using System;
using System.Threading.Tasks;

namespace AzureAIFoundryIntroduction
{
    /// <summary>
    /// Module 01 - Introduction to Azure AI Foundry
    /// This sample demonstrates basic concepts of Azure AI Foundry including:
    /// - Connecting to Azure AI Foundry
    /// - Using chat completions with Azure OpenAI models
    /// - Basic error handling and best practices
    /// </summary>
    class Program
    {
        // Configuration - Replace with your actual values
        private static readonly string ProjectEndpoint = Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT") 
            ?? "https://your-project.aiservices.azure.com";
        private static readonly string ModelDeploymentName = "gpt-4o-mini"; // Default model deployment name

        static async Task Main(string[] args)
        {
            Console.WriteLine("=== Azure AI Foundry - Module 01 Introduction Sample ===\n");

            try
            {
                // Initialize the Azure AI Foundry client
                var client = CreateAIFoundryClient();
                
                // Demonstrate basic chat completion
                await DemonstrateChatCompletion(client);
                
                // Demonstrate system message usage
                await DemonstrateSystemMessage(client);
                
                // Demonstrate conversation context
                await DemonstrateConversationContext(client);

                Console.WriteLine("\n=== Sample completed successfully! ===");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
                Console.WriteLine("\nPlease ensure you have:");
                Console.WriteLine("1. Set the AZURE_AI_PROJECT_ENDPOINT environment variable");
                Console.WriteLine("2. Authenticated with Azure CLI (az login)");
                Console.WriteLine("3. Deployed a model in your Azure AI Foundry project");
            }

            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }

        /// <summary>
        /// Creates and configures the Azure AI Foundry client
        /// </summary>
        private static ChatCompletionsClient CreateAIFoundryClient()
        {
            Console.WriteLine("🔗 Connecting to Azure AI Foundry...");
            
            // Use DefaultAzureCredential for authentication
            // This supports multiple authentication methods including:
            // - Azure CLI (az login)
            // - Managed Identity
            // - Environment variables
            // - Visual Studio / VS Code
            var credential = new DefaultAzureCredential();

            // Create the chat completions client
            var client = new ChatCompletionsClient(
                new Uri(ProjectEndpoint),
                credential
            );

            Console.WriteLine("✅ Connected successfully!\n");
            return client;
        }

        /// <summary>
        /// Demonstrates basic chat completion functionality
        /// </summary>
        private static async Task DemonstrateChatCompletion(ChatCompletionsClient client)
        {
            Console.WriteLine("📝 Demonstrating Basic Chat Completion");
            Console.WriteLine("=====================================");

            var requestOptions = new ChatCompletionsOptions()
            {
                Messages =
                {
                    new ChatRequestUserMessage("What is Azure AI Foundry? Please provide a brief explanation.")
                },
                Model = ModelDeploymentName,
                MaxTokens = 200,
                Temperature = 0.7f
            };

            try
            {
                Console.WriteLine("🤖 Sending request to Azure AI Foundry...");
                Response<ChatCompletions> response = await client.CompleteAsync(requestOptions);
                
                string responseContent = response.Value.Choices[0].Message.Content;
                Console.WriteLine($"✨ Response: {responseContent}");
                
                // Display usage information
                var usage = response.Value.Usage;
                Console.WriteLine($"📊 Token Usage - Prompt: {usage.PromptTokens}, Completion: {usage.CompletionTokens}, Total: {usage.TotalTokens}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error during chat completion: {ex.Message}");
            }

            Console.WriteLine();
        }

        /// <summary>
        /// Demonstrates the use of system messages to control AI behavior
        /// </summary>
        private static async Task DemonstrateSystemMessage(ChatCompletionsClient client)
        {
            Console.WriteLine("🎭 Demonstrating System Message Usage");
            Console.WriteLine("====================================");

            var requestOptions = new ChatCompletionsOptions()
            {
                Messages =
                {
                    new ChatRequestSystemMessage("You are a helpful AI assistant specializing in Azure cloud services. " +
                                                "Always provide accurate, technical information and include practical examples when possible. " +
                                                "Keep responses concise but informative."),
                    new ChatRequestUserMessage("How does Azure AI Foundry help with multi-agent orchestration?")
                },
                Model = ModelDeploymentName,
                MaxTokens = 300,
                Temperature = 0.5f
            };

            try
            {
                Console.WriteLine("🤖 Sending request with system message...");
                Response<ChatCompletions> response = await client.CompleteAsync(requestOptions);
                
                string responseContent = response.Value.Choices[0].Message.Content;
                Console.WriteLine($"✨ Response: {responseContent}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error during system message demo: {ex.Message}");
            }

            Console.WriteLine();
        }

        /// <summary>
        /// Demonstrates maintaining conversation context across multiple exchanges
        /// </summary>
        private static async Task DemonstrateConversationContext(ChatCompletionsClient client)
        {
            Console.WriteLine("💬 Demonstrating Conversation Context");
            Console.WriteLine("====================================");

            // Start with a conversation history
            var messages = new List<ChatRequestMessage>
            {
                new ChatRequestSystemMessage("You are an Azure AI expert. Keep track of our conversation and reference previous topics when relevant."),
                new ChatRequestUserMessage("What are the main benefits of using Azure AI Foundry?")
            };

            try
            {
                // First exchange
                Console.WriteLine("🤖 First exchange...");
                var firstResponse = await GetChatResponse(client, messages);
                Console.WriteLine($"✨ AI: {firstResponse}");
                
                // Add the AI response to conversation history
                messages.Add(new ChatRequestAssistantMessage(firstResponse));
                
                // Second exchange - referencing previous context
                messages.Add(new ChatRequestUserMessage("Can you elaborate on the agent orchestration benefit you mentioned?"));
                
                Console.WriteLine("\n🤖 Second exchange (with context)...");
                var secondResponse = await GetChatResponse(client, messages);
                Console.WriteLine($"✨ AI: {secondResponse}");
                
                Console.WriteLine("\n📋 Conversation Summary:");
                Console.WriteLine($"- Total messages in conversation: {messages.Count}");
                Console.WriteLine("- The AI maintained context between exchanges");
                Console.WriteLine("- System message guided the AI's expertise domain");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error during conversation demo: {ex.Message}");
            }

            Console.WriteLine();
        }

        /// <summary>
        /// Helper method to get chat response and handle common scenarios
        /// </summary>
        private static async Task<string> GetChatResponse(ChatCompletionsClient client, List<ChatRequestMessage> messages)
        {
            var requestOptions = new ChatCompletionsOptions()
            {
                Model = ModelDeploymentName,
                MaxTokens = 250,
                Temperature = 0.7f
            };

            // Add all messages to the request
            foreach (var message in messages)
            {
                requestOptions.Messages.Add(message);
            }

            Response<ChatCompletions> response = await client.CompleteAsync(requestOptions);
            return response.Value.Choices[0].Message.Content;
        }
    }

    /// <summary>
    /// Extension methods for better code organization
    /// </summary>
    public static class AzureAIFoundryExtensions
    {
        /// <summary>
        /// Creates a formatted display of model information
        /// </summary>
        public static void DisplayModelInfo(this ChatCompletions completions, string modelName)
        {
            Console.WriteLine($"🔧 Model: {modelName}");
            Console.WriteLine($"📈 Choices: {completions.Choices.Count}");
            Console.WriteLine($"🆔 Request ID: {completions.Id}");
            Console.WriteLine($"⏰ Created: {completions.Created}");
        }

        /// <summary>
        /// Creates a formatted display of usage statistics
        /// </summary>
        public static void DisplayUsageStats(this CompletionsUsage usage)
        {
            Console.WriteLine("📊 Usage Statistics:");
            Console.WriteLine($"   • Prompt Tokens: {usage.PromptTokens}");
            Console.WriteLine($"   • Completion Tokens: {usage.CompletionTokens}");
            Console.WriteLine($"   • Total Tokens: {usage.TotalTokens}");
        }
    }
} 