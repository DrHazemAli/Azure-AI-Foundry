# 04-6: Azure AI Document Intelligence

## Overview

Azure AI Document Intelligence (formerly Form Recognizer) extracts text, key-value pairs, tables, and structures from documents using machine learning. It enables organizations to automate document processing workflows and extract valuable insights from various document types.

## Learning Objectives

- Understand Azure AI Document Intelligence capabilities
- Implement document text extraction and analysis
- Use pre-built models for common document types
- Build custom document processing models
- Integrate document intelligence with Azure AI Foundry projects

## What is Azure AI Document Intelligence?

Azure AI Document Intelligence provides:

- **Optical Character Recognition (OCR)**: Extract text from scanned documents and images
- **Layout Analysis**: Understand document structure and formatting
- **Pre-built Models**: Ready-to-use models for common document types
- **Custom Models**: Train models for specific document formats
- **Key-Value Extraction**: Identify and extract form fields and values

## Key Components

### Document Analysis API
- General document analysis
- Layout and structure detection
- Text extraction with positioning
- Table and form recognition

### Pre-built Models
- **Invoices**: Extract vendor, amount, dates, line items
- **Receipts**: Extract merchant, total, date, items
- **Business Cards**: Extract contact information
- **Identity Documents**: Extract personal information
- **W-2 Forms**: Extract tax information

### Custom Models
- **Template-based**: For structured documents
- **Neural Models**: For complex, unstructured documents
- **Composed Models**: Combine multiple models

## Getting Started

### Basic Setup

```python
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

# Initialize the client
document_client = DocumentIntelligenceClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

# Analyze a document
with open("sample-invoice.pdf", "rb") as document:
    poller = document_client.begin_analyze_document(
        "prebuilt-invoice", 
        document=document
    )
    result = poller.result()

# Extract invoice information
for document in result.documents:
    print(f"Invoice ID: {document.fields.get('InvoiceId', {}).get('value_string')}")
    print(f"Vendor: {document.fields.get('VendorName', {}).get('value_string')}")
    print(f"Total: {document.fields.get('InvoiceTotal', {}).get('value_number')}")
```

## Integration with Azure AI Foundry

```python
from azure.ai.projects import AIProjectClient

# Create document processing agent
project_client = AIProjectClient(
    endpoint="your_project_endpoint",
    credential=DefaultAzureCredential()
)

agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="Document Processing Agent",
    instructions="You can analyze and extract information from various document types.",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "analyze_document",
                "description": "Analyze document content and extract structured information"
            }
        }
    ]
)
```

## Common Use Cases

### Financial Document Processing
- Invoice processing and approval workflows
- Expense report automation
- Tax document processing
- Insurance claim processing

### Healthcare Document Management
- Patient intake form processing
- Insurance verification
- Medical record digitization
- Prescription processing

### Legal Document Processing
- Contract analysis and extraction
- Case file digitization
- Compliance document processing
- Due diligence workflows

### Human Resources
- Resume parsing and candidate screening
- Employee onboarding documentation
- Benefits enrollment forms
- Performance review processing

## Best Practices

1. **Document Quality**
   - Ensure high-resolution scans
   - Minimize skew and distortion
   - Use proper lighting and contrast

2. **Model Selection**
   - Choose appropriate pre-built models when available
   - Train custom models for specific document types
   - Use composed models for multiple document types

3. **Performance Optimization**
   - Implement proper error handling
   - Use batch processing for large volumes
   - Cache model results when appropriate

4. **Data Security**
   - Implement proper access controls
   - Follow data retention policies
   - Ensure compliance with regulations

## Conclusion

Azure AI Document Intelligence provides powerful document processing capabilities that enable organizations to automate document workflows and extract valuable insights. Integration with Azure AI Foundry allows for seamless incorporation of document intelligence into AI solutions.

Key takeaways:
- **Comprehensive Document Processing**: Wide range of document analysis capabilities
- **Pre-built and Custom Models**: Flexible model options for different use cases
- **High Accuracy**: Advanced OCR and machine learning for reliable extraction
- **Easy Integration**: Seamless integration with Azure AI Foundry
- **Enterprise Ready**: Scalable and secure document processing

---

*This lesson is part of the Azure AI Foundry Zero-to-Hero Guide.* 