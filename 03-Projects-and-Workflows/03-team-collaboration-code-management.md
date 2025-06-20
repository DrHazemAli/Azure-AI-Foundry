# Lesson 3: Team Collaboration and Code Management

## Learning Objectives

By the end of this lesson, you will be able to:
- Implement role-based access control for AI development teams
- Design effective branching strategies for AI projects
- Set up code sharing and collaboration workflows
- Coordinate cross-functional AI development teams
- Manage permissions and security in collaborative environments
- Establish code ownership and review policies

## Overview

AI development requires unique collaboration patterns due to the experimental nature of machine learning, the diverse skill sets involved, and the need for careful model and data management. This lesson covers proven strategies for managing teams, code, and collaboration in Azure AI Foundry projects.

---

## 1. AI Team Structure and Roles

### Cross-Functional AI Team Composition

#### Core Roles

**AI/ML Engineers**
- Model development and optimization
- Algorithm implementation
- Performance tuning and evaluation
- Integration with Azure AI Foundry services

**Data Scientists**
- Data analysis and exploration
- Feature engineering
- Model experimentation
- Statistical analysis and validation

**Software Engineers**
- Application development and integration
- API design and implementation
- Infrastructure and deployment
- Performance optimization

**DevOps Engineers**
- CI/CD pipeline management
- Infrastructure automation
- Monitoring and alerting
- Security and compliance

#### Specialized Roles

**Data Engineers**
- Data pipeline development
- Data quality and governance
- ETL processes
- Data storage optimization

**AI Ethics Officer**
- Responsible AI practices
- Bias detection and mitigation
- Compliance and governance
- Risk assessment

**Product Owner**
- Business requirements definition
- Stakeholder communication
- Priority management
- Success metrics definition

### Team Organization Patterns

#### Pattern 1: Feature Teams

```
Feature Team A (Customer Service AI)
├── 1 Product Owner
├── 2 AI/ML Engineers
├── 1 Data Scientist
├── 2 Software Engineers
└── 1 DevOps Engineer (shared)

Feature Team B (Analytics AI)
├── 1 Product Owner
├── 1 AI/ML Engineer
├── 2 Data Scientists
├── 1 Software Engineer
└── 1 DevOps Engineer (shared)
```

#### Pattern 2: Platform Team + Product Teams

```
AI Platform Team
├── Platform Owner
├── 2 Platform Engineers
├── 1 Data Engineer
└── 1 DevOps Engineer

Product Teams (multiple)
├── Product Owner
├── 1 AI/ML Engineer
├── 1 Data Scientist
└── 2 Application Developers
```

---

## 2. Role-Based Access Control (RBAC)

### Azure AI Foundry Permission Model

