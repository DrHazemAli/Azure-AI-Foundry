# Monitoring and Optimization

## Overview

This lesson covers essential monitoring and optimization strategies for Azure AI Foundry applications, including performance tracking, cost management, error handling, and continuous improvement techniques.

## Learning Objectives

- Set up comprehensive monitoring for AI applications
- Implement performance tracking and analytics
- Configure alerting and notification systems
- Optimize costs and resource utilization
- Handle errors and implement retry strategies
- Establish continuous improvement processes

## Prerequisites

- Completed basic customization and configuration (Lesson 07)
- Deployed AI application in production or staging
- Understanding of application performance concepts

---

## 1. Performance Monitoring

### Application Performance Metrics

```python
import time
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import json

class MetricType(Enum):
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    TOKEN_USAGE = "token_usage"
    COST = "cost"
    USER_SATISFACTION = "user_satisfaction"

@dataclass
class PerformanceMetric:
    metric_type: MetricType
    value: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

class PerformanceMonitor:
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.session_data: Dict[str, Dict] = {}
        self.logger = logging.getLogger(__name__)
    
    def track_request_latency(self, start_time: float, end_time: float, session_id: str):
        """Track request latency."""
        latency_ms = (end_time - start_time) * 1000
        
        metric = PerformanceMetric(
            metric_type=MetricType.LATENCY,
            value=latency_ms,
            timestamp=datetime.now(),
            metadata={"session_id": session_id}
        )
        
        self.metrics.append(metric)
        self.logger.info(f"Request latency: {latency_ms:.2f}ms")
    
    def track_token_usage(self, input_tokens: int, output_tokens: int, session_id: str):
        """Track token consumption."""
        total_tokens = input_tokens + output_tokens
        
        metric = PerformanceMetric(
            metric_type=MetricType.TOKEN_USAGE,
            value=total_tokens,
            timestamp=datetime.now(),
            metadata={
                "session_id": session_id,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens
            }
        )
        
        self.metrics.append(metric)
        self.logger.info(f"Token usage: {total_tokens} (input: {input_tokens}, output: {output_tokens})")
    
    def track_error(self, error_type: str, error_message: str, session_id: str):
        """Track application errors."""
        metric = PerformanceMetric(
            metric_type=MetricType.ERROR_RATE,
            value=1.0,  # Error count
            timestamp=datetime.now(),
            metadata={
                "session_id": session_id,
                "error_type": error_type,
                "error_message": error_message
            }
        )
        
        self.metrics.append(metric)
        self.logger.error(f"Error tracked: {error_type} - {error_message}")
    
    def get_performance_summary(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get performance summary for the specified time window."""
        
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
        recent_metrics = [m for m in self.metrics if m.timestamp >= cutoff_time]
        
        summary = {
            "time_window": f"{time_window_hours} hours",
            "total_requests": len([m for m in recent_metrics if m.metric_type == MetricType.LATENCY]),
            "average_latency_ms": 0,
            "total_tokens": 0,
            "error_count": 0,
            "error_rate_percent": 0
        }
        
        # Calculate average latency
        latency_metrics = [m for m in recent_metrics if m.metric_type == MetricType.LATENCY]
        if latency_metrics:
            summary["average_latency_ms"] = sum(m.value for m in latency_metrics) / len(latency_metrics)
        
        # Calculate total token usage
        token_metrics = [m for m in recent_metrics if m.metric_type == MetricType.TOKEN_USAGE]
        summary["total_tokens"] = sum(m.value for m in token_metrics)
        
        # Calculate error rate
        error_metrics = [m for m in recent_metrics if m.metric_type == MetricType.ERROR_RATE]
        summary["error_count"] = len(error_metrics)
        
        if summary["total_requests"] > 0:
            summary["error_rate_percent"] = (summary["error_count"] / summary["total_requests"]) * 100
        
        return summary
    
    def export_metrics(self, filename: str = None) -> str:
        """Export metrics to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_metrics_{timestamp}.json"
        
        metrics_data = []
        for metric in self.metrics:
            metrics_data.append({
                "type": metric.metric_type.value,
                "value": metric.value,
                "timestamp": metric.timestamp.isoformat(),
                "metadata": metric.metadata
            })
        
        with open(filename, 'w') as f:
            json.dump(metrics_data, f, indent=2)
        
        return filename

# Example usage with Azure AI Foundry client
class MonitoredAIClient:
    def __init__(self, ai_client, monitor: PerformanceMonitor):
        self.ai_client = ai_client
        self.monitor = monitor
    
    async def send_message_with_monitoring(self, message: str, session_id: str) -> str:
        """Send message with comprehensive monitoring."""
        
        start_time = time.time()
        
        try:
            # Make the AI request
            response = await self.ai_client.send_message(message)
            
            end_time = time.time()
            
            # Track latency
            self.monitor.track_request_latency(start_time, end_time, session_id)
            
            # Track token usage (if available in response)
            if hasattr(response, 'usage'):
                self.monitor.track_token_usage(
                    response.usage.prompt_tokens,
                    response.usage.completion_tokens,
                    session_id
                )
            
            return response.content
            
        except Exception as e:
            end_time = time.time()
            
            # Track error
            self.monitor.track_error(
                error_type=type(e).__name__,
                error_message=str(e),
                session_id=session_id
            )
            
            # Still track latency for failed requests
            self.monitor.track_request_latency(start_time, end_time, session_id)
            
            raise e

# Usage example
monitor = PerformanceMonitor()
# monitored_client = MonitoredAIClient(your_ai_client, monitor)
```

