# Lesson 5: Environment Management and Configuration

## Learning Objectives

By the end of this lesson, you will be able to:
- Manage multiple deployment environments for AI applications
- Implement configuration management strategies for AI projects
- Use Infrastructure as Code (IaC) for AI infrastructure
- Handle environment-specific model configurations
- Manage secrets and sensitive data across environments
- Implement configuration drift detection and remediation

## Overview

AI applications require sophisticated environment management due to the complexity of model deployments, data dependencies, and varying performance requirements across development, staging, and production environments. This lesson covers comprehensive strategies for managing environments and configurations in Azure AI Foundry projects.

---

## 1. Multi-Environment Architecture

### Environment Strategy for AI Projects

#### Environment Types

```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum

class EnvironmentType(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"
    EXPERIMENT = "experiment"

@dataclass
class EnvironmentConfig:
    name: str
    environment_type: EnvironmentType
    azure_subscription_id: str
    resource_group: str
    ai_foundry_endpoint: str
    deployment_configs: Dict[str, Any]
    scaling_config: Dict[str, Any]
    monitoring_config: Dict[str, Any]
    security_config: Dict[str, Any]

class EnvironmentManager:
    def __init__(self):
        self.environments = {}
        self._setup_environments()
    
    def _setup_environments(self):
        """Setup standard environments for AI projects"""
        
        # Development Environment
        self.environments["dev"] = EnvironmentConfig(
            name="development",
            environment_type=EnvironmentType.DEVELOPMENT,
            azure_subscription_id="dev-subscription-id",
            resource_group="ai-foundry-dev-rg",
            ai_foundry_endpoint="https://dev-ai-foundry.cognitiveservices.azure.com",
            deployment_configs={
                "model_replicas": 1,
                "max_tokens_per_minute": 10000,
                "enable_logging": True,
                "enable_telemetry": True
            },
            scaling_config={
                "auto_scaling": False,
                "min_replicas": 1,
                "max_replicas": 2
            },
            monitoring_config={
                "detailed_metrics": True,
                "log_level": "DEBUG",
                "enable_application_insights": True
            },
            security_config={
                "enable_private_endpoint": False,
                "allowed_origins": ["*"],
                "authentication_required": False
            }
        )
        
        # Staging Environment
        self.environments["staging"] = EnvironmentConfig(
            name="staging",
            environment_type=EnvironmentType.STAGING,
            azure_subscription_id="staging-subscription-id",
            resource_group="ai-foundry-staging-rg",
            ai_foundry_endpoint="https://staging-ai-foundry.cognitiveservices.azure.com",
            deployment_configs={
                "model_replicas": 2,
                "max_tokens_per_minute": 50000,
                "enable_logging": True,
                "enable_telemetry": True
            },
            scaling_config={
                "auto_scaling": True,
                "min_replicas": 2,
                "max_replicas": 5
            },
            monitoring_config={
                "detailed_metrics": True,
                "log_level": "INFO",
                "enable_application_insights": True
            },
            security_config={
                "enable_private_endpoint": True,
                "allowed_origins": ["https://staging.company.com"],
                "authentication_required": True
            }
        )
        
        # Production Environment
        self.environments["prod"] = EnvironmentConfig(
            name="production",
            environment_type=EnvironmentType.PRODUCTION,
            azure_subscription_id="prod-subscription-id",
            resource_group="ai-foundry-prod-rg",
            ai_foundry_endpoint="https://prod-ai-foundry.cognitiveservices.azure.com",
            deployment_configs={
                "model_replicas": 5,
                "max_tokens_per_minute": 200000,
                "enable_logging": True,
                "enable_telemetry": True
            },
            scaling_config={
                "auto_scaling": True,
                "min_replicas": 5,
                "max_replicas": 20
            },
            monitoring_config={
                "detailed_metrics": True,
                "log_level": "WARN",
                "enable_application_insights": True
            },
            security_config={
                "enable_private_endpoint": True,
                "allowed_origins": ["https://company.com"],
                "authentication_required": True
            }
        )
    
    def get_environment(self, environment_name: str) -> Optional[EnvironmentConfig]:
        """Get environment configuration"""
        return self.environments.get(environment_name)
    
    def validate_environment(self, environment_name: str) -> Dict[str, Any]:
        """Validate environment configuration"""
        config = self.get_environment(environment_name)
        if not config:
            return {"valid": False, "errors": ["Environment not found"]}
        
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Validate Azure resources
        if not self._validate_azure_resources(config):
            validation_results["errors"].append("Azure resources validation failed")
            validation_results["valid"] = False
        
        # Validate model deployments
        if not self._validate_model_deployments(config):
            validation_results["errors"].append("Model deployment validation failed")
            validation_results["valid"] = False
        
        # Check security configuration
        if not self._validate_security_config(config):
            validation_results["warnings"].append("Security configuration needs review")
        
        return validation_results
    
    def _validate_azure_resources(self, config: EnvironmentConfig) -> bool:
        """Validate Azure resources exist and are accessible"""
        # In practice, this would use Azure SDK to check resources
        return True
    
    def _validate_model_deployments(self, config: EnvironmentConfig) -> bool:
        """Validate model deployments are healthy"""
        # In practice, this would check model endpoints
        return True
    
    def _validate_security_config(self, config: EnvironmentConfig) -> bool:
        """Validate security configuration"""
        if config.environment_type == EnvironmentType.PRODUCTION:
            return (config.security_config["enable_private_endpoint"] and 
                   config.security_config["authentication_required"])
        return True
```

