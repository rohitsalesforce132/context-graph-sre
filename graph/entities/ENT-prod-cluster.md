# Entity: Production Kubernetes Cluster

```yaml
id: ENT-prod-cluster
type: system
name: "prod-cluster"
category: kubernetes_cluster
environment: production
region: primary-region

version: "1.29"
node_pools:
  - name: system
    count: 3
    purpose: "System components, monitoring, ingress"
  - name: workloads
    count: 5
    purpose: "Application workloads"

depends_on:
  - id: ENT-container-registry
    type: container_registry
  - id: ENT-key-vault
    type: secret_store

depended_upon_by:
  - id: ENT-payment-api
    type: service
  - id: ENT-user-service
    type: service
  - id: ENT-notification-service
    type: service

incident_history:
  - INC-001

known_patterns:
  - ref: PRE-001
    note: "Nodes accumulate images, need weekly pruning"

behavioral_notes:
  - "workload pool accumulates images faster due to frequent deployments"
  - "OS disk 128GB is tight for weekly deploy cadence"
  - "Best maintenance window: 02:00-05:00 (lowest traffic)"
```
