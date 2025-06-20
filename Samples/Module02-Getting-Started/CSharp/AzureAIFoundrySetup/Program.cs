using System;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Identity;
using Azure.AI.Projects;
using Azure.AI.Inference;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace AzureAIFoundrySetup;

/// <summary>
/// Demonstrates Azure AI Foundry setup and authentication patterns
/// </summary>
public class Program
{
    private static ILogger<Program>? _logger;
    private static IConfiguration? _configuration;

    public static async Task Main(string[] args)
    {
        Console.WriteLine("🚀 Azure AI Foundry - Setup and Authentication Demo");
        Console.WriteLine("=" * 60);

        try
        {
            // Setup dependency injection and configuration
            var host = CreateHostBuilder(args).Build();
            _logger = host.Services.GetRequiredService<ILogger<Program>>();
            _configuration = host.Services.GetRequiredService<IConfiguration>();

            _logger.LogInformation("Starting Azure AI Foundry setup and authentication demo");

            // Run authentication demos
            await RunAuthenticationDemos();

            _logger.LogInformation("Demo completed successfully");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Error: {ex.Message}");
            _logger?.LogError(ex, "Demo failed with error");
        }

        Console.WriteLine("\nPress any key to exit...");
        Console.ReadKey();
    }

    private static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .ConfigureAppConfiguration((context, config) =>
            {
                config.AddJsonFile("appsettings.json", optional: true);
                config.AddEnvironmentVariables();
                config.AddUserSecrets<Program>();
            })
            .ConfigureLogging(logging =>
            {
                logging.ClearProviders();
                logging.AddConsole();
                logging.AddDebug();
                logging.SetMinimumLevel(LogLevel.Information);
            });

    private static async Task RunAuthenticationDemos()
    {
        Console.WriteLine("\n🔐 Testing Authentication Methods");
        Console.WriteLine("-" * 40);

        // Get configuration values
        var endpoint = _configuration?["AzureAIFoundry:Endpoint"] ?? 
                      Environment.GetEnvironmentVariable("AZURE_AI_FOUNDRY_ENDPOINT");
        var apiKey = _configuration?["AzureAIFoundry:ApiKey"] ?? 
                    Environment.GetEnvironmentVariable("AZURE_AI_FOUNDRY_API_KEY");

        if (string.IsNullOrEmpty(endpoint))
        {
            Console.WriteLine("❌ Azure AI Foundry endpoint not configured");
            return;
        }

        // Test different authentication methods
        await TestApiKeyAuthentication(endpoint, apiKey);
        await TestManagedIdentityAuthentication(endpoint);
        await TestDefaultCredentialAuthentication(endpoint);
        await TestServicePrincipalAuthentication(endpoint);
    }

    private static async Task TestApiKeyAuthentication(string endpoint, string? apiKey)
    {
        Console.WriteLine("\n1️⃣ Testing API Key Authentication");
        
        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine("   ⚠️  API Key not configured - skipping");
            return;
        }

        try
        {
            var credential = new AzureKeyCredential(apiKey);
            var client = new ChatCompletionsClient(new Uri(endpoint), credential);

            // Test connection with a simple request
            var testSuccess = await TestConnection(client, "API Key");
            
            if (testSuccess)
            {
                Console.WriteLine("   ✅ API Key authentication successful");
                _logger?.LogInformation("API Key authentication test passed");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   ❌ API Key authentication failed: {ex.Message}");
            _logger?.LogWarning(ex, "API Key authentication test failed");
        }
    }