### Environment Promotion Pipeline

```python
import json
from typing import Dict, List, Any
from dataclasses import asdict
import asyncio

class EnvironmentPromotion:
    def __init__(self, environment_manager: EnvironmentManager):
        self.env_manager = environment_manager
        self.promotion_rules = self._define_promotion_rules()
    
    def _define_promotion_rules(self) -> Dict[str, List[str]]:
        """Define allowed promotion paths between environments"""
        return {
            "dev": ["testing", "staging"],
            "testing": ["staging"],
            "staging": ["prod"],
            "experiment": ["dev", "testing"]
        }
    
    async def promote_deployment(self, source_env: str, target_env: str, 
                               deployment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Promote deployment from source to target environment"""
        
        # Validate promotion path
        if not self._validate_promotion_path(source_env, target_env):
            return {
                "success": False,
                "error": f"Invalid promotion path: {source_env} -> {target_env}"
            }
        
        # Get environment configurations
        source_config = self.env_manager.get_environment(source_env)
        target_config = self.env_manager.get_environment(target_env)
        
        if not source_config or not target_config:
            return {
                "success": False,
                "error": "Environment configuration not found"
            }
        
        try:
            # Pre-promotion validation
            validation_result = await self._pre_promotion_validation(
                source_config, target_config, deployment_config
            )
            
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": "Pre-promotion validation failed",
                    "details": validation_result["errors"]
                }
            
            # Perform promotion
            promotion_result = await self._execute_promotion(
                source_config, target_config, deployment_config
            )
            
            # Post-promotion validation
            if promotion_result["success"]:
                post_validation = await self._post_promotion_validation(
                    target_config, deployment_config
                )
                
                if not post_validation["valid"]:
                    # Rollback on validation failure
                    await self._rollback_promotion(target_config, deployment_config)
                    return {
                        "success": False,
                        "error": "Post-promotion validation failed",
                        "details": post_validation["errors"]
                    }
            
            return promotion_result
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Promotion failed: {str(e)}"
            }
    
    def _validate_promotion_path(self, source_env: str, target_env: str) -> bool:
        """Validate that promotion path is allowed"""
        allowed_targets = self.promotion_rules.get(source_env, [])
        return target_env in allowed_targets
    
    async def _pre_promotion_validation(self, source_config: EnvironmentConfig,
                                      target_config: EnvironmentConfig,
                                      deployment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate before promotion"""
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check resource capacity in target environment
        if not await self._check_resource_capacity(target_config, deployment_config):
            validation_results["errors"].append("Insufficient resource capacity in target environment")
            validation_results["valid"] = False
        
        # Validate compatibility
        if not await self._check_compatibility(source_config, target_config):
            validation_results["errors"].append("Configuration compatibility issues detected")
            validation_results["valid"] = False
        
        return validation_results
    
    async def _execute_promotion(self, source_config: EnvironmentConfig,
                               target_config: EnvironmentConfig,
                               deployment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the actual promotion"""
        try:
            # Deploy to target environment
            deployment_result = await self._deploy_to_environment(
                target_config, deployment_config
            )
            
            if deployment_result["success"]:
                # Update routing/traffic if needed
                await self._update_traffic_routing(target_config, deployment_config)
                
                return {
                    "success": True,
                    "deployment_id": deployment_result["deployment_id"],
                    "endpoint": deployment_result["endpoint"]
                }
            else:
                return deployment_result
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Deployment execution failed: {str(e)}"
            }
    
    async def _post_promotion_validation(self, target_config: EnvironmentConfig,
                                       deployment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate after promotion"""
        validation_results = {
            "valid": True,
            "errors": []
        }
        
        # Health check
        if not await self._health_check(target_config, deployment_config):
            validation_results["errors"].append("Health check failed")
            validation_results["valid"] = False
        
        # Performance validation
        if not await self._performance_validation(target_config, deployment_config):
            validation_results["errors"].append("Performance validation failed")
            validation_results["valid"] = False
        
        return validation_results
    
    async def _check_resource_capacity(self, config: EnvironmentConfig,
                                     deployment_config: Dict[str, Any]) -> bool:
        """Check if target environment has sufficient capacity"""
        # In practice, this would check Azure resource quotas and current usage
        return True
    
    async def _check_compatibility(self, source_config: EnvironmentConfig,
                                 target_config: EnvironmentConfig) -> bool:
        """Check compatibility between environments"""
        # Check API versions, dependencies, etc.
        return True
    
    async def _deploy_to_environment(self, config: EnvironmentConfig,
                                   deployment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy to specific environment"""
        # Implementation would use Azure AI Foundry deployment APIs
        return {
            "success": True,
            "deployment_id": f"deployment-{config.name}-{deployment_config['version']}",
            "endpoint": config.ai_foundry_endpoint
        }
    
    async def _update_traffic_routing(self, config: EnvironmentConfig,
                                    deployment_config: Dict[str, Any]):
        """Update traffic routing to new deployment"""
        # Implementation would update load balancer or traffic manager
        pass
    
    async def _health_check(self, config: EnvironmentConfig,
                          deployment_config: Dict[str, Any]) -> bool:
        """Perform health check on deployed service"""
        # Implementation would call health check endpoints
        return True
    
    async def _performance_validation(self, config: EnvironmentConfig,
                                    deployment_config: Dict[str, Any]) -> bool:
        """Validate performance meets requirements"""
        # Implementation would run performance tests
        return True
    
    async def _rollback_promotion(self, config: EnvironmentConfig,
                                deployment_config: Dict[str, Any]):
        """Rollback failed promotion"""
        # Implementation would restore previous deployment
        pass
```

