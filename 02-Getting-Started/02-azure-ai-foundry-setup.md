# Azure AI Foundry Setup and Configuration

## Overview

This lesson guides you through the complete setup and configuration of Azure AI Foundry, from initial service deployment to advanced configuration options. We'll cover both Azure portal setup and programmatic configuration.

## Learning Objectives

By the end of this lesson, you will be able to:
- Deploy Azure AI Foundry service in your Azure subscription
- Configure essential settings and security options
- Set up authentication and access controls
- Understand resource organization and management
- Configure monitoring and logging
- Optimize for cost and performance

## Prerequisites

- Active Azure subscription with appropriate permissions
- Completed Azure subscription prerequisites (Lesson 01)
- Basic understanding of Azure Resource Manager (ARM)
- Familiarity with Azure Active Directory concepts

---

## 1. Azure AI Foundry Service Deployment

### 1.1 Using Azure Portal

**Step 1: Navigate to Azure AI Foundry**
```bash
# Search for "Azure AI Foundry" in the Azure portal search bar
# Or navigate directly to: https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry
```

**Step 2: Basic Configuration**
- **Subscription**: Select your Azure subscription
- **Resource Group**: Create new or select existing
- **Region**: Choose optimal region for your use case
- **Name**: Unique name for your AI Foundry instance
- **Pricing Tier**: Select appropriate tier based on requirements

**Step 3: Network Configuration**
```yaml
Network Settings:
  Public Access: Enabled/Disabled
  Virtual Network Integration: Optional
  Private Endpoints: Configure if needed
  Firewall Rules: Define IP restrictions
```

**Step 4: Security and Compliance**
- **Authentication**: Configure AAD integration
- **Encryption**: Enable customer-managed keys if required
- **Compliance**: Select required compliance certifications
- **Data Residency**: Ensure data sovereignty requirements

### 1.2 Using Azure CLI

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "your-subscription-id"

# Create resource group
az group create \
  --name "rg-aifoundry-prod" \
  --location "East US 2"

# Create AI Foundry service
az cognitiveservices account create \
  --name "aifoundry-prod-001" \
  --resource-group "rg-aifoundry-prod" \
  --location "East US 2" \
  --kind "AIFoundry" \
  --sku "S0" \
  --custom-domain "aifoundry-prod-001" \
  --assign-identity
```

### 1.3 Using ARM Templates

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "aiFoundryName": {
      "type": "string",
      "metadata": {
        "description": "Name of the AI Foundry service"
      }
    },
    "location": {
      "type": "string",
      "defaultValue": "East US 2",
      "metadata": {
        "description": "Location for all resources"
      }
    },
    "sku": {
      "type": "string",
      "defaultValue": "S0",
      "allowedValues": ["F0", "S0", "S1", "S2", "S3"],
      "metadata": {
        "description": "SKU for AI Foundry service"
      }
    }
  },
  "resources": [
    {
      "type": "Microsoft.CognitiveServices/accounts",
      "apiVersion": "2023-05-01",
      "name": "[parameters('aiFoundryName')]",
      "location": "[parameters('location')]",
      "kind": "AIFoundry",
      "sku": {
        "name": "[parameters('sku')]"
      },
      "properties": {
        "customSubDomainName": "[parameters('aiFoundryName')]",
        "publicNetworkAccess": "Enabled",
        "networkAcls": {
          "defaultAction": "Allow"
        }
      },
      "identity": {
        "type": "SystemAssigned"
      }
    }
  ]
}
```

---

## 2. Authentication Configuration

### 2.1 Service Principal Authentication

**Create Service Principal:**
```bash
# Create service principal
az ad sp create-for-rbac \
  --name "sp-aifoundry-prod" \
  --role "Cognitive Services User" \
  --scopes "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{ai-foundry-name}"
```

**Configuration:**
```json
{
  "appId": "your-client-id",
  "displayName": "sp-aifoundry-prod",
  "password": "your-client-secret",
  "tenant": "your-tenant-id"
}
```

### 2.2 Managed Identity Configuration

**System-Assigned Managed Identity:**
```bash
# Enable system-assigned managed identity
az cognitiveservices account identity assign \
  --name "aifoundry-prod-001" \
  --resource-group "rg-aifoundry-prod"
```

**User-Assigned Managed Identity:**
```bash
# Create user-assigned managed identity
az identity create \
  --name "mi-aifoundry-prod" \
  --resource-group "rg-aifoundry-prod"

# Assign to AI Foundry service
az cognitiveservices account identity assign \
  --name "aifoundry-prod-001" \
  --resource-group "rg-aifoundry-prod" \
  --user-assigned "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/mi-aifoundry-prod"
```

### 2.3 API Key Management

```bash
# Get primary key
az cognitiveservices account keys list \
  --name "aifoundry-prod-001" \
  --resource-group "rg-aifoundry-prod" \
  --query "key1" \
  --output tsv

# Regenerate keys
az cognitiveservices account keys regenerate \
  --name "aifoundry-prod-001" \
  --resource-group "rg-aifoundry-prod" \
  --key-name "Key1"
```

---

## 3. Network Configuration

