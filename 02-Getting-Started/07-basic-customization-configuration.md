# Basic Customization and Configuration

## Overview

This lesson covers fundamental customization and configuration options in Azure AI Foundry, including system messages, prompt templates, response parameters, and basic conversation flow control.

## Learning Objectives

- Master system message configuration and best practices
- Understand prompt engineering and template creation
- Configure response parameters for optimal output
- Implement basic conversation flow control
- Set up content filtering and safety measures

## Prerequisites

- Completed model selection and deployment (Lesson 06)
- Understanding of your specific use case requirements
- Basic familiarity with prompt engineering concepts

---

## 1. System Message Configuration

### Understanding System Messages

System messages define the AI's personality, behavior, and capabilities. They are the foundation of customization in Azure AI Foundry.

**System Message Examples:**
```python
system_message_examples = {
    "general_assistant": """You are a helpful AI assistant. Provide accurate, 
    helpful, and friendly responses to user questions. If you're not sure about 
    something, say so rather than guessing.""",
    
    "technical_support": """You are a technical support specialist. Help users 
    troubleshoot problems by:
    1. Asking clarifying questions
    2. Providing step-by-step solutions
    3. Explaining technical concepts clearly
    4. Following up to ensure resolution""",
    
    "educational_tutor": """You are an educational tutor. Your role is to:
    - Help students learn through questioning and explanation
    - Adapt your teaching style to the student's level
    - Encourage critical thinking
    - Be patient and supportive"""
}
```

### Advanced System Message Builder

```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class PersonalityType(Enum):
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"

@dataclass
class SystemMessageConfig:
    role: str
    personality: PersonalityType
    expertise_areas: List[str]
    behavioral_guidelines: List[str]
    constraints: List[str]
    
class SystemMessageBuilder:
    def build_system_message(self, config: SystemMessageConfig) -> str:
        """Build a comprehensive system message from configuration."""
        
        personality_templates = {
            PersonalityType.PROFESSIONAL: "You are a professional {role}. ",
            PersonalityType.FRIENDLY: "You are a helpful and friendly {role}. ",
            PersonalityType.CREATIVE: "You are a creative and imaginative {role}. ",
            PersonalityType.ANALYTICAL: "You are a detail-oriented analytical {role}. "
        }
        
        # Start with personality and role
        message = personality_templates[config.personality].format(role=config.role)
        
        # Add expertise areas
        if config.expertise_areas:
            expertise_text = ", ".join(config.expertise_areas)
            message += f"You specialize in {expertise_text}. "
        
        # Add behavioral guidelines
        if config.behavioral_guidelines:
            message += "Your approach should be to:\n"
            for guideline in config.behavioral_guidelines:
                message += f"- {guideline}\n"
        
        # Add constraints
        if config.constraints:
            message += "\nImportant constraints:\n"
            for constraint in config.constraints:
                message += f"- {constraint}\n"
        
        return message.strip()

# Example usage
config = SystemMessageConfig(
    role="customer service representative",
    personality=PersonalityType.FRIENDLY,
    expertise_areas=["product troubleshooting", "account management"],
    behavioral_guidelines=[
        "Listen carefully to customer concerns",
        "Provide clear step-by-step solutions",
        "Follow up to ensure satisfaction"
    ],
    constraints=[
        "Do not provide billing information without verification",
        "Maintain customer privacy and confidentiality"
    ]
)

builder = SystemMessageBuilder()
system_message = builder.build_system_message(config)
```

---

## 2. Prompt Engineering and Templates

### Prompt Template System

```python
from string import Template
from typing import Dict, Any, List

class PromptTemplate:
    def __init__(self, template_string: str, required_variables: List[str]):
        self.template = Template(template_string)
        self.required_variables = required_variables
    
    def render(self, variables: Dict[str, Any]) -> str:
        """Render the template with provided variables."""
        
        # Validate required variables
        missing_vars = [var for var in self.required_variables if var not in variables]
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")
        
        return self.template.substitute(variables)

class PromptLibrary:
    def __init__(self):
        self.templates = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default prompt templates."""
        
        # Question Answering Template
        self.templates["qa"] = PromptTemplate(
            template_string="""Based on the following context, please answer the user's question.

Context: $context

Question: $question

Please provide a clear, accurate answer based only on the information provided in the context.

Answer:""",
            required_variables=["context", "question"]
        )
        
        # Summarization Template
        self.templates["summarize"] = PromptTemplate(
            template_string="""Please summarize the following text in $max_sentences sentences or less.

Text to summarize:
$text

Summary:""",
            required_variables=["text", "max_sentences"]
        )
        
        # Code Generation Template
        self.templates["code_gen"] = PromptTemplate(
            template_string="""Generate $language code for the following requirement:

Requirement: $requirement

Please provide clean, well-structured code that follows best practices.

Code:""",
            required_variables=["language", "requirement"]
        )
    
    def get_template(self, template_name: str) -> PromptTemplate:
        """Get a template by name."""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        return self.templates[template_name]

# Example usage
library = PromptLibrary()

# Use QA template
qa_template = library.get_template("qa")
qa_prompt = qa_template.render({
    "context": "Azure AI Foundry is Microsoft's platform for building AI applications.",
    "question": "What is Azure AI Foundry?"
})
```

