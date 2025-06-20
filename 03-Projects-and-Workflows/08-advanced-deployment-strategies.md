# Lesson 8: Advanced Deployment Strategies

## Learning Objectives

By the end of this lesson, you will be able to:
- Implement blue-green deployment strategies for AI models
- Design and execute canary releases for AI applications
- Set up multi-region deployment architectures
- Implement A/B testing frameworks for AI models
- Design sophisticated rollback mechanisms
- Manage traffic routing and load balancing for AI services

## Overview

Advanced deployment strategies are crucial for maintaining high availability, minimizing risk, and ensuring smooth updates of AI applications. This lesson covers sophisticated deployment patterns specifically adapted for AI systems, where model behavior, performance characteristics, and user experience require careful consideration during deployments.

---

## 1. Blue-Green Deployment for AI Models

### Blue-Green Architecture Design

```python
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import json

class DeploymentSlot(Enum):
    BLUE = "blue"
    GREEN = "green"

class DeploymentStatus(Enum):
    INACTIVE = "inactive"
    STAGING = "staging"
    ACTIVE = "active"
    TRANSITIONING = "transitioning"
    FAILED = "failed"

@dataclass
class ModelDeployment:
    deployment_id: str
    model_name: str
    model_version: str
    slot: DeploymentSlot
    status: DeploymentStatus
    endpoint_url: str
    created_at: datetime
    last_health_check: Optional[datetime] = None
    health_status: str = "unknown"
    traffic_percentage: int = 0
    performance_metrics: Dict[str, float] = None

class BlueGreenDeploymentManager:
    def __init__(self, azure_client):
        self.azure_client = azure_client
        self.deployments = {}
        self.active_slot = {}  # model_name -> slot
        self.traffic_router = TrafficRouter()
        self.deployment_validator = DeploymentValidator()
    
    async def deploy_new_version(self, model_name: str, model_version: str,
                               model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy new model version using blue-green strategy"""
        
        # Determine which slot to use (opposite of current active)
        current_active_slot = self.active_slot.get(model_name, DeploymentSlot.BLUE)
        new_slot = DeploymentSlot.GREEN if current_active_slot == DeploymentSlot.BLUE else DeploymentSlot.BLUE
        
        deployment_id = f"{model_name}-{model_version}-{new_slot.value}-{int(datetime.utcnow().timestamp())}"
        
        try:
            # Step 1: Deploy to inactive slot
            print(f"Deploying {model_name} v{model_version} to {new_slot.value} slot...")
            
            deployment = ModelDeployment(
                deployment_id=deployment_id,
                model_name=model_name,
                model_version=model_version,
                slot=new_slot,
                status=DeploymentStatus.STAGING,
                endpoint_url=f"https://{model_name}-{new_slot.value}.azurewebsites.net",
                created_at=datetime.utcnow(),
                performance_metrics={}
            )
            
            # Deploy to Azure (simplified)
            azure_result = await self._deploy_to_azure(deployment, model_config)
            if not azure_result["success"]:
                deployment.status = DeploymentStatus.FAILED
                return {"success": False, "error": azure_result["error"]}
            
            self.deployments[deployment_id] = deployment
            
            # Step 2: Validate deployment
            print("Validating new deployment...")
            validation_result = await self.deployment_validator.validate_deployment(deployment)
            
            if not validation_result["passed"]:
                deployment.status = DeploymentStatus.FAILED
                await self._cleanup_failed_deployment(deployment)
                return {
                    "success": False,
                    "error": "Deployment validation failed",
                    "validation_details": validation_result
                }
            
            # Step 3: Gradual traffic shift
            print("Starting gradual traffic shift...")
            shift_result = await self._gradual_traffic_shift(model_name, deployment)
            
            if not shift_result["success"]:
                deployment.status = DeploymentStatus.FAILED
                await self._rollback_deployment(model_name, deployment)
                return {
                    "success": False,
                    "error": "Traffic shift failed",
                    "details": shift_result
                }
            
            # Step 4: Complete switch
            await self._complete_blue_green_switch(model_name, new_slot)
            deployment.status = DeploymentStatus.ACTIVE
            
            return {
                "success": True,
                "deployment_id": deployment_id,
                "active_slot": new_slot.value,
                "endpoint": deployment.endpoint_url
            }
        
        except Exception as e:
            if deployment_id in self.deployments:
                self.deployments[deployment_id].status = DeploymentStatus.FAILED
                await self._cleanup_failed_deployment(self.deployments[deployment_id])
            
            return {
                "success": False,
                "error": f"Deployment failed: {str(e)}"
            }
    
    async def _deploy_to_azure(self, deployment: ModelDeployment, 
                              model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy model to Azure infrastructure"""
        # In production, this would use Azure SDK to create actual deployments
        try:
            # Simulate Azure deployment
            print(f"Creating Azure resources for {deployment.deployment_id}")
            await asyncio.sleep(2)  # Simulate deployment time
            
            # Update deployment with Azure details
            deployment.endpoint_url = f"https://{deployment.model_name}-{deployment.slot.value}.cognitiveservices.azure.com"
            
            return {"success": True, "endpoint": deployment.endpoint_url}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _gradual_traffic_shift(self, model_name: str, 
                                   new_deployment: ModelDeployment) -> Dict[str, Any]:
        """Gradually shift traffic from old to new deployment"""
        traffic_steps = [10, 25, 50, 75, 100]  # Percentage steps
        
        for step in traffic_steps:
            print(f"Shifting {step}% traffic to new deployment...")
            
            # Update traffic routing
            await self.traffic_router.update_traffic_split(
                model_name, 
                {new_deployment.slot: step, self._get_opposite_slot(new_deployment.slot): 100 - step}
            )
            
            # Monitor for issues during traffic shift
            await asyncio.sleep(30)  # Wait period between shifts
            
            monitoring_result = await self._monitor_traffic_shift(model_name, new_deployment, step)
            
            if not monitoring_result["healthy"]:
                return {
                    "success": False,
                    "error": "Health issues detected during traffic shift",
                    "details": monitoring_result
                }
        
        return {"success": True}
    
    async def _monitor_traffic_shift(self, model_name: str, deployment: ModelDeployment,
                                   traffic_percentage: int) -> Dict[str, Any]:
        """Monitor health during traffic shift"""
        # Check error rates, response times, etc.
        monitoring_result = {
            "healthy": True,
            "metrics": {},
            "alerts": []
        }
        
        # Simulate health check
        error_rate = 0.02  # 2% error rate (would be real metrics)
        avg_response_time = 1200  # ms
        
        if error_rate > 0.05:  # 5% threshold
            monitoring_result["healthy"] = False
            monitoring_result["alerts"].append(f"High error rate: {error_rate:.2%}")
        
        if avg_response_time > 5000:  # 5 second threshold
            monitoring_result["healthy"] = False
            monitoring_result["alerts"].append(f"High response time: {avg_response_time}ms")
        
        monitoring_result["metrics"] = {
            "error_rate": error_rate,
            "avg_response_time_ms": avg_response_time,
            "traffic_percentage": traffic_percentage
        }
        
        return monitoring_result
    
    async def _complete_blue_green_switch(self, model_name: str, new_active_slot: DeploymentSlot):
        """Complete the blue-green switch"""
        # Update active slot
        old_slot = self.active_slot.get(model_name)
        self.active_slot[model_name] = new_active_slot
        
        # Route 100% traffic to new slot
        await self.traffic_router.update_traffic_split(
            model_name,
            {new_active_slot: 100, self._get_opposite_slot(new_active_slot): 0}
        )
        
        # Mark old deployment as inactive
        if old_slot:
            for deployment in self.deployments.values():
                if deployment.model_name == model_name and deployment.slot == old_slot:
                    deployment.status = DeploymentStatus.INACTIVE
                    deployment.traffic_percentage = 0
        
        print(f"Blue-green switch completed. {model_name} now active on {new_active_slot.value} slot")
    
    def _get_opposite_slot(self, slot: DeploymentSlot) -> DeploymentSlot:
        """Get the opposite deployment slot"""
        return DeploymentSlot.GREEN if slot == DeploymentSlot.BLUE else DeploymentSlot.BLUE
    
    async def rollback_deployment(self, model_name: str) -> Dict[str, Any]:
        """Rollback to previous deployment"""
        current_slot = self.active_slot.get(model_name)
        if not current_slot:
            return {"success": False, "error": "No active deployment found"}
        
        # Find previous deployment in opposite slot
        previous_slot = self._get_opposite_slot(current_slot)
        previous_deployment = None
        
        for deployment in self.deployments.values():
            if (deployment.model_name == model_name and 
                deployment.slot == previous_slot and 
                deployment.status == DeploymentStatus.INACTIVE):
                previous_deployment = deployment
                break
        
        if not previous_deployment:
            return {"success": False, "error": "No previous deployment found for rollback"}
        
        try:
            print(f"Rolling back {model_name} to {previous_slot.value} slot...")
            
            # Switch traffic back to previous deployment
            await self.traffic_router.update_traffic_split(
                model_name,
                {previous_slot: 100, current_slot: 0}
            )
            
            # Update deployment statuses
            previous_deployment.status = DeploymentStatus.ACTIVE
            previous_deployment.traffic_percentage = 100
            
            # Mark current deployment as inactive
            for deployment in self.deployments.values():
                if deployment.model_name == model_name and deployment.slot == current_slot:
                    deployment.status = DeploymentStatus.INACTIVE
                    deployment.traffic_percentage = 0
            
            self.active_slot[model_name] = previous_slot
            
            return {
                "success": True,
                "rolled_back_to": previous_deployment.deployment_id,
                "active_slot": previous_slot.value
            }
        
        except Exception as e:
            return {"success": False, "error": f"Rollback failed: {str(e)}"}

# Traffic routing manager
class TrafficRouter:
    def __init__(self):
        self.routing_rules = {}
        self.health_checks = {}
    
    async def update_traffic_split(self, model_name: str, 
                                 traffic_split: Dict[DeploymentSlot, int]):
        """Update traffic split between deployment slots"""
        self.routing_rules[model_name] = traffic_split
        
        # In production, this would update Azure Traffic Manager or Application Gateway
        print(f"Updated traffic routing for {model_name}: {traffic_split}")
    
    async def route_request(self, model_name: str, request_data: Dict[str, Any]) -> str:
        """Route request to appropriate deployment slot"""
        routing_rule = self.routing_rules.get(model_name)
        if not routing_rule:
            # Default to blue slot
            return DeploymentSlot.BLUE.value
        
        # Implement weighted routing based on traffic split
        import random
        random_value = random.randint(1, 100)
        
        cumulative_weight = 0
        for slot, weight in routing_rule.items():
            cumulative_weight += weight
            if random_value <= cumulative_weight:
                return slot.value
        
        # Fallback to first slot
        return list(routing_rule.keys())[0].value

# Deployment validation framework
class DeploymentValidator:
    def __init__(self):
        self.validation_rules = [
            self._validate_health_check,
            self._validate_model_response,
            self._validate_performance,
            self._validate_compatibility
        ]
    
    async def validate_deployment(self, deployment: ModelDeployment) -> Dict[str, Any]:
        """Comprehensive deployment validation"""
        validation_result = {
            "passed": True,
            "checks": [],
            "errors": [],
            "warnings": []
        }
        
        for rule in self.validation_rules:
            try:
                check_result = await rule(deployment)
                validation_result["checks"].append(check_result)
                
                if not check_result["passed"]:
                    validation_result["passed"] = False
                    validation_result["errors"].append(check_result["message"])
                
                if check_result.get("warnings"):
                    validation_result["warnings"].extend(check_result["warnings"])
            
            except Exception as e:
                validation_result["passed"] = False
                validation_result["errors"].append(f"Validation rule failed: {str(e)}")
        
        return validation_result
    
    async def _validate_health_check(self, deployment: ModelDeployment) -> Dict[str, Any]:
        """Validate basic health check"""
        try:
            # Simulate health check call
            await asyncio.sleep(1)
            
            # In production, would make actual HTTP request to health endpoint
            health_status = "healthy"  # Simulated response
            
            deployment.last_health_check = datetime.utcnow()
            deployment.health_status = health_status
            
            return {
                "name": "health_check",
                "passed": health_status == "healthy",
                "message": f"Health check: {health_status}",
                "details": {"endpoint": deployment.endpoint_url}
            }
        
        except Exception as e:
            return {
                "name": "health_check",
                "passed": False,
                "message": f"Health check failed: {str(e)}"
            }
    
    async def _validate_model_response(self, deployment: ModelDeployment) -> Dict[str, Any]:
        """Validate model response quality"""
        try:
            # Test with sample inputs
            test_cases = [
                {"input": "Hello, how are you?", "expected_type": "greeting_response"},
                {"input": "What is 2+2?", "expected_content": "4"}
            ]
            
            passed_tests = 0
            for test_case in test_cases:
                # Simulate model call
                response = f"Mock response to: {test_case['input']}"
                
                # Basic validation
                if len(response) > 10:  # Basic response length check
                    passed_tests += 1
            
            success_rate = passed_tests / len(test_cases)
            
            return {
                "name": "model_response_validation",
                "passed": success_rate >= 0.8,  # 80% success rate required
                "message": f"Model response validation: {success_rate:.1%} success rate",
                "details": {"tests_passed": passed_tests, "total_tests": len(test_cases)}
            }
        
        except Exception as e:
            return {
                "name": "model_response_validation",
                "passed": False,
                "message": f"Model response validation failed: {str(e)}"
            }
    
    async def _validate_performance(self, deployment: ModelDeployment) -> Dict[str, Any]:
        """Validate performance requirements"""
        try:
            # Simulate performance test
            response_times = [1200, 1100, 1300, 1000, 1150]  # Mock response times in ms
            avg_response_time = sum(response_times) / len(response_times)
            
            performance_threshold = 3000  # 3 seconds
            
            warnings = []
            if avg_response_time > 2000:  # 2 seconds warning threshold
                warnings.append(f"Response time above optimal threshold: {avg_response_time:.0f}ms")
            
            return {
                "name": "performance_validation",
                "passed": avg_response_time <= performance_threshold,
                "message": f"Performance validation: {avg_response_time:.0f}ms average response time",
                "warnings": warnings,
                "details": {"avg_response_time_ms": avg_response_time, "threshold_ms": performance_threshold}
            }
        
        except Exception as e:
            return {
                "name": "performance_validation",
                "passed": False,
                "message": f"Performance validation failed: {str(e)}"
            }
    
    async def _validate_compatibility(self, deployment: ModelDeployment) -> Dict[str, Any]:
        """Validate API compatibility"""
        try:
            # Check API schema compatibility
            # In production, would compare API schemas
            
            compatibility_score = 1.0  # Mock compatibility score
            
            return {
                "name": "compatibility_validation",
                "passed": compatibility_score >= 0.95,
                "message": f"Compatibility validation: {compatibility_score:.1%} compatible",
                "details": {"compatibility_score": compatibility_score}
            }
        
        except Exception as e:
            return {
                "name": "compatibility_validation",
                "passed": False,
                "message": f"Compatibility validation failed: {str(e)}"
            }
```