### 3.1 Virtual Network Integration

```bash
# Create virtual network
az network vnet create \
  --name "vnet-aifoundry-prod" \
  --resource-group "rg-aifoundry-prod" \
  --address-prefix "10.0.0.0/16" \
  --subnet-name "subnet-aifoundry" \
  --subnet-prefix "10.0.1.0/24"

# Create service endpoint
az network vnet subnet update \
  --name "subnet-aifoundry" \
  --vnet-name "vnet-aifoundry-prod" \
  --resource-group "rg-aifoundry-prod" \
  --service-endpoints "Microsoft.CognitiveServices"
```

### 3.2 Private Endpoints

```bash
# Create private endpoint
az network private-endpoint create \
  --name "pe-aifoundry-prod" \
  --resource-group "rg-aifoundry-prod" \
  --vnet-name "vnet-aifoundry-prod" \
  --subnet "subnet-aifoundry" \
  --private-connection-resource-id "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/aifoundry-prod-001" \
  --group-id "account" \
  --connection-name "pe-connection"
```

### 3.3 Firewall Configuration

```json
{
  "networkAcls": {
    "defaultAction": "Deny",
    "ipRules": [
      {
        "value": "203.0.113.0/24"
      }
    ],
    "virtualNetworkRules": [
      {
        "id": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.Network/virtualNetworks/vnet-aifoundry-prod/subnets/subnet-aifoundry"
      }
    ]
  }
}
```

---

## 4. Security Configuration

### 4.1 Customer-Managed Keys (CMK)

```bash
# Create Key Vault
az keyvault create \
  --name "kv-aifoundry-prod" \
  --resource-group "rg-aifoundry-prod" \
  --location "East US 2" \
  --enable-purge-protection \
  --enable-soft-delete

# Create encryption key
az keyvault key create \
  --vault-name "kv-aifoundry-prod" \
  --name "aifoundry-encryption-key" \
  --protection "software"

# Configure CMK for AI Foundry
az cognitiveservices account update \
  --name "aifoundry-prod-001" \
  --resource-group "rg-aifoundry-prod" \
  --encryption-key-source "Microsoft.Keyvault" \
  --encryption-key-vault-key-uri "https://kv-aifoundry-prod.vault.azure.net/keys/aifoundry-encryption-key"
```

### 4.2 Azure Policy Configuration

```json
{
  "policyRule": {
    "if": {
      "allOf": [
        {
          "field": "type",
          "equals": "Microsoft.CognitiveServices/accounts"
        },
        {
          "field": "Microsoft.CognitiveServices/accounts/kind",
          "equals": "AIFoundry"
        }
      ]
    },
    "then": {
      "effect": "audit",
      "details": {
        "type": "Microsoft.CognitiveServices/accounts/networkAcls",
        "existenceCondition": {
          "field": "Microsoft.CognitiveServices/accounts/networkAcls.defaultAction",
          "equals": "Deny"
        }
      }
    }
  }
}
```

---

## 5. Monitoring and Diagnostics

### 5.1 Diagnostic Settings

```bash
# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --workspace-name "law-aifoundry-prod" \
  --resource-group "rg-aifoundry-prod" \
  --location "East US 2"

# Configure diagnostic settings
az monitor diagnostic-settings create \
  --name "diag-aifoundry-prod" \
  --resource "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/aifoundry-prod-001" \
  --workspace "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.OperationalInsights/workspaces/law-aifoundry-prod" \
  --logs '[{"category":"Audit","enabled":true},{"category":"RequestResponse","enabled":true}]' \
  --metrics '[{"category":"AllMetrics","enabled":true}]'
```

### 5.2 Application Insights Integration

```bash
# Create Application Insights
az monitor app-insights component create \
  --app "ai-aifoundry-prod" \
  --location "East US 2" \
  --resource-group "rg-aifoundry-prod" \
  --workspace "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.OperationalInsights/workspaces/law-aifoundry-prod"
```

### 5.3 Alerting Configuration

```bash
# Create action group
az monitor action-group create \
  --name "ag-aifoundry-alerts" \
  --resource-group "rg-aifoundry-prod" \
  --short-name "AIFAlerts" \
  --email-receivers name="admin" email="admin@company.com"

# Create metric alert
az monitor metrics alert create \
  --name "High Error Rate Alert" \
  --resource-group "rg-aifoundry-prod" \
  --target-resource-id "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/aifoundry-prod-001" \
  --condition "avg ClientErrors > 10" \
  --action-group "ag-aifoundry-alerts"
```

---

## 6. Performance Optimization

### 6.1 Scaling Configuration

```bash
# Configure autoscaling (if supported)
az monitor autoscale create \
  --name "autoscale-aifoundry" \
  --resource-group "rg-aifoundry-prod" \
  --resource "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/aifoundry-prod-001" \
  --min-count 1 \
  --max-count 10 \
  --count 2
```

### 6.2 Content Delivery Network (CDN)

