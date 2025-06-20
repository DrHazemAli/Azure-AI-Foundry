# 04-3: Azure AI Language Services

## Overview

Azure AI Language Services is a comprehensive suite of natural language processing (NLP) capabilities that enables you to build applications with industry-leading language understanding.

## Learning Objectives

- Understand Azure AI Language Services capabilities
- Implement text analytics and sentiment analysis  
- Use entity recognition and key phrase extraction
- Build custom text classification models
- Integrate language services with Azure AI Foundry

## What is Azure AI Language Services?

Azure AI Language Services provides:

- **Pre-built Language Models**: Ready-to-use models for common NLP tasks
- **Custom Model Training**: Build domain-specific language models
- **Multi-language Support**: Process text in over 100 languages
- **Real-time Processing**: Low-latency text analysis capabilities
- **Enterprise Security**: Built-in data protection and compliance

## Key Components

1. **Text Analytics**
   - Sentiment analysis
   - Opinion mining
   - Key phrase extraction
   - Language detection

2. **Entity Recognition**
   - Named Entity Recognition (NER)
   - Personally Identifiable Information (PII) detection
   - Linked entity recognition

3. **Custom Models**
   - Custom text classification
   - Custom named entity recognition
   - Conversational language understanding

## Getting Started

### Basic Setup

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Initialize the client
text_analytics_client = TextAnalyticsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Analyze sentiment
documents = ["I love using Azure AI services!"]
response = text_analytics_client.analyze_sentiment(documents=documents)

for doc in response:
    print(f"Sentiment: {doc.sentiment}")
```

## Integration with Azure AI Foundry

```python
from azure.ai.projects import AIProjectClient

# Initialize project client
project_client = AIProjectClient(
    endpoint="your_project_endpoint",
    credential=DefaultAzureCredential()
)

# Get language service connection
connection = project_client.connections.get_default("AzureAILanguage")
```

## Common Use Cases

### Customer Support Enhancement
- Analyze support ticket sentiment
- Extract key phrases for routing
- Identify urgency levels
- Automate response prioritization

### Content Moderation
- Detect inappropriate content
- Identify PII in user submissions
- Classify content types
- Implement automated moderation workflows

## Best Practices

1. **Performance Optimization**
   - Use batch processing for multiple documents
   - Implement caching for frequently analyzed content
   - Monitor API quotas and usage

2. **Security and Privacy**
   - Handle PII detection appropriately
   - Implement data retention policies
   - Use managed identities when possible

## Conclusion

Azure AI Language Services provides powerful NLP capabilities that integrate seamlessly with Azure AI Foundry, enabling sophisticated language-aware applications.

---

*This lesson is part of the Azure AI Foundry Zero-to-Hero Guide.* 