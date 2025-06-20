# Creating Your First AI Project

## Overview

In this lesson, you'll learn how to create your first AI project in Azure AI Foundry, understand project structure, configure basic settings, and build your first AI application.

## Learning Objectives

- Create and configure an AI project in Azure AI Foundry
- Understand project structure and organization
- Set up project resources and dependencies
- Build and deploy your first AI application
- Manage project settings and permissions

## Prerequisites

- Completed Azure AI Foundry setup (Lesson 02)
- Development environment configured (Lesson 03)
- Basic understanding of AI/ML concepts

---

## 1. Understanding AI Projects

### What is an AI Project?

An AI project in Azure AI Foundry is a logical container that:
- Organizes your AI assets and resources
- Provides collaboration and sharing capabilities
- Manages access control and permissions
- Tracks usage and costs
- Enables versioning and deployment

### Project Types

**Chat Applications:**
- Conversational AI assistants
- Customer service bots
- Question-answering systems

**Content Generation:**
- Text summarization
- Creative writing assistance
- Code generation

**Multi-Agent Systems:**
- Orchestrated AI workflows
- Agent-to-agent communication
- Complex reasoning tasks

---

## 2. Creating Your First Project

### Using Azure Portal

1. Navigate to Azure AI Foundry in the Azure Portal
2. Select "Projects" from the navigation menu
3. Click "Create New Project"
4. Configure project settings:
   - Name: "my-first-ai-project"
   - Description: "Learning Azure AI Foundry basics"
   - Project Type: "Chat Application"
   - Region: "East US 2"

### Using Python SDK

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Initialize client
credential = DefaultAzureCredential()
client = AIProjectClient(
    endpoint="https://your-ai-foundry.cognitiveservices.azure.com",
    credential=credential
)

# Create project
project = client.create_project(
    project_name="my-first-ai-project",
    description="Learning Azure AI Foundry basics",
    project_type="ChatApplication"
)

print(f"Project created: {project.project_id}")
```

---

## 3. Building Your First Chat Application

### Simple Chat Application

```python
#!/usr/bin/env python3
"""Simple chat application using Azure AI Foundry"""

import os
import asyncio
from azure.identity import DefaultAzureCredential
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage

class SimpleChatApp:
    def __init__(self, endpoint: str):
        self.credential = DefaultAzureCredential()
        self.chat_client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=self.credential
        )
        self.conversation_history = []
        
        # System message
        self.system_message = SystemMessage(
            content="You are a helpful AI assistant. Provide accurate, "
                   "helpful, and friendly responses to user questions."
        )
    
    async def send_message(self, user_input: str) -> str:
        """Send a message and get response."""
        
        user_message = UserMessage(content=user_input)
        
        # Build messages for API call
        messages = [self.system_message]
        messages.extend(self.conversation_history)
        messages.append(user_message)
        
        try:
            # Get completion
            response = await self.chat_client.complete(
                messages=messages,
                model="gpt-4",
                max_tokens=1000,
                temperature=0.7
            )
            
            # Extract assistant response
            assistant_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append(user_message)
            self.conversation_history.append(response.choices[0].message)
            
            # Keep only last 10 messages
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return assistant_response
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def start_chat(self):
        """Start interactive chat session."""
        print("🤖 Simple AI Chat Assistant")
        print("Type 'quit' to exit")
        print("-" * 40)
        
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("🤖 Assistant: ", end="")
            response = await self.send_message(user_input)
            print(response)

# Main execution
async def main():
    endpoint = os.getenv('AZURE_AI_FOUNDRY_ENDPOINT')
    
    if not endpoint:
        print("❌ Please set AZURE_AI_FOUNDRY_ENDPOINT environment variable")
        return
    
    app = SimpleChatApp(endpoint)
    await app.start_chat()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 4. Testing and Deployment

### Testing Your Application

```python
# test_chat_app.py
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from simple_chat import SimpleChatApp

@pytest.mark.asyncio
async def test_send_message():
    """Test sending a message."""
    app = SimpleChatApp("https://mock-endpoint.com")
    app.chat_client.complete = AsyncMock()
    
    # Mock response
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Hello! How can I help you?"
    
    app.chat_client.complete.return_value = mock_response
    
    # Test
    response = await app.send_message("Hello")
    assert response == "Hello! How can I help you?"
```

### Local Deployment

```bash
# Create deployment structure
mkdir deployment
cp simple_chat.py deployment/
cd deployment

# Create requirements.txt
echo "azure-ai-projects" > requirements.txt
echo "azure-ai-inference" >> requirements.txt
echo "azure-identity" >> requirements.txt

# Install dependencies
pip install -r requirements.txt

# Run application
export AZURE_AI_FOUNDRY_ENDPOINT="your-endpoint"
python simple_chat.py
```

---

## Summary

You've successfully created your first AI project and built a working chat application using Azure AI Foundry. The application demonstrates basic conversation management and AI integration.

## Next Steps

- Explore the Azure AI Foundry portal interface (Lesson 05)
- Learn about advanced features and customization (Lesson 06)
- Implement more complex AI workflows (Lesson 07)

---

*This lesson is part of the Azure AI Foundry Zero-to-Hero course.* 