---

## 2. Configuration Management

### Hierarchical Configuration System

```python
import os
import yaml
import json
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ConfigSource:
    name: str
    priority: int
    source_type: str  # file, environment, key_vault, etc.
    source_path: str

class ConfigurationManager:
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.config_sources = []
        self.cached_config = {}
        self._setup_config_sources()
    
    def _setup_config_sources(self):
        """Setup configuration sources in priority order (highest first)"""
        # Priority 1: Environment variables (highest)
        self.config_sources.append(ConfigSource(
            name="environment_variables",
            priority=1,
            source_type="environment",
            source_path=""
        ))
        
        # Priority 2: Environment-specific config files
        self.config_sources.append(ConfigSource(
            name=f"config_{self.environment}",
            priority=2,
            source_type="file",
            source_path=f"config/config.{self.environment}.yaml"
        ))
        
        # Priority 3: Base config file
        self.config_sources.append(ConfigSource(
            name="base_config",
            priority=3,
            source_type="file",
            source_path="config/config.yaml"
        ))
        
        # Priority 4: Default values (lowest)
        self.config_sources.append(ConfigSource(
            name="defaults",
            priority=4,
            source_type="defaults",
            source_path=""
        ))
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value with hierarchical resolution"""
        if key in self.cached_config:
            return self.cached_config[key]
        
        # Try each source in priority order
        for source in sorted(self.config_sources, key=lambda x: x.priority):
            value = self._get_value_from_source(source, key)
            if value is not None:
                self.cached_config[key] = value
                return value
        
        self.cached_config[key] = default
        return default
    
    def _get_value_from_source(self, source: ConfigSource, key: str) -> Any:
        """Get value from specific configuration source"""
        if source.source_type == "environment":
            return self._get_from_environment(key)
        elif source.source_type == "file":
            return self._get_from_file(source.source_path, key)
        elif source.source_type == "defaults":
            return self._get_default_value(key)
        
        return None
    
    def _get_from_environment(self, key: str) -> Optional[str]:
        """Get value from environment variables"""
        # Convert dot notation to environment variable format
        env_key = key.upper().replace(".", "_")
        return os.getenv(env_key)
    
    def _get_from_file(self, file_path: str, key: str) -> Any:
        """Get value from configuration file"""
        try:
            config_file = Path(file_path)
            if not config_file.exists():
                return None
            
            with open(config_file, 'r') as f:
                if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                    config_data = yaml.safe_load(f)
                else:
                    config_data = json.load(f)
            
            # Navigate nested keys (e.g., "azure.ai_foundry.endpoint")
            keys = key.split('.')
            current_data = config_data
            
            for k in keys:
                if isinstance(current_data, dict) and k in current_data:
                    current_data = current_data[k]
                else:
                    return None
            
            return current_data
        
        except Exception:
            return None
    
    def _get_default_value(self, key: str) -> Any:
        """Get default value for configuration key"""
        defaults = {
            "azure.ai_foundry.timeout": 30,
            "azure.ai_foundry.max_retries": 3,
            "azure.ai_foundry.temperature": 0.7,
            "azure.ai_foundry.max_tokens": 1000,
            "logging.level": "INFO",
            "monitoring.enabled": True,
            "security.authentication_required": True
        }
        
        return defaults.get(key)
    
    def refresh_cache(self):
        """Refresh configuration cache"""
        self.cached_config.clear()
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration as a dictionary"""
        all_config = {}
        
        # Load all configuration files
        for source in sorted(self.config_sources, key=lambda x: x.priority, reverse=True):
            if source.source_type == "file":
                file_config = self._load_file_config(source.source_path)
                all_config.update(file_config)
        
        # Override with environment variables
        env_config = self._load_environment_config()
        all_config.update(env_config)
        
        return all_config
    
    def _load_file_config(self, file_path: str) -> Dict[str, Any]:
        """Load entire configuration file"""
        try:
            config_file = Path(file_path)
            if not config_file.exists():
                return {}
            
            with open(config_file, 'r') as f:
                if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                    return yaml.safe_load(f) or {}
                else:
                    return json.load(f) or {}
        
        except Exception:
            return {}
    
    def _load_environment_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        env_config = {}
        prefix = "AI_FOUNDRY_"
        
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower().replace("_", ".")
                env_config[config_key] = value
        
        return env_config

# Model-specific configuration
class ModelConfigurationManager(ConfigurationManager):
    def __init__(self, environment: str, model_name: str):
        super().__init__(environment)
        self.model_name = model_name
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get complete model configuration"""
        base_config = {
            "name": self.model_name,
            "endpoint": self.get_config("azure.ai_foundry.endpoint"),
            "deployment_name": self.get_config(f"models.{self.model_name}.deployment_name", self.model_name),
            "temperature": self.get_config(f"models.{self.model_name}.temperature", 0.7),
            "max_tokens": self.get_config(f"models.{self.model_name}.max_tokens", 1000),
            "timeout": self.get_config("azure.ai_foundry.timeout", 30),
            "max_retries": self.get_config("azure.ai_foundry.max_retries", 3)
        }
        
        # Add environment-specific overrides
        env_overrides = self.get_config(f"environments.{self.environment}.models.{self.model_name}", {})
        base_config.update(env_overrides)
        
        return base_config
    
    def validate_model_config(self) -> Dict[str, Any]:
        """Validate model configuration"""
        config = self.get_model_config()
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Required fields
        required_fields = ["endpoint", "deployment_name"]
        for field in required_fields:
            if not config.get(field):
                validation_result["errors"].append(f"Missing required field: {field}")
                validation_result["valid"] = False
        
        # Value validation
        if config.get("temperature", 0) < 0 or config.get("temperature", 0) > 2:
            validation_result["warnings"].append("Temperature should be between 0 and 2")
        
        if config.get("max_tokens", 0) <= 0:
            validation_result["errors"].append("max_tokens must be positive")
            validation_result["valid"] = False
        
        return validation_result

# Usage example
def create_model_client(environment: str, model_name: str):
    """Factory function to create model client with proper configuration"""
    config_manager = ModelConfigurationManager(environment, model_name)
    model_config = config_manager.get_model_config()
    
    # Validate configuration
    validation = config_manager.validate_model_config()
    if not validation["valid"]:
        raise ValueError(f"Invalid model configuration: {validation['errors']}")
    
    # Create client with configuration
    from azure.ai.inference import ChatCompletionsClient
    from azure.identity import DefaultAzureCredential
    
    return ChatCompletionsClient(
        endpoint=model_config["endpoint"],
        credential=DefaultAzureCredential()
    ), model_config
```

