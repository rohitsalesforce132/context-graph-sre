# Entity: Payment API

```yaml
id: ENT-payment-api
type: service
name: "payment-api"
category: api
environment: production
cluster: ENT-prod-cluster

language: Java
current_version: "v2.3.1"
port: 8080

depends_on:
  - id: ENT-prod-cluster
    type: kubernetes_cluster
  - id: ENT-key-vault
    type: secret_store
  - id: ENT-provider-a-gateway
    type: external_provider
  - id: ENT-primary-database
    type: database

depended_upon_by:
  - id: ENT-api-gateway
    type: gateway

known_patterns:
  - ref: PRE-001
    note: "Affected when cluster nodes go NotReady"

resources:
  requests:
    cpu: "500m"
    memory: "256Mi"
  limits:
    cpu: "1000m"
    memory: "512Mi"

known_issues:
  - "Memory limit 512Mi is tight under high load (50+ RPS)"
  - "No circuit breaker for external providers — pending from DEC-002 follow-up"

incident_history:
  - INC-001
  - INC-002

decision_history:
  - DEC-001
  - DEC-002
```
