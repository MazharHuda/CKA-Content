# Chapter 4: Pod Orchestration and Scheduling - Practice Questions

## Section 1: Pod Configuration and Management

### Question 1
Given this pod manifest:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    livenessProbe:
      httpGet:
        path: /healthz
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 80
      initialDelaySeconds: 2
      periodSeconds: 5
```
What will happen if the /healthz endpoint returns a 500 error?

a) The pod will be restarted
b) The pod will be marked as not ready
c) The pod will continue running normally
d) The pod will be evicted from the node

**Answer:** a
**Explanation:** A failed liveness probe indicates that the container is unhealthy and needs to be restarted. The kubelet will automatically restart the container when the liveness probe fails.

### Question 2
In a multi-container pod, what happens when one container exits with code 0?

a) All containers in the pod are restarted
b) Only the exited container is restarted
c) The pod continues running with remaining containers
d) The pod is terminated

**Answer:** c
**Explanation:** When a container in a pod exits with code 0 (success), it's considered a normal termination. Other containers in the pod continue running unless specified otherwise in the pod's restart policy.

## Section 2: Resource Management

### Question 3
Examine this resource configuration:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-pod
spec:
  containers:
  - name: app
    image: nginx
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```
What QoS class will this pod be assigned?

a) Guaranteed
b) Burstable
c) BestEffort
d) Critical

**Answer:** b
**Explanation:** This pod is assigned the Burstable QoS class because the resource requests are lower than the limits. For Guaranteed QoS, requests must equal limits.

### Question 4
Given these node resources:
```
Node1: CPU: 2000m, Memory: 4Gi
Node2: CPU: 4000m, Memory: 8Gi
```
And this pod specification:
```yaml
spec:
  containers:
  - name: app
    resources:
      requests:
        cpu: "2500m"
        memory: "3Gi"
```
Where will the pod be scheduled?

a) Node1
b) Node2
c) Either node randomly
d) Pod will remain in Pending state

**Answer:** b
**Explanation:** The pod requires 2.5 CPU cores and 3Gi memory. Only Node2 has sufficient resources to accommodate these requests.

## Section 3: Pod Scheduling

### Question 5
You have this node affinity configuration:
```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: zone
          operator: In
          values:
          - zone1
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 1
      preference:
        matchExpressions:
        - key: disk
          operator: In
          values:
          - ssd
```
If no nodes have label zone=zone1, what happens?

a) Pod is scheduled on a node with disk=ssd
b) Pod is scheduled on any available node
c) Pod remains in Pending state
d) Pod is scheduled but with a warning

**Answer:** c
**Explanation:** The requiredDuringSchedulingIgnoredDuringExecution field creates a hard requirement. If no nodes match the required label, the pod will remain in Pending state.

### Question 6
Given this taint on a node:
```bash
kubectl taint nodes node1 key=value:NoExecute
```
Which pod configuration will allow the pod to run on this node?

a) No special configuration needed
b) nodeSelector with key=value
c) Toleration matching the taint
d) Node affinity rule for the node

**Answer:** c
**Explanation:** A NoExecute taint requires a matching toleration for pods to run on the node. Pods without the toleration will be evicted if already running.

## Section 4: Multi-Container Patterns

### Question 7
In a sidecar pattern implementation:
```yaml
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - name: logs
      mountPath: /var/log/nginx
  - name: log-shipper
    image: fluentd
    volumeMounts:
    - name: logs
      mountPath: /var/log/nginx
  volumes:
  - name: logs
    emptyDir: {}
```
What happens if the app container crashes?

a) Only the app container restarts
b) Both containers restart
c) The pod is terminated
d) The log-shipper continues running

**Answer:** a
**Explanation:** In a multi-container pod, containers are independent in terms of runtime. If one container crashes, only that container is restarted while others continue running.

### Question 8
You have an init container that checks for a service:
```yaml
initContainers:
- name: init-myservice
  image: busybox
  command: ['sh', '-c', 'until nslookup myservice; do echo waiting; sleep 2; done;']
```
What happens if the service never becomes available?

a) Pod starts anyway after timeout
b) Pod remains in Pending state
c) Pod moves to Running state
d) Pod moves to Failed state

**Answer:** b
**Explanation:** Init containers must complete successfully before the pod's main containers can start. If an init container fails to complete, the pod remains in Pending state.

## Section 5: Advanced Scenarios

### Question 9
Given this pod disruption budget:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: web
```
What happens during a node drain if only 2 matching pods are running?

a) One pod can be evicted
b) No pods can be evicted
c) All pods can be evicted
d) Drain operation fails

**Answer:** b
**Explanation:** The PDB requires minimum 2 pods to be available. If only 2 pods are running, none can be evicted as it would violate the minimum availability requirement.

### Question 10
Examine this probe configuration:
```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
  failureThreshold: 3
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 20
```
How long after pod startup will the first readiness check occur?

a) 5 seconds
b) 10 seconds
c) 15 seconds
d) 20 seconds

**Answer:** c
**Explanation:** The readinessProbe's initialDelaySeconds is set to 15, so the first check will occur 15 seconds after container startup.