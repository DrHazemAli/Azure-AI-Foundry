#!/usr/bin/env python3
"""
Azure AI Foundry - Setup and Authentication Demo

This sample demonstrates how to set up and authenticate with Azure AI Foundry
using different authentication methods and configuration patterns.

Features:
- Multiple authentication methods (API key, managed identity, service principal, default credential)
- Environment configuration management
- Connection validation and testing
- Comprehensive error handling
- Logging and monitoring

Author: Hazem Ali
Course: Azure AI Foundry Zero-to-Hero
Module: 02 - Getting Started
"""

import os
import sys
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from urllib.parse import urlparse

# Azure AI Foundry imports
from azure.identity import (
    DefaultAzureCredential,
    ClientSecretCredential,
    ManagedIdentityCredential
)
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    ChatCompletionsOptions,
    ChatMessage,
    SystemMessage,
    UserMessage
)
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import (
    AzureError,
    ClientAuthenticationError,
    ResourceNotFoundError,
    HttpResponseError
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class AzureAIFoundryConfig:
    """Configuration class for Azure AI Foundry settings."""
    
    # Required settings
    endpoint: str
    api_key: Optional[str] = None
    
    # Authentication settings
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    tenant_id: Optional[str] = None
    
    # Model settings
    deployment_name: str = "gpt-4"
    api_version: str = "2024-02-15-preview"
    max_tokens: int = 100
    temperature: float = 0.0
    
    @classmethod
    def from_environment(cls) -> 'AzureAIFoundryConfig':
        """Create configuration from environment variables."""
        return cls(
            endpoint=os.getenv('AZURE_AI_FOUNDRY_ENDPOINT', ''),
            api_key=os.getenv('AZURE_AI_FOUNDRY_API_KEY'),
            client_id=os.getenv('AZURE_CLIENT_ID'),
            client_secret=os.getenv('AZURE_CLIENT_SECRET'),
            tenant_id=os.getenv('AZURE_TENANT_ID'),
            deployment_name=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
        )
    
    def validate(self) -> None:
        """Validate configuration settings."""
        if not self.endpoint:
            raise ValueError("Azure AI Foundry endpoint is required")
        
        # Validate URL format
        try:
            parsed = urlparse(self.endpoint)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid endpoint URL format")
            if parsed.scheme != 'https':
                raise ValueError("Endpoint must use HTTPS")
        except Exception as e:
            raise ValueError(f"Invalid endpoint URL: {e}")
        
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("temperature must be between 0.0 and 2.0")
        
        logger.info("✅ Configuration validated successfully")


class AuthenticationHelper:
    """Helper class for different authentication methods."""
    
    @staticmethod
    def get_api_key_credential(api_key: str) -> AzureKeyCredential:
        """Get API key credential."""
        if not api_key:
            raise ValueError("API key is required")
        return AzureKeyCredential(api_key)
    
    @staticmethod
    def get_default_credential() -> DefaultAzureCredential:
        """Get default Azure credential (tries managed identity, CLI, etc.)."""
        return DefaultAzureCredential()
    
    @staticmethod
    def get_service_principal_credential(
        tenant_id: str, 
        client_id: str, 
        client_secret: str
    ) -> ClientSecretCredential:
        """Get service principal credential."""
        if not all([tenant_id, client_id, client_secret]):
            raise ValueError("Service principal credentials are incomplete")
        return ClientSecretCredential(tenant_id, client_id, client_secret)
    
    @staticmethod
    def get_managed_identity_credential(client_id: Optional[str] = None) -> ManagedIdentityCredential:
        """Get managed identity credential."""
        return ManagedIdentityCredential(client_id=client_id)


class AzureAIFoundrySetupDemo:
    """Main demo class for Azure AI Foundry setup and authentication."""
    
    def __init__(self):
        """Initialize the demo."""
        self.config = AzureAIFoundryConfig.from_environment()
        self.config.validate()
        
        print("🚀 Azure AI Foundry - Setup and Authentication Demo")
        print("=" * 60)
    
    async def run(self) -> None:
        """Run the authentication demonstrations."""
        try:
            print("\n🔐 Testing Authentication Methods")
            print("-" * 40)
            
            # Test different authentication methods
            await self._test_api_key_authentication()
            await self._test_default_credential_authentication()
            await self._test_service_principal_authentication()
            await self._test_managed_identity_authentication()
            
            print("\n✅ All authentication tests completed")
            
        except Exception as e:
            logger.error(f"Demo failed: {e}")
            raise
    
    async def _test_api_key_authentication(self) -> None:
        """Test API key authentication."""
        print("\n1️⃣ Testing API Key Authentication")
        
        if not self.config.api_key:
            print("   ⚠️  API Key not configured - skipping")
            return
        
        try:
            credential = AuthenticationHelper.get_api_key_credential(self.config.api_key)
            client = ChatCompletionsClient(
                endpoint=self.config.endpoint,
                credential=credential
            )
            
            success = await self._test_connection(client, "API Key")
            
            if success:
                print("   ✅ API Key authentication successful")
                logger.info("API Key authentication test passed")
        
        except Exception as e:
            print(f"   ❌ API Key authentication failed: {e}")
            logger.warning(f"API Key authentication test failed: {e}")
    
    async def _test_default_credential_authentication(self) -> None:
        """Test default Azure credential authentication."""
        print("\n2️⃣ Testing Default Azure Credential")
        
        try:
            credential = AuthenticationHelper.get_default_credential()
            client = ChatCompletionsClient(
                endpoint=self.config.endpoint,
                credential=credential
            )
            
            success = await self._test_connection(client, "Default Credential")
            
            if success:
                print("   ✅ Default Azure Credential authentication successful")
                logger.info("Default Azure Credential authentication test passed")
        
        except Exception as e:
            print(f"   ⚠️  Default Azure Credential failed: {e}")
            logger.info("Default Azure Credential authentication not available in current environment")
    
    async def _test_service_principal_authentication(self) -> None:
        """Test service principal authentication."""
        print("\n3️⃣ Testing Service Principal Authentication")
        
        if not all([self.config.client_id, self.config.client_secret, self.config.tenant_id]):
            print("   ⚠️  Service Principal credentials not configured - skipping")
            return
        
        try:
            credential = AuthenticationHelper.get_service_principal_credential(
                self.config.tenant_id,
                self.config.client_id,
                self.config.client_secret
            )
            client = ChatCompletionsClient(
                endpoint=self.config.endpoint,
                credential=credential
            )
            
            success = await self._test_connection(client, "Service Principal")
            
            if success:
                print("   ✅ Service Principal authentication successful")
                logger.info("Service Principal authentication test passed")
        
        except Exception as e:
            print(f"   ❌ Service Principal authentication failed: {e}")
            logger.warning(f"Service Principal authentication test failed: {e}")
    
    async def _test_managed_identity_authentication(self) -> None:
        """Test managed identity authentication."""
        print("\n4️⃣ Testing Managed Identity Authentication")
        
        try:
            credential = AuthenticationHelper.get_managed_identity_credential()
            client = ChatCompletionsClient(
                endpoint=self.config.endpoint,
                credential=credential
            )
            
            success = await self._test_connection(client, "Managed Identity")
            
            if success:
                print("   ✅ Managed Identity authentication successful")
                logger.info("Managed Identity authentication test passed")
        
        except Exception as e:
            print(f"   ⚠️  Managed Identity authentication not available: {e}")
            logger.info("Managed Identity authentication not available in current environment")
    
    async def _test_connection(self, client: ChatCompletionsClient, auth_method: str) -> bool:
        """Test connection with the provided client."""
        try:
            print(f"   🔄 Testing connection using {auth_method}...")
            
            # Create a simple test message
            messages = [
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content="Say 'Connection test successful' if you can read this.")
            ]
            
            options = ChatCompletionsOptions(
                model=self.config.deployment_name,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            response = await client.complete(options)
            
            if response and response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                print(f"   📝 Response: {content}")
                return True
            
            return False
        
        except Exception as e:
            print(f"   ❌ Connection test failed: {e}")
            logger.error(f"Connection test failed for {auth_method}: {e}")
            return False


class ConnectionValidator:
    """Utility class for validating connections and configuration."""
    
    @staticmethod
    def validate_endpoint(endpoint: str) -> bool:
        """Validate the endpoint URL."""
        try:
            parsed = urlparse(endpoint)
            print(f"🔍 Validating endpoint: {parsed.geturl()}")
            
            if not parsed.scheme:
                raise ValueError("No URL scheme provided")
            if not parsed.netloc:
                raise ValueError("No network location provided")
            if parsed.scheme != 'https':
                raise ValueError("Endpoint must use HTTPS")
            
            return True
        
        except Exception as e:
            print(f"❌ Invalid endpoint: {e}")
            return False
    
    @staticmethod
    def validate_configuration(config: AzureAIFoundryConfig) -> bool:
        """Validate the configuration settings."""
        print("\n🔍 Validating Configuration")
        print("-" * 30)
        
        checks = [
            ("Endpoint", config.endpoint, True),
            ("API Key", "[CONFIGURED]" if config.api_key else "[NOT SET]", False),
            ("Deployment Name", config.deployment_name, True),
            ("API Version", config.api_version, True),
        ]
        
        all_valid = True
        
        for name, value, required in checks:
            if value:
                status = "✅"
            elif required:
                status = "❌"
                all_valid = False
            else:
                status = "⚠️"
            
            print(f"   {status} {name}: {value or '[NOT SET]'}")
        
        return all_valid


class ErrorHandler:
    """Error handling utilities."""
    
    @staticmethod
    def handle_error(error: Exception) -> None:
        """Handle and log errors appropriately."""
        print(f"\n❌ Error occurred: {error}")
        
        if hasattr(error, 'status_code'):
            print(f"   HTTP Status: {error.status_code}")
        
        if hasattr(error, 'error_code'):
            print(f"   Error Code: {error.error_code}")
        
        logger.error(f"Error details: {error}", exc_info=True)
    
    @staticmethod
    def is_retryable_error(error: Exception) -> bool:
        """Check if an error is retryable."""
        retryable_status_codes = [500, 502, 503, 504, 429]
        
        if isinstance(error, HttpResponseError):
            return error.status_code in retryable_status_codes
        
        return isinstance(error, (ConnectionError, TimeoutError))


async def main():
    """Main function to run the demo."""
    try:
        demo = AzureAIFoundrySetupDemo()
        
        # Validate configuration first
        config_valid = ConnectionValidator.validate_configuration(demo.config)
        if not config_valid:
            raise ValueError("Configuration validation failed")
        
        # Validate endpoint
        endpoint_valid = ConnectionValidator.validate_endpoint(demo.config.endpoint)
        if not endpoint_valid:
            raise ValueError("Endpoint validation failed")
        
        # Run authentication demos
        await demo.run()
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Next Steps:")
        print("   • Try the first-chat-completion sample")
        print("   • Explore error-handling patterns")
        print("   • Build your own AI application")
        
    except Exception as e:
        ErrorHandler.handle_error(e)
        sys.exit(1)


if __name__ == "__main__":
    # Load environment variables from .env file if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        logger.warning("python-dotenv not installed. Environment variables must be set manually.")
    
    # Run the demo
    import asyncio
    asyncio.run(main()) 