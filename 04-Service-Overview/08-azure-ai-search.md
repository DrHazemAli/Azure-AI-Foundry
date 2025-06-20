# 04-8: Azure AI Search

## Overview

Azure AI Search is an enterprise-ready information retrieval system that provides sophisticated search capabilities for heterogeneous content. It serves as the recommended retrieval system for building Retrieval-Augmented Generation (RAG) applications and modern search experiences on Azure.

## Learning Objectives

By the end of this lesson, you will be able to:

- Understand Azure AI Search architecture and capabilities
- Implement vector search and hybrid search scenarios
- Build RAG applications with Azure AI Search
- Configure indexing and data ingestion pipelines
- Optimize search performance and relevance

## What is Azure AI Search?

Azure AI Search provides:

- **Enterprise Search Engine**: Vector, full-text, and hybrid search over indexed content
- **RAG Integration**: Native support for retrieval-augmented generation workflows
- **AI Enrichment**: Built-in content transformation and extraction capabilities
- **Scalable Architecture**: Enterprise-grade performance and security
- **Azure Integration**: Seamless connection with Azure AI services

### Key Capabilities

#### Search Technologies
- **Vector Search**: Semantic similarity search using embeddings
- **Full-Text Search**: Traditional keyword-based search with BM25 ranking
- **Hybrid Search**: Combined vector and text search with RRF (Reciprocal Rank Fusion)
- **Faceted Search**: Categorized search with dynamic filtering

#### AI Integration
- **Integrated Vectorization**: Built-in embedding generation during indexing
- **Content Enrichment**: OCR, language detection, key phrase extraction
- **Semantic Ranking**: AI-powered result reranking
- **Knowledge Mining**: Extract insights from unstructured content

## Search Architecture

### Core Components

#### Search Index
The central repository for searchable content:

```json
{
  "name": "product-index",
  "fields": [
    {
      "name": "id",
      "type": "Edm.String",
      "key": true,
      "searchable": false
    },
    {
      "name": "title",
      "type": "Edm.String",
      "searchable": true,
      "analyzer": "en.microsoft"
    },
    {
      "name": "content",
      "type": "Edm.String",
      "searchable": true
    },
    {
      "name": "contentVector",
      "type": "Collection(Edm.Single)",
      "vectorSearchDimensions": 1536,
      "vectorSearchProfile": "default-profile"
    }
  ]
}
```

#### Indexers
Automated data ingestion from various sources:

**Supported Data Sources:**
- Azure Blob Storage
- Azure SQL Database
- Azure Cosmos DB
- Azure Table Storage
- OneLake files
- SharePoint Online

#### Skillsets
AI enrichment pipelines for content transformation:

```json
{
  "name": "content-skillset",
  "skills": [
    {
      "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
      "textSplitMode": "pages",
      "maximumPageLength": 4000
    },
    {
      "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
      "resourceUri": "https://your-openai.openai.azure.com",
      "deploymentId": "text-embedding-ada-002"
    }
  ]
}
```

## Vector Search

### Overview
Vector search enables semantic similarity matching using high-dimensional embeddings.

### Vector Algorithms

#### HNSW (Hierarchical Navigable Small World)
- **Use Case**: High-throughput approximate nearest neighbor search
- **Performance**: Fast query response with good recall
- **Configuration**: Configurable accuracy vs. speed trade-offs

```json
{
  "vectorSearch": {
    "algorithms": [
      {
        "name": "hnsw-algorithm",
        "kind": "hnsw",
        "hnswParameters": {
          "m": 4,
          "efConstruction": 400,
          "efSearch": 500,
          "metric": "cosine"
        }
      }
    ]
  }
}
```

#### Exhaustive KNN
- **Use Case**: Maximum accuracy requirements
- **Performance**: Slower but exact results
- **Configuration**: Simple exhaustive search

### Vector Queries

#### Single Vector Query
```python
search_client = SearchClient(endpoint, index_name, credential)

# Generate query vector
query_vector = generate_embedding("find products about AI")

# Vector search
results = search_client.search(
    search_text=None,
    vector_queries=[VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=10,
        fields="contentVector"
    )]
)
```

