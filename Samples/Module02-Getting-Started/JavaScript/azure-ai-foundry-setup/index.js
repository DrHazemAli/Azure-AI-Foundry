#!/usr/bin/env node
/**
 * Azure AI Foundry - Setup and Authentication Demo
 * 
 * This sample demonstrates how to set up and authenticate with Azure AI Foundry
 * using different authentication methods and configuration patterns.
 * 
 * Features:
 * - Multiple authentication methods
 * - Environment configuration
 * - Connection validation
 * - Error handling
 * 
 * @author Hazem Ali
 * @course Azure AI Foundry Zero-to-Hero
 * @module 02 - Getting Started
 */

const { DefaultAzureCredential, ClientSecretCredential, ManagedIdentityCredential } = require('@azure/identity');
const { ChatCompletionsClient } = require('@azure/ai-inference');
const { AzureKeyCredential } = require('@azure/core-auth');
require('dotenv').config();

// Configuration class
class AzureAIFoundryConfig {
    constructor() {
        this.endpoint = process.env.AZURE_AI_FOUNDRY_ENDPOINT || '';
        this.apiKey = process.env.AZURE_AI_FOUNDRY_API_KEY || '';
        this.deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || 'gpt-4';
        this.apiVersion = process.env.AZURE_OPENAI_API_VERSION || '2024-02-15-preview';
        
        // Azure AD credentials
        this.clientId = process.env.AZURE_CLIENT_ID || '';
        this.clientSecret = process.env.AZURE_CLIENT_SECRET || '';
        this.tenantId = process.env.AZURE_TENANT_ID || '';
        
        this.validate();
    }

    validate() {
        if (!this.endpoint) {
            throw new Error('AZURE_AI_FOUNDRY_ENDPOINT is required');
        }

        try {
            new URL(this.endpoint);
        } catch {
            throw new Error('Invalid Azure AI Foundry endpoint URL');
        }

        console.log('✅ Configuration validated successfully');
    }
}

// Authentication helper
class AuthenticationHelper {
    static getApiKeyCredential(apiKey) {
        if (!apiKey) {
            throw new Error('API key is required');
        }
        return new AzureKeyCredential(apiKey);
    }

    static getDefaultCredential() {
        return new DefaultAzureCredential();
    }

    static getServicePrincipalCredential(tenantId, clientId, clientSecret) {
        if (!tenantId || !clientId || !clientSecret) {
            throw new Error('Service principal credentials are incomplete');
        }
        return new ClientSecretCredential(tenantId, clientId, clientSecret);
    }

    static getManagedIdentityCredential(clientId = null) {
        return new ManagedIdentityCredential(clientId);
    }
}

// Main demo class
class AzureAIFoundrySetupDemo {
    constructor() {
        this.config = new AzureAIFoundryConfig();
        console.log('🚀 Azure AI Foundry - Setup and Authentication Demo');
        console.log('='.repeat(60));
    }

    async run() {
        try {
            console.log('\n🔐 Testing Authentication Methods');
            console.log('-'.repeat(40));

            // Test different authentication methods
            await this.testApiKeyAuthentication();
            await this.testDefaultCredentialAuthentication();
            await this.testServicePrincipalAuthentication();
            await this.testManagedIdentityAuthentication();

            console.log('\n✅ All authentication tests completed');
        } catch (error) {
            console.error('❌ Demo failed:', error.message);
            process.exit(1);
        }
    }

    async testApiKeyAuthentication() {
        console.log('\n1️⃣ Testing API Key Authentication');
        
        if (!this.config.apiKey) {
            console.log('   ⚠️  API Key not configured - skipping');
            return;
        }

        try {
            const credential = AuthenticationHelper.getApiKeyCredential(this.config.apiKey);
            const client = new ChatCompletionsClient(this.config.endpoint, credential);
            
            const success = await this.testConnection(client, 'API Key');
            
            if (success) {
                console.log('   ✅ API Key authentication successful');
            }
        } catch (error) {
            console.log(`   ❌ API Key authentication failed: ${error.message}`);
        }
    }

    async testDefaultCredentialAuthentication() {
        console.log('\n2️⃣ Testing Default Azure Credential');

        try {
            const credential = AuthenticationHelper.getDefaultCredential();
            const client = new ChatCompletionsClient(this.config.endpoint, credential);
            
            const success = await this.testConnection(client, 'Default Credential');
            
            if (success) {
                console.log('   ✅ Default Azure Credential authentication successful');
            }
        } catch (error) {
            console.log(`   ⚠️  Default Azure Credential failed: ${error.message}`);
        }
    }

