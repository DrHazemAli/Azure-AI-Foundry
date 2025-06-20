# Lesson 7: Monitoring and Performance Optimization

## Learning Objectives

By the end of this lesson, you will be able to:
- Implement comprehensive monitoring for AI applications
- Set up performance metrics and alerting systems
- Analyze and optimize AI model performance
- Monitor costs and optimize resource utilization
- Create observability dashboards for AI systems
- Implement proactive performance optimization strategies

## Overview

Monitoring and performance optimization are crucial for maintaining reliable, efficient, and cost-effective AI applications. This lesson covers comprehensive strategies for observing AI system behavior, detecting issues early, and continuously optimizing performance across all aspects of Azure AI Foundry applications.

---

## 1. Comprehensive Monitoring Framework

### Multi-Dimensional Monitoring Strategy

```python
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
import statistics
import asyncio
from enum import Enum

class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class Metric:
    name: str
    metric_type: MetricType
    value: float
    timestamp: datetime
    tags: Dict[str, str]
    dimensions: Dict[str, Any] = None

@dataclass
class Alert:
    alert_id: str
    metric_name: str
    severity: AlertSeverity
    threshold: float
    current_value: float
    message: str
    timestamp: datetime
    acknowledged: bool = False

class AIMonitoringSystem:
    def __init__(self):
        self.metrics_buffer = []
        self.alerts = []
        self.alert_rules = {}
        self.metric_aggregations = {}
        self.dashboards = {}
        self._setup_default_monitoring()
    
    def _setup_default_monitoring(self):
        """Setup default monitoring rules for AI applications"""
        
        # Model performance alerts
        self.add_alert_rule(
            "model_response_time",
            threshold=5000,  # 5 seconds
            comparison="greater_than",
            severity=AlertSeverity.WARNING,
            description="Model response time exceeding threshold"
        )
        
        self.add_alert_rule(
            "model_error_rate",
            threshold=0.05,  # 5%
            comparison="greater_than",
            severity=AlertSeverity.ERROR,
            description="Model error rate too high"
        )
        
        self.add_alert_rule(
            "token_usage_rate",
            threshold=0.9,  # 90% of quota
            comparison="greater_than",
            severity=AlertSeverity.WARNING,
            description="Token usage approaching quota limit"
        )
        
        # Infrastructure alerts
        self.add_alert_rule(
            "cpu_utilization",
            threshold=0.8,  # 80%
            comparison="greater_than",
            severity=AlertSeverity.WARNING,
            description="High CPU utilization"
        )
        
        self.add_alert_rule(
            "memory_utilization",
            threshold=0.85,  # 85%
            comparison="greater_than",
            severity=AlertSeverity.ERROR,
            description="High memory utilization"
        )
    
    def record_metric(self, name: str, value: float, metric_type: MetricType,
                     tags: Dict[str, str] = None, dimensions: Dict[str, Any] = None):
        """Record a metric value"""
        metric = Metric(
            name=name,
            metric_type=metric_type,
            value=value,
            timestamp=datetime.utcnow(),
            tags=tags or {},
            dimensions=dimensions or {}
        )
        
        self.metrics_buffer.append(metric)
        
        # Check alert rules
        self._check_alert_rules(metric)
        
        # Update aggregations
        self._update_aggregations(metric)
    
    def add_alert_rule(self, metric_name: str, threshold: float, comparison: str,
                      severity: AlertSeverity, description: str, 
                      evaluation_window: int = 300):  # 5 minutes
        """Add an alert rule for a metric"""
        self.alert_rules[metric_name] = {
            "threshold": threshold,
            "comparison": comparison,
            "severity": severity,
            "description": description,
            "evaluation_window": evaluation_window,
            "last_triggered": None
        }
    
    def _check_alert_rules(self, metric: Metric):
        """Check if metric triggers any alert rules"""
        rule = self.alert_rules.get(metric.name)
        if not rule:
            return
        
        # Get recent metrics for evaluation window
        window_start = datetime.utcnow() - timedelta(seconds=rule["evaluation_window"])
        recent_metrics = [
            m for m in self.metrics_buffer 
            if m.name == metric.name and m.timestamp >= window_start
        ]
        
        if not recent_metrics:
            return
        
        # Calculate evaluation value based on metric type
        if metric.metric_type == MetricType.GAUGE:
            eval_value = metric.value
        elif metric.metric_type in [MetricType.COUNTER, MetricType.TIMER]:
            eval_value = statistics.mean([m.value for m in recent_metrics])
        else:
            eval_value = metric.value
        
        # Check threshold
        should_alert = False
        if rule["comparison"] == "greater_than" and eval_value > rule["threshold"]:
            should_alert = True
        elif rule["comparison"] == "less_than" and eval_value < rule["threshold"]:
            should_alert = True
        elif rule["comparison"] == "equals" and eval_value == rule["threshold"]:
            should_alert = True
        
        if should_alert:
            self._create_alert(metric.name, rule, eval_value)
    
    def _create_alert(self, metric_name: str, rule: Dict[str, Any], current_value: float):
        """Create an alert"""
        import uuid
        
        # Check if similar alert was recently triggered (avoid spam)
        if rule["last_triggered"]:
            time_since_last = datetime.utcnow() - rule["last_triggered"]
            if time_since_last.total_seconds() < 300:  # 5 minutes cooldown
                return
        
        alert = Alert(
            alert_id=str(uuid.uuid4()),
            metric_name=metric_name,
            severity=rule["severity"],
            threshold=rule["threshold"],
            current_value=current_value,
            message=rule["description"],
            timestamp=datetime.utcnow()
        )
        
        self.alerts.append(alert)
        rule["last_triggered"] = datetime.utcnow()
        
        # In production, this would send notifications
        print(f"ALERT: {alert.severity.value.upper()} - {alert.message} (Current: {current_value}, Threshold: {rule['threshold']})")
    
    def _update_aggregations(self, metric: Metric):
        """Update metric aggregations for dashboards"""
        if metric.name not in self.metric_aggregations:
            self.metric_aggregations[metric.name] = {
                "recent_values": [],
                "hourly_avg": 0,
                "daily_avg": 0,
                "min_value": float('inf'),
                "max_value": float('-inf')
            }
        
        aggregation = self.metric_aggregations[metric.name]
        
        # Update recent values (keep last 100)
        aggregation["recent_values"].append(metric.value)
        if len(aggregation["recent_values"]) > 100:
            aggregation["recent_values"].pop(0)
        
        # Update min/max
        aggregation["min_value"] = min(aggregation["min_value"], metric.value)
        aggregation["max_value"] = max(aggregation["max_value"], metric.value)
        
        # Calculate averages
        if aggregation["recent_values"]:
            aggregation["current_avg"] = statistics.mean(aggregation["recent_values"])
    
    def get_metrics_summary(self, time_range: int = 3600) -> Dict[str, Any]:
        """Get metrics summary for specified time range (seconds)"""
        cutoff_time = datetime.utcnow() - timedelta(seconds=time_range)
        recent_metrics = [m for m in self.metrics_buffer if m.timestamp >= cutoff_time]
        
        summary = {
            "time_range_seconds": time_range,
            "total_metrics": len(recent_metrics),
            "unique_metrics": len(set(m.name for m in recent_metrics)),
            "active_alerts": len([a for a in self.alerts if not a.acknowledged]),
            "metric_breakdown": {}
        }
        
        # Group by metric name
        for metric in recent_metrics:
            if metric.name not in summary["metric_breakdown"]:
                summary["metric_breakdown"][metric.name] = {
                    "count": 0,
                    "avg_value": 0,
                    "min_value": float('inf'),
                    "max_value": float('-inf'),
                    "latest_value": 0
                }
            
            breakdown = summary["metric_breakdown"][metric.name]
            breakdown["count"] += 1
            breakdown["min_value"] = min(breakdown["min_value"], metric.value)
            breakdown["max_value"] = max(breakdown["max_value"], metric.value)
            breakdown["latest_value"] = metric.value
        
        # Calculate averages
        for metric_name, breakdown in summary["metric_breakdown"].items():
            metric_values = [m.value for m in recent_metrics if m.name == metric_name]
            breakdown["avg_value"] = statistics.mean(metric_values) if metric_values else 0
        
        return summary

# AI-specific metrics collector
class AIMetricsCollector:
    def __init__(self, monitoring_system: AIMonitoringSystem):
        self.monitoring = monitoring_system
        self.model_sessions = {}
        self.performance_baselines = {}
    
    async def track_model_request(self, model_name: str, request_data: Dict[str, Any]) -> str:
        """Start tracking a model request"""
        import uuid
        import time
        
        session_id = str(uuid.uuid4())
        
        self.model_sessions[session_id] = {
            "model_name": model_name,
            "start_time": time.time(),
            "request_size": len(str(request_data)),
            "input_tokens": request_data.get("input_tokens", 0),
            "status": "in_progress"
        }
        
        # Record request metric
        self.monitoring.record_metric(
            "model_requests_total",
            1,
            MetricType.COUNTER,
            tags={"model_name": model_name}
        )
        
        return session_id
    
    async def complete_model_request(self, session_id: str, response_data: Dict[str, Any],
                                   error: Optional[str] = None):
        """Complete tracking of a model request"""
        import time
        
        if session_id not in self.model_sessions:
            return
        
        session = self.model_sessions[session_id]
        end_time = time.time()
        duration_ms = (end_time - session["start_time"]) * 1000
        
        session.update({
            "end_time": end_time,
            "duration_ms": duration_ms,
            "output_tokens": response_data.get("output_tokens", 0),
            "response_size": len(str(response_data)),
            "error": error,
            "status": "error" if error else "completed"
        })
        
        model_name = session["model_name"]
        
        # Record performance metrics
        self.monitoring.record_metric(
            "model_response_time",
            duration_ms,
            MetricType.TIMER,
            tags={"model_name": model_name, "status": session["status"]}
        )
        
        # Record token usage
        total_tokens = session["input_tokens"] + session["output_tokens"]
        self.monitoring.record_metric(
            "model_tokens_used",
            total_tokens,
            MetricType.COUNTER,
            tags={"model_name": model_name}
        )
        
        # Record error rate
        if error:
            self.monitoring.record_metric(
                "model_errors_total",
                1,
                MetricType.COUNTER,
                tags={"model_name": model_name, "error_type": type(error).__name__}
            )
        
        # Calculate error rate
        recent_sessions = [
            s for s in self.model_sessions.values()
            if s["model_name"] == model_name and s["status"] in ["completed", "error"]
            and (end_time - s["end_time"]) < 300  # Last 5 minutes
        ]
        
        if recent_sessions:
            error_count = len([s for s in recent_sessions if s["status"] == "error"])
            error_rate = error_count / len(recent_sessions)
            
            self.monitoring.record_metric(
                "model_error_rate",
                error_rate,
                MetricType.GAUGE,
                tags={"model_name": model_name}
            )
        
        # Clean up old sessions
        del self.model_sessions[session_id]
    
    def track_model_quality(self, model_name: str, quality_metrics: Dict[str, float]):
        """Track model quality metrics"""
        for metric_name, value in quality_metrics.items():
            self.monitoring.record_metric(
                f"model_quality_{metric_name}",
                value,
                MetricType.GAUGE,
                tags={"model_name": model_name}
            )
    
    def track_resource_usage(self, resource_metrics: Dict[str, float]):
        """Track infrastructure resource usage"""
        for resource, value in resource_metrics.items():
            self.monitoring.record_metric(
                f"resource_{resource}",
                value,
                MetricType.GAUGE
            )
    
    def get_model_performance_report(self, model_name: str, time_range: int = 3600) -> Dict[str, Any]:
        """Generate performance report for a specific model"""
        cutoff_time = datetime.utcnow() - timedelta(seconds=time_range)
        
        # Get relevant sessions
        model_sessions = [
            s for s in self.model_sessions.values()
            if s["model_name"] == model_name and s.get("end_time")
            and datetime.fromtimestamp(s["end_time"]) >= cutoff_time
        ]
        
        if not model_sessions:
            return {"model_name": model_name, "no_data": True}
        
        # Calculate statistics
        response_times = [s["duration_ms"] for s in model_sessions if s["status"] == "completed"]
        error_sessions = [s for s in model_sessions if s["status"] == "error"]
        
        report = {
            "model_name": model_name,
            "time_range_seconds": time_range,
            "total_requests": len(model_sessions),
            "successful_requests": len(response_times),
            "failed_requests": len(error_sessions),
            "error_rate": len(error_sessions) / len(model_sessions) if model_sessions else 0
        }
        
        if response_times:
            report.update({
                "avg_response_time_ms": statistics.mean(response_times),
                "p50_response_time_ms": statistics.median(response_times),
                "p95_response_time_ms": self._percentile(response_times, 0.95),
                "p99_response_time_ms": self._percentile(response_times, 0.99),
                "min_response_time_ms": min(response_times),
                "max_response_time_ms": max(response_times)
            })
        
        # Token usage statistics
        total_input_tokens = sum(s["input_tokens"] for s in model_sessions)
        total_output_tokens = sum(s["output_tokens"] for s in model_sessions)
        
        report.update({
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "avg_tokens_per_request": (total_input_tokens + total_output_tokens) / len(model_sessions)
        })
        
        return report
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile of data"""
        if not data:
            return 0
        
        sorted_data = sorted(data)
        index = int(percentile * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]
```

