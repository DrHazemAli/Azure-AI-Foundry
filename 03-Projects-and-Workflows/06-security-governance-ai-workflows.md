# Lesson 6: Security and Governance in AI Workflows

## Learning Objectives

By the end of this lesson, you will be able to:
- Implement comprehensive security frameworks for AI applications
- Design data governance and protection strategies
- Establish compliance controls for AI systems
- Create audit trails and monitoring for governance
- Implement responsible AI practices and ethical guidelines
- Manage risk assessment and mitigation for AI projects

## Overview

Security and governance are critical aspects of AI development that require specialized approaches due to the sensitive nature of AI models, training data, and the potential impact of AI decisions. This lesson covers comprehensive frameworks for securing AI workflows and ensuring compliance with regulatory requirements.

---

## 1. AI Security Framework

### Multi-Layer Security Architecture

```python
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum
import hashlib
import secrets
from datetime import datetime, timedelta

class SecurityLevel(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class DataClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    SENSITIVE = "sensitive"
    HIGHLY_SENSITIVE = "highly_sensitive"

@dataclass
class SecurityPolicy:
    name: str
    description: str
    security_level: SecurityLevel
    data_classification: DataClassification
    encryption_required: bool
    access_controls: List[str]
    audit_required: bool
    retention_period_days: int

class AISecurityManager:
    def __init__(self):
        self.security_policies = {}
        self.access_logs = []
        self.security_incidents = []
        self._setup_default_policies()
    
    def _setup_default_policies(self):
        """Setup default security policies for AI components"""
        
        # Model security policy
        self.security_policies["ai_models"] = SecurityPolicy(
            name="AI Models Security Policy",
            description="Security policy for AI model artifacts and deployments",
            security_level=SecurityLevel.CONFIDENTIAL,
            data_classification=DataClassification.SENSITIVE,
            encryption_required=True,
            access_controls=["authentication", "authorization", "rate_limiting"],
            audit_required=True,
            retention_period_days=2555  # 7 years
        )
        
        # Training data policy
        self.security_policies["training_data"] = SecurityPolicy(
            name="Training Data Security Policy",
            description="Security policy for AI training datasets",
            security_level=SecurityLevel.RESTRICTED,
            data_classification=DataClassification.HIGHLY_SENSITIVE,
            encryption_required=True,
            access_controls=["authentication", "authorization", "data_loss_prevention"],
            audit_required=True,
            retention_period_days=3650  # 10 years
        )
        
        # API endpoints policy
        self.security_policies["api_endpoints"] = SecurityPolicy(
            name="API Endpoints Security Policy",
            description="Security policy for AI service API endpoints",
            security_level=SecurityLevel.CONFIDENTIAL,
            data_classification=DataClassification.SENSITIVE,
            encryption_required=True,
            access_controls=["authentication", "authorization", "rate_limiting", "input_validation"],
            audit_required=True,
            retention_period_days=365
        )
    
    def evaluate_security_risk(self, resource_type: str, resource_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate security risk for a given resource"""
        policy = self.security_policies.get(resource_type)
        if not policy:
            return {"risk_level": "unknown", "errors": ["No security policy found"]}
        
        risk_assessment = {
            "risk_level": "low",
            "security_controls": [],
            "recommendations": [],
            "compliance_status": True
        }
        
        # Check encryption requirements
        if policy.encryption_required and not resource_metadata.get("encrypted", False):
            risk_assessment["risk_level"] = "high"
            risk_assessment["recommendations"].append("Enable encryption at rest and in transit")
            risk_assessment["compliance_status"] = False
        
        # Check access controls
        for control in policy.access_controls:
            if control not in resource_metadata.get("implemented_controls", []):
                risk_assessment["risk_level"] = "medium" if risk_assessment["risk_level"] == "low" else risk_assessment["risk_level"]
                risk_assessment["recommendations"].append(f"Implement {control}")
        
        # Check data classification
        resource_classification = resource_metadata.get("data_classification")
        if resource_classification != policy.data_classification.value:
            risk_assessment["recommendations"].append(f"Review data classification (current: {resource_classification}, required: {policy.data_classification.value})")
        
        return risk_assessment
    
    def log_access(self, user_id: str, resource_type: str, resource_id: str, 
                  action: str, result: str, metadata: Dict[str, Any] = None):
        """Log access attempts for audit purposes"""
        access_log_entry = {
            "timestamp": datetime.utcnow(),
            "user_id": user_id,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "action": action,
            "result": result,
            "metadata": metadata or {},
            "session_id": self._generate_session_id()
        }
        
        self.access_logs.append(access_log_entry)
        
        # Check for suspicious patterns
        self._detect_suspicious_activity(access_log_entry)
    
    def _generate_session_id(self) -> str:
        """Generate secure session ID"""
        return secrets.token_urlsafe(32)
    
    def _detect_suspicious_activity(self, log_entry: Dict[str, Any]):
        """Detect suspicious access patterns"""
        user_id = log_entry["user_id"]
        recent_logs = [
            log for log in self.access_logs 
            if log["user_id"] == user_id and 
            log["timestamp"] > datetime.utcnow() - timedelta(minutes=10)
        ]
        
        # Check for rapid successive failed attempts
        failed_attempts = [log for log in recent_logs if log["result"] == "failed"]
        if len(failed_attempts) >= 5:
            self._create_security_incident("multiple_failed_attempts", user_id, {
                "failed_attempts": len(failed_attempts),
                "time_window": "10 minutes"
            })
    
    def _create_security_incident(self, incident_type: str, user_id: str, details: Dict[str, Any]):
        """Create security incident for investigation"""
        incident = {
            "incident_id": secrets.token_urlsafe(16),
            "timestamp": datetime.utcnow(),
            "incident_type": incident_type,
            "user_id": user_id,
            "details": details,
            "status": "open",
            "severity": "medium"
        }
        
        self.security_incidents.append(incident)
        
        # In production, this would trigger alerts
        print(f"Security incident created: {incident['incident_id']}")

# Data encryption and protection
class DataProtectionManager:
    def __init__(self, encryption_key: bytes = None):
        self.encryption_key = encryption_key or self._generate_encryption_key()
        self.protected_fields = [
            "personal_data", "training_data", "model_weights", 
            "api_keys", "connection_strings"
        ]
    
    def _generate_encryption_key(self) -> bytes:
        """Generate encryption key for data protection"""
        from cryptography.fernet import Fernet
        return Fernet.generate_key()
    
    def encrypt_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt sensitive fields in data"""
        from cryptography.fernet import Fernet
        
        fernet = Fernet(self.encryption_key)
        encrypted_data = data.copy()
        
        for field in self.protected_fields:
            if field in data and data[field] is not None:
                # Convert to string if not already
                field_value = str(data[field]) if not isinstance(data[field], str) else data[field]
                
                # Encrypt the field
                encrypted_value = fernet.encrypt(field_value.encode())
                encrypted_data[field] = encrypted_value.decode()
                encrypted_data[f"{field}_encrypted"] = True
        
        return encrypted_data
    
    def decrypt_sensitive_data(self, encrypted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt sensitive fields in data"""
        from cryptography.fernet import Fernet
        
        fernet = Fernet(self.encryption_key)
        decrypted_data = encrypted_data.copy()
        
        for field in self.protected_fields:
            if f"{field}_encrypted" in encrypted_data and encrypted_data[f"{field}_encrypted"]:
                try:
                    encrypted_value = encrypted_data[field].encode()
                    decrypted_value = fernet.decrypt(encrypted_value).decode()
                    decrypted_data[field] = decrypted_value
                    decrypted_data[f"{field}_encrypted"] = False
                except Exception as e:
                    print(f"Failed to decrypt field {field}: {e}")
        
        return decrypted_data
    
    def sanitize_logs(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """Remove or mask sensitive data from logs"""
        sanitized_data = log_data.copy()
        
        # Mask sensitive fields
        for field in self.protected_fields:
            if field in sanitized_data:
                if isinstance(sanitized_data[field], str) and len(sanitized_data[field]) > 4:
                    sanitized_data[field] = sanitized_data[field][:2] + "*" * (len(sanitized_data[field]) - 4) + sanitized_data[field][-2:]
                else:
                    sanitized_data[field] = "***MASKED***"
        
        # Remove specific sensitive keys
        sensitive_keys = ["password", "api_key", "secret", "token"]
        for key in list(sanitized_data.keys()):
            if any(sensitive_word in key.lower() for sensitive_word in sensitive_keys):
                sanitized_data[key] = "***REDACTED***"
        
        return sanitized_data

# Input validation and sanitization
class InputValidator:
    def __init__(self):
        self.max_input_length = 10000
        self.blocked_patterns = [
            r'<script[^>]*>.*?</script>',  # XSS
            r'javascript:',                # JavaScript injection
            r'vbscript:',                 # VBScript injection
            r'(?i)(union|select|insert|update|delete|drop|create|alter|exec|execute)',  # SQL injection
        ]
        self.allowed_file_types = ['.txt', '.json', '.csv', '.xlsx', '.pdf']
    
    def validate_text_input(self, input_text: str) -> Dict[str, Any]:
        """Validate text input for security threats"""
        validation_result = {
            "valid": True,
            "issues": [],
            "sanitized_input": input_text
        }
        
        # Check input length
        if len(input_text) > self.max_input_length:
            validation_result["valid"] = False
            validation_result["issues"].append(f"Input too long (max {self.max_input_length} characters)")
        
        # Check for malicious patterns
        import re
        for pattern in self.blocked_patterns:
            if re.search(pattern, input_text, re.IGNORECASE):
                validation_result["valid"] = False
                validation_result["issues"].append(f"Potentially malicious pattern detected")
                break
        
        # Sanitize input
        if validation_result["valid"]:
            validation_result["sanitized_input"] = self._sanitize_input(input_text)
        
        return validation_result
    
    def _sanitize_input(self, input_text: str) -> str:
        """Sanitize input text"""
        import html
        
        # HTML escape
        sanitized = html.escape(input_text)
        
        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')
        
        # Normalize whitespace
        sanitized = ' '.join(sanitized.split())
        
        return sanitized
    
    def validate_file_upload(self, file_path: str, file_content: bytes) -> Dict[str, Any]:
        """Validate file uploads"""
        import os
        import magic
        
        validation_result = {
            "valid": True,
            "issues": [],
            "file_info": {}
        }
        
        # Check file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in self.allowed_file_types:
            validation_result["valid"] = False
            validation_result["issues"].append(f"File type {file_extension} not allowed")
        
        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024
        if len(file_content) > max_size:
            validation_result["valid"] = False
            validation_result["issues"].append(f"File size exceeds maximum ({max_size} bytes)")
        
        # Check file type using magic numbers
        try:
            file_type = magic.from_buffer(file_content, mime=True)
            validation_result["file_info"]["detected_type"] = file_type
            
            # Verify file type matches extension
            expected_types = {
                '.txt': 'text/plain',
                '.json': 'application/json',
                '.csv': 'text/csv',
                '.pdf': 'application/pdf'
            }
            
            expected_type = expected_types.get(file_extension)
            if expected_type and not file_type.startswith(expected_type.split('/')[0]):
                validation_result["issues"].append("File type mismatch with extension")
        
        except Exception as e:
            validation_result["issues"].append(f"Could not detect file type: {e}")
        
        return validation_result
```