```python
from dataclasses import dataclass
from typing import List, Dict, Set
from enum import Enum

class PermissionLevel(Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    OWNER = "owner"

class ResourceType(Enum):
    PROJECT = "project"
    MODEL = "model"
    DATA = "data"
    DEPLOYMENT = "deployment"
    SECRETS = "secrets"

@dataclass
class Permission:
    resource_type: ResourceType
    resource_id: str
    level: PermissionLevel

@dataclass
class TeamRole:
    name: str
    description: str
    permissions: List[Permission]
    
    def can_access(self, resource_type: ResourceType, 
                  resource_id: str, required_level: PermissionLevel) -> bool:
        """Check if role has required access to resource"""
        for permission in self.permissions:
            if (permission.resource_type == resource_type and 
                permission.resource_id == resource_id and
                self._permission_level_sufficient(permission.level, required_level)):
                return True
        return False
    
    def _permission_level_sufficient(self, granted: PermissionLevel, 
                                   required: PermissionLevel) -> bool:
        """Check if granted permission level is sufficient"""
        hierarchy = {
            PermissionLevel.READ: 1,
            PermissionLevel.WRITE: 2,
            PermissionLevel.ADMIN: 3,
            PermissionLevel.OWNER: 4
        }
        return hierarchy[granted] >= hierarchy[required]

class AITeamRoleManager:
    def __init__(self):
        self.predefined_roles = self._create_predefined_roles()
        self.user_roles = {}
    
    def _create_predefined_roles(self) -> Dict[str, TeamRole]:
        """Create predefined team roles for AI projects"""
        roles = {}
        
        # AI/ML Engineer Role
        roles["ai_engineer"] = TeamRole(
            name="AI/ML Engineer",
            description="Develops and maintains AI models",
            permissions=[
                Permission(ResourceType.PROJECT, "*", PermissionLevel.READ),
                Permission(ResourceType.MODEL, "*", PermissionLevel.WRITE),
                Permission(ResourceType.DATA, "*", PermissionLevel.READ),
                Permission(ResourceType.DEPLOYMENT, "*", PermissionLevel.WRITE),
            ]
        )
        
        # Data Scientist Role
        roles["data_scientist"] = TeamRole(
            name="Data Scientist",
            description="Analyzes data and develops experiments",
            permissions=[
                Permission(ResourceType.PROJECT, "*", PermissionLevel.READ),
                Permission(ResourceType.MODEL, "*", PermissionLevel.READ),
                Permission(ResourceType.DATA, "*", PermissionLevel.WRITE),
                Permission(ResourceType.DEPLOYMENT, "*", PermissionLevel.READ),
            ]
        )
        
        # Software Engineer Role
        roles["software_engineer"] = TeamRole(
            name="Software Engineer",
            description="Develops application and integration code",
            permissions=[
                Permission(ResourceType.PROJECT, "*", PermissionLevel.READ),
                Permission(ResourceType.MODEL, "*", PermissionLevel.READ),
                Permission(ResourceType.DATA, "*", PermissionLevel.READ),
                Permission(ResourceType.DEPLOYMENT, "*", PermissionLevel.WRITE),
            ]
        )
        
        # DevOps Engineer Role
        roles["devops_engineer"] = TeamRole(
            name="DevOps Engineer",
            description="Manages infrastructure and deployments",
            permissions=[
                Permission(ResourceType.PROJECT, "*", PermissionLevel.ADMIN),
                Permission(ResourceType.MODEL, "*", PermissionLevel.READ),
                Permission(ResourceType.DATA, "*", PermissionLevel.READ),
                Permission(ResourceType.DEPLOYMENT, "*", PermissionLevel.ADMIN),
                Permission(ResourceType.SECRETS, "*", PermissionLevel.ADMIN),
            ]
        )
        
        # Project Lead Role
        roles["project_lead"] = TeamRole(
            name="Project Lead",
            description="Leads project and manages team",
            permissions=[
                Permission(ResourceType.PROJECT, "*", PermissionLevel.OWNER),
                Permission(ResourceType.MODEL, "*", PermissionLevel.ADMIN),
                Permission(ResourceType.DATA, "*", PermissionLevel.ADMIN),
                Permission(ResourceType.DEPLOYMENT, "*", PermissionLevel.ADMIN),
                Permission(ResourceType.SECRETS, "*", PermissionLevel.ADMIN),
            ]
        )
        
        return roles
    
    def assign_role(self, user_id: str, role_name: str, project_id: str = None):
        """Assign role to user for specific project or globally"""
        if role_name not in self.predefined_roles:
            raise ValueError(f"Unknown role: {role_name}")
        
        key = f"{user_id}:{project_id}" if project_id else user_id
        if key not in self.user_roles:
            self.user_roles[key] = []
        
        self.user_roles[key].append(self.predefined_roles[role_name])
    
    def check_permission(self, user_id: str, resource_type: ResourceType,
                        resource_id: str, required_level: PermissionLevel,
                        project_id: str = None) -> bool:
        """Check if user has required permission"""
        # Check project-specific roles first
        if project_id:
            project_key = f"{user_id}:{project_id}"
            if project_key in self.user_roles:
                for role in self.user_roles[project_key]:
                    if role.can_access(resource_type, resource_id, required_level):
                        return True
        
        # Check global roles
        if user_id in self.user_roles:
            for role in self.user_roles[user_id]:
                if role.can_access(resource_type, resource_id, required_level):
                    return True
        
        return False

# Usage Example
role_manager = AITeamRoleManager()

# Assign roles to team members
role_manager.assign_role("alice@company.com", "ai_engineer", "project-1")
role_manager.assign_role("bob@company.com", "data_scientist", "project-1")
role_manager.assign_role("charlie@company.com", "devops_engineer")  # Global role

# Check permissions
can_deploy = role_manager.check_permission(
    "alice@company.com", 
    ResourceType.DEPLOYMENT, 
    "model-v1", 
    PermissionLevel.WRITE,
    "project-1"
)
```

### Azure AD Integration

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.resource import ResourceManagementClient