---

## 2. Cost Monitoring and Optimization

### Cost Tracking System

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

@dataclass
class CostEntry:
    timestamp: datetime
    model_name: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    session_id: str
    user_id: Optional[str] = None

class CostTracker:
    def __init__(self):
        self.cost_entries: List[CostEntry] = []
        self.pricing_table = {
            "gpt-4": {"input": 0.03, "output": 0.06},  # per 1K tokens
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "claude-3": {"input": 0.015, "output": 0.075}
        }
    
    def calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for a request."""
        
        if model_name not in self.pricing_table:
            # Default to GPT-4 pricing if model not found
            model_name = "gpt-4"
        
        pricing = self.pricing_table[model_name]
        
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        
        return input_cost + output_cost
    
    def track_usage(self, model_name: str, input_tokens: int, output_tokens: int, 
                   session_id: str, user_id: Optional[str] = None) -> float:
        """Track usage and calculate cost."""
        
        cost = self.calculate_cost(model_name, input_tokens, output_tokens)
        
        entry = CostEntry(
            timestamp=datetime.now(),
            model_name=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            session_id=session_id,
            user_id=user_id
        )
        
        self.cost_entries.append(entry)
        return cost
    
    def get_cost_summary(self, days: int = 30) -> Dict:
        """Get cost summary for specified period."""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_entries = [e for e in self.cost_entries if e.timestamp >= cutoff_date]
        
        summary = {
            "period_days": days,
            "total_cost_usd": sum(e.cost_usd for e in recent_entries),
            "total_requests": len(recent_entries),
            "total_tokens": sum(e.input_tokens + e.output_tokens for e in recent_entries),
            "cost_by_model": {},
            "cost_by_day": {},
            "average_cost_per_request": 0
        }
        
        # Cost by model
        for entry in recent_entries:
            if entry.model_name not in summary["cost_by_model"]:
                summary["cost_by_model"][entry.model_name] = 0
            summary["cost_by_model"][entry.model_name] += entry.cost_usd
        
        # Cost by day
        for entry in recent_entries:
            day_key = entry.timestamp.strftime("%Y-%m-%d")
            if day_key not in summary["cost_by_day"]:
                summary["cost_by_day"][day_key] = 0
            summary["cost_by_day"][day_key] += entry.cost_usd
        
        # Average cost per request
        if recent_entries:
            summary["average_cost_per_request"] = summary["total_cost_usd"] / len(recent_entries)
        
        return summary
    
    def get_optimization_recommendations(self) -> List[Dict]:
        """Generate cost optimization recommendations."""
        
        summary = self.get_cost_summary(30)
        recommendations = []
        
        # High-cost model recommendation
        if summary["cost_by_model"]:
            most_expensive_model = max(summary["cost_by_model"].items(), key=lambda x: x[1])
            
            if most_expensive_model[1] > summary["total_cost_usd"] * 0.5:
                recommendations.append({
                    "type": "model_optimization",
                    "title": "Consider Model Alternatives",
                    "description": f"{most_expensive_model[0]} accounts for {(most_expensive_model[1]/summary['total_cost_usd'])*100:.1f}% of costs",
                    "suggestion": "Evaluate if a less expensive model can meet your requirements",
                    "potential_savings": f"${most_expensive_model[1] * 0.3:.2f}/month"
                })
        
        # High token usage recommendation
        avg_tokens = summary["total_tokens"] / max(summary["total_requests"], 1)
        if avg_tokens > 1000:
            recommendations.append({
                "type": "token_optimization",
                "title": "Optimize Prompt Length",
                "description": f"Average tokens per request: {avg_tokens:.0f}",
                "suggestion": "Review prompts to reduce unnecessary context and improve efficiency",
                "potential_savings": f"${summary['total_cost_usd'] * 0.2:.2f}/month"
            })
        
        # Usage pattern recommendation
        daily_costs = list(summary["cost_by_day"].values())
        if daily_costs:
            cost_variance = max(daily_costs) - min(daily_costs)
            if cost_variance > summary["total_cost_usd"] * 0.1:
                recommendations.append({
                    "type": "usage_pattern",
                    "title": "Consider Usage-Based Scaling",
                    "description": "High variance in daily usage detected",
                    "suggestion": "Implement auto-scaling or scheduled resources to match usage patterns",
                    "potential_savings": f"${cost_variance * 0.3:.2f}/month"
                })
        
        return recommendations

# Example usage
cost_tracker = CostTracker()

# Track a request
cost = cost_tracker.track_usage("gpt-4", 150, 300, "session_123", "user_456")
print(f"Request cost: ${cost:.4f}")

# Get cost summary
summary = cost_tracker.get_cost_summary(7)  # Last 7 days
print(f"Weekly cost: ${summary['total_cost_usd']:.2f}")

# Get optimization recommendations
recommendations = cost_tracker.get_optimization_recommendations()
for rec in recommendations:
    print(f"💡 {rec['title']}: {rec['suggestion']}")
```

---

## 3. Error Handling and Retry Strategies

### Robust Error Handling System

```python
import asyncio
import random
from typing import Any, Callable, Optional, Union
from enum import Enum
from dataclasses import dataclass
import logging

class ErrorType(Enum):
    RATE_LIMIT = "rate_limit"
    NETWORK_ERROR = "network_error"
    SERVICE_UNAVAILABLE = "service_unavailable"
    AUTHENTICATION_ERROR = "authentication_error"
    VALIDATION_ERROR = "validation_error"
    UNKNOWN_ERROR = "unknown_error"

@dataclass
class RetryConfig:
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_backoff: bool = True
    jitter: bool = True

class ErrorHandler:
    def __init__(self, retry_config: RetryConfig = None):
        self.retry_config = retry_config or RetryConfig()
        self.logger = logging.getLogger(__name__)
        
        # Define which errors should be retried
        self.retryable_errors = {
            ErrorType.RATE_LIMIT,
            ErrorType.NETWORK_ERROR,
            ErrorType.SERVICE_UNAVAILABLE
        }
    
    def classify_error(self, exception: Exception) -> ErrorType:
        """Classify the type of error based on exception."""
        
        error_message = str(exception).lower()
        
        if "rate limit" in error_message or "429" in error_message:
            return ErrorType.RATE_LIMIT
        elif "network" in error_message or "connection" in error_message:
            return ErrorType.NETWORK_ERROR
        elif "503" in error_message or "service unavailable" in error_message:
            return ErrorType.SERVICE_UNAVAILABLE
        elif "401" in error_message or "authentication" in error_message:
            return ErrorType.AUTHENTICATION_ERROR
        elif "400" in error_message or "validation" in error_message:
            return ErrorType.VALIDATION_ERROR
        else:
            return ErrorType.UNKNOWN_ERROR
    
    def should_retry(self, error_type: ErrorType, attempt: int) -> bool:
        """Determine if an error should be retried."""
        
        if attempt >= self.retry_config.max_attempts:
            return False
        
        return error_type in self.retryable_errors
    
    def calculate_delay(self, attempt: int, error_type: ErrorType) -> float:
        """Calculate delay before retry."""
        
        if self.retry_config.exponential_backoff:
            delay = self.retry_config.base_delay * (2 ** attempt)
        else:
            delay = self.retry_config.base_delay
        
        # Special handling for rate limits
        if error_type == ErrorType.RATE_LIMIT:
            delay *= 2  # Longer delay for rate limits
        
        # Apply maximum delay
        delay = min(delay, self.retry_config.max_delay)
        
        # Add jitter to avoid thundering herd
        if self.retry_config.jitter:
            delay += random.uniform(0, delay * 0.1)
        
        return delay
    
    async def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function with retry logic."""
        
        last_exception = None
        
        for attempt in range(self.retry_config.max_attempts):
            try:
                result = await func(*args, **kwargs)
                
                if attempt > 0:
                    self.logger.info(f"Function succeeded on attempt {attempt + 1}")
                
                return result
                
            except Exception as e:
                last_exception = e
                error_type = self.classify_error(e)
                
                self.logger.warning(f"Attempt {attempt + 1} failed: {error_type.value} - {str(e)}")
                
                if not self.should_retry(error_type, attempt):
                    self.logger.error(f"Not retrying error type: {error_type.value}")
                    break
                
                if attempt < self.retry_config.max_attempts - 1:
                    delay = self.calculate_delay(attempt, error_type)
                    self.logger.info(f"Retrying in {delay:.2f} seconds...")
                    await asyncio.sleep(delay)
        
        # All retries exhausted
        self.logger.error(f"All retry attempts exhausted. Last error: {last_exception}")
        raise last_exception