---

## 2. Data Governance Framework

### Data Lineage and Classification

```python
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field

@dataclass
class DataAsset:
    asset_id: str
    name: str
    description: str
    data_classification: DataClassification
    owner: str
    created_at: datetime
    last_modified: datetime
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DataLineageEntry:
    source_asset_id: str
    target_asset_id: str
    transformation_type: str
    transformation_details: Dict[str, Any]
    created_at: datetime
    created_by: str

class DataGovernanceManager:
    def __init__(self):
        self.data_assets = {}
        self.lineage_entries = []
        self.classification_rules = {}
        self.compliance_policies = {}
        self._setup_classification_rules()
    
    def _setup_classification_rules(self):
        """Setup automatic data classification rules"""
        self.classification_rules = {
            "personal_identifiers": {
                "patterns": [
                    r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
                    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
                    r'\b\d{3}-\d{3}-\d{4}\b',  # Phone
                ],
                "classification": DataClassification.HIGHLY_SENSITIVE
            },
            "financial_data": {
                "patterns": [
                    r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit card
                    r'\b\d{9}\b',  # Bank routing
                ],
                "classification": DataClassification.HIGHLY_SENSITIVE
            },
            "business_data": {
                "patterns": [
                    r'revenue', r'profit', r'confidential', r'internal'
                ],
                "classification": DataClassification.SENSITIVE
            }
        }
    
    def register_data_asset(self, asset: DataAsset) -> str:
        """Register a new data asset"""
        if not asset.asset_id:
            asset.asset_id = str(uuid.uuid4())
        
        # Auto-classify if not already classified
        if asset.data_classification == DataClassification.PUBLIC:
            asset.data_classification = self._auto_classify_data(asset)
        
        self.data_assets[asset.asset_id] = asset
        return asset.asset_id
    
    def _auto_classify_data(self, asset: DataAsset) -> DataClassification:
        """Automatically classify data based on content patterns"""
        import re
        
        # Combine all text content for analysis
        content_text = f"{asset.name} {asset.description} {' '.join(asset.tags)}"
        if "sample_content" in asset.metadata:
            content_text += f" {asset.metadata['sample_content']}"
        
        highest_classification = DataClassification.PUBLIC
        
        for rule_name, rule_config in self.classification_rules.items():
            for pattern in rule_config["patterns"]:
                if re.search(pattern, content_text, re.IGNORECASE):
                    rule_classification = rule_config["classification"]
                    if self._classification_priority(rule_classification) > self._classification_priority(highest_classification):
                        highest_classification = rule_classification
        
        return highest_classification
    
    def _classification_priority(self, classification: DataClassification) -> int:
        """Get priority level for data classification"""
        priorities = {
            DataClassification.PUBLIC: 1,
            DataClassification.INTERNAL: 2,
            DataClassification.SENSITIVE: 3,
            DataClassification.HIGHLY_SENSITIVE: 4
        }
        return priorities[classification]
    
    def record_data_lineage(self, source_id: str, target_id: str, 
                           transformation_type: str, transformation_details: Dict[str, Any],
                           user_id: str):
        """Record data lineage between assets"""
        lineage_entry = DataLineageEntry(
            source_asset_id=source_id,
            target_asset_id=target_id,
            transformation_type=transformation_type,
            transformation_details=transformation_details,
            created_at=datetime.utcnow(),
            created_by=user_id
        )
        
        self.lineage_entries.append(lineage_entry)
    
    def get_data_lineage(self, asset_id: str, direction: str = "both") -> Dict[str, List[str]]:
        """Get data lineage for an asset"""
        upstream = []
        downstream = []
        
        for entry in self.lineage_entries:
            if entry.target_asset_id == asset_id:
                upstream.append(entry.source_asset_id)
            if entry.source_asset_id == asset_id:
                downstream.append(entry.target_asset_id)
        
        if direction == "upstream":
            return {"upstream": upstream}
        elif direction == "downstream":
            return {"downstream": downstream}
        else:
            return {"upstream": upstream, "downstream": downstream}
    
    def get_compliance_report(self, asset_id: str) -> Dict[str, Any]:
        """Generate compliance report for a data asset"""
        asset = self.data_assets.get(asset_id)
        if not asset:
            return {"error": "Asset not found"}
        
        lineage = self.get_data_lineage(asset_id)
        
        report = {
            "asset_id": asset_id,
            "asset_name": asset.name,
            "data_classification": asset.data_classification.value,
            "owner": asset.owner,
            "created_at": asset.created_at.isoformat(),
            "last_modified": asset.last_modified.isoformat(),
            "upstream_dependencies": len(lineage["upstream"]),
            "downstream_impacts": len(lineage["downstream"]),
            "compliance_checks": self._run_compliance_checks(asset),
            "recommendations": []
        }
        
        # Add recommendations based on classification
        if asset.data_classification in [DataClassification.SENSITIVE, DataClassification.HIGHLY_SENSITIVE]:
            if "encryption" not in asset.metadata.get("security_controls", []):
                report["recommendations"].append("Enable encryption for sensitive data")
            
            if not asset.metadata.get("access_controls_enabled", False):
                report["recommendations"].append("Implement access controls")
        
        return report
    
    def _run_compliance_checks(self, asset: DataAsset) -> Dict[str, bool]:
        """Run compliance checks for an asset"""
        checks = {
            "has_owner": bool(asset.owner),
            "has_classification": asset.data_classification != DataClassification.PUBLIC,
            "has_description": bool(asset.description),
            "retention_policy_defined": "retention_period" in asset.metadata,
            "access_controls_enabled": asset.metadata.get("access_controls_enabled", False)
        }
        
        # Additional checks for sensitive data
        if asset.data_classification in [DataClassification.SENSITIVE, DataClassification.HIGHLY_SENSITIVE]:
            checks.update({
                "encryption_enabled": "encryption" in asset.metadata.get("security_controls", []),
                "audit_logging_enabled": asset.metadata.get("audit_logging", False),
                "privacy_review_completed": asset.metadata.get("privacy_review_date") is not None
            })
        
        return checks

# GDPR Compliance Manager
class GDPRComplianceManager:
    def __init__(self, data_governance: DataGovernanceManager):
        self.data_governance = data_governance
        self.personal_data_registry = {}
        self.consent_records = {}
        self.data_subject_requests = []
    
    def register_personal_data(self, data_asset_id: str, personal_data_types: List[str],
                             lawful_basis: str, retention_period: int):
        """Register personal data for GDPR compliance"""
        self.personal_data_registry[data_asset_id] = {
            "personal_data_types": personal_data_types,
            "lawful_basis": lawful_basis,
            "retention_period_days": retention_period,
            "registered_at": datetime.utcnow()
        }
    
    def record_consent(self, data_subject_id: str, data_asset_id: str, 
                      consent_type: str, consent_given: bool):
        """Record data subject consent"""
        consent_key = f"{data_subject_id}:{data_asset_id}"
        
        self.consent_records[consent_key] = {
            "data_subject_id": data_subject_id,
            "data_asset_id": data_asset_id,
            "consent_type": consent_type,
            "consent_given": consent_given,
            "timestamp": datetime.utcnow()
        }
    
    def process_data_subject_request(self, request_type: str, data_subject_id: str,
                                   details: Dict[str, Any]) -> str:
        """Process data subject requests (access, rectification, erasure, etc.)"""
        request_id = str(uuid.uuid4())
        
        request = {
            "request_id": request_id,
            "request_type": request_type,
            "data_subject_id": data_subject_id,
            "details": details,
            "status": "received",
            "created_at": datetime.utcnow(),
            "response_due_date": datetime.utcnow() + timedelta(days=30)  # GDPR requirement
        }
        
        self.data_subject_requests.append(request)
        
        # Auto-process certain request types
        if request_type == "access":
            self._process_access_request(request)
        elif request_type == "erasure":
            self._process_erasure_request(request)
        
        return request_id
    
    def _process_access_request(self, request: Dict[str, Any]):
        """Process data subject access request"""
        data_subject_id = request["data_subject_id"]
        
        # Find all data assets containing this subject's data
        subject_data = {}
        
        for asset_id, asset in self.data_governance.data_assets.items():
            if asset_id in self.personal_data_registry:
                # Check if this asset contains the subject's data
                if self._asset_contains_subject_data(asset_id, data_subject_id):
                    subject_data[asset_id] = {
                        "asset_name": asset.name,
                        "data_types": self.personal_data_registry[asset_id]["personal_data_types"],
                        "lawful_basis": self.personal_data_registry[asset_id]["lawful_basis"]
                    }
        
        request["response_data"] = subject_data
        request["status"] = "completed"
    
    def _process_erasure_request(self, request: Dict[str, Any]):
        """Process data subject erasure request (right to be forgotten)"""
        data_subject_id = request["data_subject_id"]
        
        # Find all assets that need erasure
        assets_for_erasure = []
        
        for asset_id in self.personal_data_registry:
            if self._can_erase_data(asset_id, data_subject_id):
                assets_for_erasure.append(asset_id)
        
        request["assets_for_erasure"] = assets_for_erasure
        request["status"] = "processing"
        
        # In production, this would trigger actual data erasure processes
    
    def _asset_contains_subject_data(self, asset_id: str, data_subject_id: str) -> bool:
        """Check if asset contains data for specific subject"""
        # This would integrate with actual data systems to check
        return True  # Simplified for example
    
    def _can_erase_data(self, asset_id: str, data_subject_id: str) -> bool:
        """Check if data can be erased (considering legal obligations)"""
        personal_data_info = self.personal_data_registry.get(asset_id)
        if not personal_data_info:
            return False
        
        # Check if legal obligation prevents erasure
        legal_hold_reasons = ["legal_obligation", "vital_interests", "public_task"]
        if personal_data_info["lawful_basis"] in legal_hold_reasons:
            return False
        
        return True
    
    def generate_gdpr_compliance_report(self) -> Dict[str, Any]:
        """Generate comprehensive GDPR compliance report"""
        report = {
            "report_date": datetime.utcnow().isoformat(),
            "personal_data_assets": len(self.personal_data_registry),
            "active_consents": len([c for c in self.consent_records.values() if c["consent_given"]]),
            "pending_requests": len([r for r in self.data_subject_requests if r["status"] == "received"]),
            "overdue_requests": [],
            "compliance_issues": []
        }
        
        # Check for overdue requests
        for request in self.data_subject_requests:
            if request["status"] in ["received", "processing"] and datetime.utcnow() > request["response_due_date"]:
                report["overdue_requests"].append(request["request_id"])
        
        # Check for compliance issues
        for asset_id, asset in self.data_governance.data_assets.items():
            if asset_id in self.personal_data_registry:
                personal_data_info = self.personal_data_registry[asset_id]
                
                # Check retention periods
                days_since_creation = (datetime.utcnow() - asset.created_at).days
                if days_since_creation > personal_data_info["retention_period_days"]:
                    report["compliance_issues"].append({
                        "asset_id": asset_id,
                        "issue": "Data retention period exceeded",
                        "days_overdue": days_since_creation - personal_data_info["retention_period_days"]
                    })
        
        return report
```

---

## Summary

In this lesson, we've covered:

✅ **Security Framework**: Multi-layer security architecture with policies, access controls, and threat detection
✅ **Data Protection**: Encryption, input validation, and secure data handling practices
✅ **Data Governance**: Asset registration, classification, and lineage tracking
✅ **Compliance Management**: GDPR compliance framework with consent management and data subject rights
✅ **Audit and Monitoring**: Comprehensive logging and security incident management
✅ **Risk Assessment**: Automated security risk evaluation and recommendations

## Next Steps

In the next lesson, we'll explore **Monitoring and Performance Optimization**, where you'll learn how to implement comprehensive monitoring solutions, performance tracking, and optimization strategies for AI applications.

## Additional Resources

- [Azure Security Best Practices](https://docs.microsoft.com/en-us/azure/security/fundamentals/best-practices-and-patterns)
- [GDPR Compliance Guide](https://gdpr.eu/compliance/)
- [Azure Information Protection](https://docs.microsoft.com/en-us/azure/information-protection/)
- [Responsible AI Practices](https://www.microsoft.com/en-us/ai/responsible-ai)

---

*This lesson provides the security and governance foundation needed to develop trustworthy and compliant AI applications.* 