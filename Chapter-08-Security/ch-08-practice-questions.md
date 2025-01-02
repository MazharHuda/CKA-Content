# Chapter 8: Security - Practice Questions

## Section 1: Authentication and Authorization

### Question 1
Given this Certificate Signing Request (CSR):
```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: john-developer
spec:
  request: <base64-encoded-csr>
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
```
What happens if you don't specify the usages field?

a) The CSR will be automatically approved
b) The CSR will be rejected
c) The CSR will use default usages
d) The CSR creation will fail

**Answer:** d
**Explanation:** The usages field is mandatory for CSRs. Without it, the API server will reject the CSR creation. Common usages include:
- client auth (for client certificates)
- server auth (for server certificates)
- digital signature
- key encipherment

### Question 2
Examine this Role configuration:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: development
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
```
Which action would NOT be allowed with this Role?

a) View pod logs
b) List all pods
c) Get pod details
d) Watch pod status

**Answer:** a
**Explanation:** Viewing pod logs requires access to the pods/log resource, which is not included in this Role. To allow log access, you would need to add:
```yaml
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]
```

### Question 3
You need to create a service account that can only read pods in all namespaces. Which resource should you use?

a) Role
b) ClusterRole
c) RoleBinding
d) ClusterRoleBinding

**Answer:** b
**Explanation:** A ClusterRole is required because:
1. The access needs to span all namespaces
2. Roles are namespace-scoped
3. ClusterRoles are cluster-wide
4. This is a common pattern for monitoring systems

## Section 2: Pod Security

### Question 4
Given this security context:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: security-pod
spec:
  securityContext:
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: app
    image: nginx
    securityContext:
      runAsUser: 100
      allowPrivilegeEscalation: false
```
What user ID will the container run as?

a) 1000
b) 100
c) 0
d) 2000

**Answer:** b
**Explanation:** Container-level securityContext overrides pod-level settings:
1. Container runAsUser: 100 takes precedence
2. Pod-level runAsUser: 1000 is ignored for this container
3. fsGroup: 2000 still applies
4. allowPrivilegeEscalation applies only to this container

### Question 5
What is the effect of this Pod Security Standard label?
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
```

a) Allows privileged pods
b) Blocks privileged pods
c) Only affects new pods
d) Only affects existing pods

**Answer:** b
**Explanation:** The 'restricted' profile:
1. Enforces most security controls
2. Blocks privileged containers
3. Requires running as non-root
4. Applies to all pods in the namespace

## Section 3: Network Policies

### Question 6
Examine this NetworkPolicy:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
```
What is the effect of this policy?

a) Allows all ingress traffic to api pods
b) Blocks all ingress traffic to api pods
c) No effect on traffic
d) Allows only egress traffic

**Answer:** b
**Explanation:** This policy:
1. Selects pods with label app: api
2. Specifies ingress type but no ingress rules
3. Results in denying all ingress traffic
4. Does not affect egress traffic

### Question 7
Your pod can't communicate with the Kubernetes API server after applying network policies. What should you check first?

a) Pod labels
b) RBAC permissions
c) Egress policy
d) API server status

**Answer:** c
**Explanation:** Check egress policy because:
1. Pods need egress access to API server
2. Default deny policies block all traffic
3. Need explicit egress rule for API server
4. Common issue in restricted environments

## Section 4: Secret Management

### Question 8
Given this Secret usage:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod
spec:
  containers:
  - name: app
    image: nginx
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-creds
          key: password
          optional: true
```
What happens if the secret 'db-creds' doesn't exist?

a) Pod will fail to start
b) Pod will start with empty password
c) Pod will start and wait for secret
d) Pod will start with default value

**Answer:** b
**Explanation:** With optional: true:
1. Pod will start even if secret is missing
2. Environment variable will not be set
3. Application must handle missing variable
4. Useful for optional configurations

### Question 9
Given this audit policy:
```yaml
apiVersion: audit.k8s.io/v1
kind: Policy
metadata:
  name: audit-policy
rules:
- level: Metadata
  resources:
  - group: ""
    resources: ["secrets"]
- level: RequestResponse
  resources:
  - group: ""
    resources: ["pods"]