### Configuration Files Structure

```yaml
# config/config.yaml (base configuration)
azure:
  ai_foundry:
    endpoint: "https://base-ai-foundry.cognitiveservices.azure.com"
    api_version: "2024-02-15-preview"
    timeout: 30
    max_retries: 3

models:
  chat_assistant:
    deployment_name: "gpt-4"
    temperature: 0.7
    max_tokens: 1000
  
  summarizer:
    deployment_name: "gpt-3.5-turbo"
    temperature: 0.3
    max_tokens: 500

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

monitoring:
  enabled: true
  application_insights:
    enabled: true
  
security:
  authentication_required: true
  cors:
    enabled: true
    allowed_origins: []
```

```yaml
# config/config.production.yaml (production overrides)
azure:
  ai_foundry:
    endpoint: "https://prod-ai-foundry.cognitiveservices.azure.com"

models:
  chat_assistant:
    temperature: 0.5  # More conservative for production
    max_tokens: 800
  
environments:
  production:
    scaling:
      auto_scaling: true
      min_replicas: 5
      max_replicas: 20
    
    monitoring:
      detailed_metrics: true
      alert_thresholds:
        response_time_ms: 5000
        error_rate_percent: 1.0
    
    security:
      private_endpoint: true
      allowed_origins:
        - "https://company.com"
        - "https://app.company.com"

logging:
  level: "WARN"  # Reduced logging in production

security:
  cors:
    allowed_origins:
      - "https://company.com"
```