class AzureRBACManager:
    def __init__(self, subscription_id: str):
        self.subscription_id = subscription_id
        self.credential = DefaultAzureCredential()
        self.auth_client = AuthorizationManagementClient(
            self.credential, subscription_id
        )
        self.resource_client = ResourceManagementClient(
            self.credential, subscription_id
        )
    
    def create_custom_role(self, role_definition: dict) -> str:
        """Create custom role for AI team members"""
        scope = f"/subscriptions/{self.subscription_id}"
        
        role_def = {
            "roleName": role_definition["name"],
            "description": role_definition["description"],
            "assignableScopes": [scope],
            "permissions": [{
                "actions": role_definition["actions"],
                "notActions": role_definition.get("notActions", []),
                "dataActions": role_definition.get("dataActions", []),
                "notDataActions": role_definition.get("notDataActions", [])
            }]
        }
        
        result = self.auth_client.role_definitions.create_or_update(
            scope=scope,
            role_definition_id=f"{scope}/providers/Microsoft.Authorization/roleDefinitions/{role_definition['id']}",
            role_definition=role_def
        )
        
        return result.name
    
    def assign_role_to_user(self, user_principal_id: str, role_definition_id: str,
                           resource_group: str = None, resource_name: str = None):
        """Assign role to user at specified scope"""
        if resource_name and resource_group:
            scope = f"/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.CognitiveServices/accounts/{resource_name}"
        elif resource_group:
            scope = f"/subscriptions/{self.subscription_id}/resourceGroups/{resource_group}"
        else:
            scope = f"/subscriptions/{self.subscription_id}"
        
        assignment_name = f"assignment-{user_principal_id}-{role_definition_id}"
        
        assignment = {
            "roleDefinitionId": f"/subscriptions/{self.subscription_id}/providers/Microsoft.Authorization/roleDefinitions/{role_definition_id}",
            "principalId": user_principal_id,
            "principalType": "User"
        }
        
        self.auth_client.role_assignments.create(
            scope=scope,
            role_assignment_name=assignment_name,
            parameters=assignment
        )

# AI-specific role definitions
AI_ROLES = {
    "ai_model_developer": {
        "id": "12345678-1234-1234-1234-123456789012",
        "name": "AI Model Developer",
        "description": "Can develop and deploy AI models",
        "actions": [
            "Microsoft.CognitiveServices/accounts/read",
            "Microsoft.CognitiveServices/accounts/deployments/*",
            "Microsoft.CognitiveServices/accounts/models/*"
        ],
        "dataActions": [
            "Microsoft.CognitiveServices/accounts/models/invoke/action"
        ]
    },
    "ai_data_scientist": {
        "id": "87654321-4321-4321-4321-210987654321",
        "name": "AI Data Scientist",
        "description": "Can access data and perform experiments",
        "actions": [
            "Microsoft.CognitiveServices/accounts/read",
            "Microsoft.Storage/storageAccounts/blobServices/containers/read"
        ],
        "dataActions": [
            "Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read",
            "Microsoft.CognitiveServices/accounts/models/invoke/action"
        ]
    }
}
```

---

## 3. Branching Strategies for AI Projects

### Git-Flow Adapted for AI Development

#### Branch Structure

```
main (production-ready models)
├── develop (integration branch)
├── feature/
│   ├── feature/chat-model-v2
│   ├── feature/sentiment-analysis
│   └── feature/data-pipeline-optimization
├── experiment/
│   ├── experiment/temperature-tuning
│   ├── experiment/prompt-engineering
│   └── experiment/model-comparison
├── data/
│   ├── data/customer-data-v2
│   ├── data/training-set-update
│   └── data/quality-improvement
└── hotfix/
    ├── hotfix/model-response-fix
    └── hotfix/security-patch
```

#### Branching Rules for AI Projects

```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
import re

class BranchType(Enum):
    MAIN = "main"
    DEVELOP = "develop"
    FEATURE = "feature"
    EXPERIMENT = "experiment"
    DATA = "data"
    HOTFIX = "hotfix"
    RELEASE = "release"

@dataclass
class BranchingRule:
    branch_type: BranchType
    naming_pattern: str
    allowed_sources: List[BranchType]
    allowed_targets: List[BranchType]
    requires_review: bool
    min_reviewers: int
    requires_tests: bool

