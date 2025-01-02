# Chapter 3: Cluster Setup and Configuration - Practice Questions

## Section 1: Cluster Architecture and Setup

### Question 1
You are setting up a new Kubernetes cluster using kubeadm. Which of the following commands must be run FIRST on all nodes?

```bash
a) kubeadm init
b) systemctl start kubelet
c) apt-get install containerd
d) modprobe br_netfilter
```

**Answer:** d

**Explanation:** Before installing any Kubernetes components, kernel modules like br_netfilter must be loaded to enable proper network functionality. This is a prerequisite for container runtime and Kubernetes installation.

### Question 2
Given this kubeadm init command:
```bash
kubeadm init --pod-network-cidr=192.168.0.0/16 --kubernetes-version=v1.23.0 --control-plane-endpoint="cp.example.com"
```
What is the purpose of the --control-plane-endpoint parameter?

a) Specifies the API server's advertise address
b) Sets up high availability for the control plane
c) Configures the pod network CIDR
d) Defines the kubelet endpoint

**Answer:** b

**Explanation:** The --control-plane-endpoint parameter specifies a stable endpoint for the control plane, which is crucial for high availability setups. It allows additional control plane nodes to join the cluster.

## Section 2: High Availability Configuration

### Question 3
In a highly available Kubernetes cluster, what is the minimum recommended number of control plane nodes?

a) 1
b) 2
c) 3
d) 5

**Answer:** c

**Explanation:** Three control plane nodes are recommended for high availability to maintain quorum and handle node failures. This ensures the cluster can continue operating even if one node fails.

### Question 4
You have the following HAProxy configuration:
```conf
frontend kubernetes-frontend
  bind *:6443
  mode tcp
  default_backend kubernetes-backend

backend kubernetes-backend
  mode tcp
  balance roundrobin
  server master1 192.168.1.10:6443 check
  server master2 192.168.1.11:6443 check
```
What type of load balancing is being used?

a) Least connections
b) Source IP hash
c) Round robin
d) Weighted round robin

**Answer:** c

**Explanation:** The configuration shows 'balance roundrobin', which distributes requests sequentially to each server in turn.

## Section 3: Storage Configuration

### Question 5
Given this StorageClass manifest:
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
volumeBindingMode: WaitForFirstConsumer
```
What is the purpose of WaitForFirstConsumer?

a) Delays volume creation until pod is scheduled
b) Waits for admin approval before creating volume
c) Creates volume immediately upon PVC creation
d) Binds volume to the first available node

**Answer:** a

**Explanation:** WaitForFirstConsumer delays volume binding and creation until a pod using the PVC is created and scheduled to a node, improving scheduling flexibility.

## Section 4: Troubleshooting Scenarios

### Question 6
After installing a new Kubernetes cluster, pods are stuck in 'Pending' state. The cluster status shows:
```bash
kubectl get nodes
NAME     STATUS   ROLES    AGE   VERSION
master   Ready    master   10m   v1.23.0
node1    Ready    <none>   5m    v1.23.0
```

What could be the cause?

a) Container runtime not installed
b) Network plugin not installed
c) Insufficient resources
d) Node not labeled correctly

**Answer:** b

**Explanation:** If no network plugin is installed, pods will remain in 'Pending' state even though nodes show as Ready. A CNI plugin must be installed for pod networking to function.

### Question 7
Examine this etcd backup command:
```bash
ETCDCTL_API=3 etcdctl snapshot save backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```
What is missing from this command?

a) Backup location
b) API version
c) Authentication credentials
d) Snapshot name

**Answer:** a

**Explanation:** While the command will work, it's best practice to specify a full path for the backup location rather than just a filename to ensure the backup is stored in a known, accessible location.

## Section 5: Advanced Configuration

### Question 8
You need to add a new control plane node to an existing HA cluster. Which component must be updated FIRST?

a) etcd
b) Load balancer configuration
c) API server certificate
d) kubelet configuration

**Answer:** b

**Explanation:** The load balancer configuration must be updated first to include the new control plane node, ensuring traffic can be properly distributed to the new node once it joins.

### Question 9
Given this node configuration:
```yaml
apiVersion: v1
kind: Node
metadata:
  name: worker1
  labels:
    node-role.kubernetes.io/worker: ""
    disk: ssd
spec:
  taints:
  - key: special
    value: gpu
    effect: NoSchedule
```
Which pod configuration would allow scheduling on this node?

a) No special configuration needed
b) Node selector for disk=ssd
c) Toleration for the special=gpu taint
d) Both b and c

**Answer:** d

**Explanation:** The pod needs both a node selector to match the disk=ssd label and a toleration for the special=gpu:NoSchedule taint to be scheduled on this node.

### Question 10
You're configuring kubelet on a new node. What is the correct order of operations?

1. Start kubelet service
2. Generate node certificates
3. Create kubelet configuration
4. Join cluster with kubeadm

a) 1,2,3,4
b) 2,3,1,4
c) 3,2,1,4
d) 2,3,4,1

**Answer:** b

**Explanation:** The correct order is: generate certificates, create configuration, start kubelet service, then join the cluster. This ensures all necessary components are in place before attempting to join.

[Continue with more questions...]

## Mixed Advanced Practice Questions

### Question 11: Advanced Networking
Given this NetworkPolicy:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          environment: production
    - podSelector:
        matchLabels:
          role: backend
    ports:
    - protocol: TCP
      port: 5432
```
Which statement is TRUE?

a) Only production namespace pods can access the database
b) All backend pods can access the database
c) Database pods can only be accessed on port 5432
d) Pods matching BOTH namespace and pod selectors can access the database