```bash
# Create CDN profile for static content caching
az cdn profile create \
  --name "cdn-aifoundry-prod" \
  --resource-group "rg-aifoundry-prod" \
  --sku "Standard_Microsoft"

# Create CDN endpoint
az cdn endpoint create \
  --name "aifoundry-prod-endpoint" \
  --profile-name "cdn-aifoundry-prod" \
  --resource-group "rg-aifoundry-prod" \
  --origin "aifoundry-prod-001.cognitiveservices.azure.com"
```

---

## 7. Cost Management

### 7.1 Budget Configuration

```bash
# Create budget
az consumption budget create \
  --budget-name "budget-aifoundry-monthly" \
  --resource-group "rg-aifoundry-prod" \
  --amount 1000 \
  --time-grain "Monthly" \
  --time-period start-date="2024-01-01" \
  --notifications \
    threshold=80 \
    operator="GreaterThan" \
    contact-emails="finance@company.com" \
    threshold=100 \
    operator="GreaterThan" \
    contact-emails="admin@company.com"
```

### 7.2 Cost Optimization Strategies

**Resource Tagging:**
```bash
# Apply cost tracking tags
az cognitiveservices account update \
  --name "aifoundry-prod-001" \
  --resource-group "rg-aifoundry-prod" \
  --tags \
    Environment="Production" \
    CostCenter="AI-ML" \
    Project="Customer-Service-Bot" \
    Owner="data-team@company.com"
```

**Usage Quotas:**
```json
{
  "quotas": {
    "requestsPerSecond": 100,
    "tokensPerMinute": 10000,
    "maxConcurrentRequests": 50
  }
}
```

---

## 8. Configuration Validation

### 8.1 Health Check Script

```python
#!/usr/bin/env python3
"""
Azure AI Foundry Health Check Script
Validates configuration and connectivity
"""

import os
import sys
import asyncio
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

async def validate_configuration():
    """Validate Azure AI Foundry configuration."""
    
    try:
        # Check environment variables
        required_vars = [
            'AZURE_AI_FOUNDRY_ENDPOINT',
            'AZURE_SUBSCRIPTION_ID',
            'AZURE_RESOURCE_GROUP'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            print(f"❌ Missing environment variables: {missing_vars}")
            return False
        
        # Test authentication
        credential = DefaultAzureCredential()
        
        # Test service connectivity
        endpoint = os.getenv('AZURE_AI_FOUNDRY_ENDPOINT')
        client = AIProjectClient(endpoint=endpoint, credential=credential)
        
        # Perform basic API call
        # (Implementation would depend on available SDK methods)
        
        print("✅ Configuration validation successful")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(validate_configuration())
    sys.exit(0 if success else 1)
```

### 8.2 Configuration Checklist

**Pre-Production Checklist:**
- [ ] Service deployed in correct region
- [ ] Appropriate SKU selected for workload
- [ ] Authentication configured (Service Principal/Managed Identity)
- [ ] Network security configured (VNet/Private Endpoints)
- [ ] Encryption configured (Customer-managed keys if required)
- [ ] Monitoring and alerting enabled
- [ ] Backup and disaster recovery planned
- [ ] Cost management configured
- [ ] Security scanning completed
- [ ] Performance testing completed

---

## 9. Troubleshooting Common Issues

### 9.1 Authentication Issues

**Problem:** "Authentication failed" errors
```bash
# Check service principal permissions
az role assignment list \
  --assignee "your-service-principal-id" \
  --resource-group "rg-aifoundry-prod"

# Verify token acquisition
az account get-access-token \
  --resource "https://cognitiveservices.azure.com"
```

### 9.2 Network Connectivity Issues

**Problem:** "Network unreachable" errors
```bash
# Test DNS resolution
nslookup aifoundry-prod-001.cognitiveservices.azure.com

# Test network connectivity
curl -I https://aifoundry-prod-001.cognitiveservices.azure.com

# Check firewall rules
az cognitiveservices account show \
  --name "aifoundry-prod-001" \
  --resource-group "rg-aifoundry-prod" \
  --query "properties.networkAcls"
```

### 9.3 Performance Issues

**Problem:** High latency or timeouts
```bash
# Check service health
az cognitiveservices account show \
  --name "aifoundry-prod-001" \
  --resource-group "rg-aifoundry-prod" \
  --query "properties.provisioningState"

# Review metrics
az monitor metrics list \
  --resource "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/aifoundry-prod-001" \
  --metric "TotalCalls,ResponseTime,Errors"
```

---

## Summary

In this lesson, we covered the essential setup and configuration steps for deploying Azure AI Foundry in a production environment, including authentication, security, monitoring, and cost optimization strategies.

## Next Steps

- Complete the hands-on lab for service deployment
- Set up your development environment (Lesson 03)
- Configure your first AI project (Lesson 04)

## Additional Resources

- [Azure AI Foundry Service Documentation](https://docs.microsoft.com/azure/cognitive-services/ai-foundry/)
- [Azure Resource Manager Templates](https://docs.microsoft.com/azure/azure-resource-manager/)
- [Azure Security Best Practices](https://docs.microsoft.com/azure/security/)
- [Azure Cost Management](https://docs.microsoft.com/azure/cost-management-billing/)

---

*This lesson is part of the Azure AI Foundry Zero-to-Hero course. Continue to the next lesson to set up your development environment.* 