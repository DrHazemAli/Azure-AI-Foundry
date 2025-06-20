# Lesson 1: Azure Subscription and Prerequisites

## Learning Objectives

By the end of this lesson, you will be able to:
- Understand Azure subscription requirements for Azure AI Foundry
- Set up proper permissions and access controls
- Verify regional availability and service limits
- Configure billing and cost management
- Prepare your Azure environment for AI development

## Overview

Before you can start building with Azure AI Foundry, you need to ensure your Azure environment is properly configured. This lesson covers all the prerequisites, from subscription setup to permissions and regional considerations.

## Azure Subscription Requirements

### Subscription Types

Azure AI Foundry works with various Azure subscription types:

#### **Supported Subscription Types**
- **Pay-As-You-Go**: Most flexible for development and testing
- **Enterprise Agreement (EA)**: Best for large organizations
- **Cloud Solution Provider (CSP)**: Through Microsoft partners
- **Free Tier**: Limited features, good for initial exploration
- **Visual Studio Subscriptions**: Includes monthly credits
- **Azure for Students**: Educational accounts with credits

#### **Recommended Subscription Types**
- **Development/Learning**: Pay-As-You-Go or Free Tier
- **Production**: Enterprise Agreement or Pay-As-You-Go with reserved capacity
- **Enterprise**: Enterprise Agreement with dedicated support

### Free Tier Limitations

If using Azure Free Tier, be aware of these limitations:

#### **Free Tier Restrictions**
- Limited monthly credits ($200 for first 30 days)
- Restricted to specific regions
- Limited compute resources
- No access to premium features
- 12-month time limit on free services

#### **AI-Specific Limitations**
- Limited model access (basic OpenAI models only)
- Reduced API call quotas
- No fine-tuning capabilities
- Limited storage capacity
- Basic support only

## Required Permissions

### Subscription-Level Permissions

To create and manage Azure AI Foundry resources, you need appropriate permissions:

#### **Minimum Required Roles**
- **Owner**: Full control over subscription resources
- **Contributor**: Can create and manage resources (recommended minimum)
- **User Access Administrator**: Can manage access to resources

#### **Service-Specific Roles**
- **Cognitive Services Contributor**: For AI services management
- **Storage Account Contributor**: For data storage management
- **Key Vault Contributor**: For secrets management (hub-based projects)

### Resource Group Permissions

For team environments, consider resource group-level permissions:

#### **Recommended Resource Group Roles**
- **Resource Group Owner**: Team leads and administrators
- **Contributor**: Developers and data scientists
- **Reader**: Stakeholders and observers

### Custom Role Creation

For enterprise environments, you may need custom roles:

```json
{
    "Name": "AI Foundry Developer",
    "Description": "Custom role for Azure AI Foundry development",
    "Actions": [
        "Microsoft.CognitiveServices/*",
        "Microsoft.MachineLearningServices/*",
        "Microsoft.Storage/storageAccounts/read",
        "Microsoft.Storage/storageAccounts/listkeys/action",
        "Microsoft.KeyVault/vaults/read",
        "Microsoft.KeyVault/vaults/secrets/read"
    ],
    "NotActions": [],
    "AssignableScopes": [
        "/subscriptions/{subscription-id}"
    ]
}
```

## Regional Availability

### Supported Regions

Azure AI Foundry is available in most Azure regions, but model availability varies:

#### **Primary Regions** (Full feature support)
- **East US**: Complete model catalog, latest features
- **East US 2**: High availability, full features
- **West US 2**: West Coast option, full features
- **West Europe**: European data residency
- **North Europe**: European alternative
- **Southeast Asia**: Asia-Pacific coverage
- **Australia East**: Australian data residency

#### **Secondary Regions** (Limited features)
- **Central US**: Basic features available
- **South Central US**: Expanding availability
- **UK South**: European option
- **Japan East**: Asia-Pacific alternative
- **Canada Central**: Canadian data residency

### Model Availability by Region

Different models are available in different regions:

| **Model Family** | **East US** | **West Europe** | **Southeast Asia** |
|---|---|---|---|
| **GPT-4 Turbo** | ✅ | ✅ | ✅ |
| **GPT-4 Vision** | ✅ | ✅ | ❌ |
| **DALL-E 3** | ✅ | ✅ | ❌ |
| **Whisper** | ✅ | ✅ | ✅ |
| **Claude Models** | ✅ | ❌ | ❌ |
| **Llama Models** | ✅ | ✅ | ✅ |

### Data Residency Considerations

For compliance and performance:

#### **Data Residency Requirements**
- **GDPR Compliance**: Use European regions (West/North Europe)
- **US Data**: Use US regions (East/West US)
- **APAC Data**: Use Asia-Pacific regions (Southeast Asia, Japan East)
- **Government**: Use Azure Government regions if required

## Service Limits and Quotas

### Default Quotas

Azure AI Foundry has default quotas that may need adjustment:

#### **Model Deployment Quotas**
- **GPT-4**: 20,000 tokens per minute (default)
- **GPT-3.5 Turbo**: 240,000 tokens per minute (default)
- **DALL-E**: 2 images per minute (default)
- **Whisper**: 300 requests per minute (default)

#### **Project Limits**
- **Foundry Projects**: 10 per subscription (default)
- **Hub-Based Projects**: 100 per hub (default)
- **Deployments**: 20 per project (default)
- **Connections**: 50 per project (default)

### Quota Management

#### **Requesting Quota Increases**
1. Navigate to Azure portal
2. Go to "Subscriptions" → "Usage + quotas"
3. Find "Cognitive Services" quotas
4. Request increase with business justification
5. Expect 2-5 business days for approval

#### **Monitoring Usage**
- Use Azure Cost Management for billing
- Monitor quotas in Azure portal
- Set up alerts for quota thresholds
- Implement application-level monitoring

## Cost Management Setup

### Understanding Pricing

Azure AI Foundry pricing has multiple components:

#### **Foundry Project Costs**
- **Model Usage**: Token-based pricing
- **Storage**: File and data storage
- **Compute**: Processing and inference
- **Network**: Data transfer costs

#### **Hub-Based Project Costs**
- **All Foundry costs** plus:
- **Azure Storage Account**: Required dependency
- **Azure Key Vault**: Required dependency
- **Azure Container Registry**: Optional dependency
- **Compute Instances**: For training and development

### Cost Estimation

#### **Sample Monthly Costs** (Foundry Project)
- **Light Usage** (10K tokens/day): $15-30/month
- **Medium Usage** (100K tokens/day): $150-300/month
- **Heavy Usage** (1M tokens/day): $1,500-3,000/month

#### **Additional Considerations**
- Model type affects pricing (GPT-4 vs GPT-3.5)
- Input vs output tokens priced differently
- Fine-tuning adds training costs
- Storage and compute scale with usage

### Cost Controls

#### **Setting Up Budgets**
1. Navigate to Azure Cost Management
2. Create budget for AI services
3. Set spending limits and alerts
4. Configure notification recipients
5. Monitor regularly

#### **Cost Optimization Strategies**
- Use appropriate model sizes for use cases
- Implement caching for repeated queries
- Optimize prompt length and structure
- Monitor and analyze usage patterns
- Use reserved capacity for predictable workloads

## Security and Compliance Setup

### Identity and Access Management

#### **Azure Active Directory Setup**
- Configure Azure AD tenant
- Set up user accounts and groups
- Implement conditional access policies
- Enable multi-factor authentication
- Configure privileged identity management

#### **Service Principal Creation**
For application authentication:

```bash
# Create service principal for AI Foundry
az ad sp create-for-rbac --name "ai-foundry-sp" \
    --role "Cognitive Services Contributor" \
    --scopes "/subscriptions/{subscription-id}"
```

### Compliance Considerations

#### **Data Protection**
- **GDPR**: Use European regions for EU data
- **HIPAA**: Enable HIPAA compliance features
- **SOC 2**: Azure provides SOC 2 compliance
- **ISO 27001**: Available in all regions