    private static async Task TestManagedIdentityAuthentication(string endpoint)
    {
        Console.WriteLine("\n2️⃣ Testing Managed Identity Authentication");

        try
        {
            var credential = new ManagedIdentityCredential();
            var client = new ChatCompletionsClient(new Uri(endpoint), credential);

            var testSuccess = await TestConnection(client, "Managed Identity");
            
            if (testSuccess)
            {
                Console.WriteLine("   ✅ Managed Identity authentication successful");
                _logger?.LogInformation("Managed Identity authentication test passed");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   ⚠️  Managed Identity authentication not available: {ex.Message}");
            _logger?.LogInformation("Managed Identity authentication not available in current environment");
        }
    }

    private static async Task TestDefaultCredentialAuthentication(string endpoint)
    {
        Console.WriteLine("\n3️⃣ Testing Default Azure Credential");

        try
        {
            var credential = new DefaultAzureCredential();
            var client = new ChatCompletionsClient(new Uri(endpoint), credential);

            var testSuccess = await TestConnection(client, "Default Credential");
            
            if (testSuccess)
            {
                Console.WriteLine("   ✅ Default Azure Credential authentication successful");
                _logger?.LogInformation("Default Azure Credential authentication test passed");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   ⚠️  Default Azure Credential failed: {ex.Message}");
            _logger?.LogWarning(ex, "Default Azure Credential authentication test failed");
        }
    }

    private static async Task TestServicePrincipalAuthentication(string endpoint)
    {
        Console.WriteLine("\n4️⃣ Testing Service Principal Authentication");

        var clientId = _configuration?["AzureAD:ClientId"] ?? 
                      Environment.GetEnvironmentVariable("AZURE_CLIENT_ID");
        var clientSecret = _configuration?["AzureAD:ClientSecret"] ?? 
                          Environment.GetEnvironmentVariable("AZURE_CLIENT_SECRET");
        var tenantId = _configuration?["AzureAD:TenantId"] ?? 
                      Environment.GetEnvironmentVariable("AZURE_TENANT_ID");

        if (string.IsNullOrEmpty(clientId) || string.IsNullOrEmpty(clientSecret) || string.IsNullOrEmpty(tenantId))
        {
            Console.WriteLine("   ⚠️  Service Principal credentials not configured - skipping");
            return;
        }

        try
        {
            var credential = new ClientSecretCredential(tenantId, clientId, clientSecret);
            var client = new ChatCompletionsClient(new Uri(endpoint), credential);

            var testSuccess = await TestConnection(client, "Service Principal");
            
            if (testSuccess)
            {
                Console.WriteLine("   ✅ Service Principal authentication successful");
                _logger?.LogInformation("Service Principal authentication test passed");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   ❌ Service Principal authentication failed: {ex.Message}");
            _logger?.LogWarning(ex, "Service Principal authentication test failed");
        }
    }

    private static async Task<bool> TestConnection(ChatCompletionsClient client, string authMethod)
    {
        try
        {
            var deploymentName = _configuration?["AzureOpenAI:DeploymentName"] ?? 
                               Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME") ?? 
                               "gpt-4";

            Console.WriteLine($"   🔄 Testing connection using {authMethod}...");

            // Create a simple test message
            var messages = new List<ChatRequestMessage>
            {
                new ChatRequestSystemMessage("You are a helpful assistant."),
                new ChatRequestUserMessage("Say 'Connection test successful' if you can read this.")
            };

            var chatCompletionsOptions = new ChatCompletionsOptions(deploymentName, messages)
            {
                MaxTokens = 10,
                Temperature = 0.0f
            };

            var response = await client.GetChatCompletionsAsync(chatCompletionsOptions);

            if (response?.Value?.Choices?.Count > 0)
            {
                var content = response.Value.Choices[0].Message.Content;
                Console.WriteLine($"   📝 Response: {content}");
                return true;
            }

            return false;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   ❌ Connection test failed: {ex.Message}");
            return false;
        }
    }
}

/// <summary>
/// Configuration helper class for Azure AI Foundry settings
/// </summary>
public class AzureAIFoundryConfig
{
    public string Endpoint { get; set; } = string.Empty;
    public string? ApiKey { get; set; }
    public string DeploymentName { get; set; } = "gpt-4";
    public string ApiVersion { get; set; } = "2024-02-15-preview";
    public int MaxTokens { get; set; } = 1000;
    public float Temperature { get; set; } = 0.7f;
    public int Timeout { get; set; } = 30;
    public int MaxRetries { get; set; } = 3;

    /// <summary>
    /// Validate configuration settings
    /// </summary>
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

/// <summary>
/// Authentication helper class
/// </summary>
public static class AuthenticationHelper
{
    /// <summary>
    /// Get the appropriate credential based on available configuration
    /// </summary>
    public static TokenCredential GetCredential(IConfiguration configuration)
    {
        // Try API key first
        var apiKey = configuration["AzureAIFoundry:ApiKey"] ?? 
                    Environment.GetEnvironmentVariable("AZURE_AI_FOUNDRY_API_KEY");
        
        if (!string.IsNullOrEmpty(apiKey))
        {
            return new AzureKeyCredential(apiKey) as TokenCredential ?? new DefaultAzureCredential();
        }

        // Try service principal
        var clientId = configuration["AzureAD:ClientId"] ?? 
                      Environment.GetEnvironmentVariable("AZURE_CLIENT_ID");
        var clientSecret = configuration["AzureAD:ClientSecret"] ?? 
                          Environment.GetEnvironmentVariable("AZURE_CLIENT_SECRET");
        var tenantId = configuration["AzureAD:TenantId"] ?? 
                      Environment.GetEnvironmentVariable("AZURE_TENANT_ID");

        if (!string.IsNullOrEmpty(clientId) && !string.IsNullOrEmpty(clientSecret) && !string.IsNullOrEmpty(tenantId))
        {
            return new ClientSecretCredential(tenantId, clientId, clientSecret);
        }

        // Fall back to default credential chain
        return new DefaultAzureCredential();
    }

    /// <summary>
    /// Test authentication with the provided credential
    /// </summary>
    public static async Task<bool> TestAuthenticationAsync(TokenCredential credential, string endpoint, string deploymentName)
    {
        try
        {
            var client = new ChatCompletionsClient(new Uri(endpoint), credential);
            
            var messages = new List<ChatRequestMessage>
            {
                new ChatRequestSystemMessage("You are a helpful assistant."),
                new ChatRequestUserMessage("Test message")
            };

            var options = new ChatCompletionsOptions(deploymentName, messages)
            {
                MaxTokens = 1,
                Temperature = 0.0f
            };

            var response = await client.GetChatCompletionsAsync(options);
            return response?.Value != null;
        }
        catch
        {
            return false;
        }
    }
} 