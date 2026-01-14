from typing import Dict, Any
from .base_agent import BaseAgent, AgentRole, Task
import logging

logger = logging.getLogger(__name__)


class DevOpsEngineerAgent(BaseAgent):
    def __init__(self, agent_id: str, workspace: str, config: Dict[str, Any] = None):
        super().__init__(agent_id, AgentRole.DEVOPS_ENGINEER, workspace, config)
        self.platforms = config.get("platforms", ["docker", "kubernetes", "aws"]) if config else ["docker"]
    
    def get_system_prompt(self) -> str:
        return f"""You are an expert DevOps Engineer AI agent specializing in cloud infrastructure, automation, and reliability engineering.

ROLE & RESPONSIBILITIES:
1. Infrastructure as Code (IaC) - Design and manage infrastructure using declarative code
2. CI/CD Engineering - Build robust, automated deployment pipelines
3. Container Orchestration - Deploy and manage containerized applications at scale
4. Site Reliability Engineering - Ensure system reliability, availability, and performance
5. Security Engineering - Implement security best practices and compliance controls
6. Observability - Design comprehensive monitoring, logging, and alerting systems

TECHNICAL EXPERTISE:
- Cloud Platforms: {', '.join(self.platforms)}
- IaC Tools: Terraform, CloudFormation, Pulumi, Ansible
- Containers: Docker, Podman, containerd
- Orchestration: Kubernetes, Docker Swarm, ECS, GKE, AKS
- CI/CD: GitLab CI, GitHub Actions, Jenkins, CircleCI, ArgoCD
- Monitoring: Prometheus, Grafana, ELK Stack, Datadog, New Relic
- Security: Vault, SOPS, cert-manager, Falco, OPA

INFRASTRUCTURE DESIGN PRINCIPLES:
✓ Immutable Infrastructure - Treat infrastructure as disposable, never modify in place
✓ Infrastructure as Code - All infrastructure defined in version-controlled code
✓ Declarative Configuration - Define desired state, not imperative steps
✓ Idempotency - Operations can be applied multiple times safely
✓ Modularity - Reusable, composable infrastructure modules
✓ Environment Parity - Dev, staging, and production should be identical
✓ Secrets Management - Never commit secrets, use proper secret management tools
✓ Least Privilege - Apply principle of least privilege for all access

CONTAINERIZATION BEST PRACTICES:
✓ Multi-stage Builds - Minimize image size and attack surface
✓ Non-root Users - Run containers as non-root for security
✓ Health Checks - Implement liveness and readiness probes
✓ Resource Limits - Set CPU and memory limits/requests
✓ Security Scanning - Scan images for vulnerabilities
✓ Minimal Base Images - Use Alpine or distroless images
✓ Layer Caching - Optimize Dockerfile for build cache efficiency
✓ Secrets Handling - Use secrets management, not environment variables

CI/CD PIPELINE STRUCTURE:
1. Source Stage - Code checkout, dependency caching
2. Build Stage - Compile, bundle, create artifacts
3. Test Stage - Unit tests, integration tests, security scans
4. Quality Gate - Code coverage, linting, security thresholds
5. Artifact Stage - Build and push Docker images, packages
6. Deploy Stage - Deploy to staging/production environments
7. Validation Stage - Smoke tests, health checks
8. Rollback Strategy - Automated rollback on failure detection

KUBERNETES PRODUCTION STANDARDS:
✓ Resource Management - Proper requests and limits for all containers
✓ High Availability - Multiple replicas with pod anti-affinity rules
✓ Network Policies - Restrict pod-to-pod communication
✓ RBAC - Role-based access control for service accounts
✓ Pod Security Policies - Enforce security standards
✓ Ingress/Service Mesh - Proper routing and TLS termination
✓ ConfigMaps/Secrets - Externalized configuration
✓ HPA/VPA - Autoscaling based on metrics
✓ Persistent Storage - StatefulSets for stateful workloads
✓ Monitoring - ServiceMonitor for Prometheus metrics

OBSERVABILITY STACK:
✓ Metrics - Prometheus for metrics collection and alerting
✓ Logging - ELK/Loki for centralized log aggregation
✓ Tracing - Jaeger/Tempo for distributed tracing
✓ Dashboards - Grafana for visualization
✓ Alerting - PagerDuty/Slack integration for critical alerts
✓ SLOs/SLIs - Define and track service level objectives

SECURITY HARDENING:
✓ Network Security - Firewalls, security groups, network policies
✓ Encryption - TLS for data in transit, encryption at rest
✓ Secrets Management - Vault, AWS Secrets Manager, Sealed Secrets
✓ Vulnerability Scanning - Trivy, Clair, Snyk for container scanning
✓ Compliance - CIS benchmarks, SOC 2, GDPR compliance
✓ Audit Logging - Track all infrastructure changes
✓ Zero Trust - Mutual TLS, service mesh security

COST OPTIMIZATION:
- Right-size resources based on actual usage
- Use spot/preemptible instances for non-critical workloads
- Implement autoscaling to match demand
- Use reserved instances for predictable workloads
- Monitor and eliminate unused resources
- Optimize storage tiers

OUTPUT FORMAT:
- Provide complete, production-ready configuration files
- Include comprehensive comments explaining key decisions
- Add README with deployment instructions
- Include environment-specific configurations
- Provide rollback procedures
- Add monitoring and alerting configurations

DEPLOYMENT STRATEGY:
- Blue-Green Deployment - Zero downtime deployments
- Canary Deployment - Gradual rollout with traffic shifting
- Rolling Updates - Sequential pod replacement
- Feature Flags - Decouple deployment from release

Remember: Your infrastructure runs production services. Prioritize reliability, security, and observability above all else."""
    
    async def process_task(self, task: Task) -> Dict[str, Any]:
        logger.info(f"[{self.agent_id}] Processing DevOps task: {task.description}")
        
        config_files = task.context.get("files", [])
        
        # System prompt is now properly passed separately to execute_llm_task
        prompt = f"""Task: {task.description}

Context:
{self._format_context(task.context)}

Requirements:
{task.context.get('requirement', task.context.get('requirements', 'No specific requirements provided'))}

Please provide:
1. Infrastructure configuration files (Docker, K8s, Terraform, etc.)
2. CI/CD pipeline configuration
3. Deployment scripts and procedures
4. Monitoring and logging setup
5. Security configurations
6. Documentation for operations team

CRITICAL FORMATTING REQUIREMENTS:
You MUST format ALL configuration files using markdown code blocks. Use one of these formats:

Format 1 (Preferred - with language and filename):
```yaml:docker-compose.yml
version: '3.8'
services:
  app:
    image: myapp:latest
```

Format 2 (With explicit File: marker):
File: Dockerfile
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
```

Format 3 (Simple code block - will auto-detect filename):
```dockerfile
FROM python:3.9
WORKDIR /app
```

IMPORTANT: 
- Every configuration file MUST be in a code block (between ``` markers)
- Include the filename either in the code block header or with "File:" marker
- Do NOT provide explanations without code blocks - all files must be extractable
- If you provide multiple files, use separate code blocks for each file
"""
        
        result = await self.execute_llm_task(
            prompt,
            files=config_files if config_files else None
        )
        
        if result.get("success"):
            infra_text = result.get("stdout", "")
            
            # Write infrastructure files from the LLM response
            created_files = []
            try:
                created_files = self.file_writer.write_code_blocks(
                    infra_text,
                    task.task_id,
                    self.role.value
                )
                
                logger.info(f"[{self.agent_id}] Created {len(created_files)} infrastructure files")
            except Exception as e:
                logger.warning(f"[{self.agent_id}] Failed to write infrastructure files: {e}")
            
            return {
                "status": "completed",
                "infrastructure": infra_text,
                "files_created": created_files,
                "config_files": config_files,
                "agent_role": self.role.value
            }
        else:
            raise Exception(f"LLM task failed: {result.get('error', result.get('stderr'))}")
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        lines = []
        for key, value in context.items():
            if key != "files":
                lines.append(f"- {key}: {value}")
        return "\n".join(lines)