**Answer:** d
**Explanation:** The policy uses AND logic between the namespaceSelector and podSelector within the same from array element. Only pods with role=backend in namespaces labeled environment=production can access the database pods.

### Question 12: Security Configuration
You need to rotate the certificates in your Kubernetes cluster. Which command will check the expiration dates of your certificates?

a) kubectl get certificates
b) kubeadm certs check-expiration
c) kubectl describe certificates
d) openssl x509 -in /etc/kubernetes/pki/ca.crt -text

**Answer:** b
**Explanation:** kubeadm certs check-expiration shows the expiration dates of all certificates managed by kubeadm. Example output:
```bash
CERTIFICATE                EXPIRES                  RESIDUAL TIME
admin.conf                 May 15, 2023 09:12 UTC   342d
apiserver                 May 15, 2023 09:12 UTC   342d
apiserver-kubelet-client  May 15, 2023 09:12 UTC   342d
```

### Question 13: Performance and Scaling
Your cluster's etcd performance is degrading. Given these metrics:
```bash
etcd_disk_wal_fsync_duration_seconds_avg = 0.045
etcd_disk_backend_commit_duration_seconds_avg = 0.086
etcd_network_peer_round_trip_time_seconds_avg = 0.032
```
What should you do FIRST?

a) Add more etcd members
b) Move etcd to SSD storage
c) Increase network bandwidth
d) Add more memory to etcd nodes

**Answer:** b
**Explanation:** High fsync and commit durations indicate disk I/O bottlenecks. Moving etcd to SSD storage would improve these metrics most effectively.

### Question 14: Backup and Disaster Recovery
You're implementing a backup strategy. Which components need to be backed up for a COMPLETE cluster recovery?

a) etcd data only
b) etcd data and certificates
c) etcd data, certificates, and kubeadm configuration
d) etcd data, certificates, kubeadm configuration, and persistent volumes

**Answer:** d
**Explanation:** A complete recovery requires:
- etcd data for cluster state
- Certificates for security
- kubeadm configuration for cluster settings
- Persistent volumes for application data

### Question 15: Advanced Networking
Examine this Service configuration:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-internal: "true"
spec:
  type: LoadBalancer
  ports:
  - port: 443
    targetPort: 8443
  selector:
    app: web
```
What type of load balancer will be created in AWS?

a) External Application Load Balancer
b) Internal Network Load Balancer
c) External Network Load Balancer
d) Internal Application Load Balancer

**Answer:** b
**Explanation:** The annotations specify:
- nlb: Network Load Balancer
- internal: "true": Internal load balancer
Therefore, an internal Network Load Balancer will be created.

### Question 16: Performance and Scaling
Given this HorizontalPodAutoscaler configuration:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
```
What will happen if CPU utilization drops to 40% for 2 minutes?

a) Pods will scale down immediately
b) No scaling will occur yet
c) Pods will scale down after 5 minutes
d) Pods will maintain minimum 3 replicas

**Answer:** b
**Explanation:** The stabilizationWindowSeconds of 300 (5 minutes) prevents scale-down actions until the condition persists for the full window, preventing premature scaling.

### Question 17: Security Configuration
You need to implement pod security standards. Given:
```yaml
apiVersion: pod-security.kubernetes.io/v1
kind: Namespace
metadata:
  name: secure-apps
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/audit: restricted
```
Which pod will be ALLOWED in this namespace?

```yaml
a) 
spec:
  containers:
  - name: app
    image: nginx
    securityContext:
      runAsUser: 0

b)
spec:
  containers:
  - name: app
    image: nginx
    securityContext:
      runAsNonRoot: true
      allowPrivilegeEscalation: false

c)
spec:
  containers:
  - name: app
    image: nginx
    securityContext:
      capabilities:
        add: ["NET_ADMIN"]

d)
spec:
  containers:
  - name: app
    image: nginx:latest
```

**Answer:** b
**Explanation:** The 'restricted' policy requires:
- Non-root user
- No privilege escalation
- No additional capabilities
Only option b meets these requirements.

### Question 18: Backup and Disaster Recovery
During a disaster recovery test, you restore etcd from backup but pods aren't being scheduled. What should you check FIRST?

a) Node certificates
b) API server configuration
c) Node labels and taints
d) Network plugin status

**Answer:** c
**Explanation:** After etcd restore:
- Node labels and taints might be lost
- This affects pod scheduling immediately
- Check with: kubectl describe nodes
- Restore labels/taints as needed

### Question 19: Performance and Scaling
Your cluster nodes show these metrics:
```bash
Node1: CPU: 85%, Memory: 60%, Pods: 95/110
Node2: CPU: 45%, Memory: 90%, Pods: 70/110
Node3: CPU: 55%, Memory: 55%, Pods: 85/110
```
Which scheduling decision would be MOST efficient?

a) Schedule new pods to Node3
b) Schedule new pods to Node2
c) Add a new node to the cluster
d) Redistribute existing pods

**Answer:** c
**Explanation:** Analysis shows:
- Node1: High CPU utilization
- Node2: High memory utilization
- Node3: High pod count
Adding a new node is best as all existing nodes have constraints.

### Question 20: Advanced Networking
Examine this Ingress configuration:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```
What URL transformation will occur?

a) /api/users → /api/users
b) /api/users → /users
c) /api/users → /api
d) No transformation

**Answer:** b
**Explanation:** The rewrite-target annotation:
- Captures everything after /api in $2
- Rewrites the path to just the captured portion
- Example: /api/users becomes /users