class AIBranchingStrategy:
    def __init__(self):
        self.rules = self._define_branching_rules()
    
    def _define_branching_rules(self) -> Dict[BranchType, BranchingRule]:
        """Define branching rules for AI projects"""
        return {
            BranchType.MAIN: BranchingRule(
                branch_type=BranchType.MAIN,
                naming_pattern="main",
                allowed_sources=[BranchType.RELEASE, BranchType.HOTFIX],
                allowed_targets=[],
                requires_review=True,
                min_reviewers=2,
                requires_tests=True
            ),
            BranchType.DEVELOP: BranchingRule(
                branch_type=BranchType.DEVELOP,
                naming_pattern="develop",
                allowed_sources=[BranchType.FEATURE, BranchType.EXPERIMENT, BranchType.DATA],
                allowed_targets=[BranchType.RELEASE],
                requires_review=True,
                min_reviewers=1,
                requires_tests=True
            ),
            BranchType.FEATURE: BranchingRule(
                branch_type=BranchType.FEATURE,
                naming_pattern="feature/[a-z0-9-]+",
                allowed_sources=[BranchType.DEVELOP],
                allowed_targets=[BranchType.DEVELOP],
                requires_review=True,
                min_reviewers=1,
                requires_tests=True
            ),
            BranchType.EXPERIMENT: BranchingRule(
                branch_type=BranchType.EXPERIMENT,
                naming_pattern="experiment/[a-z0-9-]+",
                allowed_sources=[BranchType.DEVELOP, BranchType.FEATURE],
                allowed_targets=[BranchType.DEVELOP],
                requires_review=False,
                min_reviewers=0,
                requires_tests=False
            ),
            BranchType.DATA: BranchingRule(
                branch_type=BranchType.DATA,
                naming_pattern="data/[a-z0-9-]+",
                allowed_sources=[BranchType.DEVELOP],
                allowed_targets=[BranchType.DEVELOP],
                requires_review=True,
                min_reviewers=1,
                requires_tests=True
            ),
            BranchType.HOTFIX: BranchingRule(
                branch_type=BranchType.HOTFIX,
                naming_pattern="hotfix/[a-z0-9-]+",
                allowed_sources=[BranchType.MAIN],
                allowed_targets=[BranchType.MAIN, BranchType.DEVELOP],
                requires_review=True,
                min_reviewers=2,
                requires_tests=True
            )
        }
    
    def validate_branch_name(self, branch_name: str) -> bool:
        """Validate branch name against naming conventions"""
        for branch_type, rule in self.rules.items():
            if re.match(rule.naming_pattern, branch_name):
                return True
        return False
    
    def can_merge(self, source_branch: str, target_branch: str) -> tuple[bool, str]:
        """Check if merge is allowed based on branching rules"""
        source_type = self._get_branch_type(source_branch)
        target_type = self._get_branch_type(target_branch)
        
        if not source_type or not target_type:
            return False, "Invalid branch type"
        
        target_rule = self.rules[target_type]
        
        if source_type not in target_rule.allowed_sources:
            return False, f"Cannot merge {source_type.value} into {target_type.value}"
        
        return True, "Merge allowed"
    
    def _get_branch_type(self, branch_name: str) -> Optional[BranchType]:
        """Determine branch type from branch name"""
        for branch_type, rule in self.rules.items():
            if re.match(rule.naming_pattern, branch_name):
                return branch_type
        return None

# GitHub/Azure DevOps Integration
class GitHubBranchProtection:
    def __init__(self, github_client, repository):
        self.github = github_client
        self.repo = repository
        self.strategy = AIBranchingStrategy()
    
    def setup_branch_protection(self):
        """Set up branch protection rules for AI project"""
        
        # Protect main branch
        self.github.repos.update_branch_protection(
            owner=self.repo.owner.login,
            repo=self.repo.name,
            branch="main",
            protection={
                "required_status_checks": {
                    "strict": True,
                    "contexts": ["ci/tests", "ci/model-validation", "ci/security-scan"]
                },
                "enforce_admins": True,
                "required_pull_request_reviews": {
                    "required_approving_review_count": 2,
                    "dismiss_stale_reviews": True,
                    "require_code_owner_reviews": True
                },
                "restrictions": {
                    "users": [],
                    "teams": ["ai-leads", "devops-team"]
                }
            }
        )
        
        # Protect develop branch
        self.github.repos.update_branch_protection(
            owner=self.repo.owner.login,
            repo=self.repo.name,
            branch="develop",
            protection={
                "required_status_checks": {
                    "strict": True,
                    "contexts": ["ci/tests", "ci/model-validation"]
                },
                "enforce_admins": False,
                "required_pull_request_reviews": {
                    "required_approving_review_count": 1,
                    "dismiss_stale_reviews": True,
                    "require_code_owner_reviews": False
                }
            }
        )
```

### AI-Specific Merge Strategies

#### Model Version Merging

```python
import json
from typing import Dict, List
from dataclasses import dataclass, asdict

