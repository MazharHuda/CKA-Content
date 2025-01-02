# Chapter 2: Core Concepts - Practice Questions

## Section 1: Kubernetes Architecture

### Question 1
What is the primary purpose of the kube-apiserver?

a) To schedule pods on nodes
b) To serve as the front-end for the Kubernetes control plane
c) To maintain network rules
d) To monitor node health

**Answer:** b

**Explanation:** The kube-apiserver serves as the front-end for the Kubernetes control plane. It exposes the Kubernetes API and handles all API requests, including authentication, authorization, and validation.

### Question 2
Which component is responsible for maintaining the desired state of ReplicaSets and Deployments?

a) kubelet
b) kube-scheduler
c) kube-controller-manager
d) etcd

**Answer:** c

**Explanation:** The kube-controller-manager runs controller processes, including the ReplicaSet and Deployment controllers, which ensure the desired state is maintained.

## Section 2: Control Plane Components

### Question 3
In a highly available Kubernetes cluster, what is the minimum recommended number of etcd instances?

a) 1
b) 2
c) 3
d) 5

**Answer:** c

**Explanation:** A minimum of 3 etcd instances is recommended for high availability to maintain quorum and handle node failures.

### Question 4
Which statement about the kube-scheduler is correct?

a) It runs containers on nodes
b) It monitors node health
c) It selects which nodes pods should run on
d) It manages network routing

**Answer:** c

**Explanation:** The kube-scheduler is responsible for selecting appropriate nodes for newly created pods based on various factors like resource requirements and constraints.

## Section 3: Worker Node Components

### Question 5
What is the primary responsibility of kubelet?

a) Load balancing traffic between pods
b) Ensuring containers are running in a pod
c) Scheduling pods on nodes
d) Storing cluster configuration

**Answer:** b

**Explanation:** The kubelet is the primary node agent that runs on each node and ensures containers are running in a pod according to the PodSpec.

### Question 6
Which component maintains network rules on nodes?

a) kube-proxy
b) kubelet
c) flannel
d) etcd

**Answer:** a

**Explanation:** kube-proxy maintains network rules (iptables or IPVS rules) on nodes, enabling pod-to-pod communication and implementing the Service concept.

## Section 4: Pods and Containers

### Question 7
Given the following pod manifest:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: container1
    image: nginx
  - name: container2
    image: redis
```
What is true about the containers in this pod?

a) They run on different nodes
b) They share the same network namespace
c) They have separate IP addresses
d) They cannot communicate with each other

**Answer:** b

**Explanation:** Containers within the same pod share the same network namespace, allowing them to communicate via localhost.

### Question 8
What happens to containers in a pod if one container fails?

a) All containers are automatically restarted
b) Only the failed container is restarted
c) The pod is rescheduled on another node
d) Nothing happens

**Answer:** b

**Explanation:** By default, only the failed container is restarted according to the pod's restart policy, while other containers continue running.

## Section 5: Services and Networking

### Question 9
What is the default type of Kubernetes Service?

a) NodePort
b) ClusterIP
c) LoadBalancer
d) ExternalName

**Answer:** b

**Explanation:** ClusterIP is the default Service type, providing internal cluster access to the service.

### Question 10
Given this Service manifest:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30007
```
What port will be accessible from outside the cluster?

a) 80
b) 8080
c) 30007
d) None of the above

**Answer:** c

**Explanation:** The nodePort (30007) is the port that will be exposed on each node's IP address for external access.

## Section 6: Storage and Persistence

### Question 11
What is the relationship between PersistentVolumes and PersistentVolumeClaims?

a) They must be created in the same namespace
b) PVCs request storage from PVs
c) PVs request storage from PVCs
d) They must have the same name

**Answer:** b

**Explanation:** PersistentVolumeClaims (PVCs) request storage resources from PersistentVolumes (PVs), acting as a means for pods to claim persistent storage.

## Section 7: Configuration and Security

### Question 12
What is the purpose of a ConfigMap?

a) To store sensitive information
b) To store non-confidential configuration data
c) To configure network policies
d) To manage container images

**Answer:** b

**Explanation:** ConfigMaps are used to store non-confidential configuration data in key-value pairs that can be consumed by pods.

## Section 8: Scenario-based Questions

### Question 13
You have a pod that's stuck in 'Pending' state. What could be the cause?

a) Invalid image name
b) Insufficient cluster resources
c) Network policy blocking access
d) All of the above

**Answer:** b

**Explanation:** A pod in 'Pending' state often indicates that the scheduler cannot find a node with sufficient resources to run the pod.

### Question 14
Your service isn't routing traffic to pods. Which command would be most helpful in diagnosing this?

a) kubectl get pods
b) kubectl get endpoints
c) kubectl get nodes
d) kubectl get deployments

**Answer:** b

**Explanation:** kubectl get endpoints shows whether a service has successfully selected pods, helping diagnose service-to-pod routing issues.

### Question 15
You need to run a pod with elevated privileges. Which security context configuration would you use?

```yaml
a) securityContext:
     privileged: true

b) securityContext:
     runAsUser: 0

c) securityContext:
     allowPrivilegeEscalation: true

d) securityContext:
     capabilities:
       add: ["ALL"]
```

**Answer:** a