class ResilientAIClient:
    def __init__(self, ai_client, error_handler: ErrorHandler = None):
        self.ai_client = ai_client
        self.error_handler = error_handler or ErrorHandler()
        self.logger = logging.getLogger(__name__)
    
    async def send_message_with_retry(self, message: str, **kwargs) -> str:
        """Send message with automatic retry logic."""
        
        async def _send_message():
            return await self.ai_client.send_message(message, **kwargs)
        
        try:
            return await self.error_handler.execute_with_retry(_send_message)
        except Exception as e:
            self.logger.error(f"Failed to send message after all retries: {e}")
            
            # Return a fallback response
            return self._get_fallback_response(e)
    
    def _get_fallback_response(self, error: Exception) -> str:
        """Provide a fallback response when all retries fail."""
        
        error_type = self.error_handler.classify_error(error)
        
        fallback_responses = {
            ErrorType.RATE_LIMIT: "I'm currently experiencing high demand. Please try again in a few moments.",
            ErrorType.NETWORK_ERROR: "I'm having trouble connecting right now. Please check your connection and try again.",
            ErrorType.SERVICE_UNAVAILABLE: "The service is temporarily unavailable. Please try again later.",
            ErrorType.AUTHENTICATION_ERROR: "There's an authentication issue. Please check your credentials.",
            ErrorType.VALIDATION_ERROR: "There seems to be an issue with your request. Please check your input and try again.",
            ErrorType.UNKNOWN_ERROR: "I'm sorry, but I encountered an unexpected error. Please try again."
        }
        
        return fallback_responses.get(error_type, fallback_responses[ErrorType.UNKNOWN_ERROR])