---

## 2. Canary Release Strategy

### Canary Release Implementation

```python
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import random
import asyncio
from datetime import datetime, timedelta

@dataclass
class CanaryConfiguration:
    model_name: str
    canary_version: str
    baseline_version: str
    canary_traffic_percentage: int
    success_criteria: Dict[str, float]
    rollout_duration_minutes: int
    evaluation_interval_minutes: int

class CanaryReleaseManager:
    def __init__(self, traffic_router: TrafficRouter, monitoring_system):
        self.traffic_router = traffic_router
        self.monitoring = monitoring_system
        self.active_canaries = {}
        self.canary_results = {}
    
    async def start_canary_release(self, config: CanaryConfiguration) -> Dict[str, Any]:
        """Start canary release for model deployment"""
        
        canary_id = f"canary-{config.model_name}-{config.canary_version}-{int(datetime.utcnow().timestamp())}"
        
        try:
            print(f"Starting canary release for {config.model_name}")
            print(f"Canary version: {config.canary_version}")
            print(f"Baseline version: {config.baseline_version}")
            print(f"Traffic percentage: {config.canary_traffic_percentage}%")
            
            # Initialize canary tracking
            self.active_canaries[canary_id] = {
                "config": config,
                "start_time": datetime.utcnow(),
                "status": "running",
                "evaluations": [],
                "current_traffic_percentage": 0
            }
            
            # Start with small traffic percentage
            initial_traffic = min(config.canary_traffic_percentage, 5)  # Start with max 5%
            await self._update_canary_traffic(canary_id, initial_traffic)
            
            # Start monitoring and evaluation
            evaluation_task = asyncio.create_task(self._monitor_canary_release(canary_id))
            
            return {
                "success": True,
                "canary_id": canary_id,
                "initial_traffic_percentage": initial_traffic,
                "status": "started"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to start canary release: {str(e)}"
            }
    
    async def _monitor_canary_release(self, canary_id: str):
        """Monitor canary release and make decisions"""
        canary_info = self.active_canaries[canary_id]
        config = canary_info["config"]
        
        total_duration = timedelta(minutes=config.rollout_duration_minutes)
        evaluation_interval = timedelta(minutes=config.evaluation_interval_minutes)
        
        while canary_info["status"] == "running":
            elapsed_time = datetime.utcnow() - canary_info["start_time"]
            
            if elapsed_time >= total_duration:
                # Canary period completed
                await self._complete_canary_release(canary_id)
                break
            
            # Evaluate canary performance
            evaluation_result = await self._evaluate_canary_performance(canary_id)
            canary_info["evaluations"].append(evaluation_result)
            
            if evaluation_result["decision"] == "abort":
                await self._abort_canary_release(canary_id, evaluation_result["reason"])
                break
            elif evaluation_result["decision"] == "proceed":
                # Increase traffic gradually
                new_traffic_percentage = self._calculate_next_traffic_percentage(canary_id)
                await self._update_canary_traffic(canary_id, new_traffic_percentage)
            
            await asyncio.sleep(evaluation_interval.total_seconds())
    
    async def _evaluate_canary_performance(self, canary_id: str) -> Dict[str, Any]:
        """Evaluate canary performance against success criteria"""
        canary_info = self.active_canaries[canary_id]
        config = canary_info["config"]
        
        # Get metrics for canary and baseline versions
        canary_metrics = await self._get_version_metrics(config.model_name, config.canary_version)
        baseline_metrics = await self._get_version_metrics(config.model_name, config.baseline_version)
        
        evaluation = {
            "timestamp": datetime.utcnow(),
            "canary_metrics": canary_metrics,
            "baseline_metrics": baseline_metrics,
            "criteria_results": {},
            "decision": "proceed",
            "reason": "",
            "confidence": 0.0
        }
        
        # Evaluate each success criterion
        total_criteria = len(config.success_criteria)
        passed_criteria = 0
        
        for criterion, threshold in config.success_criteria.items():
            canary_value = canary_metrics.get(criterion, 0)
            baseline_value = baseline_metrics.get(criterion, 0)
            
            # Different evaluation logic based on criterion type
            if criterion == "error_rate":
                # Lower is better
                passed = canary_value <= baseline_value * (1 + threshold)
                evaluation["criteria_results"][criterion] = {
                    "passed": passed,
                    "canary_value": canary_value,
                    "baseline_value": baseline_value,
                    "threshold": threshold
                }
            elif criterion == "response_time":
                # Lower is better
                passed = canary_value <= baseline_value * (1 + threshold)
                evaluation["criteria_results"][criterion] = {
                    "passed": passed,
                    "canary_value": canary_value,
                    "baseline_value": baseline_value,
                    "threshold": threshold
                }
            elif criterion == "user_satisfaction":
                # Higher is better
                passed = canary_value >= baseline_value * (1 - threshold)
                evaluation["criteria_results"][criterion] = {
                    "passed": passed,
                    "canary_value": canary_value,
                    "baseline_value": baseline_value,
                    "threshold": threshold
                }
            else:
                # Default: canary should be within threshold of baseline
                passed = abs(canary_value - baseline_value) <= threshold
                evaluation["criteria_results"][criterion] = {
                    "passed": passed,
                    "canary_value": canary_value,
                    "baseline_value": baseline_value,
                    "threshold": threshold
                }
            
            if passed:
                passed_criteria += 1
        
        # Make decision based on criteria results
        success_rate = passed_criteria / total_criteria
        evaluation["confidence"] = success_rate
        
        if success_rate < 0.7:  # Less than 70% criteria passed
            evaluation["decision"] = "abort"
            evaluation["reason"] = f"Only {success_rate:.1%} of criteria passed (minimum 70% required)"
        elif success_rate >= 0.9:  # 90% or more criteria passed
            evaluation["decision"] = "proceed"
            evaluation["reason"] = f"{success_rate:.1%} of criteria passed - proceeding with rollout"
        else:
            evaluation["decision"] = "hold"
            evaluation["reason"] = f"{success_rate:.1%} of criteria passed - maintaining current traffic"
        
        return evaluation
    
    async def _get_version_metrics(self, model_name: str, version: str) -> Dict[str, float]:
        """Get performance metrics for specific model version"""
        # In production, this would query actual monitoring data
        # Simulated metrics for demonstration
        base_error_rate = 0.02
        base_response_time = 1200
        base_satisfaction = 0.85
        
        # Add some variation for different versions
        version_factor = hash(version) % 100 / 1000  # Small variation
        
        return {
            "error_rate": base_error_rate + version_factor,
            "response_time": base_response_time + (version_factor * 200),
            "user_satisfaction": base_satisfaction + (version_factor / 10),
            "throughput": 100 - (version_factor * 10)
        }
    
    async def _update_canary_traffic(self, canary_id: str, traffic_percentage: int):
        """Update traffic percentage for canary version"""
        canary_info = self.active_canaries[canary_id]
        config = canary_info["config"]
        
        # Update traffic routing
        await self.traffic_router.update_traffic_split(
            config.model_name,
            {
                "canary": traffic_percentage,
                "baseline": 100 - traffic_percentage
            }
        )
        
        canary_info["current_traffic_percentage"] = traffic_percentage
        print(f"Updated canary traffic to {traffic_percentage}%")
    
    def _calculate_next_traffic_percentage(self, canary_id: str) -> int:
        """Calculate next traffic percentage for gradual rollout"""
        canary_info = self.active_canaries[canary_id]
        config = canary_info["config"]
        current_percentage = canary_info["current_traffic_percentage"]
        
        # Gradual increase strategy
        if current_percentage < 5:
            return 5
        elif current_percentage < 10:
            return 10
        elif current_percentage < 25:
            return 25
        elif current_percentage < 50:
            return 50
        elif current_percentage < config.canary_traffic_percentage:
            return min(config.canary_traffic_percentage, current_percentage + 25)
        else:
            return current_percentage
    
    async def _complete_canary_release(self, canary_id: str):
        """Complete successful canary release"""
        canary_info = self.active_canaries[canary_id]
        config = canary_info["config"]
        
        print(f"Completing canary release for {config.model_name}")
        
        # Route 100% traffic to canary version
        await self.traffic_router.update_traffic_split(
            config.model_name,
            {"canary": 100, "baseline": 0}
        )
        
        canary_info["status"] = "completed"
        canary_info["completion_time"] = datetime.utcnow()
        
        # Store results
        self.canary_results[canary_id] = {
            "config": config,
            "evaluations": canary_info["evaluations"],
            "final_status": "success",
            "duration_minutes": (canary_info["completion_time"] - canary_info["start_time"]).total_seconds() / 60
        }
        
        print(f"Canary release completed successfully for {config.model_name}")
    
    async def _abort_canary_release(self, canary_id: str, reason: str):
        """Abort failed canary release"""
        canary_info = self.active_canaries[canary_id]
        config = canary_info["config"]
        
        print(f"Aborting canary release for {config.model_name}: {reason}")
        
        # Route all traffic back to baseline
        await self.traffic_router.update_traffic_split(
            config.model_name,
            {"canary": 0, "baseline": 100}
        )
        
        canary_info["status"] = "aborted"
        canary_info["abort_time"] = datetime.utcnow()
        canary_info["abort_reason"] = reason
        
        # Store results
        self.canary_results[canary_id] = {
            "config": config,
            "evaluations": canary_info["evaluations"],
            "final_status": "aborted",
            "abort_reason": reason,
            "duration_minutes": (canary_info["abort_time"] - canary_info["start_time"]).total_seconds() / 60
        }
        
        print(f"Canary release aborted for {config.model_name}")
    
    def get_canary_status(self, canary_id: str) -> Dict[str, Any]:
        """Get current status of canary release"""
        if canary_id in self.active_canaries:
            canary_info = self.active_canaries[canary_id]
            config = canary_info["config"]
            
            return {
                "canary_id": canary_id,
                "model_name": config.model_name,
                "status": canary_info["status"],
                "current_traffic_percentage": canary_info["current_traffic_percentage"],
                "start_time": canary_info["start_time"].isoformat(),
                "evaluations_count": len(canary_info["evaluations"]),
                "latest_evaluation": canary_info["evaluations"][-1] if canary_info["evaluations"] else None
            }
        elif canary_id in self.canary_results:
            return self.canary_results[canary_id]
        else:
            return {"error": "Canary release not found"}

# A/B Testing Framework
class ABTestingManager:
    def __init__(self, traffic_router: TrafficRouter, analytics_client):
        self.traffic_router = traffic_router
        self.analytics = analytics_client
        self.active_tests = {}
        self.test_results = {}
    
    async def create_ab_test(self, test_config: Dict[str, Any]) -> str:
        """Create A/B test for model comparison"""
        test_id = f"ab-test-{test_config['model_name']}-{int(datetime.utcnow().timestamp())}"
        
        self.active_tests[test_id] = {
            "config": test_config,
            "start_time": datetime.utcnow(),
            "status": "running",
            "results": {"variant_a": [], "variant_b": []}
        }
        
        # Configure traffic split
        await self.traffic_router.update_traffic_split(
            test_config["model_name"],
            {
                "variant_a": test_config["traffic_split"]["variant_a"],
                "variant_b": test_config["traffic_split"]["variant_b"]
            }
        )
        
        print(f"Started A/B test {test_id}")
        return test_id
    
    async def record_test_result(self, test_id: str, variant: str, 
                               user_feedback: Dict[str, Any]):
        """Record user feedback for A/B test"""
        if test_id not in self.active_tests:
            return
        
        test_info = self.active_tests[test_id]
        test_info["results"][variant].append({
            "timestamp": datetime.utcnow(),
            "feedback": user_feedback
        })
    
    async def analyze_ab_test(self, test_id: str) -> Dict[str, Any]:
        """Analyze A/B test results"""
        if test_id not in self.active_tests:
            return {"error": "Test not found"}
        
        test_info = self.active_tests[test_id]
        variant_a_results = test_info["results"]["variant_a"]
        variant_b_results = test_info["results"]["variant_b"]
        
        if not variant_a_results or not variant_b_results:
            return {"error": "Insufficient data for analysis"}
        
        # Calculate metrics for each variant
        def calculate_metrics(results):
            if not results:
                return {}
            
            satisfaction_scores = [r["feedback"].get("satisfaction", 0) for r in results]
            response_quality_scores = [r["feedback"].get("response_quality", 0) for r in results]
            
            return {
                "sample_size": len(results),
                "avg_satisfaction": sum(satisfaction_scores) / len(satisfaction_scores),
                "avg_response_quality": sum(response_quality_scores) / len(response_quality_scores)
            }
        
        variant_a_metrics = calculate_metrics(variant_a_results)
        variant_b_metrics = calculate_metrics(variant_b_results)
        
        # Determine statistical significance (simplified)
        min_sample_size = 30
        significance_threshold = 0.05  # 5% improvement threshold
        
        analysis = {
            "test_id": test_id,
            "variant_a_metrics": variant_a_metrics,
            "variant_b_metrics": variant_b_metrics,
            "statistically_significant": (
                variant_a_metrics["sample_size"] >= min_sample_size and
                variant_b_metrics["sample_size"] >= min_sample_size
            ),
            "recommended_variant": None,
            "confidence": 0.0
        }
        
        if analysis["statistically_significant"]:
            # Simple comparison (in production, would use proper statistical tests)
            a_score = (variant_a_metrics["avg_satisfaction"] + variant_a_metrics["avg_response_quality"]) / 2
            b_score = (variant_b_metrics["avg_satisfaction"] + variant_b_metrics["avg_response_quality"]) / 2
            
            if abs(a_score - b_score) > significance_threshold:
                analysis["recommended_variant"] = "variant_a" if a_score > b_score else "variant_b"
                analysis["confidence"] = abs(a_score - b_score)
        
        return analysis
```

