#!/usr/bin/env python3
"""
Azure AI Foundry - First Chat Completion Sample

This sample demonstrates how to build a comprehensive chat completion application
using Azure AI Foundry with Python. It includes error handling, logging,
configuration management, and best practices for production use.

Features:
- Multiple authentication methods
- Comprehensive error handling and retry logic
- Conversation context management
- Streaming and non-streaming responses
- Cost tracking and optimization
- Security best practices

Author: Hazem Ali
Course: Azure AI Foundry Zero-to-Hero
Module: 02 - Getting Started
"""

import os
import sys
import json
import time
import logging
import asyncio
from typing import List, Dict, Optional, AsyncGenerator
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import uuid

# Azure AI Foundry imports
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    ChatCompletions,
    ChatCompletionsOptions,
    ChatMessage,
    SystemMessage,
    UserMessage,
    AssistantMessage
)
from azure.core.exceptions import (
    AzureError,
    ClientAuthenticationError,
    ResourceNotFoundError,
    HttpResponseError
)

# Configuration and logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('azure_ai_foundry.log'),
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
    
    # Authentication settings (for managed identity)
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    tenant_id: Optional[str] = None
    
    # Model settings
    deployment_name: str = "gpt-4"
    api_version: str = "2024-02-15-preview"
    max_tokens: int = 1000
    temperature: float = 0.7
    
    # Performance settings
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # Feature flags
    enable_streaming: bool = True
    enable_cost_tracking: bool = True
    enable_conversation_history: bool = True
    
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
            api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
            max_tokens=int(os.getenv('MAX_TOKENS', '1000')),
            temperature=float(os.getenv('TEMPERATURE', '0.7')),
            timeout=int(os.getenv('TIMEOUT', '30')),
            max_retries=int(os.getenv('MAX_RETRIES', '3')),
            enable_streaming=os.getenv('ENABLE_STREAMING', 'true').lower() == 'true',
            enable_cost_tracking=os.getenv('ENABLE_COST_TRACKING', 'true').lower() == 'true',
            enable_conversation_history=os.getenv('ENABLE_CONVERSATION_HISTORY', 'true').lower() == 'true'
        )
    
    def validate(self) -> None:
        """Validate configuration settings."""
        if not self.endpoint:
            raise ValueError("Azure AI Foundry endpoint is required")
        
        if not self.endpoint.startswith(('http://', 'https://')):
            raise ValueError("Endpoint must be a valid URL")
        
        if not self.api_key and not (self.client_id and self.client_secret and self.tenant_id):
            raise ValueError("Either API key or service principal credentials are required")
        
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("temperature must be between 0.0 and 2.0")


@dataclass
class ConversationMessage:
    """Represents a message in the conversation."""
    
    role: str  # 'system', 'user', 'assistant'
    content: str
    timestamp: datetime
    tokens_used: Optional[int] = None
    cost_estimate: Optional[float] = None
    
    def to_chat_message(self) -> ChatMessage:
        """Convert to Azure AI chat message format."""
        if self.role == 'system':
            return SystemMessage(content=self.content)
        elif self.role == 'user':
            return UserMessage(content=self.content)
        elif self.role == 'assistant':
            return AssistantMessage(content=self.content)
        else:
            raise ValueError(f"Unknown role: {self.role}")


@dataclass
class ConversationStats:
    """Statistics for conversation tracking."""
    
    total_messages: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    average_response_time: float = 0.0
    error_count: int = 0
    start_time: datetime = None
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now(timezone.utc)