---

## 3. Response Parameter Configuration

### Model Parameter Optimization

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class ModelParameters:
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: Optional[List[str]] = None
    
    def validate(self):
        """Validate parameter ranges."""
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        if not 1 <= self.max_tokens <= 4096:
            raise ValueError("Max tokens must be between 1 and 4096")

class ParameterOptimizer:
    def __init__(self):
        self.preset_configs = {
            "creative": ModelParameters(
                temperature=0.9,
                max_tokens=1500,
                top_p=0.95,
                frequency_penalty=0.3,
                presence_penalty=0.3
            ),
            "balanced": ModelParameters(
                temperature=0.7,
                max_tokens=1000,
                top_p=0.9,
                frequency_penalty=0.0,
                presence_penalty=0.0
            ),
            "focused": ModelParameters(
                temperature=0.3,
                max_tokens=800,
                top_p=0.8
            ),
            "factual": ModelParameters(
                temperature=0.1,
                max_tokens=500,
                top_p=0.7
            )
        }
    
    def get_preset(self, preset_name: str) -> ModelParameters:
        """Get a preset parameter configuration."""
        if preset_name not in self.preset_configs:
            raise ValueError(f"Preset '{preset_name}' not found")
        return self.preset_configs[preset_name]
    
    def optimize_for_task(self, task_type: str, context: Dict[str, Any]) -> ModelParameters:
        """Optimize parameters based on task type and context."""
        
        base_params = self.preset_configs.get("balanced")
        
        # Task-specific optimizations
        if task_type == "creative_writing":
            base_params.temperature = 0.8
            base_params.max_tokens = 1500
            base_params.frequency_penalty = 0.3
            
        elif task_type == "technical_qa":
            base_params.temperature = 0.2
            base_params.max_tokens = 800
            base_params.top_p = 0.8
            
        elif task_type == "code_generation":
            base_params.temperature = 0.2
            base_params.max_tokens = 2000
            base_params.stop_sequences = ["```", "###"]
        
        base_params.validate()
        return base_params

# Example usage
optimizer = ParameterOptimizer()

# Get preset configurations
creative_params = optimizer.get_preset("creative")
factual_params = optimizer.get_preset("factual")

# Optimize for specific tasks
writing_params = optimizer.optimize_for_task("creative_writing", {})
qa_params = optimizer.optimize_for_task("technical_qa", {})
```

---

## 4. Conversation Flow Control

### Basic Conversation State Management

```python
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime

class ConversationState(Enum):
    GREETING = "greeting"
    INFORMATION_GATHERING = "information_gathering"
    PROBLEM_SOLVING = "problem_solving"
    RESOLUTION = "resolution"
    CLOSING = "closing"

@dataclass
class ConversationContext:
    user_id: str
    session_id: str
    current_state: ConversationState
    collected_info: Dict[str, Any]
    conversation_goal: str = None

class ConversationFlowManager:
    def __init__(self):
        self.state_prompts = {
            ConversationState.GREETING: "Hello! How can I help you today?",
            ConversationState.INFORMATION_GATHERING: "To better assist you, could you provide more details about {topic}?",
            ConversationState.PROBLEM_SOLVING: "Based on what you've told me, here are some solutions to consider:",
            ConversationState.RESOLUTION: "Here's a summary of our discussion and the recommended next steps:",
            ConversationState.CLOSING: "Is there anything else I can help you with today?"
        }
    
    def determine_next_state(self, current_context: ConversationContext, user_input: str) -> ConversationState:
        """Determine the next conversation state based on context and input."""
        
        current_state = current_context.current_state
        
        # Simple rule-based state transition logic
        if current_state == ConversationState.GREETING:
            if self._has_clear_problem(user_input):
                return ConversationState.PROBLEM_SOLVING
            else:
                return ConversationState.INFORMATION_GATHERING
        
        elif current_state == ConversationState.INFORMATION_GATHERING:
            if self._has_sufficient_info(current_context):
                return ConversationState.PROBLEM_SOLVING
            else:
                return ConversationState.INFORMATION_GATHERING
        
        elif current_state == ConversationState.PROBLEM_SOLVING:
            return ConversationState.RESOLUTION
        
        elif current_state == ConversationState.RESOLUTION:
            if self._conversation_complete(user_input):
                return ConversationState.CLOSING
            else:
                return ConversationState.INFORMATION_GATHERING
        
        else:  # CLOSING
            return ConversationState.GREETING
    
    def _has_clear_problem(self, user_input: str) -> bool:
        """Check if user input contains a clear problem statement."""
        problem_indicators = ["help", "issue", "problem", "error", "need"]
        return any(indicator in user_input.lower() for indicator in problem_indicators)
    
    def _has_sufficient_info(self, context: ConversationContext) -> bool:
        """Check if we have sufficient information to provide solutions."""
        required_fields = ["problem_description"]
        return all(field in context.collected_info for field in required_fields)
    
    def _conversation_complete(self, user_input: str) -> bool:
        """Check if conversation is complete."""
        completion_indicators = ["thank", "thanks", "solved", "good", "bye"]
        return any(indicator in user_input.lower() for indicator in completion_indicators)
    
    def get_state_prompt(self, context: ConversationContext) -> str:
        """Get a prompt appropriate for the current conversation state."""
        return self.state_prompts.get(context.current_state, "How can I help you?")