---

## 3. Infrastructure as Code (IaC)

### Terraform for Azure AI Foundry

```hcl
# terraform/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
  
  backend "azurerm" {
    # Backend configuration will be provided via environment variables
  }
}

provider "azurerm" {
  features {}
}

# Data sources
data "azurerm_client_config" "current" {}

# Variables
variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "location" {
  description = "Azure location"
  type        = string
  default     = "East US 2"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "ai-foundry-project"
}

# Local values
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
  
  resource_prefix = "${var.project_name}-${var.environment}"
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${local.resource_prefix}-rg"
  location = var.location
  tags     = local.common_tags
}

# Cognitive Services Account (AI Foundry)
resource "azurerm_cognitive_account" "ai_foundry" {
  name                = "${local.resource_prefix}-ai-foundry"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "OpenAI"
  sku_name           = var.environment == "prod" ? "S0" : "S0"
  
  tags = local.common_tags
}

# Key Vault for secrets
resource "azurerm_key_vault" "main" {
  name                = "${local.resource_prefix}-kv"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name           = "standard"
  
  purge_protection_enabled = var.environment == "prod"
  
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id
    
    secret_permissions = [
      "Get", "List", "Set", "Delete", "Purge"
    ]
  }
  
  tags = local.common_tags
}

# Store AI Foundry key in Key Vault
resource "azurerm_key_vault_secret" "ai_foundry_key" {
  name         = "ai-foundry-api-key"
  value        = azurerm_cognitive_account.ai_foundry.primary_access_key
  key_vault_id = azurerm_key_vault.main.id
  
  depends_on = [azurerm_key_vault.main]
}

# Application Insights for monitoring
resource "azurerm_application_insights" "main" {
  name                = "${local.resource_prefix}-ai"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"
  
  tags = local.common_tags
}

# Storage Account for data and models
resource "azurerm_storage_account" "main" {
  name                     = replace("${local.resource_prefix}storage", "-", "")
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = var.environment == "prod" ? "GRS" : "LRS"
  
  blob_properties {
    versioning_enabled = true
    delete_retention_policy {
      days = var.environment == "prod" ? 30 : 7
    }
  }
  
  tags = local.common_tags
}

# Storage containers
resource "azurerm_storage_container" "models" {
  name                  = "models"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "data" {
  name                  = "data"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

# Outputs
output "ai_foundry_endpoint" {
  value = azurerm_cognitive_account.ai_foundry.endpoint
}

output "key_vault_uri" {
  value = azurerm_key_vault.main.vault_uri
}

output "application_insights_key" {
  value = azurerm_application_insights.main.instrumentation_key
  sensitive = true
}

output "storage_account_name" {
  value = azurerm_storage_account.main.name
}
```