@dataclass
class ModelConfig:
    name: str
    version: str
    parameters: Dict
    performance_metrics: Dict
    training_data_version: str

class ModelMergeStrategy:
    def __init__(self):
        self.conflict_resolvers = {
            "performance_metrics": self._resolve_performance_conflict,
            "parameters": self._resolve_parameter_conflict,
            "version": self._resolve_version_conflict
        }
    
    def merge_model_configs(self, base_config: ModelConfig, 
                           feature_config: ModelConfig) -> ModelConfig:
        """Merge model configurations from different branches"""
        merged_config = ModelConfig(
            name=feature_config.name,
            version=self._resolve_version_conflict(base_config.version, feature_config.version),
            parameters=self._resolve_parameter_conflict(base_config.parameters, feature_config.parameters),
            performance_metrics=self._resolve_performance_conflict(base_config.performance_metrics, feature_config.performance_metrics),
            training_data_version=feature_config.training_data_version
        )
        
        return merged_config
    
    def _resolve_version_conflict(self, base_version: str, feature_version: str) -> str:
        """Resolve version conflicts using semantic versioning"""
        base_parts = list(map(int, base_version.split('.')))
        feature_parts = list(map(int, feature_version.split('.')))
        
        # Take the higher version
        if feature_parts > base_parts:
            return feature_version
        else:
            # Increment patch version
            base_parts[2] += 1
            return '.'.join(map(str, base_parts))
    
    def _resolve_parameter_conflict(self, base_params: Dict, feature_params: Dict) -> Dict:
        """Resolve parameter conflicts by taking feature branch values"""
        merged_params = base_params.copy()
        merged_params.update(feature_params)
        return merged_params
    
    def _resolve_performance_conflict(self, base_metrics: Dict, feature_metrics: Dict) -> Dict:
        """Resolve performance metrics by taking better values"""
        merged_metrics = {}
        
        all_metrics = set(base_metrics.keys()) | set(feature_metrics.keys())
        
        for metric in all_metrics:
            base_value = base_metrics.get(metric, 0)
            feature_value = feature_metrics.get(metric, 0)
            
            # For accuracy-like metrics, take higher value
            if metric in ["accuracy", "precision", "recall", "f1_score"]:
                merged_metrics[metric] = max(base_value, feature_value)
            # For error-like metrics, take lower value
            elif metric in ["error_rate", "latency", "cost"]:
                merged_metrics[metric] = min(base_value, feature_value) if min(base_value, feature_value) > 0 else max(base_value, feature_value)
            else:
                # Default to feature branch value
                merged_metrics[metric] = feature_value
        
        return merged_metrics

# Usage in pre-merge hook
def pre_merge_model_validation(source_branch: str, target_branch: str) -> bool:
    """Validate model changes before merge"""
    source_config = load_model_config(source_branch)
    target_config = load_model_config(target_branch)
    
    merger = ModelMergeStrategy()
    merged_config = merger.merge_model_configs(target_config, source_config)
    
    # Validate merged configuration
    if not validate_model_config(merged_config):
        return False
    
    # Run performance regression test
    if merged_config.performance_metrics["accuracy"] < target_config.performance_metrics["accuracy"] * 0.95:
        print("Performance regression detected")
        return False
    
    return True
```

---

## 4. Code Sharing and Collaboration Patterns

### Shared Libraries and Components

#### AI Component Library Structure

```python
# ai_components/
# ├── __init__.py
# ├── models/
# │   ├── __init__.py
# │   ├── base_model.py
# │   ├── chat_model.py
# │   └── embedding_model.py
# ├── data/
# │   ├── __init__.py
# │   ├── preprocessors.py
# │   └── validators.py
# ├── utils/
# │   ├── __init__.py
# │   ├── config.py
# │   └── logging.py
# └── deployment/
#     ├── __init__.py
#     └── azure_deployer.py

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from azure.ai.inference import ChatCompletionsClient

