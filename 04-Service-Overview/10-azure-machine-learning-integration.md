# 04-10: Azure Machine Learning Integration

## Overview

Azure Machine Learning (AML) integration with Azure AI Foundry provides a comprehensive MLOps platform for building, training, and deploying machine learning models at scale. This integration enables seamless workflows between model development and AI application deployment.

## Learning Objectives

- Understand Azure Machine Learning integration with Azure AI Foundry
- Implement model training and deployment workflows
- Use MLOps best practices for model lifecycle management
- Integrate custom models with Azure AI Foundry projects
- Implement model monitoring and governance

## What is Azure Machine Learning Integration?

Azure Machine Learning integration provides:

- **Model Development**: Build and train custom ML models
- **Model Registry**: Centralized model management and versioning
- **Automated ML**: Automated machine learning capabilities
- **MLOps Pipelines**: End-to-end machine learning workflows
- **Model Deployment**: Deploy models to various compute targets

## Key Components

### Azure ML Workspace
- Centralized environment for ML development
- Compute resources management
- Data and model versioning
- Experiment tracking and monitoring

### Model Registry
- Model versioning and lineage tracking
- Model metadata and documentation
- Model deployment and serving
- Model governance and compliance

### MLOps Pipelines
- Automated training pipelines
- Continuous integration and deployment
- Model validation and testing
- Production deployment workflows

## Getting Started

### Basic Setup

```python
from azure.ai.ml import MLClient
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Initialize Azure ML client
ml_client = MLClient(
    credential=DefaultAzureCredential(),
    subscription_id="your-subscription-id",
    resource_group_name="your-resource-group",
    workspace_name="your-workspace-name"
)

# Initialize AI Foundry project client
project_client = AIProjectClient(
    endpoint="your_project_endpoint",
    credential=DefaultAzureCredential()
)

# Connect Azure ML workspace to AI Foundry project
connection = project_client.connections.create_or_update({
    "name": "azure-ml-connection",
    "type": "azure_ml",
    "target": ml_client.workspace_name,
    "credentials": {
        "type": "service_principal",
        "client_id": "your-client-id",
        "client_secret": "your-client-secret",
        "tenant_id": "your-tenant-id"
    }
})
```

### Model Training Integration

```python
from azure.ai.ml import command
from azure.ai.ml.entities import Environment, Model

# Define training job
training_job = command(
    inputs={
        "training_data": "azureml://datastores/workspaceblobstore/paths/training-data/",
        "learning_rate": 0.01,
        "epochs": 10
    },
    code="./src",
    command="python train.py --training_data ${{inputs.training_data}} --learning_rate ${{inputs.learning_rate}} --epochs ${{inputs.epochs}}",
    environment="azureml:custom-sklearn-env:1",
    compute="cpu-cluster",
    display_name="Custom Model Training"
)

# Submit training job
training_job_result = ml_client.create_or_update(training_job)
print(f"Training job submitted: {training_job_result.name}")
```

## Integration with Azure AI Foundry

### Using Azure ML Models in AI Foundry

```python
# Register model in Azure ML
from azure.ai.ml.entities import Model

model = Model(
    path="./outputs/model.pkl",
    name="custom-classification-model",
    description="Custom classification model trained with Azure ML",
    version="1.0"
)

registered_model = ml_client.models.create_or_update(model)

# Use model in AI Foundry agent
agent = project_client.agents.create_agent(
    model="gpt-4o",
    name="ML-Enhanced Agent",
    instructions="You can use custom ML models for specialized predictions and analysis.",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "predict_with_custom_model",
                "description": "Make predictions using custom ML model",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input_data": {"type": "object"},
                        "model_name": {"type": "string"}
                    }
                }
            }
        }
    ]
)
```

### MLOps Pipeline Integration

```python
from azure.ai.ml import dsl
from azure.ai.ml.entities import PipelineJob

@dsl.pipeline(
    compute="cpu-cluster",
    description="End-to-end ML pipeline for AI Foundry integration"
)
def ml_pipeline(
    training_data,
    model_name: str,
    learning_rate: float = 0.01
):
    # Data preparation step
    data_prep_step = command(
        inputs={"raw_data": training_data},
        outputs={"processed_data": None},
        code="./src",
        command="python data_prep.py --input ${{inputs.raw_data}} --output ${{outputs.processed_data}}",
        environment="azureml:data-prep-env:1"
    )
    
    # Model training step
    training_step = command(
        inputs={
            "training_data": data_prep_step.outputs.processed_data,
            "learning_rate": learning_rate
        },
        outputs={"model_output": None},
        code="./src",
        command="python train.py --data ${{inputs.training_data}} --lr ${{inputs.learning_rate}} --output ${{outputs.model_output}}",
        environment="azureml:training-env:1"
    )
    
    # Model evaluation step
    evaluation_step = command(
        inputs={
            "model": training_step.outputs.model_output,
            "test_data": data_prep_step.outputs.processed_data
        },
        outputs={"evaluation_results": None},
        code="./src",
        command="python evaluate.py --model ${{inputs.model}} --test_data ${{inputs.test_data}} --output ${{outputs.evaluation_results}}",
        environment="azureml:evaluation-env:1"
    )
    
    # Model registration step
    registration_step = command(
        inputs={
            "model": training_step.outputs.model_output,
            "evaluation": evaluation_step.outputs.evaluation_results,
            "model_name": model_name
        },
        code="./src",
        command="python register_model.py --model ${{inputs.model}} --evaluation ${{inputs.evaluation}} --name ${{inputs.model_name}}",
        environment="azureml:registration-env:1"
    )
    
    return {
        "model_output": training_step.outputs.model_output,
        "evaluation_results": evaluation_step.outputs.evaluation_results
    }

# Create and run pipeline
pipeline_job = ml_pipeline(
    training_data="azureml://datastores/workspaceblobstore/paths/data/training.csv",
    model_name="production-model-v1"
)

pipeline_result = ml_client.jobs.create_or_update(pipeline_job)
```