```hcl
# terraform/variables.tf
variable "model_deployments" {
  description = "Model deployments configuration"
  type = map(object({
    model_name    = string
    model_version = string
    scale_type    = string
    capacity      = number
  }))
  
  default = {
    gpt-4 = {
      model_name    = "gpt-4"
      model_version = "latest"
      scale_type    = "Standard"
      capacity      = 10
    }
  }
}

variable "security_config" {
  description = "Security configuration"
  type = object({
    enable_private_endpoint = bool
    allowed_ip_ranges      = list(string)
    require_authentication = bool
  })
  
  default = {
    enable_private_endpoint = false
    allowed_ip_ranges      = []
    require_authentication = true
  }
}

variable "scaling_config" {
  description = "Auto-scaling configuration"
  type = object({
    enable_auto_scaling = bool
    min_capacity       = number
    max_capacity       = number
    target_utilization = number
  })
  
  default = {
    enable_auto_scaling = true
    min_capacity       = 1
    max_capacity       = 10
    target_utilization = 70
  }
}
```

### Environment-Specific Terraform Configurations

```hcl
# terraform/environments/dev.tfvars
environment = "dev"
location    = "East US 2"

model_deployments = {
  gpt-4 = {
    model_name    = "gpt-4"
    model_version = "latest"
    scale_type    = "Standard"
    capacity      = 5
  }
  gpt-35-turbo = {
    model_name    = "gpt-35-turbo"
    model_version = "latest"
    scale_type    = "Standard"
    capacity      = 10
  }
}

security_config = {
  enable_private_endpoint = false
  allowed_ip_ranges      = ["0.0.0.0/0"]  # Allow all for dev
  require_authentication = false
}

scaling_config = {
  enable_auto_scaling = false
  min_capacity       = 1
  max_capacity       = 3
  target_utilization = 80
}
```

```hcl
# terraform/environments/prod.tfvars
environment = "prod"
location    = "East US 2"

model_deployments = {
  gpt-4 = {
    model_name    = "gpt-4"
    model_version = "0613"  # Pinned version for production
    scale_type    = "Standard"
    capacity      = 50
  }
  gpt-35-turbo = {
    model_name    = "gpt-35-turbo"
    model_version = "0613"
    scale_type    = "Standard"
    capacity      = 100
  }
}

security_config = {
  enable_private_endpoint = true
  allowed_ip_ranges      = [
    "10.0.0.0/8",    # Corporate network
    "172.16.0.0/12"  # VPN ranges
  ]
  require_authentication = true
}

scaling_config = {
  enable_auto_scaling = true
  min_capacity       = 10
  max_capacity       = 100
  target_utilization = 70
}
```