class BaseAIModel(ABC):
    """Base class for all AI models in the organization"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = None
        self._initialize_client()
    
    @abstractmethod
    def _initialize_client(self):
        """Initialize the AI client"""
        pass
    
    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """Process input and return output"""
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "name": self.__class__.__name__,
            "version": getattr(self, "VERSION", "unknown"),
            "config": self.config
        }

class StandardChatModel(BaseAIModel):
    """Standard chat model implementation"""
    
    VERSION = "1.0.0"
    
    def _initialize_client(self):
        """Initialize Azure AI client"""
        from azure.identity import DefaultAzureCredential
        
        self.client = ChatCompletionsClient(
            endpoint=self.config["endpoint"],
            credential=DefaultAzureCredential()
        )
    
    async def process(self, messages: List[Dict[str, str]]) -> str:
        """Process chat messages"""
        response = await self.client.complete({
            "model": self.config.get("model", "gpt-4"),
            "messages": messages,
            "max_tokens": self.config.get("max_tokens", 1000),
            "temperature": self.config.get("temperature", 0.7)
        })
        
        return response.choices[0].message.content

# Shared configuration management
class ConfigManager:
    """Centralized configuration management for AI projects"""
    
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.config_cache = {}
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Get configuration for specific model"""
        cache_key = f"{model_name}:{self.environment}"
        
        if cache_key not in self.config_cache:
            self.config_cache[cache_key] = self._load_model_config(model_name)
        
        return self.config_cache[cache_key]
    
    def _load_model_config(self, model_name: str) -> Dict[str, Any]:
        """Load model configuration from Azure Key Vault or environment"""
        # In practice, this would load from Azure Key Vault or config files
        default_configs = {
            "chat_model": {
                "endpoint": "https://your-ai-foundry.cognitiveservices.azure.com",
                "model": "gpt-4",
                "max_tokens": 1000,
                "temperature": 0.7
            },
            "embedding_model": {
                "endpoint": "https://your-ai-foundry.cognitiveservices.azure.com",
                "model": "text-embedding-ada-002",
                "dimensions": 1536
            }
        }
        
        return default_configs.get(model_name, {})

# Usage across projects
def create_chat_model(environment: str = "development") -> StandardChatModel:
    """Factory function to create standardized chat model"""
    config_manager = ConfigManager(environment)
    config = config_manager.get_model_config("chat_model")
    return StandardChatModel(config)