    async testServicePrincipalAuthentication() {
        console.log('\n3️⃣ Testing Service Principal Authentication');

        if (!this.config.clientId || !this.config.clientSecret || !this.config.tenantId) {
            console.log('   ⚠️  Service Principal credentials not configured - skipping');
            return;
        }

        try {
            const credential = AuthenticationHelper.getServicePrincipalCredential(
                this.config.tenantId,
                this.config.clientId,
                this.config.clientSecret
            );
            const client = new ChatCompletionsClient(this.config.endpoint, credential);
            
            const success = await this.testConnection(client, 'Service Principal');
            
            if (success) {
                console.log('   ✅ Service Principal authentication successful');
            }
        } catch (error) {
            console.log(`   ❌ Service Principal authentication failed: ${error.message}`);
        }
    }

    async testManagedIdentityAuthentication() {
        console.log('\n4️⃣ Testing Managed Identity Authentication');

        try {
            const credential = AuthenticationHelper.getManagedIdentityCredential();
            const client = new ChatCompletionsClient(this.config.endpoint, credential);
            
            const success = await this.testConnection(client, 'Managed Identity');
            
            if (success) {
                console.log('   ✅ Managed Identity authentication successful');
            }
        } catch (error) {
            console.log(`   ⚠️  Managed Identity authentication not available: ${error.message}`);
        }
    }

    async testConnection(client, authMethod) {
        try {
            console.log(`   🔄 Testing connection using ${authMethod}...`);

            const messages = [
                { role: 'system', content: 'You are a helpful assistant.' },
                { role: 'user', content: 'Say "Connection test successful" if you can read this.' }
            ];

            const options = {
                model: this.config.deploymentName,
                messages: messages,
                maxTokens: 10,
                temperature: 0.0
            };

            const response = await client.getChatCompletions(options);
            
            if (response && response.choices && response.choices.length > 0) {
                const content = response.choices[0].message.content;
                console.log(`   📝 Response: ${content}`);
                return true;
            }

            return false;
        } catch (error) {
            console.log(`   ❌ Connection test failed: ${error.message}`);
            return false;
        }
    }
}

// Connection validator utility
class ConnectionValidator {
    static async validateEndpoint(endpoint) {
        try {
            const url = new URL(endpoint);
            console.log(`🔍 Validating endpoint: ${url.origin}`);
            
            // Basic URL validation
            if (!url.protocol.startsWith('https')) {
                throw new Error('Endpoint must use HTTPS');
            }

            return true;
        } catch (error) {
            console.error(`❌ Invalid endpoint: ${error.message}`);
            return false;
        }
    }

    static async validateConfiguration(config) {
        console.log('\n🔍 Validating Configuration');
        console.log('-'.repeat(30));

        const checks = [
            { name: 'Endpoint', value: config.endpoint, required: true },
            { name: 'API Key', value: config.apiKey ? '[CONFIGURED]' : '[NOT SET]', required: false },
            { name: 'Deployment Name', value: config.deploymentName, required: true },
            { name: 'API Version', value: config.apiVersion, required: true }
        ];

        let allValid = true;

        for (const check of checks) {
            const status = check.value ? '✅' : (check.required ? '❌' : '⚠️');
            console.log(`   ${status} ${check.name}: ${check.value || '[NOT SET]'}`);
            
            if (check.required && !check.value) {
                allValid = false;
            }
        }

        return allValid;
    }
}

// Error handler
class ErrorHandler {
    static handle(error) {
        console.error('\n❌ Error occurred:', error.message);
        
        if (error.code) {
            console.error(`   Error Code: ${error.code}`);
        }

        if (error.statusCode) {
            console.error(`   HTTP Status: ${error.statusCode}`);
        }

        console.error(`   Stack: ${error.stack}`);
    }

    static isRetryable(error) {
        const retryableCodes = [500, 502, 503, 504, 429];
        return retryableCodes.includes(error.statusCode);
    }
}

// Main execution
async function main() {
    try {
        const demo = new AzureAIFoundrySetupDemo();
        
        // Validate configuration first
        const configValid = await ConnectionValidator.validateConfiguration(demo.config);
        if (!configValid) {
            throw new Error('Configuration validation failed');
        }

        // Validate endpoint
        const endpointValid = await ConnectionValidator.validateEndpoint(demo.config.endpoint);
        if (!endpointValid) {
            throw new Error('Endpoint validation failed');
        }

        // Run authentication demos
        await demo.run();
        
        console.log('\n🎉 Demo completed successfully!');
        console.log('\n💡 Next Steps:');
        console.log('   • Try the first-chat-completion sample');
        console.log('   • Explore error-handling patterns');
        console.log('   • Build your own AI application');

    } catch (error) {
        ErrorHandler.handle(error);
        process.exit(1);
    }
}

// Export for testing
module.exports = {
    AzureAIFoundryConfig,
    AuthenticationHelper,
    AzureAIFoundrySetupDemo,
    ConnectionValidator,
    ErrorHandler
};

// Run if called directly
if (require.main === module) {
    main();
} 