**Explanation:** Setting privileged: true in the security context allows the container to run with elevated privileges, similar to root on the host.

[Continue with more questions...]

## Mixed Practice Questions - Storage, Security, and Troubleshooting

### Storage Scenarios

### Question 16
You have a PersistentVolumeClaim that remains in 'Pending' state. Given this manifest:
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
  storageClassName: "standard"
```
What could be the cause?

a) No PV available with ReadWriteMany access mode
b) StorageClass "standard" doesn't exist
c) Requested storage size too large
d) All of the above

**Answer:** d
**Explanation:** A PVC can remain in 'Pending' state for any of these reasons. Check:
- Available PVs and their access modes
- StorageClass existence and configuration
- Available storage capacity

### Question 17
In a production environment, you need to expand a PVC. Which statement must be true?

a) The StorageClass must allow volume expansion
b) The pod using the PVC must be deleted first
c) The original PV must be manually expanded
d) A new PVC must be created

**Answer:** a
**Explanation:** Volume expansion requires the StorageClass to have allowVolumeExpansion: true. The storage provider must also support online volume resizing.

### Security Scenarios

### Question 18
You notice unauthorized access to your cluster's pods. Given this NetworkPolicy:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```
Why might it not be working?

a) Network plugin doesn't support NetworkPolicies
b) Policy is missing egress rules
c) podSelector is empty
d) Policy is in wrong namespace

**Answer:** a
**Explanation:** NetworkPolicies require a network plugin that supports them (like Calico or Weave). Some plugins don't implement NetworkPolicy support.

### Question 19
A pod needs to access a Secret, but it's failing. Given:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-pod
spec:
  containers:
  - name: myapp
    image: nginx
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
```
What should you check first?

a) Secret exists in the same namespace as the pod
b) Pod has correct RBAC permissions
c) Secret is properly encoded
d) Container image supports secrets

**Answer:** a
**Explanation:** Secrets are namespace-scoped. The most common issue is the Secret not existing in the same namespace as the pod trying to use it.

### Troubleshooting Scenarios

### Question 20
Your pod shows CrashLoopBackOff status. Given these events:
```
10s   Warning   BackOff     Pod   Back-off restarting failed container
25s   Normal    Pulled      Pod   Container image "myapp:v1" already present on machine
26s   Normal    Created     Pod   Created container myapp
26s   Warning   Failed      Pod   Error: Command 'python app.py' not found
```
What's the most likely cause?

a) Image doesn't contain required executable
b) Resource limits too low
c) Network connectivity issues
d) Volume mount failure

**Answer:** a
**Explanation:** The error "Command not found" indicates the container image doesn't contain the specified command or necessary runtime (python in this case).

### Question 21
A deployment's pods aren't being scheduled. Given:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: web
        image: nginx
        resources:
          requests:
            memory: "2Gi"
            cpu: "2"
```
And cluster nodes:
```
NAME       CPU    MEMORY
node-1     2      4Gi
node-2     2      4Gi
```
Why aren't pods scheduling?

a) Resource requests exceed node capacity
b) Deployment missing selector
c) Image pull failure
d) Node affinity rules preventing scheduling

**Answer:** a
**Explanation:** Each pod requests 2 CPU cores and 2Gi memory. Nodes only have 2 CPU cores each, and with system resources reserved, there's not enough capacity for pods.

### Question 22
Your service isn't accessible. Given:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 8080
```
And pod:
```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    application: web
spec:
  containers:
  - name: web
    image: nginx
    ports:
    - containerPort: 8080
```
What's the issue?

a) Service selector doesn't match pod labels
b) Port mismatch
c) Service type not specified
d) Pod not ready

**Answer:** a
**Explanation:** Service selector (app: web) doesn't match pod labels (application: web). Labels must match exactly for the service to select the pod.

### Question 23
During a cluster upgrade, you notice etcd data loss. Which statement about etcd backup is correct?

a) etcd automatically replicates data to all master nodes
b) Taking snapshots while etcd is running is unsafe
c) Backing up etcd requires stopping the API server
d) etcd snapshot includes all cluster resources

**Answer:** d
**Explanation:** etcd snapshots contain the complete state of the cluster at the time of backup, including all resources, their states, and metadata.

### Question 24
A pod with multiple containers shows one container not ready. Given:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-pod
spec:
  containers:
  - name: web
    image: nginx
    readinessProbe:
      httpGet:
        path: /healthz
        port: 8080
  - name: cache
    image: redis
```
What should you check first?

a) Container port configuration
b) Readiness probe endpoint existence
c) Container logs
d) Network policy

**Answer:** b
**Explanation:** The readiness probe is checking /healthz on port 8080, but there's no indication this endpoint exists. Check container logs and ensure the application serves the health check endpoint.

### Question 25
Your StatefulSet pods aren't retaining data after restarts. Given:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
  replicas: 3
  template:
    spec:
      containers:
      - name: nginx
        image: nginx
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```
What's missing?

a) StorageClass specification
b) PersistentVolume definition
c) Volume retention policy
d) Pod anti-affinity rules

**Answer:** a
**Explanation:** Without a specified StorageClass, the default StorageClass will be used. If no default StorageClass exists, PVC creation will fail and pods won't have persistent storage.