### Terraform Deployment Pipeline

```yaml
# .github/workflows/terraform.yml
name: Terraform Infrastructure

on:
  push:
    paths:
      - 'terraform/**'
    branches:
      - main
      - develop
  pull_request:
    paths:
      - 'terraform/**'

env:
  TF_VERSION: '1.5.0'
  ARM_CLIENT_ID: ${{ secrets.ARM_CLIENT_ID }}
  ARM_CLIENT_SECRET: ${{ secrets.ARM_CLIENT_SECRET }}
  ARM_SUBSCRIPTION_ID: ${{ secrets.ARM_SUBSCRIPTION_ID }}
  ARM_TENANT_ID: ${{ secrets.ARM_TENANT_ID }}

jobs:
  terraform-plan:
    name: Terraform Plan
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [dev, staging, prod]
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: ${{ env.TF_VERSION }}
    
    - name: Terraform Init
      run: |
        cd terraform
        terraform init \
          -backend-config="storage_account_name=${{ secrets.TF_STATE_STORAGE_ACCOUNT }}" \
          -backend-config="container_name=tfstate" \
          -backend-config="key=${{ matrix.environment }}.terraform.tfstate"
    
    - name: Terraform Validate
      run: |
        cd terraform
        terraform validate
    
    - name: Terraform Plan
      run: |
        cd terraform
        terraform plan \
          -var-file="environments/${{ matrix.environment }}.tfvars" \
          -out="${{ matrix.environment }}.tfplan"
    
    - name: Upload Plan
      uses: actions/upload-artifact@v3
      with:
        name: ${{ matrix.environment }}-tfplan
        path: terraform/${{ matrix.environment }}.tfplan

  terraform-apply:
    name: Terraform Apply
    needs: terraform-plan
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    strategy:
      matrix:
        environment: [dev, staging, prod]
    environment: ${{ matrix.environment }}
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: ${{ env.TF_VERSION }}
    
    - name: Download Plan
      uses: actions/download-artifact@v3
      with:
        name: ${{ matrix.environment }}-tfplan
        path: terraform/
    
    - name: Terraform Init
      run: |
        cd terraform
        terraform init \
          -backend-config="storage_account_name=${{ secrets.TF_STATE_STORAGE_ACCOUNT }}" \
          -backend-config="container_name=tfstate" \
          -backend-config="key=${{ matrix.environment }}.terraform.tfstate"
    
    - name: Terraform Apply
      run: |
        cd terraform
        terraform apply -auto-approve "${{ matrix.environment }}.tfplan"
    
    - name: Output Infrastructure Info
      run: |
        cd terraform
        terraform output -json > ../infrastructure-outputs-${{ matrix.environment }}.json
    
    - name: Upload Infrastructure Outputs
      uses: actions/upload-artifact@v3
      with:
        name: infrastructure-outputs-${{ matrix.environment }}
        path: infrastructure-outputs-${{ matrix.environment }}.json
```

---

## Summary

In this lesson, we've covered:

✅ **Multi-Environment Architecture**: Designing and managing development, staging, and production environments
✅ **Configuration Management**: Implementing hierarchical configuration with environment-specific overrides
✅ **Infrastructure as Code**: Using Terraform to provision and manage Azure AI Foundry infrastructure
✅ **Environment Promotion**: Automated promotion pipelines with validation and rollback capabilities
✅ **Security Configuration**: Environment-specific security settings and access controls
✅ **Deployment Automation**: CI/CD pipelines for infrastructure and configuration management

## Next Steps

In the next lesson, we'll explore **Security and Governance in AI Workflows**, where you'll learn how to implement comprehensive security frameworks, data governance, and compliance controls for AI applications.

## Additional Resources

- [Azure Resource Manager Templates](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Azure Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/)
- [Azure DevOps Environments](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/environments)

---

*This lesson provides the foundation for reliable, scalable, and secure environment management in AI projects.* 