# Example usage
flow_manager = ConversationFlowManager()

# Create conversation context
context = ConversationContext(
    user_id="user123",
    session_id="session456", 
    current_state=ConversationState.GREETING,
    collected_info={}
)

# Get state-specific prompt
prompt = flow_manager.get_state_prompt(context)
print(f"Current prompt: {prompt}")
```

---

## 5. Content Filtering and Safety

### Basic Content Safety Configuration

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

class SafetyLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ContentCategory(Enum):
    HATE = "hate"
    VIOLENCE = "violence"
    HARASSMENT = "harassment"
    INAPPROPRIATE = "inappropriate"

@dataclass
class ContentFilter:
    category: ContentCategory
    severity_threshold: SafetyLevel
    action: str  # "block", "warn", "flag"

class ContentSafetyManager:
    def __init__(self, safety_level: SafetyLevel = SafetyLevel.MEDIUM):
        self.safety_level = safety_level
        self.content_filters = self._initialize_filters()
        self.blocked_terms = []
    
    def _initialize_filters(self) -> List[ContentFilter]:
        """Initialize content filters based on safety level."""
        filters = [
            ContentFilter(ContentCategory.HATE, SafetyLevel.LOW, "block"),
            ContentFilter(ContentCategory.VIOLENCE, SafetyLevel.LOW, "block"),
            ContentFilter(ContentCategory.HARASSMENT, SafetyLevel.LOW, "block")
        ]
        
        if self.safety_level == SafetyLevel.HIGH:
            filters.append(
                ContentFilter(ContentCategory.INAPPROPRIATE, SafetyLevel.LOW, "warn")
            )
        
        return filters
    
    def add_blocked_terms(self, terms: List[str]):
        """Add custom blocked terms."""
        self.blocked_terms.extend(terms)
    
    def evaluate_content(self, text: str) -> Dict[str, Any]:
        """Evaluate content against safety filters."""
        
        results = {
            "is_safe": True,
            "triggered_filters": [],
            "recommendations": []
        }
        
        # Check custom blocked terms
        for term in self.blocked_terms:
            if term.lower() in text.lower():
                results["is_safe"] = False
                results["triggered_filters"].append({
                    "category": "custom_blocked",
                    "term": term,
                    "action": "block"
                })
        
        # Simple content analysis simulation
        if self._contains_inappropriate_content(text):
            results["triggered_filters"].append({
                "category": "inappropriate",
                "action": "warn"
            })
        
        # Generate recommendations
        if not results["is_safe"]:
            results["recommendations"] = ["Please rephrase using appropriate language"]
        
        return results
    
    def _contains_inappropriate_content(self, text: str) -> bool:
        """Simple check for inappropriate content."""
        inappropriate_keywords = ["hate", "violence", "harassment"]
        return any(keyword in text.lower() for keyword in inappropriate_keywords)

# Example usage
safety_manager = ContentSafetyManager(SafetyLevel.MEDIUM)
safety_manager.add_blocked_terms(["confidential", "proprietary"])

# Evaluate content
test_content = "This is a normal message"
safety_result = safety_manager.evaluate_content(test_content)
print(f"Safety evaluation: {safety_result}")
```

---

## Summary

This lesson covered fundamental customization and configuration in Azure AI Foundry:

- **System Messages**: Building personality and behavior definitions
- **Prompt Engineering**: Creating templates and dynamic prompts
- **Response Parameters**: Optimizing model parameters for different tasks
- **Conversation Flow**: Managing state and conversation progression
- **Content Safety**: Implementing basic filtering and safety measures

## Next Steps

- Implement custom system messages for your use case
- Create prompt templates for common scenarios
- Configure appropriate safety filters
- Test different parameter combinations
- Explore monitoring and optimization (Lesson 08)

---

*This lesson is part of the Azure AI Foundry Zero-to-Hero course.* 