# Example usage
error_handler = ErrorHandler(RetryConfig(max_attempts=5, base_delay=2.0))
# resilient_client = ResilientAIClient(your_ai_client, error_handler)
```

---

## 4. Alerting and Notification System

### Alert Configuration and Management

```python
from dataclasses import dataclass
from typing import List, Dict, Callable, Any
from enum import Enum
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import requests

class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertChannel(Enum):
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"

@dataclass
class AlertRule:
    name: str
    metric_type: MetricType
    threshold_value: float
    comparison: str  # "greater_than", "less_than", "equals"
    severity: AlertSeverity
    channels: List[AlertChannel]
    enabled: bool = True

@dataclass
class Alert:
    rule_name: str
    severity: AlertSeverity
    message: str
    current_value: float
    threshold_value: float
    timestamp: datetime
    metadata: Dict[str, Any]

class AlertManager:
    def __init__(self):
        self.rules: List[AlertRule] = []
        self.alert_history: List[Alert] = []
        self.notification_config = {}
        self.logger = logging.getLogger(__name__)
    
    def add_alert_rule(self, rule: AlertRule):
        """Add an alert rule."""
        self.rules.append(rule)
        self.logger.info(f"Added alert rule: {rule.name}")
    
    def configure_email(self, smtp_server: str, smtp_port: int, username: str, password: str):
        """Configure email notifications."""
        self.notification_config["email"] = {
            "smtp_server": smtp_server,
            "smtp_port": smtp_port,
            "username": username,
            "password": password
        }
    
    def configure_slack(self, webhook_url: str):
        """Configure Slack notifications."""
        self.notification_config["slack"] = {
            "webhook_url": webhook_url
        }
    
    def check_metric_against_rules(self, metric: PerformanceMetric):
        """Check a metric against all alert rules."""
        
        for rule in self.rules:
            if not rule.enabled or rule.metric_type != metric.metric_type:
                continue
            
            if self._evaluate_threshold(metric.value, rule.threshold_value, rule.comparison):
                alert = Alert(
                    rule_name=rule.name,
                    severity=rule.severity,
                    message=f"{rule.name}: {metric.metric_type.value} is {metric.value} (threshold: {rule.threshold_value})",
                    current_value=metric.value,
                    threshold_value=rule.threshold_value,
                    timestamp=metric.timestamp,
                    metadata=metric.metadata
                )
                
                self._trigger_alert(alert, rule.channels)
    
    def _evaluate_threshold(self, current_value: float, threshold: float, comparison: str) -> bool:
        """Evaluate if current value triggers the threshold."""
        
        if comparison == "greater_than":
            return current_value > threshold
        elif comparison == "less_than":
            return current_value < threshold
        elif comparison == "equals":
            return current_value == threshold
        else:
            return False
    
    def _trigger_alert(self, alert: Alert, channels: List[AlertChannel]):
        """Trigger an alert through specified channels."""
        
        self.alert_history.append(alert)
        self.logger.warning(f"ALERT: {alert.message}")
        
        for channel in channels:
            try:
                if channel == AlertChannel.EMAIL:
                    self._send_email_alert(alert)
                elif channel == AlertChannel.SLACK:
                    self._send_slack_alert(alert)
                elif channel == AlertChannel.WEBHOOK:
                    self._send_webhook_alert(alert)
                    
            except Exception as e:
                self.logger.error(f"Failed to send alert via {channel.value}: {e}")
    
    def _send_email_alert(self, alert: Alert):
        """Send alert via email."""
        
        config = self.notification_config.get("email")
        if not config:
            self.logger.warning("Email configuration not found")
            return
        
        msg = MIMEMultipart()
        msg['From'] = config['username']
        msg['To'] = config.get('recipients', ['admin@company.com'])
        msg['Subject'] = f"[{alert.severity.value.upper()}] Azure AI Foundry Alert"
        
        body = f"""
        Alert: {alert.rule_name}
        Severity: {alert.severity.value}
        Message: {alert.message}
        Time: {alert.timestamp}
        Current Value: {alert.current_value}
        Threshold: {alert.threshold_value}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['username'], config['password'])
            server.send_message(msg)
    
    def _send_slack_alert(self, alert: Alert):
        """Send alert via Slack."""
        
        config = self.notification_config.get("slack")
        if not config:
            self.logger.warning("Slack configuration not found")
            return
        
        severity_colors = {
            AlertSeverity.LOW: "#36a64f",
            AlertSeverity.MEDIUM: "#ff9900", 
            AlertSeverity.HIGH: "#ff6600",
            AlertSeverity.CRITICAL: "#ff0000"
        }
        
        payload = {
            "attachments": [{
                "color": severity_colors.get(alert.severity, "#ff0000"),
                "title": f"Azure AI Foundry Alert - {alert.severity.value.upper()}",
                "text": alert.message,
                "fields": [
                    {"title": "Current Value", "value": str(alert.current_value), "short": True},
                    {"title": "Threshold", "value": str(alert.threshold_value), "short": True},
                    {"title": "Time", "value": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S"), "short": False}
                ]
            }]
        }
        
        requests.post(config['webhook_url'], json=payload)
    
    def _send_webhook_alert(self, alert: Alert):
        """Send alert via webhook."""
        
        webhook_url = self.notification_config.get("webhook_url")
        if not webhook_url:
            return
        
        payload = {
            "alert": {
                "rule_name": alert.rule_name,
                "severity": alert.severity.value,
                "message": alert.message,
                "current_value": alert.current_value,
                "threshold_value": alert.threshold_value,
                "timestamp": alert.timestamp.isoformat(),
                "metadata": alert.metadata
            }
        }
        
        requests.post(webhook_url, json=payload)

# Example usage
alert_manager = AlertManager()

# Configure notifications
alert_manager.configure_slack("https://hooks.slack.com/your-webhook-url")

# Add alert rules
high_latency_rule = AlertRule(
    name="High Latency Alert",
    metric_type=MetricType.LATENCY,
    threshold_value=2000.0,  # 2 seconds
    comparison="greater_than",
    severity=AlertSeverity.HIGH,
    channels=[AlertChannel.SLACK, AlertChannel.EMAIL]
)

error_rate_rule = AlertRule(
    name="High Error Rate",
    metric_type=MetricType.ERROR_RATE,
    threshold_value=5.0,  # 5% error rate
    comparison="greater_than",
    severity=AlertSeverity.CRITICAL,
    channels=[AlertChannel.SLACK]
)

alert_manager.add_alert_rule(high_latency_rule)
alert_manager.add_alert_rule(error_rate_rule)
```

---

## Summary

This lesson covered comprehensive monitoring and optimization strategies for Azure AI Foundry applications:

- **Performance Monitoring**: Tracking latency, throughput, token usage, and errors
- **Cost Management**: Monitoring expenses and implementing optimization strategies  
- **Error Handling**: Robust retry mechanisms and fallback strategies
- **Alerting**: Automated notifications through multiple channels

## Next Steps

- Implement monitoring for your AI applications
- Set up cost tracking and optimization
- Configure alerting for critical metrics
- Establish continuous improvement processes
- Complete Module 02 with troubleshooting best practices (Lesson 09)

---

*This lesson is part of the Azure AI Foundry Zero-to-Hero course.* 