class TokenCostCalculator:
    """Utility class for calculating token costs."""
    
    # Pricing per 1K tokens (as of 2024)
    PRICING = {
        'gpt-4': {'input': 0.03, 'output': 0.06},
        'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
        'gpt-3.5-turbo': {'input': 0.0015, 'output': 0.002}
    }
    
    @classmethod
    def calculate_cost(cls, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost based on token usage."""
        if model not in cls.PRICING:
            # Default to GPT-4 pricing if model not found
            model = 'gpt-4'
        
        pricing = cls.PRICING[model]
        input_cost = (input_tokens / 1000) * pricing['input']
        output_cost = (output_tokens / 1000) * pricing['output']
        
        return input_cost + output_cost


class AzureAIFoundryClient:
    """
    Comprehensive Azure AI Foundry client with advanced features.
    
    This client provides:
    - Multiple authentication methods
    - Robust error handling and retry logic
    - Conversation management
    - Cost tracking
    - Performance monitoring
    """
    
    def __init__(self, config: AzureAIFoundryConfig):
        """Initialize the Azure AI Foundry client."""
        self.config = config
        self.config.validate()
        
        self.conversation_history: List[ConversationMessage] = []
        self.stats = ConversationStats()
        self.session_id = str(uuid.uuid4())
        
        # Initialize clients
        self._project_client = None
        self._chat_client = None
        
        logger.info(f"Initialized Azure AI Foundry client (Session: {self.session_id})")
    
    def _get_credential(self):
        """Get appropriate Azure credential based on configuration."""
        if self.config.api_key:
            # Use API key authentication
            return None  # Will use API key directly
        elif self.config.client_id and self.config.client_secret and self.config.tenant_id:
            # Use service principal authentication
            return ClientSecretCredential(
                tenant_id=self.config.tenant_id,
                client_id=self.config.client_id,
                client_secret=self.config.client_secret
            )
        else:
            # Use default credential chain (managed identity, Azure CLI, etc.)
            return DefaultAzureCredential()
    
    def _initialize_clients(self):
        """Initialize Azure AI clients with proper authentication."""
        try:
            credential = self._get_credential()
            
            if credential:
                # Use credential-based authentication
                self._project_client = AIProjectClient(
                    endpoint=self.config.endpoint,
                    credential=credential
                )
                
                self._chat_client = ChatCompletionsClient(
                    endpoint=self.config.endpoint,
                    credential=credential
                )
            else:
                # Use API key authentication
                from azure.core.credentials import AzureKeyCredential
                key_credential = AzureKeyCredential(self.config.api_key)
                
                self._chat_client = ChatCompletionsClient(
                    endpoint=self.config.endpoint,
                    credential=key_credential
                )
            
            logger.info("Successfully initialized Azure AI clients")
            
        except Exception as e:
            logger.error(f"Failed to initialize Azure AI clients: {e}")
            raise
    
    async def test_connection(self) -> bool:
        """Test connection to Azure AI Foundry."""
        try:
            if not self._chat_client:
                self._initialize_clients()
            
            # Test with a simple completion
            test_messages = [
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content="Say 'Connection test successful'")
            ]
            
            response = await self._chat_client.complete(
                messages=test_messages,
                model=self.config.deployment_name,
                max_tokens=10,
                temperature=0.0
            )
            
            if response and response.choices:
                logger.info("Connection test successful")
                return True
            else:
                logger.error("Connection test failed: No response received")
                return False
                
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def add_system_message(self, content: str) -> None:
        """Add a system message to the conversation."""
        message = ConversationMessage(
            role='system',
            content=content,
            timestamp=datetime.now(timezone.utc)
        )
        self.conversation_history.append(message)
        logger.debug(f"Added system message: {content[:50]}...")
    
    def add_user_message(self, content: str) -> None:
        """Add a user message to the conversation."""
        message = ConversationMessage(
            role='user',
            content=content,
            timestamp=datetime.now(timezone.utc)
        )
        self.conversation_history.append(message)
        self.stats.total_messages += 1
        logger.debug(f"Added user message: {content[:50]}...")
    
    async def get_completion(
        self,
        user_message: str,
        system_message: Optional[str] = None,
        use_conversation_history: bool = None
    ) -> str:
        """
        Get a completion from Azure AI Foundry.
        
        Args:
            user_message: The user's message
            system_message: Optional system message
            use_conversation_history: Whether to include conversation history
            
        Returns:
            The assistant's response
        """
        start_time = time.time()
        
        try:
            if not self._chat_client:
                self._initialize_clients()
            
            # Determine whether to use conversation history
            if use_conversation_history is None:
                use_conversation_history = self.config.enable_conversation_history
            
            # Build messages list
            messages = []
            
            if use_conversation_history and self.conversation_history:
                # Include conversation history
                for msg in self.conversation_history:
                    messages.append(msg.to_chat_message())
            
            # Add system message if provided
            if system_message:
                messages.append(SystemMessage(content=system_message))
            
            # Add user message
            messages.append(UserMessage(content=user_message))
            
            # Add user message to history
            self.add_user_message(user_message)
            
            # Make the API call with retry logic
            response = await self._make_completion_request(messages)
            
            # Extract response content
            if response and response.choices and len(response.choices) > 0:
                assistant_message = response.choices[0].message.content
                
                # Calculate costs if enabled
                tokens_used = None
                cost_estimate = None
                
                if self.config.enable_cost_tracking and hasattr(response, 'usage'):
                    usage = response.usage
                    tokens_used = usage.total_tokens
                    cost_estimate = TokenCostCalculator.calculate_cost(
                        self.config.deployment_name,
                        usage.prompt_tokens,
                        usage.completion_tokens
                    )
                    
                    # Update stats
                    self.stats.total_tokens += tokens_used
                    self.stats.total_cost += cost_estimate
                
                # Add assistant message to history
                assistant_msg = ConversationMessage(
                    role='assistant',
                    content=assistant_message,
                    timestamp=datetime.now(timezone.utc),
                    tokens_used=tokens_used,
                    cost_estimate=cost_estimate
                )
                self.conversation_history.append(assistant_msg)
                
                # Update response time stats
                response_time = time.time() - start_time
                self._update_response_time_stats(response_time)
                
                logger.info(f"Completion successful (took {response_time:.2f}s)")
                if cost_estimate:
                    logger.info(f"Cost estimate: ${cost_estimate:.6f}")
                
                return assistant_message
            else:
                raise ValueError("No response received from Azure AI Foundry")
                
        except Exception as e:
            self.stats.error_count += 1
            logger.error(f"Completion failed: {e}")
            raise
    
    async def get_completion_stream(
        self,
        user_message: str,
        system_message: Optional[str] = None,
        use_conversation_history: bool = None
    ) -> AsyncGenerator[str, None]:
        """
        Get a streaming completion from Azure AI Foundry.
        
        Args:
            user_message: The user's message
            system_message: Optional system message
            use_conversation_history: Whether to include conversation history
            
        Yields:
            Chunks of the assistant's response
        """
        if not self.config.enable_streaming:
            # Fall back to non-streaming
            response = await self.get_completion(
                user_message, system_message, use_conversation_history
            )
            yield response
            return
        
        start_time = time.time()
        full_response = ""
        
        try:
            if not self._chat_client:
                self._initialize_clients()
            
            # Build messages (similar to get_completion)
            messages = []
            
            if use_conversation_history is None:
                use_conversation_history = self.config.enable_conversation_history
            
            if use_conversation_history and self.conversation_history:
                for msg in self.conversation_history:
                    messages.append(msg.to_chat_message())
            
            if system_message:
                messages.append(SystemMessage(content=system_message))
            
            messages.append(UserMessage(content=user_message))
            self.add_user_message(user_message)
            
            # Make streaming request
            async for chunk in self._make_streaming_request(messages):
                if chunk:
                    full_response += chunk
                    yield chunk
            
            # Add complete response to history
            assistant_msg = ConversationMessage(
                role='assistant',
                content=full_response,
                timestamp=datetime.now(timezone.utc)
            )
            self.conversation_history.append(assistant_msg)
            
            # Update stats
            response_time = time.time() - start_time
            self._update_response_time_stats(response_time)
            
            logger.info(f"Streaming completion successful (took {response_time:.2f}s)")
            
        except Exception as e:
            self.stats.error_count += 1
            logger.error(f"Streaming completion failed: {e}")
            raise
    
    async def _make_completion_request(self, messages: List[ChatMessage]) -> ChatCompletions:
        """Make completion request with retry logic."""
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                options = ChatCompletionsOptions(
                    model=self.config.deployment_name,
                    messages=messages,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature
                )
                
                response = await self._chat_client.complete(options)
                return response
                
            except (HttpResponseError, AzureError) as e:
                last_exception = e
                
                if attempt < self.config.max_retries:
                    delay = self.config.retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Request failed (attempt {attempt + 1}), retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Request failed after {self.config.max_retries + 1} attempts")
                    break
            
            except Exception as e:
                # Non-retryable error
                logger.error(f"Non-retryable error: {e}")
                raise
        
        raise last_exception
    
    async def _make_streaming_request(self, messages: List[ChatMessage]) -> AsyncGenerator[str, None]:
        """Make streaming completion request with retry logic."""
        # Note: Streaming implementation would depend on the specific Azure AI SDK version
        # This is a placeholder implementation
        
        # For now, fall back to non-streaming and simulate streaming
        response = await self._make_completion_request(messages)
        
        if response and response.choices:
            content = response.choices[0].message.content
            # Simulate streaming by yielding chunks
            chunk_size = 10
            for i in range(0, len(content), chunk_size):
                chunk = content[i:i + chunk_size]
                yield chunk
                await asyncio.sleep(0.05)  # Small delay to simulate streaming
    
    def _update_response_time_stats(self, response_time: float) -> None:
        """Update response time statistics."""
        total_responses = self.stats.total_messages
        if total_responses == 0:
            self.stats.average_response_time = response_time
        else:
            # Calculate running average
            self.stats.average_response_time = (
                (self.stats.average_response_time * (total_responses - 1) + response_time) 
                / total_responses
            )
    
    def get_conversation_summary(self) -> Dict:
        """Get a summary of the current conversation."""
        return {
            'session_id': self.session_id,
            'message_count': len(self.conversation_history),
            'stats': asdict(self.stats),
            'conversation_duration': (
                datetime.now(timezone.utc) - self.stats.start_time
            ).total_seconds() if self.stats.start_time else 0
        }
    
    def clear_conversation(self) -> None:
        """Clear the conversation history."""
        self.conversation_history.clear()
        logger.info("Conversation history cleared")
    
    def export_conversation(self, filename: Optional[str] = None) -> str:
        """Export conversation to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{self.session_id}_{timestamp}.json"
        
        conversation_data = {
            'session_id': self.session_id,
            'export_timestamp': datetime.now(timezone.utc).isoformat(),
            'summary': self.get_conversation_summary(),
            'messages': [
                {
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat(),
                    'tokens_used': msg.tokens_used,
                    'cost_estimate': msg.cost_estimate
                }
                for msg in self.conversation_history
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Conversation exported to {filename}")
        return filename


class InteractiveChatApp:
    """Interactive chat application demonstrating Azure AI Foundry capabilities."""
    
    def __init__(self, config: AzureAIFoundryConfig):
        """Initialize the chat application."""
        self.config = config
        self.client = AzureAIFoundryClient(config)
        self.running = False
    
    async def start(self) -> None:
        """Start the interactive chat application."""
        print("🚀 Azure AI Foundry Chat Application")
        print("=" * 50)
        print(f"Model: {self.config.deployment_name}")
        print(f"Session ID: {self.client.session_id}")
        print("=" * 50)
        
        # Test connection
        print("Testing connection to Azure AI Foundry...")
        if not await self.client.test_connection():
            print("❌ Connection test failed. Please check your configuration.")
            return
        
        print("✅ Connection successful!")
        print("\nType 'help' for commands or 'quit' to exit.\n")
        
        # Add default system message
        self.client.add_system_message(
            "You are a helpful AI assistant powered by Azure AI Foundry. "
            "You provide accurate, helpful, and friendly responses to user queries."
        )
        
        self.running = True
        
        try:
            while self.running:
                await self._handle_user_input()
        except KeyboardInterrupt:
            print("\n\n👋 Chat session ended by user.")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            await self._cleanup()
    
    async def _handle_user_input(self) -> None:
        """Handle user input and commands."""
        try:
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                return
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                self.running = False
                return
            elif user_input.lower() == 'help':
                self._show_help()
                return
            elif user_input.lower() == 'stats':
                self._show_stats()
                return
            elif user_input.lower() == 'clear':
                self.client.clear_conversation()
                print("🧹 Conversation history cleared.")
                return
            elif user_input.lower() == 'export':
                filename = self.client.export_conversation()
                print(f"📁 Conversation exported to {filename}")
                return
            
            # Get AI response
            print("\n🤖 Assistant: ", end="", flush=True)
            
            if self.config.enable_streaming:
                # Streaming response
                async for chunk in self.client.get_completion_stream(user_input):
                    print(chunk, end="", flush=True)
                print()  # New line after streaming
            else:
                # Non-streaming response
                response = await self.client.get_completion(user_input)
                print(response)
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            logger.error(f"Error handling user input: {e}")
    
    def _show_help(self) -> None:
        """Show help information."""
        help_text = """
🆘 Available Commands:
• help     - Show this help message
• stats    - Show conversation statistics
• clear    - Clear conversation history
• export   - Export conversation to JSON file
• quit/exit/q - Exit the application

💡 Tips:
• The assistant maintains conversation context
• Streaming is enabled for real-time responses
• All conversations are logged for debugging
• Cost tracking is enabled (if configured)
        """
        print(help_text)
    
    def _show_stats(self) -> None:
        """Show conversation statistics."""
        summary = self.client.get_conversation_summary()
        stats = summary['stats']
        
        print("\n📊 Conversation Statistics:")
        print(f"• Messages: {summary['message_count']}")
        print(f"• Total tokens: {stats['total_tokens']}")
        print(f"• Total cost: ${stats['total_cost']:.6f}")
        print(f"• Average response time: {stats['average_response_time']:.2f}s")
        print(f"• Errors: {stats['error_count']}")
        print(f"• Duration: {summary['conversation_duration']:.0f}s")
    
    async def _cleanup(self) -> None:
        """Cleanup resources."""
        print("\n🧹 Cleaning up...")
        
        # Show final stats
        self._show_stats()
        
        # Export conversation if there are messages
        if len(self.client.conversation_history) > 0:
            try:
                filename = self.client.export_conversation()
                print(f"📁 Final conversation exported to {filename}")
            except Exception as e:
                logger.error(f"Failed to export conversation: {e}")
        
        print("✅ Cleanup complete. Goodbye!")


async def main():
    """Main function to run the chat application."""
    try:
        # Load configuration from environment
        config = AzureAIFoundryConfig.from_environment()
        
        # Create and start the chat application
        app = InteractiveChatApp(config)
        await app.start()
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n💡 Please check your environment variables:")
        print("• AZURE_AI_FOUNDRY_ENDPOINT")
        print("• AZURE_AI_FOUNDRY_API_KEY (or service principal credentials)")
        print("• AZURE_OPENAI_DEPLOYMENT_NAME")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Load environment variables from .env file if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        logger.warning("python-dotenv not installed. Environment variables must be set manually.")
    
    # Run the application
    asyncio.run(main()) 