#### Multi-Vector Search
```python
# Search with multiple vector fields
results = search_client.search(
    search_text=None,
    vector_queries=[
        VectorizedQuery(
            vector=text_vector,
            k_nearest_neighbors=10,
            fields="textVector",
            weight=0.7
        ),
        VectorizedQuery(
            vector=image_vector,
            k_nearest_neighbors=10,
            fields="imageVector",
            weight=0.3
        )
    ]
)
```

## Hybrid Search

### Overview
Hybrid search combines vector search with traditional text search for optimal relevance.

### Implementation
```python
# Hybrid search combining text and vector
results = search_client.search(
    search_text="artificial intelligence products",
    vector_queries=[VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=50,
        fields="contentVector"
    )],
    select=["title", "content", "price"],
    top=10
)
```

### Reciprocal Rank Fusion (RRF)
Azure AI Search automatically merges vector and text search results using RRF:

- Combines rankings from different search algorithms
- Produces unified relevance scores
- Configurable fusion parameters

### Query Optimization
```python
# Advanced hybrid search with filters
results = search_client.search(
    search_text="machine learning",
    vector_queries=[VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=50,
        fields="contentVector"
    )],
    filter="category eq 'technology' and price le 1000",
    facets=["brand", "category"],
    scoring_profile="popularity-boost"
)
```

## RAG Implementation

### Basic RAG Pattern

#### 1. Document Indexing
```python
# Index documents with embeddings
documents = [
    {
        "id": "doc1",
        "title": "AI Introduction",
        "content": "Artificial intelligence is...",
        "contentVector": generate_embedding("Artificial intelligence is...")
    }
]

search_client.upload_documents(documents)
```

#### 2. Retrieval Phase
```python
def retrieve_context(query: str, top_k: int = 5):
    query_vector = generate_embedding(query)
    
    results = search_client.search(
        search_text=query,
        vector_queries=[VectorizedQuery(
            vector=query_vector,
            k_nearest_neighbors=top_k,
            fields="contentVector"
        )],
        select=["content", "title"],
        top=top_k
    )
    
    return [result["content"] for result in results]
```

#### 3. Generation Phase
```python
def generate_answer(query: str):
    # Retrieve relevant context
    context = retrieve_context(query)
    
    # Prepare prompt with context
    prompt = f"""
    Context: {' '.join(context)}
    
    Question: {query}
    
    Answer based on the context provided:
    """
    
    # Generate response using Azure OpenAI
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
```

### Advanced RAG Patterns

#### Agentic Retrieval
```python
# Create knowledge agent for complex queries
knowledge_agent = search_client.create_knowledge_agent(
    name="document-assistant",
    instructions="Help users find information in the document collection",
    index_connection=index_connection
)

# Query with complex reasoning
response = knowledge_agent.chat(
    "Compare the advantages and disadvantages of different ML algorithms mentioned in the documents"
)
```

#### Query Rewriting
```python
# Enhance queries for better retrieval
enhanced_results = search_client.search(
    search_text=original_query,
    query_rewrite=True,  # Enable semantic query enhancement
    vector_queries=[VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=20,
        fields="contentVector"
    )]
)
```

## Integrated Vectorization

### Overview
Built-in pipeline for automatic content chunking and embedding generation.

### Configuration
```json
{
  "skillset": {
    "name": "integrated-vectorization",
    "skills": [
      {
        "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
        "textSplitMode": "pages",
        "maximumPageLength": 2000,
        "pageOverlapLength": 500
      },
      {
        "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
        "resourceUri": "https://your-openai.openai.azure.com",
        "deploymentId": "text-embedding-3-large",
        "inputs": [
          {
            "name": "text",
            "source": "/document/pages/*"
          }
        ],
        "outputs": [
          {
            "name": "embedding",
            "targetName": "vector"
          }
        ]
      }
    ]
  }
}
```

### Vectorizers
Query-time embedding generation:

```json
{
  "vectorizers": [
    {
      "name": "openai-vectorizer",
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": "https://your-openai.openai.azure.com",
        "deploymentId": "text-embedding-3-large"
      }
    }
  ]
}
```

## Performance Optimization

### Vector Compression

#### Binary Quantization
Reduce vector index size by up to 32x:

```json
{
  "compressions": [
    {
      "name": "binary-compression",
      "kind": "binaryQuantization",
      "rerankWithOriginalVectors": true,
      "defaultOversampling": 4.0
    }
  ]
}
```

#### Scalar Quantization
Balance between compression and accuracy:

```json
{
  "compressions": [
    {
      "name": "scalar-compression",
      "kind": "scalarQuantization",
      "quantizedDataType": "int8",
      "rerankWithOriginalVectors": true
    }
  ]
}
```

### Search Optimization

#### Caching Strategies
- **Query Caching**: Cache frequent search results
- **Vector Caching**: Cache computed embeddings
- **Index Warming**: Pre-load frequently accessed data

#### Scaling Techniques
- **Partition Strategy**: Distribute index across partitions
- **Replica Configuration**: Add replicas for query performance
- **Resource Allocation**: Optimize compute and storage resources

### Monitoring and Analytics

#### Built-in Metrics
- Query latency and throughput
- Index size and growth
- Search relevance metrics
- Resource utilization

#### Custom Analytics
```python
# Track search performance
search_analytics = {
    "query": query,
    "results_count": len(results),
    "search_duration": duration,
    "relevance_score": calculate_relevance(results, query)
}

# Log for analysis
analytics_client.track_search(search_analytics)
```

## Security and Governance

### Access Control

#### Role-Based Access Control (RBAC)
```python
# Assign search roles
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=index_name,
    credential=credential
)
```

#### API Key Authentication
```python
# Use API keys for service access
from azure.core.credentials import AzureKeyCredential

credential = AzureKeyCredential(api_key)
search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=index_name,
    credential=credential
)
```

### Network Security

#### Private Endpoints
- Secure network connectivity
- VNet integration
- Private link configuration

#### IP Filtering
- Restrict access by IP ranges
- Firewall configuration
- Network security groups

### Data Protection

#### Encryption
- **At Rest**: Automatic encryption of all stored data
- **In Transit**: TLS encryption for all communications
- **Customer-Managed Keys**: Advanced encryption options

#### Compliance
- SOC 2 Type II compliance
- GDPR compliance features
- HIPAA-eligible configurations

## Best Practices

### Index Design

1. **Field Strategy**
   - Include only necessary fields
   - Optimize field types and attributes
   - Use appropriate analyzers

2. **Vector Configuration**
   - Choose optimal embedding dimensions
   - Select appropriate algorithms
   - Configure compression when needed

3. **Schema Evolution**
   - Plan for schema changes
   - Version control index definitions
   - Implement migration strategies

### Query Optimization

1. **Query Patterns**
   - Use appropriate search types
   - Optimize filter expressions
   - Implement query caching

2. **Performance Tuning**
   - Monitor query performance
   - Optimize vector parameters
   - Use scoring profiles effectively

3. **Relevance Improvement**
   - Implement semantic ranking
   - Use custom scoring profiles
   - Fine-tune result presentation

### Operational Excellence

1. **Monitoring**
   - Set up comprehensive monitoring
   - Define performance baselines
   - Implement alerting

2. **Scaling**
   - Plan capacity requirements
   - Monitor resource utilization
   - Implement auto-scaling

3. **Maintenance**
   - Regular index optimization
   - Update management
   - Backup and recovery planning

## Summary

Azure AI Search provides enterprise-grade search and retrieval capabilities essential for modern AI applications. Key features include:

- **Advanced Search**: Vector, hybrid, and traditional search capabilities
- **RAG Integration**: Built-in support for retrieval-augmented generation
- **AI Enrichment**: Intelligent content processing and extraction
- **Enterprise Security**: Comprehensive security and compliance features
- **Performance Optimization**: Advanced techniques for scale and speed

The service enables organizations to build sophisticated search experiences and RAG applications that can scale to enterprise requirements.

## Next Steps

Continue to [Azure AI Content Understanding](./09-azure-ai-content-understanding.md) to learn about multimodal content processing capabilities.

---

**Additional Resources:**
- [Azure AI Search Documentation](https://learn.microsoft.com/en-us/azure/search/)
- [Vector Search Guide](https://learn.microsoft.com/en-us/azure/search/vector-search-overview)
- [RAG Implementation Patterns](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview) 