```

### Package Management and Distribution

#### Internal Package Registry

```yaml
# azure-pipelines.yml for package publishing
trigger:
  branches:
    include:
    - main
  paths:
    include:
    - ai_components/*

variables:
  packageVersion: '1.0.$(Build.BuildId)'

stages:
- stage: Build
  jobs:
  - job: BuildPackage
    pool:
      vmImage: 'ubuntu-latest'
    
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.11'
    
    - script: |
        python -m pip install --upgrade pip
        pip install build twine
      displayName: 'Install build tools'
    
    - script: |
        python -m build
      displayName: 'Build package'
    
    - task: TwineAuthenticate@1
      inputs:
        artifactFeed: 'ai-components'
    
    - script: |
        python -m twine upload --repository ai-components dist/*
      displayName: 'Publish package'

- stage: Test
  dependsOn: Build
  jobs:
  - job: TestPackage
    pool:
      vmImage: 'ubuntu-latest'
    
    steps:
    - script: |
        pip install ai-components==$(packageVersion)
        python -m pytest tests/
      displayName: 'Test published package'
```

#### Dependency Management

```toml
# pyproject.toml for ai_components package
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "ai-components"
description = "Shared AI components for organization"
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "azure-ai-inference>=1.0.0b2",
    "azure-identity>=1.15.0",
    "azure-keyvault-secrets>=4.7.0",
    "pydantic>=2.0.0",
    "typing-extensions>=4.0.0"
]
dynamic = ["version"]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "mypy>=1.0.0"
]

[tool.setuptools_scm]
write_to = "ai_components/_version.py"

[tool.mypy]
python_version = "3.8"
strict = true
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
asyncio_mode = "auto"
```

---

## 5. Cross-Functional Coordination

### Coordination Frameworks

#### Scrum of Scrums for AI Teams

```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum

class BlockerType(Enum):
    TECHNICAL = "technical"
    DATA = "data"
    RESOURCE = "resource"
    DEPENDENCY = "dependency"
    COMPLIANCE = "compliance"

@dataclass
class TeamUpdate:
    team_name: str
    completed_work: List[str]
    planned_work: List[str]
    blockers: List[Dict[str, str]]
    dependencies_needed: List[str]
    dependencies_provided: List[str]
    
class ScrumOfScrums:
    def __init__(self):
        self.teams = {}
        self.cross_team_dependencies = {}
        self.meeting_history = []
    
    def register_team(self, team_name: str, representative: str):
        """Register a team in the Scrum of Scrums"""
        self.teams[team_name] = {
            "representative": representative,
            "last_update": None
        }
    
    def submit_update(self, update: TeamUpdate):
        """Submit team update for Scrum of Scrums meeting"""
        self.teams[update.team_name]["last_update"] = update
        self._update_dependencies(update)
    
    def _update_dependencies(self, update: TeamUpdate):
        """Track cross-team dependencies"""
        team_name = update.team_name
        
        # Clear existing dependencies for this team
        if team_name in self.cross_team_dependencies:
            del self.cross_team_dependencies[team_name]
        
        # Add new dependencies
        if update.dependencies_needed:
            self.cross_team_dependencies[team_name] = {
                "needs": update.dependencies_needed,
                "provides": update.dependencies_provided
            }
    
    def generate_coordination_report(self) -> Dict[str, Any]:
        """Generate coordination report for leadership"""
        report = {
            "teams_count": len(self.teams),
            "active_blockers": [],
            "dependency_conflicts": [],
            "recommendations": []
        }
        
        # Collect all blockers
        for team_name, team_info in self.teams.items():
            if team_info["last_update"] and team_info["last_update"].blockers:
                for blocker in team_info["last_update"].blockers:
                    report["active_blockers"].append({
                        "team": team_name,
                        "blocker": blocker
                    })
        
        # Identify dependency conflicts
        all_needs = {}
        all_provides = {}
        
        for team_name, deps in self.cross_team_dependencies.items():
            for need in deps["needs"]:
                if need not in all_needs:
                    all_needs[need] = []
                all_needs[need].append(team_name)
            
            for provide in deps["provides"]:
                if provide not in all_provides:
                    all_provides[provide] = []
                all_provides[provide].append(team_name)
        
        # Find unmet dependencies
        for need, teams_needing in all_needs.items():
            if need not in all_provides:
                report["dependency_conflicts"].append({
                    "dependency": need,
                    "teams_needing": teams_needing,
                    "providers": []
                })
        
        return report

# AI-specific coordination patterns
class AIProjectCoordinator:
    def __init__(self):
        self.data_dependencies = {}
        self.model_dependencies = {}
        self.infrastructure_dependencies = {}
    
    def track_data_pipeline(self, pipeline_name: str, stages: List[str], 
                           owners: Dict[str, str]):
        """Track data pipeline across teams"""
        self.data_dependencies[pipeline_name] = {
            "stages": stages,
            "owners": owners,
            "status": {stage: "pending" for stage in stages}
        }
    
    def update_pipeline_status(self, pipeline_name: str, stage: str, status: str):
        """Update status of pipeline stage"""
        if pipeline_name in self.data_dependencies:
            self.data_dependencies[pipeline_name]["status"][stage] = status
    
    def get_pipeline_blockers(self) -> List[Dict[str, str]]:
        """Get all pipeline blockers"""
        blockers = []
        
        for pipeline_name, pipeline_info in self.data_dependencies.items():
            for stage, status in pipeline_info["status"].items():
                if status == "blocked":
                    blockers.append({
                        "pipeline": pipeline_name,
                        "stage": stage,
                        "owner": pipeline_info["owners"].get(stage, "unknown")
                    })
        
        return blockers
```

### Communication Patterns

#### Asynchronous Communication Framework

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from datetime import datetime
import json
import asyncio

@dataclass
class Message:
    id: str
    sender: str
    channel: str
    content: str
    message_type: str
    timestamp: datetime
    metadata: Dict[str, Any] = None

class CommunicationChannel:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.subscribers = set()
        self.message_handlers = {}
        self.message_history = []
    
    def subscribe(self, user_id: str, handler: Optional[Callable] = None):
        """Subscribe to channel updates"""
        self.subscribers.add(user_id)
        if handler:
            self.message_handlers[user_id] = handler
    
    def unsubscribe(self, user_id: str):
        """Unsubscribe from channel"""
        self.subscribers.discard(user_id)
        if user_id in self.message_handlers:
            del self.message_handlers[user_id]
    
    async def post_message(self, message: Message):
        """Post message to channel"""
        self.message_history.append(message)
        
        # Notify subscribers
        for subscriber in self.subscribers:
            if subscriber in self.message_handlers:
                try:
                    await self.message_handlers[subscriber](message)
                except Exception as e:
                    print(f"Error notifying {subscriber}: {e}")

class AITeamCommunication:
    def __init__(self):
        self.channels = {}
        self._setup_default_channels()
    
    def _setup_default_channels(self):
        """Set up default communication channels for AI teams"""
        channels_config = [
            ("general", "General team communication"),
            ("data-updates", "Data pipeline and quality updates"),
            ("model-releases", "Model deployment and release notifications"),
            ("incidents", "Production incidents and issues"),
            ("experiments", "Experiment results and findings"),
            ("compliance", "Compliance and ethics discussions")
        ]
        
        for name, description in channels_config:
            self.channels[name] = CommunicationChannel(name, description)
    
    def create_channel(self, name: str, description: str) -> CommunicationChannel:
        """Create a new communication channel"""
        if name in self.channels:
            raise ValueError(f"Channel {name} already exists")
        
        self.channels[name] = CommunicationChannel(name, description)
        return self.channels[name]
    
    def get_channel(self, name: str) -> Optional[CommunicationChannel]:
        """Get communication channel by name"""
        return self.channels.get(name)
    
    async def broadcast_model_release(self, model_name: str, version: str, 
                                    performance_metrics: Dict[str, float]):
        """Broadcast model release to relevant channels"""
        message = Message(
            id=f"model-release-{model_name}-{version}",
            sender="system",
            channel="model-releases",
            content=f"New model release: {model_name} v{version}",
            message_type="model_release",
            timestamp=datetime.utcnow(),
            metadata={
                "model_name": model_name,
                "version": version,
                "performance_metrics": performance_metrics
            }
        )
        
        model_channel = self.get_channel("model-releases")
        if model_channel:
            await model_channel.post_message(message)
    
    async def broadcast_data_quality_alert(self, pipeline_name: str, 
                                         issue_description: str):
        """Broadcast data quality alert"""
        message = Message(
            id=f"data-alert-{pipeline_name}-{int(datetime.utcnow().timestamp())}",
            sender="data-quality-system",
            channel="data-updates",
            content=f"Data quality issue in {pipeline_name}: {issue_description}",
            message_type="data_quality_alert",
            timestamp=datetime.utcnow(),
            metadata={
                "pipeline_name": pipeline_name,
                "severity": "high",
                "requires_action": True
            }
        )
        
        data_channel = self.get_channel("data-updates")
        if data_channel:
            await data_channel.post_message(message)

# Integration with external systems
class SlackIntegration:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def send_notification(self, message: Message):
        """Send notification to Slack"""
        slack_message = {
            "text": f"*{message.channel.upper()}*: {message.content}",
            "username": "AI Team Bot",
            "icon_emoji": ":robot_face:"
        }
        
        if message.message_type == "model_release":
            slack_message["attachments"] = [{
                "color": "good",
                "fields": [
                    {
                        "title": "Model",
                        "value": message.metadata["model_name"],
                        "short": True
                    },
                    {
                        "title": "Version",
                        "value": message.metadata["version"],
                        "short": True
                    }
                ]
            }]
        
        # Send to Slack (would use actual HTTP client in practice)
        print(f"Sending to Slack: {json.dumps(slack_message, indent=2)}")

# Usage
async def setup_team_communication():
    """Set up team communication system"""
    comm_system = AITeamCommunication()
    slack_integration = SlackIntegration("https://hooks.slack.com/...")
    
    # Subscribe key team members to channels
    model_channel = comm_system.get_channel("model-releases")
    if model_channel:
        model_channel.subscribe("ai-lead@company.com", slack_integration.send_notification)
        model_channel.subscribe("devops-lead@company.com", slack_integration.send_notification)
    
    # Simulate model release notification
    await comm_system.broadcast_model_release(
        "chat-assistant", 
        "2.1.0", 
        {"accuracy": 0.87, "response_time": 1.2}
    )
    
    return comm_system
```

---

## Summary

In this lesson, we've covered:

✅ **Team Structure**: Organizing cross-functional AI teams with clear roles and responsibilities
✅ **Role-Based Access Control**: Implementing proper permissions and security for AI development
✅ **Branching Strategies**: Adapting Git workflows for AI projects with experiment and data branches
✅ **Code Sharing**: Creating reusable components and managing internal packages
✅ **Cross-Functional Coordination**: Establishing communication patterns and dependency management
✅ **Collaboration Tools**: Setting up effective communication channels and notification systems

## Next Steps

In the next lesson, we'll explore **Version Control and CI/CD for AI Projects**, where you'll learn how to implement automated testing, continuous integration, and deployment pipelines specifically designed for AI applications.

## Additional Resources

- [Azure DevOps Team Management](https://docs.microsoft.com/en-us/azure/devops/organizations/security/)
- [Git Branching Strategies](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [Azure RBAC Documentation](https://docs.microsoft.com/en-us/azure/role-based-access-control/)
- [Cross-functional Teams in Agile](https://www.scrum.org/resources/blog/cross-functional-teams)

---

*This lesson provides the collaboration foundation needed to effectively manage AI development teams and coordinate complex AI projects.* 