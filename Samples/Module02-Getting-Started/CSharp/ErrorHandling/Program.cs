using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Net;
using Azure.Core;
using Azure.Identity;
using Azure.AI.Inference;
using Azure.AI.Inference.Models;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace ErrorHandling;

/// <summary>
/// Demonstrates comprehensive error handling and retry logic for Azure AI Foundry
/// </summary>
public class Program
{
    private static ILogger<Program>? _logger;
    private static IConfiguration? _configuration;

    public static async Task Main(string[] args)
    {
        Console.WriteLine("🛡️ Azure AI Foundry - Error Handling and Retry Logic Demo");
        Console.WriteLine("=" * 60);

        try
        {
            // Setup dependency injection and configuration
            var host = CreateHostBuilder(args).Build();
            _logger = host.Services.GetRequiredService<ILogger<Program>>();
            _configuration = host.Services.GetRequiredService<IConfiguration>();

            _logger.LogInformation("Starting Azure AI Foundry error handling demo");

            // Create resilient chat client
            var resilientClient = new ResilientChatClient(_configuration, _logger);

            // Run error handling demonstrations
            await RunErrorHandlingDemos(resilientClient);

            _logger.LogInformation("Demo completed successfully");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Critical Error: {ex.Message}");
            _logger?.LogCritical(ex, "Demo failed with critical error");
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

    private static async Task RunErrorHandlingDemos(ResilientChatClient client)
    {
        Console.WriteLine("\n🔧 Testing Error Handling Scenarios");
        Console.WriteLine("-" * 50);

        // Test 1: Normal operation
        await TestNormalOperation(client);

        // Test 2: Network retry scenario
        await TestNetworkRetry(client);

        // Test 3: Rate limiting scenario
        await TestRateLimiting(client);

        // Test 4: Invalid configuration
        await TestInvalidConfiguration();

        // Test 5: Circuit breaker pattern
        await TestCircuitBreaker(client);

        // Test 6: Timeout handling
        await TestTimeoutHandling(client);

        Console.WriteLine("\n✅ All error handling tests completed");
    }

    private static async Task TestNormalOperation(ResilientChatClient client)
    {
        Console.WriteLine("\n1️⃣ Testing Normal Operation");
        
        try
        {
            var response = await client.SendMessageAsync(
                "Hello! This is a test message for normal operation."
            );
            
            Console.WriteLine($"   ✅ Normal operation successful");
            Console.WriteLine($"   📝 Response: {response.Substring(0, Math.Min(50, response.Length))}...");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   ❌ Normal operation failed: {ex.Message}");
        }
    }

    private static async Task TestNetworkRetry(ResilientChatClient client)
    {
        Console.WriteLine("\n2️⃣ Testing Network Retry Logic");
        
        try
        {
            // This will trigger retry logic if network issues occur
            var response = await client.SendMessageWithRetryAsync(
                "Test message for retry logic demonstration",
                maxRetries: 3
            );
            
            Console.WriteLine($"   ✅ Network retry test successful");
            Console.WriteLine($"   📝 Response received after retry attempts");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   ⚠️  Network retry test completed with error: {ex.Message}");
        }
    }

    private static async Task TestRateLimiting(ResilientChatClient client)
    {
        Console.WriteLine("\n3️⃣ Testing Rate Limiting Handling");
        
        try
        {
            // Send multiple rapid requests to potentially trigger rate limiting
            var tasks = new List<Task<string>>();
            
            for (int i = 0; i < 5; i++)
            {
                tasks.Add(client.SendMessageAsync($"Rate limit test message {i + 1}"));
            }

            var results = await Task.WhenAll(tasks);
            Console.WriteLine($"   ✅ Rate limiting test completed - {results.Length} responses received");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   ⚠️  Rate limiting test completed with error: {ex.Message}");
        }
    }

    private static async Task TestInvalidConfiguration()
    {
        Console.WriteLine("\n4️⃣ Testing Invalid Configuration Handling");
        
        try
        {
            // Create client with invalid configuration to test error handling
            var invalidConfig = new ConfigurationBuilder()
                .AddInMemoryCollection(new Dictionary<string, string?>
                {
                    ["AzureAIFoundry:Endpoint"] = "https://invalid-endpoint.com",
                    ["AzureAIFoundry:ApiKey"] = "invalid-key"
                })
                .Build();

            var invalidClient = new ResilientChatClient(invalidConfig, _logger!);
            
            await invalidClient.SendMessageAsync("This should fail with invalid configuration");
            Console.WriteLine($"   ❌ Invalid configuration test failed - should have thrown exception");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   ✅ Invalid configuration properly handled: {ex.GetType().Name}");
        }
    }

    private static async Task TestCircuitBreaker(ResilientChatClient client)
    {
        Console.WriteLine("\n5️⃣ Testing Circuit Breaker Pattern");
        
        try
        {
            // Test circuit breaker behavior
            var circuitBreakerResult = await client.TestCircuitBreakerAsync();
            
            if (circuitBreakerResult)
            {
                Console.WriteLine($"   ✅ Circuit breaker test successful");
            }
            else
            {
                Console.WriteLine($"   ⚠️  Circuit breaker activated - preventing further calls");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   ⚠️  Circuit breaker test error: {ex.Message}");
        }
    }

    private static async Task TestTimeoutHandling(ResilientChatClient client)
    {
        Console.WriteLine("\n6️⃣ Testing Timeout Handling");
        
        try
        {
            // Test with very short timeout to trigger timeout handling
            var response = await client.SendMessageWithTimeoutAsync(
                "This is a timeout test message",
                timeoutSeconds: 1
            );
            
            Console.WriteLine($"   ✅ Timeout handling test successful");
        }
        catch (TimeoutException)
        {
            Console.WriteLine($"   ✅ Timeout properly handled");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"   ⚠️  Timeout test error: {ex.Message}");
        }
    }
}

/// <summary>
/// Resilient chat client with comprehensive error handling and retry logic
/// </summary>
public class ResilientChatClient
{
    private readonly IConfiguration _configuration;
    private readonly ILogger _logger;
    private readonly ChatCompletionsClient _chatClient;
    private readonly CircuitBreakerState _circuitBreaker;
    private readonly RetryPolicy _retryPolicy;

    public ResilientChatClient(IConfiguration configuration, ILogger logger)
    {
        _configuration = configuration;
        _logger = logger;
        _circuitBreaker = new CircuitBreakerState();
        _retryPolicy = new RetryPolicy();

        // Initialize chat client with error handling
        try
        {
            var endpoint = GetRequiredConfiguration("AZURE_AI_FOUNDRY_ENDPOINT");
            var credential = GetCredential();
            
            _chatClient = new ChatCompletionsClient(new Uri(endpoint), credential);
            _logger.LogInformation("ResilientChatClient initialized successfully");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to initialize ResilientChatClient");
            throw;
        }
    }

    public async Task<string> SendMessageAsync(string message)
    {
        return await SendMessageWithRetryAsync(message, _retryPolicy.MaxRetries);
    }

    public async Task<string> SendMessageWithRetryAsync(string message, int maxRetries)
    {
        var attempt = 0;
        Exception? lastException = null;

        while (attempt <= maxRetries)
        {
            try
            {
                // Check circuit breaker
                if (_circuitBreaker.IsOpen)
                {
                    throw new InvalidOperationException("Circuit breaker is open - service unavailable");
                }

                var response = await SendMessageInternalAsync(message);
                
                // Reset circuit breaker on success
                _circuitBreaker.RecordSuccess();
                
                return response;
            }
            catch (Exception ex) when (IsRetryableError(ex))
            {
                lastException = ex;
                attempt++;
                
                // Record failure for circuit breaker
                _circuitBreaker.RecordFailure();

                if (attempt <= maxRetries)
                {
                    var delay = _retryPolicy.GetDelay(attempt);
                    _logger.LogWarning(
                        "Attempt {Attempt} failed, retrying in {Delay}ms: {Error}",
                        attempt, delay, ex.Message
                    );
                    
                    await Task.Delay(delay);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Non-retryable error occurred");
                throw;
            }
        }

        _logger.LogError("All retry attempts exhausted");
        throw lastException ?? new InvalidOperationException("All retry attempts failed");
    }

    public async Task<string> SendMessageWithTimeoutAsync(string message, int timeoutSeconds)
    {
        using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(timeoutSeconds));
        
        try
        {
            var response = await SendMessageInternalAsync(message, cts.Token);
            return response;
        }
        catch (OperationCanceledException) when (cts.Token.IsCancellationRequested)
        {
            throw new TimeoutException($"Operation timed out after {timeoutSeconds} seconds");
        }
    }

    public async Task<bool> TestCircuitBreakerAsync()
    {
        try
        {
            if (_circuitBreaker.IsOpen)
            {
                _logger.LogInformation("Circuit breaker is open");
                return false;
            }

            // Try to send a test message
            await SendMessageAsync("Circuit breaker test");
            return true;
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Circuit breaker test failed");
            return false;
        }
    }

    private async Task<string> SendMessageInternalAsync(string message, CancellationToken cancellationToken = default)
    {
        var deploymentName = _configuration["AzureOpenAI:DeploymentName"] ?? 
                           Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME") ?? 
                           "gpt-4";

        var messages = new List<ChatRequestMessage>
        {
            new ChatRequestSystemMessage("You are a helpful assistant."),
            new ChatRequestUserMessage(message)
        };

        var options = new ChatCompletionsOptions(deploymentName, messages)
        {
            MaxTokens = 100,
            Temperature = 0.7f
        };

        var response = await _chatClient.GetChatCompletionsAsync(options, cancellationToken);

        if (response?.Value?.Choices?.Count > 0)
        {
            return response.Value.Choices[0].Message.Content ?? "No response content";
        }

        throw new InvalidOperationException("No valid response received from the service");
    }

    private string GetRequiredConfiguration(string key)
    {
        var value = _configuration[key.Replace("_", ":")] ?? Environment.GetEnvironmentVariable(key);
        
        if (string.IsNullOrEmpty(value))
        {
            throw new InvalidOperationException($"Required configuration '{key}' is missing");
        }

        return value;
    }

    private TokenCredential GetCredential()
    {
        var apiKey = _configuration["AzureAIFoundry:ApiKey"] ?? 
                    Environment.GetEnvironmentVariable("AZURE_AI_FOUNDRY_API_KEY");

        if (!string.IsNullOrEmpty(apiKey))
        {
            return new AzureKeyCredential(apiKey) as TokenCredential ?? new DefaultAzureCredential();
        }

        return new DefaultAzureCredential();
    }

    private static bool IsRetryableError(Exception ex)
    {
        return ex switch
        {
            HttpRequestException => true,
            TaskCanceledException => true,
            RequestFailedException rfe => rfe.Status is >= 500 or 429,
            _ => false
        };
    }
}

/// <summary>
/// Circuit breaker implementation for preventing cascade failures
/// </summary>
public class CircuitBreakerState
{
    private int _failureCount = 0;
    private DateTime _lastFailureTime = DateTime.MinValue;
    private readonly int _failureThreshold = 5;
    private readonly TimeSpan _timeout = TimeSpan.FromMinutes(1);

    public bool IsOpen => _failureCount >= _failureThreshold && 
                         DateTime.UtcNow - _lastFailureTime < _timeout;

    public void RecordSuccess()
    {
        _failureCount = 0;
    }

    public void RecordFailure()
    {
        _failureCount++;
        _lastFailureTime = DateTime.UtcNow;
    }
}

/// <summary>
/// Retry policy with exponential backoff
/// </summary>
public class RetryPolicy
{
    public int MaxRetries { get; set; } = 3;
    public int BaseDelayMs { get; set; } = 1000;
    public int MaxDelayMs { get; set; } = 30000;

    public int GetDelay(int attempt)
    {
        var delay = BaseDelayMs * Math.Pow(2, attempt - 1);
        return Math.Min((int)delay, MaxDelayMs);
    }
}

/// <summary>
/// Custom exception types for better error handling
/// </summary>
public class AzureAIFoundryException : Exception
{
    public string? ErrorCode { get; }
    public int? HttpStatusCode { get; }

    public AzureAIFoundryException(string message) : base(message) { }

    public AzureAIFoundryException(string message, Exception innerException) 
        : base(message, innerException) { }

    public AzureAIFoundryException(string message, string? errorCode, int? httpStatusCode) 
        : base(message)
    {
        ErrorCode = errorCode;
        HttpStatusCode = httpStatusCode;
    }
}

public class RateLimitException : AzureAIFoundryException
{
    public TimeSpan RetryAfter { get; }

    public RateLimitException(string message, TimeSpan retryAfter) 
        : base(message, "RateLimitExceeded", 429)
    {
        RetryAfter = retryAfter;
    }
}

public class QuotaExceededException : AzureAIFoundryException
{
    public QuotaExceededException(string message) 
        : base(message, "QuotaExceeded", 429) { }
}

/// <summary>
/// Health check service for monitoring application health
/// </summary>
public class HealthCheckService
{
    private readonly ResilientChatClient _client;
    private readonly ILogger _logger;

    public HealthCheckService(ResilientChatClient client, ILogger logger)
    {
        _client = client;
        _logger = logger;
    }

    public async Task<HealthStatus> CheckHealthAsync()
    {
        try
        {
            var response = await _client.SendMessageAsync("Health check test");
            
            return new HealthStatus
            {
                IsHealthy = true,
                Message = "Service is healthy",
                LastChecked = DateTime.UtcNow
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Health check failed");
            
            return new HealthStatus
            {
                IsHealthy = false,
                Message = $"Service is unhealthy: {ex.Message}",
                LastChecked = DateTime.UtcNow
            };
        }
    }
}

public class HealthStatus
{
    public bool IsHealthy { get; set; }
    public string Message { get; set; } = string.Empty;
    public DateTime LastChecked { get; set; }
} 