---

## Summary

In this lesson, we've covered:

✅ **Blue-Green Deployments**: Zero-downtime deployment strategy with automated validation and rollback
✅ **Canary Releases**: Gradual rollout with automated monitoring and decision-making
✅ **Traffic Management**: Sophisticated routing and load balancing for AI services
✅ **A/B Testing**: Framework for comparing model performance and user satisfaction
✅ **Automated Validation**: Comprehensive deployment validation including health, performance, and compatibility
✅ **Risk Mitigation**: Advanced rollback mechanisms and failure detection

## Module 3 Completion

Congratulations! You have completed Module 3: Projects and Workflows. This module has provided you with:

- **Advanced project architecture patterns** for scalable AI applications
- **Professional development workflows** adapted for AI projects
- **Team collaboration strategies** for cross-functional AI development
- **Comprehensive CI/CD pipelines** with AI-specific testing and validation
- **Environment management** with infrastructure as code
- **Security and governance frameworks** for enterprise AI
- **Monitoring and optimization** strategies for production AI systems
- **Advanced deployment patterns** for risk-free AI deployments

## Next Steps

You are now ready to proceed to:

- **[Module 04: Service Overview](../04-Service-Overview/README.md)** - Deep dive into Azure AI Foundry services and capabilities
- **[Module 05: SDK Guide](../05-SDK-Guide/README.md)** - Comprehensive SDK usage across programming languages
- **[Module 06: Building AI Agents](../06-Building-AI-Agents/README.md)** - Advanced agent development and orchestration

## Additional Resources

- [Azure DevOps Advanced Deployment](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/deployment-strategies)
- [Blue-Green Deployment in Azure](https://docs.microsoft.com/en-us/azure/architecture/example-scenario/blue-green-spring/blue-green-spring)
- [Canary Deployments](https://docs.microsoft.com/en-us/azure/architecture/framework/devops/deployment-strategies)
- [Azure Traffic Manager](https://docs.microsoft.com/en-us/azure/traffic-manager/)

---

*This module has equipped you with the advanced project management and deployment skills needed to successfully develop, deploy, and maintain enterprise-grade AI applications using Azure AI Foundry.* 