## Automated ML Integration

### AutoML for Azure AI Foundry

```python
from azure.ai.ml import automl

# Configure AutoML job
automl_job = automl.classification(
    training_data="azureml://datastores/workspaceblobstore/paths/training-data/",
    target_column_name="target",
    primary_metric="accuracy",
    n_cross_validations=5,
    enable_early_stopping=True,
    experiment_timeout_minutes=60,
    max_trials=10
)

# Set compute and other properties
automl_job.set_limits(
    timeout_minutes=60,
    trial_timeout_minutes=10,
    max_trials=10,
    max_concurrent_trials=4
)

# Submit AutoML job
automl_result = ml_client.jobs.create_or_update(automl_job)

# Get best model
best_model = ml_client.models.get(
    name=automl_result.name,
    version="1"
)
```

## Model Deployment and Serving

### Deploy Models for AI Foundry Integration

```python
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment, CodeConfiguration

# Create online endpoint
endpoint = ManagedOnlineEndpoint(
    name="ai-foundry-model-endpoint",
    description="Model endpoint for AI Foundry integration",
    auth_mode="key"
)

endpoint_result = ml_client.online_endpoints.begin_create_or_update(endpoint).result()

# Create deployment
deployment = ManagedOnlineDeployment(
    name="production",
    endpoint_name="ai-foundry-model-endpoint",
    model=registered_model,
    instance_type="Standard_DS3_v2",
    instance_count=1,
    code_configuration=CodeConfiguration(
        code="./scoring",
        scoring_script="score.py"
    ),
    environment="azureml:inference-env:1"
)

deployment_result = ml_client.online_deployments.begin_create_or_update(deployment).result()

# Set traffic allocation
endpoint_result.traffic = {"production": 100}
ml_client.online_endpoints.begin_create_or_update(endpoint_result).result()
```

### Custom Scoring Script

```python
# score.py - Custom scoring script for model serving
import os
import logging
import json
import joblib
import numpy as np
import pandas as pd

def init():
    """Initialize the model"""
    global model
    
    # Get the path to the registered model file
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'model.pkl')
    
    # Load the model
    model = joblib.load(model_path)
    logging.info("Model loaded successfully")

def run(raw_data):
    """Make predictions on input data"""
    try:
        # Parse input data
        data = json.loads(raw_data)
        
        # Convert to DataFrame
        df = pd.DataFrame(data['data'])
        
        # Make predictions
        predictions = model.predict(df)
        probabilities = model.predict_proba(df) if hasattr(model, 'predict_proba') else None
        
        # Prepare response
        response = {
            'predictions': predictions.tolist(),
            'probabilities': probabilities.tolist() if probabilities is not None else None
        }
        
        return json.dumps(response)
        
    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        return json.dumps({'error': str(e)})
```

## Model Monitoring and Governance

### Model Performance Monitoring

```python
from azure.ai.ml.entities import ModelMonitor, MonitoringTarget

# Set up model monitoring
monitor = ModelMonitor(
    name="ai-foundry-model-monitor",
    target=MonitoringTarget(
        endpoint_name="ai-foundry-model-endpoint",
        deployment_name="production"
    ),
    monitoring_signals={
        "data_drift": {
            "type": "data_drift",
            "reference_data": "azureml://datastores/workspaceblobstore/paths/reference-data/",
            "features": ["feature1", "feature2", "feature3"],
            "metric_thresholds": {
                "numerical_features": 0.1,
                "categorical_features": 0.1
            }
        },
        "prediction_drift": {
            "type": "prediction_drift",
            "reference_data": "azureml://datastores/workspaceblobstore/paths/reference-predictions/",
            "metric_thresholds": {
                "prediction_drift": 0.1
            }
        }
    },
    alert_notification={
        "email_recipients": ["ml-team@company.com"],
        "alert_on": ["data_drift", "prediction_drift"]
    }
)

# Create monitor
monitor_result = ml_client.model_monitors.begin_create_or_update(monitor).result()
```

### Model Governance

