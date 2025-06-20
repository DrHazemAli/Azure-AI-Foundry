#!/usr/bin/env python3
"""
Azure AI Foundry - Advanced Deployment Manager

This comprehensive deployment manager demonstrates advanced deployment strategies
for AI models including blue-green deployments, canary releases, and A/B testing.

Features:
- Blue-green deployment with automated validation
- Canary releases with intelligent rollout
- A/B testing framework for model comparison
- Traffic routing and load balancing
- Automated rollback mechanisms
- Performance monitoring and optimization

Author: Hazem Ali
Course: Azure AI Foundry Zero-to-Hero
Module: 03 - Projects and Workflows
Lesson: 08 - Advanced Deployment Strategies
"""

import asyncio
import argparse
import json
import logging
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import statistics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deployment-manager.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class DeploymentSlot(Enum):
    BLUE = "blue"
    GREEN = "green"


class DeploymentStatus(Enum):
    INACTIVE = "inactive"
    STAGING = "staging"
    ACTIVE = "active"
    TRANSITIONING = "transitioning"
    FAILED = "failed"


class CanaryStatus(Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    ABORTED = "aborted"
    PAUSED = "paused"


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

    def to_dict(self):
        return {
            'deployment_id': self.deployment_id,
            'model_name': self.model_name,
            'model_version': self.model_version,
            'slot': self.slot.value,
            'status': self.status.value,
            'endpoint_url': self.endpoint_url,
            'created_at': self.created_at.isoformat(),
            'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None,
            'health_status': self.health_status,
            'traffic_percentage': self.traffic_percentage,
            'performance_metrics': self.performance_metrics or {}
        }


@dataclass
class CanaryConfiguration:
    model_name: str
    canary_version: str
    baseline_version: str
    canary_traffic_percentage: int
    success_criteria: Dict[str, float]
    rollout_duration_minutes: int
    evaluation_interval_minutes: int
    auto_promote: bool = True


class HealthChecker:
    """Health check and validation service for deployments"""
    
    def __init__(self):
        self.validation_rules = [
            self._validate_endpoint_connectivity,
            self._validate_model_response,
            self._validate_performance_metrics,
            self._validate_api_compatibility
        ]
    
    async def validate_deployment(self, deployment: ModelDeployment) -> Dict[str, Any]:
        """Comprehensive deployment validation"""
        logger.info(f"Starting validation for deployment {deployment.deployment_id}")
        
        validation_result = {
            "deployment_id": deployment.deployment_id,
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
                logger.error(f"Validation rule failed: {e}")
        
        logger.info(f"Validation completed for {deployment.deployment_id}: {'PASSED' if validation_result['passed'] else 'FAILED'}")
        return validation_result
    
    async def _validate_endpoint_connectivity(self, deployment: ModelDeployment) -> Dict[str, Any]:
        """Validate endpoint connectivity"""
        try:
            # Simulate health check call
            await asyncio.sleep(0.5)  # Simulate network delay
            
            # In production, would make actual HTTP request
            health_status = "healthy"
            
            deployment.last_health_check = datetime.utcnow()
            deployment.health_status = health_status
            
            return {
                "name": "endpoint_connectivity",
                "passed": health_status == "healthy",
                "message": f"Endpoint health: {health_status}",
                "details": {"endpoint": deployment.endpoint_url, "status": health_status}
            }
        
        except Exception as e:
            return {
                "name": "endpoint_connectivity",
                "passed": False,
                "message": f"Endpoint connectivity failed: {str(e)}"
            }
    
    async def _validate_model_response(self, deployment: ModelDeployment) -> Dict[str, Any]:
        """Validate model response quality"""
        try:
            # Test with sample inputs
            test_cases = [
                {"input": "Hello, how are you?", "expected_type": "greeting"},
                {"input": "What is 2+2?", "expected_content": "4"},
                {"input": "Summarize this text: The quick brown fox jumps over the lazy dog.", 
                 "expected_type": "summary"}
            ]
            
            passed_tests = 0
            test_results = []
            
            for i, test_case in enumerate(test_cases):
                # Simulate model call
                await asyncio.sleep(0.2)  # Simulate processing time
                
                # Mock response based on input
                if "hello" in test_case["input"].lower():
                    response = "Hello! I'm doing well, thank you for asking."
                elif "2+2" in test_case["input"]:
                    response = "2+2 equals 4."
                elif "summarize" in test_case["input"].lower():
                    response = "A fox jumps over a dog."
                else:
                    response = f"I understand you asked: {test_case['input']}"
                
                # Basic validation
                is_valid = len(response) > 5 and response.strip() != ""
                if is_valid:
                    passed_tests += 1
                
                test_results.append({
                    "test_case": i + 1,
                    "passed": is_valid,
                    "response_length": len(response)
                })
            
            success_rate = passed_tests / len(test_cases)
            
            return {
                "name": "model_response_validation",
                "passed": success_rate >= 0.8,  # 80% success rate required
                "message": f"Model response validation: {success_rate:.1%} success rate",
                "details": {
                    "tests_passed": passed_tests,
                    "total_tests": len(test_cases),
                    "test_results": test_results
                }
            }
        
        except Exception as e:
            return {
                "name": "model_response_validation",
                "passed": False,
                "message": f"Model response validation failed: {str(e)}"
            }
    
    async def _validate_performance_metrics(self, deployment: ModelDeployment) -> Dict[str, Any]:
        """Validate performance requirements"""
        try:
            # Simulate performance test
            response_times = []
            for _ in range(5):
                start_time = datetime.utcnow()
                await asyncio.sleep(0.1)  # Simulate processing
                end_time = datetime.utcnow()
                response_time_ms = (end_time - start_time).total_seconds() * 1000
                response_times.append(response_time_ms)
            
            avg_response_time = statistics.mean(response_times)
            p95_response_time = sorted(response_times)[int(0.95 * len(response_times))]
            
            # Performance thresholds
            avg_threshold = 3000  # 3 seconds
            p95_threshold = 5000  # 5 seconds
            
            warnings = []
            if avg_response_time > 2000:  # 2 seconds warning
                warnings.append(f"Average response time above optimal: {avg_response_time:.0f}ms")
            
            # Update deployment metrics
            deployment.performance_metrics = {
                "avg_response_time_ms": avg_response_time,
                "p95_response_time_ms": p95_response_time,
                "last_updated": datetime.utcnow().isoformat()
            }
            
            return {
                "name": "performance_validation",
                "passed": avg_response_time <= avg_threshold and p95_response_time <= p95_threshold,
                "message": f"Performance: {avg_response_time:.0f}ms avg, {p95_response_time:.0f}ms p95",
                "warnings": warnings,
                "details": {
                    "avg_response_time_ms": avg_response_time,
                    "p95_response_time_ms": p95_response_time,
                    "avg_threshold_ms": avg_threshold,
                    "p95_threshold_ms": p95_threshold
                }
            }
        
        except Exception as e:
            return {
                "name": "performance_validation",
                "passed": False,
                "message": f"Performance validation failed: {str(e)}"
            }
    
    async def _validate_api_compatibility(self, deployment: ModelDeployment) -> Dict[str, Any]:
        """Validate API compatibility"""
        try:
            # Check API schema compatibility
            # In production, would compare OpenAPI specs
            compatibility_score = 1.0  # Mock perfect compatibility
            
            return {
                "name": "api_compatibility",
                "passed": compatibility_score >= 0.95,
                "message": f"API compatibility: {compatibility_score:.1%}",
                "details": {"compatibility_score": compatibility_score}
            }
        
        except Exception as e:
            return {
                "name": "api_compatibility",
                "passed": False,
                "message": f"API compatibility validation failed: {str(e)}"
            }


class TrafficRouter:
    """Traffic routing and load balancing for deployments"""
    
    def __init__(self):
        self.routing_rules = {}
        self.request_counts = {}
        logger.info("Traffic router initialized")
    
    async def update_traffic_split(self, model_name: str, traffic_split: Dict[str, int]):
        """Update traffic split for a model"""
        self.routing_rules[model_name] = traffic_split
        
        # Initialize request counters
        if model_name not in self.request_counts:
            self.request_counts[model_name] = {}
        
        for variant in traffic_split.keys():
            if variant not in self.request_counts[model_name]:
                self.request_counts[model_name][variant] = 0
        
        logger.info(f"Updated traffic routing for {model_name}: {traffic_split}")
    
    def route_request(self, model_name: str) -> str:
        """Route request to appropriate variant based on traffic split"""
        routing_rule = self.routing_rules.get(model_name)
        if not routing_rule:
            return "default"
        
        # Weighted random routing
        import random
        random_value = random.randint(1, 100)
        
        cumulative_weight = 0
        for variant, weight in routing_rule.items():
            cumulative_weight += weight
            if random_value <= cumulative_weight:
                # Track request
                self.request_counts[model_name][variant] += 1
                return variant
        
        # Fallback
        return list(routing_rule.keys())[0]
    
    def get_traffic_stats(self, model_name: str) -> Dict[str, Any]:
        """Get traffic statistics for a model"""
        if model_name not in self.request_counts:
            return {}
        
        total_requests = sum(self.request_counts[model_name].values())
        if total_requests == 0:
            return {"total_requests": 0}
        
        stats = {"total_requests": total_requests, "distribution": {}}
        for variant, count in self.request_counts[model_name].items():
            stats["distribution"][variant] = {
                "requests": count,
                "percentage": (count / total_requests) * 100
            }
        
        return stats


class BlueGreenDeploymentManager:
    """Blue-green deployment manager for zero-downtime deployments"""
    
    def __init__(self, traffic_router: TrafficRouter, health_checker: HealthChecker):
        self.traffic_router = traffic_router
        self.health_checker = health_checker
        self.deployments = {}
        self.active_slots = {}  # model_name -> slot
        logger.info("Blue-green deployment manager initialized")
    
    async def deploy_new_version(self, model_name: str, model_version: str,
                               model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy new model version using blue-green strategy"""
        logger.info(f"Starting blue-green deployment: {model_name} v{model_version}")
        
        # Determine which slot to use
        current_active_slot = self.active_slots.get(model_name, DeploymentSlot.BLUE)
        new_slot = DeploymentSlot.GREEN if current_active_slot == DeploymentSlot.BLUE else DeploymentSlot.BLUE
        
        deployment_id = f"{model_name}-{model_version}-{new_slot.value}-{int(datetime.utcnow().timestamp())}"
        
        try:
            # Step 1: Deploy to inactive slot
            logger.info(f"Deploying {model_name} v{model_version} to {new_slot.value} slot")
            
            deployment = ModelDeployment(
                deployment_id=deployment_id,
                model_name=model_name,
                model_version=model_version,
                slot=new_slot,
                status=DeploymentStatus.STAGING,
                endpoint_url=f"https://{model_name}-{new_slot.value}.azure-ai-foundry.com",
                created_at=datetime.utcnow(),
                performance_metrics={}
            )
            
            # Simulate Azure deployment
            await self._deploy_to_azure(deployment, model_config)
            self.deployments[deployment_id] = deployment
            
            # Step 2: Validate deployment
            logger.info("Validating new deployment...")
            validation_result = await self.health_checker.validate_deployment(deployment)
            
            if not validation_result["passed"]:
                deployment.status = DeploymentStatus.FAILED
                await self._cleanup_failed_deployment(deployment)
                return {
                    "success": False,
                    "error": "Deployment validation failed",
                    "validation_details": validation_result
                }
            
            # Step 3: Gradual traffic shift
            logger.info("Starting gradual traffic shift...")
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
            
            logger.info(f"Blue-green deployment completed successfully: {deployment_id}")
            return {
                "success": True,
                "deployment_id": deployment_id,
                "active_slot": new_slot.value,
                "endpoint": deployment.endpoint_url
            }
        
        except Exception as e:
            logger.error(f"Blue-green deployment failed: {e}")
            if deployment_id in self.deployments:
                self.deployments[deployment_id].status = DeploymentStatus.FAILED
                await self._cleanup_failed_deployment(self.deployments[deployment_id])
            
            return {
                "success": False,
                "error": f"Deployment failed: {str(e)}"
            }
    
    async def _deploy_to_azure(self, deployment: ModelDeployment, model_config: Dict[str, Any]):
        """Simulate Azure deployment"""
        logger.info(f"Creating Azure resources for {deployment.deployment_id}")
        # Simulate deployment time
        await asyncio.sleep(2)
        
        # Update deployment with Azure details
        deployment.endpoint_url = f"https://{deployment.model_name}-{deployment.slot.value}.cognitiveservices.azure.com"
    
    async def _gradual_traffic_shift(self, model_name: str, new_deployment: ModelDeployment) -> Dict[str, Any]:
        """Gradually shift traffic from old to new deployment"""
        traffic_steps = [10, 25, 50, 75, 100]
        
        for step in traffic_steps:
            logger.info(f"Shifting {step}% traffic to new deployment")
            
            # Update traffic routing
            await self.traffic_router.update_traffic_split(
                model_name,
                {
                    new_deployment.slot.value: step,
                    self._get_opposite_slot(new_deployment.slot).value: 100 - step
                }
            )
            
            # Monitor during traffic shift
            await asyncio.sleep(2)  # Wait between shifts
            
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
        # Simulate health metrics
        error_rate = 0.02  # 2% error rate
        avg_response_time = 1200  # ms
        
        monitoring_result = {
            "healthy": True,
            "metrics": {
                "error_rate": error_rate,
                "avg_response_time_ms": avg_response_time,
                "traffic_percentage": traffic_percentage
            },
            "alerts": []
        }
        
        if error_rate > 0.05:  # 5% threshold
            monitoring_result["healthy"] = False
            monitoring_result["alerts"].append(f"High error rate: {error_rate:.2%}")
        
        if avg_response_time > 5000:  # 5 second threshold
            monitoring_result["healthy"] = False
            monitoring_result["alerts"].append(f"High response time: {avg_response_time}ms")
        
        return monitoring_result
    
    async def _complete_blue_green_switch(self, model_name: str, new_active_slot: DeploymentSlot):
        """Complete the blue-green switch"""
        old_slot = self.active_slots.get(model_name)
        self.active_slots[model_name] = new_active_slot
        
        # Route 100% traffic to new slot
        await self.traffic_router.update_traffic_split(
            model_name,
            {new_active_slot.value: 100, self._get_opposite_slot(new_active_slot).value: 0}
        )
        
        # Mark old deployment as inactive
        if old_slot:
            for deployment in self.deployments.values():
                if deployment.model_name == model_name and deployment.slot == old_slot:
                    deployment.status = DeploymentStatus.INACTIVE
                    deployment.traffic_percentage = 0
        
        logger.info(f"Blue-green switch completed. {model_name} now active on {new_active_slot.value} slot")
    
    def _get_opposite_slot(self, slot: DeploymentSlot) -> DeploymentSlot:
        """Get the opposite deployment slot"""
        return DeploymentSlot.GREEN if slot == DeploymentSlot.BLUE else DeploymentSlot.BLUE
    
    async def rollback_deployment(self, model_name: str) -> Dict[str, Any]:
        """Rollback to previous deployment"""
        logger.info(f"Initiating rollback for {model_name}")
        
        current_slot = self.active_slots.get(model_name)
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
            logger.info(f"Rolling back {model_name} to {previous_slot.value} slot")
            
            # Switch traffic back to previous deployment
            await self.traffic_router.update_traffic_split(
                model_name,
                {previous_slot.value: 100, current_slot.value: 0}
            )
            
            # Update deployment statuses
            previous_deployment.status = DeploymentStatus.ACTIVE
            previous_deployment.traffic_percentage = 100
            
            # Mark current deployment as inactive
            for deployment in self.deployments.values():
                if deployment.model_name == model_name and deployment.slot == current_slot:
                    deployment.status = DeploymentStatus.INACTIVE
                    deployment.traffic_percentage = 0
            
            self.active_slots[model_name] = previous_slot
            
            logger.info(f"Rollback completed for {model_name}")
            return {
                "success": True,
                "rolled_back_to": previous_deployment.deployment_id,
                "active_slot": previous_slot.value
            }
        
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return {"success": False, "error": f"Rollback failed: {str(e)}"}
    
    async def _cleanup_failed_deployment(self, deployment: ModelDeployment):
        """Clean up failed deployment resources"""
        logger.info(f"Cleaning up failed deployment: {deployment.deployment_id}")
        # In production, would delete Azure resources
        await asyncio.sleep(1)
    
    async def _rollback_deployment(self, model_name: str, failed_deployment: ModelDeployment):
        """Rollback failed deployment"""
        logger.warning(f"Rolling back failed deployment: {failed_deployment.deployment_id}")
        await self.rollback_deployment(model_name)
    
    def get_deployment_status(self, model_name: str) -> Dict[str, Any]:
        """Get current deployment status"""
        active_slot = self.active_slots.get(model_name)
        deployments_info = []
        
        for deployment in self.deployments.values():
            if deployment.model_name == model_name:
                deployments_info.append(deployment.to_dict())
        
        return {
            "model_name": model_name,
            "active_slot": active_slot.value if active_slot else None,
            "deployments": deployments_info,
            "traffic_stats": self.traffic_router.get_traffic_stats(model_name)
        }


class CanaryReleaseManager:
    """Canary release manager for gradual rollouts with automated monitoring"""
    
    def __init__(self, traffic_router: TrafficRouter, health_checker: HealthChecker):
        self.traffic_router = traffic_router
        self.health_checker = health_checker
        self.active_canaries = {}
        self.canary_results = {}
        logger.info("Canary release manager initialized")
    
    async def start_canary_release(self, config: CanaryConfiguration) -> Dict[str, Any]:
        """Start canary release for model deployment"""
        canary_id = f"canary-{config.model_name}-{config.canary_version}-{int(datetime.utcnow().timestamp())}"
        
        logger.info(f"Starting canary release: {canary_id}")
        logger.info(f"Canary: {config.canary_version}, Baseline: {config.baseline_version}")
        logger.info(f"Target traffic: {config.canary_traffic_percentage}%")
        
        try:
            # Initialize canary tracking
            self.active_canaries[canary_id] = {
                "config": config,
                "start_time": datetime.utcnow(),
                "status": CanaryStatus.RUNNING,
                "evaluations": [],
                "current_traffic_percentage": 0
            }
            
            # Start with small traffic percentage
            initial_traffic = min(config.canary_traffic_percentage, 5)
            await self._update_canary_traffic(canary_id, initial_traffic)
            
            # Start monitoring task
            asyncio.create_task(self._monitor_canary_release(canary_id))
            
            return {
                "success": True,
                "canary_id": canary_id,
                "initial_traffic_percentage": initial_traffic,
                "status": "started"
            }
        
        except Exception as e:
            logger.error(f"Failed to start canary release: {e}")
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
        
        logger.info(f"Starting canary monitoring for {canary_id}")
        
        while canary_info["status"] == CanaryStatus.RUNNING:
            elapsed_time = datetime.utcnow() - canary_info["start_time"]
            
            if elapsed_time >= total_duration:
                await self._complete_canary_release(canary_id)
                break
            
            # Evaluate canary performance
            evaluation_result = await self._evaluate_canary_performance(canary_id)
            canary_info["evaluations"].append(evaluation_result)
            
            logger.info(f"Canary evaluation: {evaluation_result['decision']} (confidence: {evaluation_result['confidence']:.1%})")
            
            if evaluation_result["decision"] == "abort":
                await self._abort_canary_release(canary_id, evaluation_result["reason"])
                break
            elif evaluation_result["decision"] == "proceed":
                new_traffic_percentage = self._calculate_next_traffic_percentage(canary_id)
                await self._update_canary_traffic(canary_id, new_traffic_percentage)
            
            # Wait for next evaluation
            await asyncio.sleep(min(30, evaluation_interval.total_seconds()))  # Cap at 30 seconds for demo
    
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
            
            if criterion == "error_rate":
                # Lower is better
                passed = canary_value <= baseline_value * (1 + threshold)
            elif criterion == "response_time":
                # Lower is better
                passed = canary_value <= baseline_value * (1 + threshold)
            elif criterion == "user_satisfaction":
                # Higher is better
                passed = canary_value >= baseline_value * (1 - threshold)
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
        
        if success_rate < 0.7:
            evaluation["decision"] = "abort"
            evaluation["reason"] = f"Only {success_rate:.1%} of criteria passed (minimum 70% required)"
        elif success_rate >= 0.9:
            evaluation["decision"] = "proceed"
            evaluation["reason"] = f"{success_rate:.1%} of criteria passed - proceeding with rollout"
        else:
            evaluation["decision"] = "hold"
            evaluation["reason"] = f"{success_rate:.1%} of criteria passed - maintaining current traffic"
        
        return evaluation
    
    async def _get_version_metrics(self, model_name: str, version: str) -> Dict[str, float]:
        """Get performance metrics for specific model version"""
        # Simulate metrics based on version
        base_error_rate = 0.02
        base_response_time = 1200
        base_satisfaction = 0.85
        
        # Add variation based on version hash
        version_factor = (hash(version) % 100) / 1000
        
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
        
        await self.traffic_router.update_traffic_split(
            config.model_name,
            {
                "canary": traffic_percentage,
                "baseline": 100 - traffic_percentage
            }
        )
        
        canary_info["current_traffic_percentage"] = traffic_percentage
        logger.info(f"Updated canary traffic to {traffic_percentage}%")
    
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
        
        logger.info(f"Completing canary release: {canary_id}")
        
        if config.auto_promote:
            # Route 100% traffic to canary version
            await self.traffic_router.update_traffic_split(
                config.model_name,
                {"canary": 100, "baseline": 0}
            )
        
        canary_info["status"] = CanaryStatus.COMPLETED
        canary_info["completion_time"] = datetime.utcnow()
        
        # Store results
        self.canary_results[canary_id] = {
            "config": asdict(config),
            "evaluations": canary_info["evaluations"],
            "final_status": "success",
            "duration_minutes": (canary_info["completion_time"] - canary_info["start_time"]).total_seconds() / 60
        }
        
        logger.info(f"Canary release completed successfully: {canary_id}")
    
    async def _abort_canary_release(self, canary_id: str, reason: str):
        """Abort failed canary release"""
        canary_info = self.active_canaries[canary_id]
        config = canary_info["config"]
        
        logger.warning(f"Aborting canary release {canary_id}: {reason}")
        
        # Route all traffic back to baseline
        await self.traffic_router.update_traffic_split(
            config.model_name,
            {"canary": 0, "baseline": 100}
        )
        
        canary_info["status"] = CanaryStatus.ABORTED
        canary_info["abort_time"] = datetime.utcnow()
        canary_info["abort_reason"] = reason
        
        # Store results
        self.canary_results[canary_id] = {
            "config": asdict(config),
            "evaluations": canary_info["evaluations"],
            "final_status": "aborted",
            "abort_reason": reason,
            "duration_minutes": (canary_info["abort_time"] - canary_info["start_time"]).total_seconds() / 60
        }
    
    def get_canary_status(self, canary_id: str) -> Dict[str, Any]:
        """Get current status of canary release"""
        if canary_id in self.active_canaries:
            canary_info = self.active_canaries[canary_id]
            config = canary_info["config"]
            
            return {
                "canary_id": canary_id,
                "model_name": config.model_name,
                "status": canary_info["status"].value,
                "current_traffic_percentage": canary_info["current_traffic_percentage"],
                "start_time": canary_info["start_time"].isoformat(),
                "evaluations_count": len(canary_info["evaluations"]),
                "latest_evaluation": canary_info["evaluations"][-1] if canary_info["evaluations"] else None
            }
        elif canary_id in self.canary_results:
            return self.canary_results[canary_id]
        else:
            return {"error": "Canary release not found"}


class DeploymentManagerCLI:
    """Command-line interface for the deployment manager"""
    
    def __init__(self):
        self.traffic_router = TrafficRouter()
        self.health_checker = HealthChecker()
        self.blue_green_manager = BlueGreenDeploymentManager(self.traffic_router, self.health_checker)
        self.canary_manager = CanaryReleaseManager(self.traffic_router, self.health_checker)
    
    async def run_blue_green_deployment(self, model_name: str, model_version: str):
        """Run blue-green deployment"""
        print(f"\n🚀 Starting Blue-Green Deployment")
        print(f"Model: {model_name}")
        print(f"Version: {model_version}")
        print("=" * 50)
        
        model_config = {
            "temperature": 0.7,
            "max_tokens": 1000,
            "deployment_type": "blue-green"
        }
        
        result = await self.blue_green_manager.deploy_new_version(model_name, model_version, model_config)
        
        if result["success"]:
            print(f"✅ Deployment successful!")
            print(f"   Deployment ID: {result['deployment_id']}")
            print(f"   Active Slot: {result['active_slot']}")
            print(f"   Endpoint: {result['endpoint']}")
        else:
            print(f"❌ Deployment failed: {result['error']}")
            if "validation_details" in result:
                print("\nValidation Details:")
                for error in result["validation_details"]["errors"]:
                    print(f"   - {error}")
        
        return result
    
    async def run_canary_release(self, model_name: str, canary_version: str, baseline_version: str):
        """Run canary release"""
        print(f"\n🐤 Starting Canary Release")
        print(f"Model: {model_name}")
        print(f"Canary Version: {canary_version}")
        print(f"Baseline Version: {baseline_version}")
        print("=" * 50)
        
        config = CanaryConfiguration(
            model_name=model_name,
            canary_version=canary_version,
            baseline_version=baseline_version,
            canary_traffic_percentage=50,
            success_criteria={
                "error_rate": 0.05,  # Max 5% increase
                "response_time": 0.10,  # Max 10% increase
                "user_satisfaction": 0.02  # Max 2% decrease
            },
            rollout_duration_minutes=5,  # Shortened for demo
            evaluation_interval_minutes=1,
            auto_promote=True
        )
        
        result = await self.canary_manager.start_canary_release(config)
        
        if result["success"]:
            print(f"✅ Canary release started!")
            print(f"   Canary ID: {result['canary_id']}")
            print(f"   Initial Traffic: {result['initial_traffic_percentage']}%")
            
            # Monitor progress
            await self._monitor_canary_progress(result["canary_id"])
        else:
            print(f"❌ Canary release failed: {result['error']}")
        
        return result
    
    async def _monitor_canary_progress(self, canary_id: str):
        """Monitor canary release progress"""
        print("\n📊 Monitoring Canary Progress...")
        
        while True:
            await asyncio.sleep(5)  # Check every 5 seconds
            
            status = self.canary_manager.get_canary_status(canary_id)
            
            if status.get("error"):
                print(f"❌ Error getting canary status: {status['error']}")
                break
            
            print(f"Status: {status['status']}, Traffic: {status.get('current_traffic_percentage', 0)}%")
            
            if status["status"] in ["completed", "aborted"]:
                if status["status"] == "completed":
                    print("✅ Canary release completed successfully!")
                else:
                    print(f"❌ Canary release aborted: {status.get('abort_reason', 'Unknown reason')}")
                break
    
    def show_deployment_status(self, model_name: str):
        """Show current deployment status"""
        print(f"\n📋 Deployment Status for {model_name}")
        print("=" * 50)
        
        status = self.blue_green_manager.get_deployment_status(model_name)
        
        print(f"Active Slot: {status.get('active_slot', 'None')}")
        print(f"Deployments: {len(status['deployments'])}")
        
        for deployment in status["deployments"]:
            print(f"\n  Deployment: {deployment['deployment_id']}")
            print(f"    Version: {deployment['model_version']}")
            print(f"    Slot: {deployment['slot']}")
            print(f"    Status: {deployment['status']}")
            print(f"    Health: {deployment['health_status']}")
            print(f"    Traffic: {deployment['traffic_percentage']}%")
        
        traffic_stats = status.get("traffic_stats", {})
        if traffic_stats:
            print(f"\nTraffic Statistics:")
            print(f"  Total Requests: {traffic_stats['total_requests']}")
            for variant, stats in traffic_stats.get("distribution", {}).items():
                print(f"  {variant}: {stats['requests']} requests ({stats['percentage']:.1f}%)")


async def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Azure AI Foundry Advanced Deployment Manager")
    parser.add_argument("command", choices=["blue-green", "canary", "status", "rollback"],
                       help="Deployment command to execute")
    parser.add_argument("--model-name", required=True, help="Model name")
    parser.add_argument("--model-version", help="Model version for deployment")
    parser.add_argument("--canary-version", help="Canary version for canary release")
    parser.add_argument("--baseline-version", help="Baseline version for canary release")
    
    args = parser.parse_args()
    
    cli = DeploymentManagerCLI()
    
    try:
        if args.command == "blue-green":
            if not args.model_version:
                print("❌ --model-version is required for blue-green deployment")
                return
            
            await cli.run_blue_green_deployment(args.model_name, args.model_version)
        
        elif args.command == "canary":
            if not args.canary_version or not args.baseline_version:
                print("❌ --canary-version and --baseline-version are required for canary release")
                return
            
            await cli.run_canary_release(args.model_name, args.canary_version, args.baseline_version)
        
        elif args.command == "status":
            cli.show_deployment_status(args.model_name)
        
        elif args.command == "rollback":
            result = await cli.blue_green_manager.rollback_deployment(args.model_name)
            if result["success"]:
                print(f"✅ Rollback successful!")
                print(f"   Rolled back to: {result['rolled_back_to']}")
                print(f"   Active slot: {result['active_slot']}")
            else:
                print(f"❌ Rollback failed: {result['error']}")
    
    except KeyboardInterrupt:
        print("\n\n👋 Deployment manager interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    print("Azure AI Foundry - Advanced Deployment Manager")
    print("=" * 50)
    asyncio.run(main()) 