#### **Audit and Monitoring**
- Enable Azure Activity Log
- Configure diagnostic settings
- Set up Azure Monitor alerts
- Implement Azure Security Center

## Network and Security Configuration

### Network Security

#### **Virtual Network Integration**
For hub-based projects requiring network isolation:

- Configure Azure Virtual Network
- Set up private endpoints
- Implement network security groups
- Configure Azure Firewall rules

#### **Private Endpoint Setup**
```bash
# Create private endpoint for AI services
az network private-endpoint create \
    --name "ai-foundry-pe" \
    --resource-group "myResourceGroup" \
    --vnet-name "myVNet" \
    --subnet "mySubnet" \
    --private-connection-resource-id "/subscriptions/{subscription-id}/resourceGroups/myResourceGroup/providers/Microsoft.CognitiveServices/accounts/myAIFoundry" \
    --connection-name "ai-foundry-connection" \
    --group-id "account"
```

### Security Best Practices

#### **Access Control**
- Use least privilege principle
- Implement role-based access control (RBAC)
- Regular access reviews
- Secure service principal management

#### **Data Security**
- Enable encryption at rest
- Use managed identities where possible
- Implement secure key management
- Regular security assessments

## Prerequisites Checklist

### Before Starting Development

#### **✅ Azure Environment**
- [ ] Active Azure subscription with appropriate permissions
- [ ] Verified regional availability for required models
- [ ] Quota limits reviewed and increased if needed
- [ ] Cost management and budgets configured
- [ ] Security and compliance requirements addressed

#### **✅ Access and Permissions**
- [ ] Contributor or Owner role on subscription/resource group
- [ ] Azure Active Directory access configured
- [ ] Multi-factor authentication enabled
- [ ] Service principals created for applications

#### **✅ Compliance and Security**
- [ ] Data residency requirements identified
- [ ] Compliance frameworks reviewed (GDPR, HIPAA, etc.)
- [ ] Network security requirements assessed
- [ ] Audit and monitoring configured

#### **✅ Cost Management**
- [ ] Pricing model understood
- [ ] Budget and spending alerts configured
- [ ] Cost optimization strategies planned
- [ ] Usage monitoring tools set up

## Common Setup Issues

### Subscription Problems

#### **Insufficient Permissions**
**Problem**: Cannot create AI Foundry resources
**Solution**: 
- Verify Contributor role assignment
- Check resource provider registration
- Contact subscription administrator

#### **Regional Limitations**
**Problem**: Desired models not available in region
**Solution**:
- Choose region with full model support
- Consider multi-region deployment
- Check model roadmap for availability

#### **Quota Limitations**
**Problem**: Cannot deploy models due to quota
**Solution**:
- Request quota increase through Azure portal
- Consider different model sizes
- Implement usage optimization

### Billing Issues

#### **Unexpected Costs**
**Problem**: Higher than expected charges
**Solution**:
- Review cost breakdown in Azure portal
- Implement usage monitoring
- Optimize model usage patterns
- Set up spending alerts

#### **Budget Overruns**
**Problem**: Exceeding planned budget
**Solution**:
- Implement automatic shutdown policies
- Review and optimize usage patterns
- Consider reserved capacity for predictable workloads
- Implement application-level cost controls

## Next Steps

After completing this lesson, you should have:

1. ✅ **Azure subscription ready** with proper permissions
2. ✅ **Regional considerations** understood and planned
3. ✅ **Cost management** configured and monitored
4. ✅ **Security and compliance** requirements addressed
5. ✅ **Quotas and limits** reviewed and optimized

In the next lesson, we'll use this prepared environment to create your first Azure AI Foundry project.

## Additional Resources

- [Azure AI Foundry Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/)
- [Azure Subscription Management](https://docs.microsoft.com/en-us/azure/cost-management-billing/)
- [Azure RBAC Documentation](https://docs.microsoft.com/en-us/azure/role-based-access-control/)
- [Azure Compliance Documentation](https://docs.microsoft.com/en-us/azure/compliance/)
- [Azure Cost Management](https://docs.microsoft.com/en-us/azure/cost-management-billing/cost-management-billing-overview) 