```python
# Model governance and compliance tracking
def track_model_governance(model_name, model_version):
    """Track model governance information"""
    
    # Get model information
    model = ml_client.models.get(name=model_name, version=model_version)
    
    # Governance information
    governance_info = {
        "model_name": model_name,
        "model_version": model_version,
        "created_by": model.created_by,
        "created_date": model.creation_context.created_at,
        "training_data_source": model.properties.get("training_data_source"),
        "performance_metrics": model.properties.get("performance_metrics"),
        "validation_status": model.properties.get("validation_status"),
        "compliance_status": model.properties.get("compliance_status"),
        "approval_status": model.properties.get("approval_status")
    }
    
    # Log governance information
    logging.info(f"Model governance info: {governance_info}")
    
    return governance_info

# Model validation workflow
def validate_model_for_production(model_name, model_version):
    """Validate model before production deployment"""
    
    validation_results = {
        "performance_check": False,
        "bias_check": False,
        "security_check": False,
        "compliance_check": False,
        "overall_status": "failed"
    }
    
    try:
        # Performance validation
        model = ml_client.models.get(name=model_name, version=model_version)
        performance_metrics = model.properties.get("performance_metrics", {})
        
        if performance_metrics.get("accuracy", 0) > 0.85:
            validation_results["performance_check"] = True
        
        # Bias and fairness check
        # Implementation depends on specific requirements
        validation_results["bias_check"] = True
        
        # Security check
        # Implementation depends on security requirements
        validation_results["security_check"] = True
        
        # Compliance check
        # Implementation depends on compliance requirements
        validation_results["compliance_check"] = True
        
        # Overall status
        if all([validation_results["performance_check"],
                validation_results["bias_check"],
                validation_results["security_check"],
                validation_results["compliance_check"]]):
            validation_results["overall_status"] = "passed"
        
        # Update model properties with validation results
        model.properties["validation_results"] = validation_results
        ml_client.models.create_or_update(model)
        
    except Exception as e:
        logging.error(f"Model validation failed: {str(e)}")
        validation_results["error"] = str(e)
    
    return validation_results
```

## Best Practices

1. **MLOps Integration**
   - Implement automated CI/CD pipelines for model deployment
   - Use version control for model code and configurations
   - Implement proper testing and validation workflows

2. **Model Management**
   - Maintain comprehensive model documentation
   - Track model lineage and dependencies
   - Implement model versioning strategies

3. **Performance Monitoring**
   - Set up continuous monitoring for model performance
   - Implement alerting for model drift and degradation
   - Regular model retraining and updates

4. **Security and Compliance**
   - Implement proper access controls and authentication
   - Ensure data privacy and security compliance
   - Regular security audits and assessments

## Common Integration Patterns

### Batch Inference Integration

```python
# Batch inference pipeline for AI Foundry
def run_batch_inference(input_data_path, model_name, output_path):
    """Run batch inference using Azure ML model"""
    
    # Load model
    model = ml_client.models.get(name=model_name, version="latest")
    
    # Create batch inference job
    batch_job = command(
        inputs={
            "input_data": input_data_path,
            "model": model
        },
        outputs={"predictions": output_path},
        code="./inference",
        command="python batch_inference.py --input ${{inputs.input_data}} --model ${{inputs.model}} --output ${{outputs.predictions}}",
        environment="azureml:inference-env:1",
        compute="batch-cluster"
    )
    
    # Submit and monitor job
    job_result = ml_client.jobs.create_or_update(batch_job)
    return job_result
```

### Real-time Inference Integration

```python
# Real-time inference integration with AI Foundry agents
def create_ml_enhanced_agent():
    """Create AI Foundry agent with ML model integration"""
    
    # Function to call ML model endpoint
    def call_ml_model(input_features):
        import requests
        import json
        
        # Get endpoint details
        endpoint = ml_client.online_endpoints.get("ai-foundry-model-endpoint")
        
        # Prepare request
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {endpoint.scoring_uri}'
        }
        
        payload = {
            'data': [input_features]
        }
        
        # Make prediction request
        response = requests.post(
            endpoint.scoring_uri,
            headers=headers,
            data=json.dumps(payload)
        )
        
        return response.json()
    
    # Create agent with ML capabilities
    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="ML-Enhanced Agent",
        instructions="You can use ML models for specialized predictions and analysis.",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "predict_with_ml_model",
                    "description": "Make predictions using Azure ML model",
                    "implementation": call_ml_model
                }
            }
        ]
    )
    
    return agent
```

## Conclusion

Azure Machine Learning integration with Azure AI Foundry provides a comprehensive platform for building, deploying, and managing machine learning models in AI applications. This integration enables MLOps best practices and seamless workflows between model development and AI application deployment.

Key takeaways:
- **Comprehensive MLOps**: End-to-end machine learning lifecycle management
- **Seamless Integration**: Easy integration between Azure ML and AI Foundry
- **Automated Workflows**: Automated training, validation, and deployment pipelines
- **Model Governance**: Comprehensive model tracking and compliance
- **Enterprise Ready**: Production-ready ML infrastructure and monitoring

---

*This lesson is part of the Azure AI Foundry Zero-to-Hero Guide.* 