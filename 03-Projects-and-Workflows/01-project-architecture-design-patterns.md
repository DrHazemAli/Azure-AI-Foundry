# Lesson 1: Project Architecture and Design Patterns

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand different architectural patterns for Azure AI Foundry projects
- Choose between microservices and monolithic architectures based on project requirements
- Design scalable and maintainable project structures
- Implement proven design patterns for AI applications
- Plan for future growth and scalability from project inception

## Overview

Project architecture is the foundation of any successful AI application. In this lesson, we'll explore different architectural approaches, design patterns, and best practices specifically tailored for Azure AI Foundry projects. We'll cover everything from simple single-service applications to complex multi-agent systems.

---

## 1. Architectural Patterns Overview

### Monolithic Architecture

**Definition**: A single, self-contained application where all components are interconnected and interdependent.

#### When to Use Monolithic Architecture
- **Small to medium teams** (2-8 developers)
- **Simple applications** with limited scope
- **Rapid prototyping** and MVP development
- **Limited deployment complexity** requirements
- **Single domain** business logic

#### Advantages
```
✅ Simple to develop, test, and deploy initially
✅ Easy debugging and monitoring
✅ No network latency between components
✅ Consistent data management
✅ Simpler security model
```

#### Disadvantages
```
❌ Difficult to scale individual components
❌ Technology stack lock-in
❌ Large codebase becomes hard to maintain
❌ Single point of failure
❌ Deployment of entire application for small changes
```

### Microservices Architecture

**Definition**: An architectural approach where applications are built as a collection of small, independent services.

#### When to Use Microservices Architecture
- **Large teams** (10+ developers)
- **Complex business domains** with multiple bounded contexts
- **High scalability** requirements
- **Technology diversity** needs
- **Independent deployment** requirements

#### Advantages
```
✅ Independent scaling of components
✅ Technology diversity and flexibility
✅ Better fault isolation
✅ Team autonomy and ownership
✅ Easier to maintain and update individual services
```

#### Disadvantages
```
❌ Increased complexity in deployment and monitoring
❌ Network latency and communication overhead
❌ Data consistency challenges
❌ More complex security and authentication
❌ Distributed system debugging complexity
```

---

## 2. Azure AI Foundry Project Structures

### Foundry Project Architecture

Azure AI Foundry projects can be organized using different patterns:

#### Pattern 1: Single-Service Architecture

```
ai-foundry-project/
├── src/
│   ├── main.py                    # Main application entry point
│   ├── models/
│   │   ├── chat_model.py         # Chat completion logic
│   │   ├── embedding_model.py    # Embedding generation
│   │   └── vision_model.py       # Vision processing
│   ├── services/
│   │   ├── ai_service.py         # Core AI service logic
│   │   ├── data_service.py       # Data processing
│   │   └── validation_service.py # Input validation
│   ├── api/
│   │   ├── routes.py             # API endpoints
│   │   ├── middleware.py         # Authentication, logging
│   │   └── schemas.py            # Request/response schemas
│   └── utils/
│       ├── config.py             # Configuration management
│       ├── logging.py            # Logging utilities
│       └── helpers.py            # Common utilities
├── tests/
├── config/
├── docs/
└── requirements.txt
```

#### Pattern 2: Multi-Service Architecture

```
ai-foundry-project/
├── services/
│   ├── chat-service/             # Chat completion service
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── embedding-service/        # Embedding generation service
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── vision-service/           # Vision processing service
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── api-gateway/              # API gateway service
│       ├── src/
│       ├── tests/
│       ├── Dockerfile
│       └── requirements.txt
├── shared/
│   ├── schemas/                  # Shared data models
│   ├── auth/                     # Authentication utilities
│   └── monitoring/               # Shared monitoring
├── infrastructure/
│   ├── terraform/
│   ├── docker-compose.yml
│   └── kubernetes/
├── docs/
└── README.md
```

---

## 3. Design Patterns for AI Applications

### Repository Pattern

Abstracts data access logic and provides a consistent interface for data operations.

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from azure.ai.inference import ChatCompletionsClient

class ConversationRepository(ABC):
    @abstractmethod
    async def save_conversation(self, conversation: dict) -> str:
        pass
    
    @abstractmethod
    async def get_conversation(self, conversation_id: str) -> Optional[dict]:
        pass
    
    @abstractmethod
    async def list_conversations(self, user_id: str) -> List[dict]:
        pass