---

## 2. Performance Optimization Framework

### Automated Performance Analysis

```python
from typing import Dict, List, Any, Tuple, Optional
import asyncio
import statistics
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class PerformanceBaseline:
    metric_name: str
    baseline_value: float
    baseline_date: datetime
    confidence_interval: Tuple[float, float]
    sample_size: int

@dataclass
class OptimizationRecommendation:
    category: str
    priority: str
    description: str
    expected_improvement: float
    implementation_effort: str
    estimated_cost_impact: float

class PerformanceOptimizer:
    def __init__(self, metrics_collector: AIMetricsCollector):
        self.metrics_collector = metrics_collector
        self.baselines = {}
        self.optimization_history = []
        self.cost_tracker = {}
    
    def establish_baseline(self, model_name: str, time_range: int = 86400):  # 24 hours
        """Establish performance baseline for a model"""
        report = self.metrics_collector.get_model_performance_report(model_name, time_range)
        
        if report.get("no_data"):
            return None
        
        baseline = PerformanceBaseline(
            metric_name=f"{model_name}_performance",
            baseline_value=report["avg_response_time_ms"],
            baseline_date=datetime.utcnow(),
            confidence_interval=(
                report["p5_response_time_ms"] if "p5_response_time_ms" in report else report["min_response_time_ms"],
                report["p95_response_time_ms"]
            ),
            sample_size=report["total_requests"]
        )
        
        self.baselines[model_name] = baseline
        return baseline
    
    def analyze_performance_degradation(self, model_name: str) -> Dict[str, Any]:
        """Analyze if performance has degraded compared to baseline"""
        baseline = self.baselines.get(model_name)
        if not baseline:
            return {"error": "No baseline established"}
        
        current_report = self.metrics_collector.get_model_performance_report(model_name, 3600)  # Last hour
        
        if current_report.get("no_data"):
            return {"error": "No recent data available"}
        
        analysis = {
            "model_name": model_name,
            "baseline_date": baseline.baseline_date.isoformat(),
            "current_avg_response_time": current_report["avg_response_time_ms"],
            "baseline_avg_response_time": baseline.baseline_value,
            "performance_change_percent": 0,
            "degradation_detected": False,
            "recommendations": []
        }
        
        # Calculate performance change
        current_avg = current_report["avg_response_time_ms"]
        baseline_avg = baseline.baseline_value
        
        if baseline_avg > 0:
            change_percent = ((current_avg - baseline_avg) / baseline_avg) * 100
            analysis["performance_change_percent"] = change_percent
            
            # Consider degradation if >20% slower
            if change_percent > 20:
                analysis["degradation_detected"] = True
                analysis["recommendations"] = self._generate_performance_recommendations(
                    model_name, current_report, baseline
                )
        
        return analysis
    
    def _generate_performance_recommendations(self, model_name: str, 
                                           current_report: Dict[str, Any],
                                           baseline: PerformanceBaseline) -> List[OptimizationRecommendation]:
        """Generate optimization recommendations"""
        recommendations = []
        
        # High response time recommendation
        if current_report["avg_response_time_ms"] > 3000:  # 3 seconds
            recommendations.append(OptimizationRecommendation(
                category="model_optimization",
                priority="high",
                description="Consider reducing max_tokens or temperature to improve response time",
                expected_improvement=0.25,  # 25% improvement
                implementation_effort="low",
                estimated_cost_impact=0.0
            ))
        
        # High error rate recommendation
        if current_report["error_rate"] > 0.05:  # 5%
            recommendations.append(OptimizationRecommendation(
                category="reliability",
                priority="critical",
                description="Investigate and fix high error rate",
                expected_improvement=0.90,  # 90% error reduction
                implementation_effort="medium",
                estimated_cost_impact=0.0
            ))
        
        # Token usage optimization
        avg_tokens = current_report["avg_tokens_per_request"]
        if avg_tokens > 1500:
            recommendations.append(OptimizationRecommendation(
                category="cost_optimization",
                priority="medium",
                description="Optimize prompts to reduce token usage",
                expected_improvement=0.30,  # 30% token reduction
                implementation_effort="medium",
                estimated_cost_impact=-0.30  # 30% cost reduction
            ))
        
        # Scaling recommendation
        p99_response_time = current_report.get("p99_response_time_ms", 0)
        if p99_response_time > 10000:  # 10 seconds
            recommendations.append(OptimizationRecommendation(
                category="infrastructure",
                priority="high",
                description="Consider increasing model deployment capacity",
                expected_improvement=0.40,  # 40% improvement
                implementation_effort="low",
                estimated_cost_impact=0.50  # 50% cost increase
            ))
        
        return recommendations
    
    def optimize_model_configuration(self, model_name: str, 
                                   current_config: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest optimized model configuration"""
        performance_report = self.metrics_collector.get_model_performance_report(model_name)
        
        if performance_report.get("no_data"):
            return current_config
        
        optimized_config = current_config.copy()
        optimizations_applied = []
        
        # Optimize temperature based on response quality and speed
        current_temp = current_config.get("temperature", 0.7)
        avg_response_time = performance_report["avg_response_time_ms"]
        
        if avg_response_time > 5000:  # Slow responses
            new_temp = max(0.1, current_temp - 0.2)
            optimized_config["temperature"] = new_temp
            optimizations_applied.append(f"Reduced temperature from {current_temp} to {new_temp} for faster responses")
        
        # Optimize max_tokens based on usage patterns
        current_max_tokens = current_config.get("max_tokens", 1000)
        avg_output_tokens = performance_report["total_output_tokens"] / max(performance_report["total_requests"], 1)
        
        if avg_output_tokens < current_max_tokens * 0.5:  # Using less than 50% of allowed tokens
            new_max_tokens = int(avg_output_tokens * 1.5)  # 50% buffer
            optimized_config["max_tokens"] = new_max_tokens
            optimizations_applied.append(f"Reduced max_tokens from {current_max_tokens} to {new_max_tokens}")
        
        # Add caching if high repeat patterns
        if not current_config.get("enable_caching", False):
            # In production, would analyze request patterns
            optimized_config["enable_caching"] = True
            optimizations_applied.append("Enabled response caching for better performance")
        
        return {
            "optimized_config": optimized_config,
            "optimizations_applied": optimizations_applied,
            "estimated_improvements": {
                "response_time_improvement": "10-30%",
                "cost_reduction": "15-25%",
                "reliability_improvement": "5-10%"
            }
        }

# Cost optimization module
class CostOptimizer:
    def __init__(self, metrics_collector: AIMetricsCollector):
        self.metrics_collector = metrics_collector
        self.cost_models = self._setup_cost_models()
        self.usage_patterns = {}
    
    def _setup_cost_models(self) -> Dict[str, Dict[str, float]]:
        """Setup cost models for different Azure AI services"""
        return {
            "gpt-4": {
                "input_token_cost": 0.00003,  # $0.03 per 1K tokens
                "output_token_cost": 0.00006,  # $0.06 per 1K tokens
                "deployment_cost_per_hour": 0.50
            },
            "gpt-35-turbo": {
                "input_token_cost": 0.0000015,  # $0.0015 per 1K tokens
                "output_token_cost": 0.000002,   # $0.002 per 1K tokens
                "deployment_cost_per_hour": 0.10
            }
        }
    
    def calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int,
                      deployment_hours: float = 1.0) -> Dict[str, float]:
        """Calculate cost for model usage"""
        cost_model = self.cost_models.get(model_name, self.cost_models["gpt-4"])
        
        input_cost = (input_tokens / 1000) * cost_model["input_token_cost"]
        output_cost = (output_tokens / 1000) * cost_model["output_token_cost"]
        deployment_cost = deployment_hours * cost_model["deployment_cost_per_hour"]
        
        return {
            "input_token_cost": input_cost,
            "output_token_cost": output_cost,
            "deployment_cost": deployment_cost,
            "total_cost": input_cost + output_cost + deployment_cost
        }
    
    def analyze_cost_trends(self, model_name: str, days: int = 7) -> Dict[str, Any]:
        """Analyze cost trends over time"""
        # Get usage data for the period
        daily_costs = []
        
        for day in range(days):
            day_start = datetime.utcnow() - timedelta(days=day+1)
            day_end = day_start + timedelta(days=1)
            
            # Calculate daily usage and cost
            # In production, this would query actual usage data
            daily_usage = {
                "date": day_start.date().isoformat(),
                "input_tokens": 50000 + (day * 5000),  # Simulated data
                "output_tokens": 25000 + (day * 2500),
                "deployment_hours": 24
            }
            
            daily_cost = self.calculate_cost(
                model_name,
                daily_usage["input_tokens"],
                daily_usage["output_tokens"],
                daily_usage["deployment_hours"]
            )
            
            daily_costs.append({
                "date": daily_usage["date"],
                "total_cost": daily_cost["total_cost"],
                "token_cost": daily_cost["input_token_cost"] + daily_cost["output_token_cost"],
                "deployment_cost": daily_cost["deployment_cost"]
            })
        
        # Calculate trends
        total_costs = [d["total_cost"] for d in daily_costs]
        avg_daily_cost = statistics.mean(total_costs)
        
        # Calculate trend (simple linear regression slope)
        days_list = list(range(len(total_costs)))
        if len(total_costs) > 1:
            slope = (statistics.mean([d * c for d, c in zip(days_list, total_costs)]) - 
                    statistics.mean(days_list) * statistics.mean(total_costs)) / \
                   (statistics.mean([d * d for d in days_list]) - statistics.mean(days_list) ** 2)
            trend_direction = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
        else:
            trend_direction = "stable"
        
        return {
            "model_name": model_name,
            "period_days": days,
            "total_cost": sum(total_costs),
            "avg_daily_cost": avg_daily_cost,
            "trend_direction": trend_direction,
            "daily_breakdown": daily_costs,
            "optimization_opportunities": self._identify_cost_optimizations(daily_costs, model_name)
        }
    
    def _identify_cost_optimizations(self, daily_costs: List[Dict[str, Any]], 
                                   model_name: str) -> List[Dict[str, Any]]:
        """Identify cost optimization opportunities"""
        opportunities = []
        
        # Check if deployment costs are high relative to usage
        avg_deployment_cost = statistics.mean([d["deployment_cost"] for d in daily_costs])
        avg_token_cost = statistics.mean([d["token_cost"] for d in daily_costs])
        
        if avg_deployment_cost > avg_token_cost * 2:  # Deployment cost > 2x token cost
            opportunities.append({
                "type": "deployment_optimization",
                "description": "Consider using pay-per-call pricing instead of dedicated deployment",
                "potential_savings": avg_deployment_cost * 0.6,  # 60% savings estimate
                "implementation": "Switch to consumption-based pricing model"
            })
        
        # Check for usage spikes that could benefit from autoscaling
        daily_total_costs = [d["total_cost"] for d in daily_costs]
        if max(daily_total_costs) > statistics.mean(daily_total_costs) * 2:
            opportunities.append({
                "type": "autoscaling",
                "description": "Implement autoscaling to handle usage spikes efficiently",
                "potential_savings": max(daily_total_costs) * 0.3,  # 30% savings on spike days
                "implementation": "Configure autoscaling rules based on request volume"
            })
        
        # Check for consistent unused capacity
        if all(d["deployment_cost"] > d["token_cost"] for d in daily_costs):
            opportunities.append({
                "type": "rightsizing",
                "description": "Reduce deployment capacity to match actual usage",
                "potential_savings": avg_deployment_cost * 0.4,  # 40% savings
                "implementation": "Scale down deployment to match usage patterns"
            })
        
        return opportunities
    
    def generate_cost_optimization_plan(self, model_name: str) -> Dict[str, Any]:
        """Generate comprehensive cost optimization plan"""
        cost_analysis = self.analyze_cost_trends(model_name)
        performance_report = self.metrics_collector.get_model_performance_report(model_name)
        
        plan = {
            "model_name": model_name,
            "current_monthly_cost_estimate": cost_analysis["avg_daily_cost"] * 30,
            "optimization_recommendations": [],
            "implementation_priority": [],
            "expected_savings": 0
        }
        
        # Add cost optimization recommendations
        for opportunity in cost_analysis["optimization_opportunities"]:
            plan["optimization_recommendations"].append({
                "category": "cost",
                "type": opportunity["type"],
                "description": opportunity["description"],
                "potential_monthly_savings": opportunity["potential_savings"] * 30,
                "implementation_effort": "medium"
            })
            plan["expected_savings"] += opportunity["potential_savings"] * 30
        
        # Add performance-based optimizations
        if not performance_report.get("no_data"):
            if performance_report["avg_tokens_per_request"] > 1000:
                plan["optimization_recommendations"].append({
                    "category": "efficiency",
                    "type": "prompt_optimization",
                    "description": "Optimize prompts to reduce token usage",
                    "potential_monthly_savings": cost_analysis["avg_daily_cost"] * 30 * 0.2,
                    "implementation_effort": "low"
                })
                plan["expected_savings"] += cost_analysis["avg_daily_cost"] * 30 * 0.2
        
        # Prioritize recommendations
        plan["implementation_priority"] = sorted(
            plan["optimization_recommendations"],
            key=lambda x: x["potential_monthly_savings"] / (1 if x["implementation_effort"] == "low" 
                                                           else 2 if x["implementation_effort"] == "medium" 
                                                           else 3),
            reverse=True
        )
        
        return plan
```

---

## Summary

In this lesson, we've covered:

✅ **Comprehensive Monitoring**: Multi-dimensional monitoring strategy with metrics, alerts, and dashboards
✅ **AI-Specific Metrics**: Model performance tracking, token usage, and quality metrics
✅ **Performance Analysis**: Automated baseline establishment and degradation detection
✅ **Optimization Framework**: Automated recommendations for configuration and infrastructure
✅ **Cost Optimization**: Cost tracking, trend analysis, and optimization planning
✅ **Observability Strategy**: Proactive monitoring and alerting for AI applications

## Next Steps

In the next lesson, we'll explore **Advanced Deployment Strategies**, where you'll learn about blue-green deployments, canary releases, multi-region strategies, and sophisticated rollback mechanisms for AI applications.

## Additional Resources

- [Azure Monitor Documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/)
- [Application Insights for AI Applications](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)
- [Azure Cost Management](https://docs.microsoft.com/en-us/azure/cost-management-billing/)
- [Performance Optimization Best Practices](https://docs.microsoft.com/en-us/azure/architecture/framework/performance-efficiency/)

---

*This lesson provides the monitoring and optimization foundation needed to maintain high-performing, cost-effective AI applications in production.* 