```
What information will be logged for secret operations?

a) Full request and response bodies
b) Only metadata about the request
c) No information
d) Only error responses

**Answer:** b
**Explanation:** The Metadata audit level logs:
1. Request metadata (user, timestamp, resource)
2. No request or response bodies
3. Response status
4. No sensitive data

### Question 10
You need to rotate the API server's serving certificate. What's the correct sequence?

a) Generate new cert, update kubeconfig, restart API server
b) Generate new cert, restart API server, update kubeconfig
c) Update kubeconfig, generate new cert, restart API server
d) Restart API server, generate new cert, update kubeconfig

**Answer:** a
**Explanation:** Certificate rotation steps:
1. Generate new certificate while old one is valid
2. Update kubeconfig files with new certificate
3. Restart API server to use new certificate
4. Verify cluster functionality

### Question 11
Examine this pod specification:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: restricted-pod
spec:
  containers:
  - name: app
    image: nginx
    securityContext:
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
```
What is the effect of this capability configuration?

a) Pod can bind to any port
b) Pod can bind to privileged ports only
c) Pod can bind to unprivileged ports only
d) Pod cannot bind to any ports

**Answer:** b
**Explanation:** This configuration:
1. Drops all default capabilities
2. Adds only NET_BIND_SERVICE
3. Allows binding to ports below 1024
4. Follows principle of least privilege

### Question 12
Your cluster's etcd data isn't encrypted. How should you enable encryption?

a) Restart etcd with encryption flag
b) Configure encryption provider in API server
c) Enable TLS for etcd
d) Use encrypted volumes

**Answer:** b
**Explanation:** To enable etcd encryption:
1. Configure EncryptionConfiguration in API server
2. Create encryption key
3. Restart API server
4. Encrypt existing secrets

### Question 13
Given this ServiceAccount configuration:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
automountServiceAccountToken: false
---
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  serviceAccountName: app-sa
  automountServiceAccountToken: true
```
Will the service account token be mounted?

a) Yes, pod setting overrides ServiceAccount
b) No, ServiceAccount setting takes precedence
c) Yes, default token will be mounted
d) No, a different token will be mounted

**Answer:** a
**Explanation:** For service account token mounting:
1. Pod-level setting overrides ServiceAccount setting
2. If not specified at pod level, ServiceAccount setting is used
3. Default is true if neither specifies
4. Token will be mounted in this case

### Question 14
You notice unauthorized API requests in your audit logs. What should you implement first?

a) Network policies
b) Pod security policies
c) RBAC policies
d) Admission controllers

**Answer:** c
**Explanation:** To address unauthorized API requests:
1. Implement RBAC to control access
2. Review and restrict service account permissions
3. Audit existing RoleBindings
4. Monitor audit logs for effectiveness

### Question 15
Examine this admission controller configuration:
```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: pod-policy
webhooks:
- name: pod-policy.example.com
  rules:
  - apiGroups: [""]
    apiVersions: ["v1"]
    operations: ["CREATE"]
    resources: ["pods"]
  failurePolicy: Ignore
```
What happens if the webhook server is unavailable?

a) Pod creation is blocked
b) Pod creation proceeds
c) Pod creation waits for server
d) Pod is created in pending state

**Answer:** b
**Explanation:** With failurePolicy: Ignore:
1. Webhook failures are ignored
2. Requests proceed normally
3. No blocking of operations
4. Useful for non-critical validations

### Question 16
Your cluster uses external authentication. What must be configured in the API server?

a) Static tokens
b) Client certificates
c) OIDC flags
d) Basic auth file

**Answer:** c
**Explanation:** For external authentication:
1. Configure OIDC flags in API server
2. Set up identity provider
3. Configure token validation
4. Set up group claims

### Question 17
Given this network policy:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      app: database
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          environment: production
    - podSelector:
        matchLabels:
          role: frontend
```
Which pods can access the database?

a) Only pods with label role=frontend in production namespace
b) Any pod in production namespace
c) Pods with role=frontend in any namespace
d) Either pods with role=frontend OR any pod in production namespace

**Answer:** d
**Explanation:** This policy allows access from:
1. Any pod in namespaces labeled environment=production
2. Any pod labeled role=frontend in any namespace
3. The selectors are not combined (not AND condition)
4. Common misconception in network policy configuration

[Continue with more questions...]