class AzureConversationRepository(ConversationRepository):
    def __init__(self, cosmos_client):
        self.cosmos_client = cosmos_client
    
    async def save_conversation(self, conversation: dict) -> str:
        # Implementation for Azure Cosmos DB
        return await self.cosmos_client.create_item(conversation)
    
    async def get_conversation(self, conversation_id: str) -> Optional[dict]:
        # Implementation for Azure Cosmos DB
        return await self.cosmos_client.read_item(conversation_id)
    
    async def list_conversations(self, user_id: str) -> List[dict]:
        # Implementation for Azure Cosmos DB
        query = f"SELECT * FROM c WHERE c.user_id = '{user_id}'"
        return await self.cosmos_client.query_items(query)
```

### Factory Pattern

Creates objects without specifying their exact classes, useful for model selection.

```python
from abc import ABC, abstractmethod
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

class AIModelFactory(ABC):
    @abstractmethod
    def create_model(self, model_type: str, **kwargs):
        pass

class AzureAIModelFactory(AIModelFactory):
    def __init__(self, endpoint: str, credential):
        self.endpoint = endpoint
        self.credential = credential
    
    def create_model(self, model_type: str, **kwargs):
        if model_type == "chat":
            return ChatCompletionsClient(
                endpoint=self.endpoint,
                credential=self.credential
            )
        elif model_type == "embedding":
            return EmbeddingClient(
                endpoint=self.endpoint,
                credential=self.credential
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")

# Usage
factory = AzureAIModelFactory(endpoint, DefaultAzureCredential())
chat_model = factory.create_model("chat")
embedding_model = factory.create_model("embedding")
```

### Strategy Pattern

Defines a family of algorithms and makes them interchangeable at runtime.

```python
from abc import ABC, abstractmethod

class ProcessingStrategy(ABC):
    @abstractmethod
    async def process(self, input_data: str) -> str:
        pass

class SimpleProcessingStrategy(ProcessingStrategy):
    async def process(self, input_data: str) -> str:
        # Simple processing logic
        return input_data.strip().lower()

class AdvancedProcessingStrategy(ProcessingStrategy):
    def __init__(self, ai_client):
        self.ai_client = ai_client
    
    async def process(self, input_data: str) -> str:
        # Advanced AI-powered processing
        response = await self.ai_client.complete({
            "messages": [
                {"role": "user", "content": f"Process this text: {input_data}"}
            ]
        })
        return response.choices[0].message.content

class TextProcessor:
    def __init__(self, strategy: ProcessingStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: ProcessingStrategy):
        self._strategy = strategy
    
    async def process_text(self, text: str) -> str:
        return await self._strategy.process(text)

# Usage
processor = TextProcessor(SimpleProcessingStrategy())
result = await processor.process_text("Hello World")

# Switch to advanced strategy
processor.set_strategy(AdvancedProcessingStrategy(ai_client))
result = await processor.process_text("Complex text processing")
```

### Observer Pattern

Defines a one-to-many dependency between objects for event notifications.

```python
from abc import ABC, abstractmethod
from typing import List

class EventObserver(ABC):
    @abstractmethod
    async def notify(self, event_type: str, data: dict):
        pass

class LoggingObserver(EventObserver):
    async def notify(self, event_type: str, data: dict):
        print(f"LOG: {event_type} - {data}")

class MetricsObserver(EventObserver):
    async def notify(self, event_type: str, data: dict):
        # Send metrics to monitoring system
        await self.send_metric(event_type, data)

class ConversationService:
    def __init__(self):
        self._observers: List[EventObserver] = []
    
    def add_observer(self, observer: EventObserver):
        self._observers.append(observer)
    
    def remove_observer(self, observer: EventObserver):
        self._observers.remove(observer)
    
    async def _notify_observers(self, event_type: str, data: dict):
        for observer in self._observers:
            await observer.notify(event_type, data)
    
    async def create_conversation(self, user_id: str) -> str:
        # Create conversation logic
        conversation_id = "conv_123"
        
        # Notify observers
        await self._notify_observers("conversation_created", {
            "conversation_id": conversation_id,
            "user_id": user_id
        })
        
        return conversation_id
```

---

## 4. Component Design Principles

### Single Responsibility Principle (SRP)

Each component should have only one reason to change.

```python
# ❌ Violates SRP - handles multiple responsibilities
class AIService:
    def __init__(self, ai_client):
        self.ai_client = ai_client
    
    def process_request(self, request):
        # Validation
        if not request.get('message'):
            raise ValueError("Message is required")
        
        # Logging
        print(f"Processing request: {request}")
        
        # AI processing
        response = self.ai_client.complete(request)
        
        # Database saving
        self.save_to_database(response)
        
        # Email notification
        self.send_email_notification(response)
        
        return response

# ✅ Follows SRP - each class has single responsibility
class RequestValidator:
    def validate(self, request):
        if not request.get('message'):
            raise ValueError("Message is required")

class ConversationLogger:
    def log_request(self, request):
        print(f"Processing request: {request}")

class AIProcessor:
    def __init__(self, ai_client):
        self.ai_client = ai_client
    
    def process(self, request):
        return self.ai_client.complete(request)

class ConversationPersistence:
    def save(self, conversation):
        # Save to database
        pass

class NotificationService:
    def send_notification(self, data):
        # Send notification
        pass
```

### Dependency Injection

Promotes loose coupling by injecting dependencies rather than creating them.

```python
from typing import Protocol

class AIClient(Protocol):
    async def complete(self, request: dict) -> dict:
        ...

class ConversationStorage(Protocol):
    async def save(self, conversation: dict) -> str:
        ...

class ConversationService:
    def __init__(self, ai_client: AIClient, storage: ConversationStorage):
        self.ai_client = ai_client
        self.storage = storage
    
    async def create_conversation(self, message: str) -> dict:
        # Process with AI
        ai_response = await self.ai_client.complete({
            "messages": [{"role": "user", "content": message}]
        })
        
        # Save conversation
        conversation = {
            "user_message": message,
            "ai_response": ai_response.choices[0].message.content,
            "timestamp": datetime.utcnow()
        }
        
        conversation_id = await self.storage.save(conversation)
        conversation["id"] = conversation_id
        
        return conversation

# Usage with dependency injection
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

ai_client = ChatCompletionsClient(endpoint, DefaultAzureCredential())
storage = AzureConversationRepository(cosmos_client)

conversation_service = ConversationService(ai_client, storage)
```

---

## 5. Scalability Patterns

### Horizontal Scaling Patterns

#### Load Balancing

```python
import random
from typing import List

class LoadBalancer:
    def __init__(self, endpoints: List[str]):
        self.endpoints = endpoints
        self.current_index = 0
    
    def get_endpoint_round_robin(self) -> str:
        """Round-robin load balancing"""
        endpoint = self.endpoints[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.endpoints)
        return endpoint
    
    def get_endpoint_random(self) -> str:
        """Random load balancing"""
        return random.choice(self.endpoints)
    
    def get_endpoint_weighted(self, weights: List[int]) -> str:
        """Weighted random load balancing"""
        return random.choices(self.endpoints, weights=weights)[0]

class ScalableAIService:
    def __init__(self, endpoints: List[str]):
        self.load_balancer = LoadBalancer(endpoints)
        self.clients = {}
    
    def get_client(self, endpoint: str):
        if endpoint not in self.clients:
            self.clients[endpoint] = ChatCompletionsClient(
                endpoint=endpoint,
                credential=DefaultAzureCredential()
            )
        return self.clients[endpoint]
    
    async def process_request(self, request: dict) -> dict:
        endpoint = self.load_balancer.get_endpoint_round_robin()
        client = self.get_client(endpoint)
        
        try:
            return await client.complete(request)
        except Exception as e:
            # Fallback to different endpoint
            fallback_endpoint = self.load_balancer.get_endpoint_random()
            if fallback_endpoint != endpoint:
                fallback_client = self.get_client(fallback_endpoint)
                return await fallback_client.complete(request)
            raise e
```

#### Caching Patterns

```python
import hashlib
import json
from typing import Optional
from datetime import datetime, timedelta

class ConversationCache:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.default_ttl = 3600  # 1 hour
    
    def _generate_key(self, request: dict) -> str:
        """Generate cache key from request"""
        request_str = json.dumps(request, sort_keys=True)
        return hashlib.md5(request_str.encode()).hexdigest()
    
    async def get(self, request: dict) -> Optional[dict]:
        """Get cached response"""
        key = self._generate_key(request)
        cached_response = await self.redis_client.get(key)
        
        if cached_response:
            return json.loads(cached_response)
        return None
    
    async def set(self, request: dict, response: dict, ttl: int = None):
        """Cache response"""
        key = self._generate_key(request)
        ttl = ttl or self.default_ttl
        
        await self.redis_client.setex(
            key, 
            ttl, 
            json.dumps(response)
        )

class CachedAIService:
    def __init__(self, ai_client, cache: ConversationCache):
        self.ai_client = ai_client
        self.cache = cache
    
    async def process_request(self, request: dict) -> dict:
        # Check cache first
        cached_response = await self.cache.get(request)
        if cached_response:
            return cached_response
        
        # Process with AI if not cached
        response = await self.ai_client.complete(request)
        
        # Cache the response
        await self.cache.set(request, response)
        
        return response
```

### Vertical Scaling Patterns

#### Resource Optimization

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List

class OptimizedAIService:
    def __init__(self, ai_client, max_workers: int = 10):
        self.ai_client = ai_client
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.semaphore = asyncio.Semaphore(max_workers)
    
    async def process_batch(self, requests: List[dict]) -> List[dict]:
        """Process multiple requests concurrently"""
        async def process_single(request):
            async with self.semaphore:
                return await self.ai_client.complete(request)
        
        tasks = [process_single(req) for req in requests]
        return await asyncio.gather(*tasks)
    
    async def process_with_timeout(self, request: dict, timeout: int = 30) -> dict:
        """Process request with timeout"""
        try:
            return await asyncio.wait_for(
                self.ai_client.complete(request),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            raise TimeoutError(f"Request timed out after {timeout} seconds")
```

---

## 6. Data Flow Architecture

### Event-Driven Architecture

```python
import asyncio
from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime
    correlation_id: str

class EventBus:
    def __init__(self):
        self.subscribers = {}
    
    def subscribe(self, event_type: str, handler):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    async def publish(self, event: Event):
        if event.event_type in self.subscribers:
            tasks = []
            for handler in self.subscribers[event.event_type]:
                tasks.append(handler(event))
            await asyncio.gather(*tasks)

class ConversationHandler:
    def __init__(self, ai_client, event_bus: EventBus):
        self.ai_client = ai_client
        self.event_bus = event_bus
        
        # Subscribe to events
        self.event_bus.subscribe("user_message_received", self.handle_user_message)
    
    async def handle_user_message(self, event: Event):
        """Handle user message event"""
        message = event.data.get("message")
        user_id = event.data.get("user_id")
        
        # Process with AI
        response = await self.ai_client.complete({
            "messages": [{"role": "user", "content": message}]
        })
        
        # Publish AI response event
        await self.event_bus.publish(Event(
            event_type="ai_response_generated",
            data={
                "user_id": user_id,
                "response": response.choices[0].message.content,
                "original_message": message
            },
            timestamp=datetime.utcnow(),
            correlation_id=event.correlation_id
        ))
```

### Pipeline Pattern

```python
from abc import ABC, abstractmethod
from typing import Any

class ProcessingStep(ABC):
    @abstractmethod
    async def process(self, data: Any) -> Any:
        pass

class ValidationStep(ProcessingStep):
    async def process(self, data: dict) -> dict:
        if not data.get("message"):
            raise ValueError("Message is required")
        return data

class PreprocessingStep(ProcessingStep):
    async def process(self, data: dict) -> dict:
        # Clean and preprocess the message
        data["message"] = data["message"].strip()
        data["processed_at"] = datetime.utcnow()
        return data

class AIProcessingStep(ProcessingStep):
    def __init__(self, ai_client):
        self.ai_client = ai_client
    
    async def process(self, data: dict) -> dict:
        response = await self.ai_client.complete({
            "messages": [{"role": "user", "content": data["message"]}]
        })
        data["ai_response"] = response.choices[0].message.content
        return data

class PostprocessingStep(ProcessingStep):
    async def process(self, data: dict) -> dict:
        # Format the response
        data["formatted_response"] = f"AI: {data['ai_response']}"
        return data

class ProcessingPipeline:
    def __init__(self, steps: List[ProcessingStep]):
        self.steps = steps
    
    async def execute(self, initial_data: Any) -> Any:
        data = initial_data
        for step in self.steps:
            data = await step.process(data)
        return data

# Usage
pipeline = ProcessingPipeline([
    ValidationStep(),
    PreprocessingStep(),
    AIProcessingStep(ai_client),
    PostprocessingStep()
])

result = await pipeline.execute({"message": "Hello, world!"})
```

---

## 7. Performance Considerations

### Memory Management

```python
import gc
import psutil
from typing import Optional

class ResourceMonitor:
    def __init__(self, memory_threshold: float = 0.8):
        self.memory_threshold = memory_threshold
    
    def get_memory_usage(self) -> float:
        """Get current memory usage percentage"""
        return psutil.virtual_memory().percent / 100
    
    def should_trigger_cleanup(self) -> bool:
        """Check if memory cleanup should be triggered"""
        return self.get_memory_usage() > self.memory_threshold
    
    def cleanup_memory(self):
        """Force garbage collection"""
        gc.collect()

class MemoryOptimizedAIService:
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.monitor = ResourceMonitor()
        self.conversation_cache = {}
        self.max_cache_size = 1000
    
    async def process_request(self, request: dict) -> dict:
        # Check memory before processing
        if self.monitor.should_trigger_cleanup():
            self._cleanup_cache()
            self.monitor.cleanup_memory()
        
        response = await self.ai_client.complete(request)
        
        # Cache with size limit
        if len(self.conversation_cache) < self.max_cache_size:
            cache_key = str(hash(str(request)))
            self.conversation_cache[cache_key] = response
        
        return response
    
    def _cleanup_cache(self):
        """Remove oldest cache entries"""
        if len(self.conversation_cache) > self.max_cache_size // 2:
            # Remove half of the cache entries (oldest first)
            items_to_remove = len(self.conversation_cache) // 2
            keys_to_remove = list(self.conversation_cache.keys())[:items_to_remove]
            for key in keys_to_remove:
                del self.conversation_cache[key]
```

### Connection Pooling

```python
import asyncio
from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential

class ConnectionPool:
    def __init__(self, endpoint: str, pool_size: int = 10):
        self.endpoint = endpoint
        self.pool_size = pool_size
        self.available_clients = asyncio.Queue(maxsize=pool_size)
        self.credential = DefaultAzureCredential()
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize the connection pool"""
        for _ in range(self.pool_size):
            client = ChatCompletionsClient(
                endpoint=self.endpoint,
                credential=self.credential
            )
            self.available_clients.put_nowait(client)
    
    async def acquire(self) -> ChatCompletionsClient:
        """Acquire a client from the pool"""
        return await self.available_clients.get()
    
    async def release(self, client: ChatCompletionsClient):
        """Release a client back to the pool"""
        await self.available_clients.put(client)

class PooledAIService:
    def __init__(self, connection_pool: ConnectionPool):
        self.pool = connection_pool
    
    async def process_request(self, request: dict) -> dict:
        # Acquire client from pool
        client = await self.pool.acquire()
        
        try:
            # Process request
            response = await client.complete(request)
            return response
        finally:
            # Always release client back to pool
            await self.pool.release(client)

# Usage
pool = ConnectionPool(endpoint="https://your-ai-foundry.cognitiveservices.azure.com")
service = PooledAIService(pool)
```

---

## 8. Practical Exercises

### Exercise 1: Design a Microservices Architecture

Design a microservices architecture for a customer service AI application with the following requirements:
- Chat completion service
- Document analysis service
- User management service
- Analytics service

**Solution Approach:**
1. Define service boundaries
2. Design API contracts
3. Plan data flow between services
4. Consider deployment and scaling strategies

### Exercise 2: Implement the Repository Pattern

Create a repository pattern implementation for conversation management with support for multiple storage backends (Azure Cosmos DB, Azure SQL Database).

### Exercise 3: Build a Scalable AI Service

Implement a scalable AI service that can handle high traffic using:
- Load balancing
- Caching
- Connection pooling
- Error handling and retries

---

## Summary

In this lesson, we've covered:

✅ **Architectural Patterns**: Understanding when to use monolithic vs microservices architectures
✅ **Design Patterns**: Implementing Repository, Factory, Strategy, and Observer patterns
✅ **Component Design**: Following SOLID principles and dependency injection
✅ **Scalability Patterns**: Horizontal and vertical scaling strategies
✅ **Data Flow Architecture**: Event-driven and pipeline patterns
✅ **Performance Optimization**: Memory management and connection pooling

## Next Steps

In the next lesson, we'll explore **Development Workflows and Methodologies**, where you'll learn how to implement effective development processes for AI projects, including agile methodologies, sprint planning, and quality assurance practices.

## Additional Resources

- [Azure Architecture Center](https://docs.microsoft.com/en-us/azure/architecture/)
- [Microservices Patterns](https://microservices.io/patterns/)
- [Azure AI Foundry Best Practices](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/best-practices)
- [Design Patterns in Python](https://refactoring.guru/design-patterns/python)

---

*This lesson provides the architectural foundation needed to build scalable, maintainable, and efficient Azure AI Foundry applications.* 