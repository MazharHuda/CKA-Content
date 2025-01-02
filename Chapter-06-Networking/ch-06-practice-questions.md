# Chapter 6: Kubernetes Networking - Practice Questions

## Section 1: Pod Networking Fundamentals

### Question 1
What is the default network model in Kubernetes that states "all pods can communicate with all other pods without NAT"?

a) Container Network Model
b) Kubernetes Network Model
c) Pod Network Model
d) Container Network Interface

**Answer:** b
**Explanation:** The Kubernetes Network Model is a fundamental requirement stating that all pods must be able to communicate with each other without NAT, regardless of which node they are on.

### Question 2
Given this pod definition:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
  - name: container1
    image: nginx
  - name: container2
    image: redis
```
How do these containers communicate with each other within the pod?

a) Using the pod's IP address and different ports
b) Using localhost and different ports
c) Using container IPs and different ports
d) Using service discovery

**Answer:** b
**Explanation:** Containers within the same pod share the same network namespace and can communicate with each other using localhost, as they share the same network stack.

## Section 2: Services and Service Discovery

### Question 3
You have a service defined as follows:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080
  selector:
    app: myapp
```
What is the correct way to access this service from outside the cluster?

a) http://cluster-ip:80
b) http://node-ip:30080
c) http://node-ip:8080
d) http://my-service:80

**Answer:** b
**Explanation:** NodePort services can be accessed from outside the cluster using any node's IP address and the specified nodePort (30080 in this case).

### Question 4
What happens to a service's endpoints if all pods matching its selector are down?

a) The service is automatically deleted
b) The service continues to exist but has zero endpoints
c) The service starts routing to random pods
d) The service is marked as failed

**Answer:** b
**Explanation:** When no pods match a service's selector, the service continues to exist but has zero endpoints. Any attempts to access the service will fail until matching pods become available.

## Section 3: Network Policies

### Question 5
Given this network policy:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
```
What is the effect of this policy?

a) Allows all traffic to pods with label role=db
b) Denies all traffic to pods with label role=db
c) Allows only ingress traffic to pods with label role=db
d) Has no effect as no ingress rules are specified

**Answer:** b
**Explanation:** This network policy selects pods with label role=db and specifies only ingress type without any ingress rules, effectively denying all incoming traffic to these pods.

### Question 6
In a namespace with no network policies, what is the default behavior for pod communication?

a) All pods can communicate with each other
b) No pods can communicate with each other
c) Only pods in the same namespace can communicate
d) Communication is only allowed within the same node

**Answer:** a
**Explanation:** By default, if no network policies exist in a namespace, all pods can communicate with each other without restrictions.

## Section 4: DNS and Service Discovery

### Question 7
What is the fully qualified domain name (FQDN) for a service named 'web' in namespace 'prod'?

a) web.prod
b) web.prod.svc
c) web.prod.svc.cluster.local
d) web.cluster.local

**Answer:** c
**Explanation:** The FQDN format for Kubernetes services is: service-name.namespace.svc.cluster.local

### Question 8
You have a pod that needs to resolve external DNS names. Which DNS policy should you use?

a) ClusterFirst
b) Default
c) None
d) ClusterFirstWithHostNet

**Answer:** a
**Explanation:** ClusterFirst is the default DNS policy that allows pods to resolve both cluster internal DNS and external DNS names, with preference given to cluster DNS.

## Section 5: Load Balancing and Ingress

### Question 9
Examine this ingress configuration:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: test-ingress
spec:
  rules:
  - host: foo.bar.com
    http:
      paths:
      - path: /foo
        pathType: Prefix
        backend:
          service:
            name: service1
            port:
              number: 80
      - path: /bar
        pathType: Prefix
        backend:
          service:
            name: service2
            port:
              number: 80
```
What will happen to a request to foo.bar.com/test?

a) It will be routed to service1
b) It will be routed to service2
c) It will return a 404 error
d) It will be load balanced between service1 and service2

**Answer:** c
**Explanation:** The request path /test doesn't match any of the defined paths (/foo or /bar), so it will result in a 404 error.

### Question 10
What is the purpose of sessionAffinity in a Service configuration?

a) To ensure high availability
b) To route requests from the same client to the same pod
c) To enable persistent storage
d) To configure load balancing

**Answer:** b
**Explanation:** sessionAffinity: ClientIP ensures that requests from the same client IP address are always routed to the same pod.

## Section 6: Advanced Networking Scenarios

### Question 11
You need to connect your Kubernetes cluster to an external database using its FQDN. Which service type should you use?

a) ClusterIP
b) NodePort
c) LoadBalancer
d) ExternalName

**Answer:** d
**Explanation:** ExternalName service type is used to create a CNAME record to an external domain name, making it ideal for connecting to external services using DNS names.

### Question 12
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

a) Only pods with label role=frontend in any namespace
b) Only pods in namespaces with label environment=production
c) Pods with label role=frontend in namespaces with label environment=production
d) Either pods with label role=frontend OR pods in namespaces with label environment=production

**Answer:** d
**Explanation:** The policy uses separate selectors (not nested), so it allows traffic from either pods with label role=frontend OR from any pod in namespaces labeled environment=production.

[Continue with more questions...]

## Section 7: CNI Configuration and Troubleshooting

### Question 13
Given this CNI configuration:
```json
{
  "cniVersion": "0.3.1",
  "name": "cluster-network",
  "type": "calico",
  "ipam": {
    "type": "calico-ipam",
    "assign_ipv4": "true",
    "ipv4_pools": ["10.244.0.0/16"]
  },
  "policy": {
    "type": "k8s"
  }
}
```
What is the purpose of the "ipam" section?

a) To configure network security policies
b) To manage IP address allocation for pods
c) To set up routing between nodes
d) To configure DNS settings

**Answer:** b
**Explanation:** The IPAM (IP Address Management) section in CNI configuration defines how IP addresses are allocated to pods. It specifies the IP range (10.244.0.0/16) and the IPAM plugin (calico-ipam) to use for address management.

### Question 14
You notice pods are stuck in "ContainerCreating" state with the following error:
```bash
failed to find plugin "calico" in path [/opt/cni/bin]
```
What is the most likely cause?

a) CNI plugin binary is missing
b) Incorrect network policy
c) Pod configuration error
d) Node network issue

**Answer:** a
**Explanation:** This error indicates that the CNI plugin binary (calico in this case) is not present in the CNI binary directory (/opt/cni/bin). This commonly occurs when:
- CNI plugin is not properly installed
- CNI binary path is incorrect
- Plugin files are corrupted or missing permissions

### Question 15
Examine this Calico network policy:
```yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: allow-tcp-6379
spec:
  selector: app == 'redis'
  types:
  - Ingress
  - Egress
  ingress:
  - action: Allow
    protocol: TCP
    source:
      selector: role == 'frontend'
    destination:
      ports:
      - 6379
```
A pod with label role=frontend cannot connect to Redis. What should you check first?

a) Redis pod labels
b) TCP port configuration
c) Network plugin status
d) Pod CIDR configuration

**Answer:** a
**Explanation:** The policy uses selector app == 'redis' to identify target pods. First, verify that the Redis pods have the correct label (app: redis). Common troubleshooting steps:
1. Check pod labels: kubectl get pods --show-labels
2. Verify policy is applied: kubectl get networkpolicy
3. Check calico node status: calicoctl node status

### Question 16
Your cluster uses Weave Net and pods on different nodes cannot communicate. Given this output:
```bash
$ kubectl get pods -n kube-system
NAME                READY   STATUS    RESTARTS   AGE
weave-net-1abc2    1/1     Running   0          1h
weave-net-3def4    1/1     Running   0          1h
```
What should you check next?

a) Pod IP ranges
b) Weave Net logs
c) Node firewall rules
d) Service configuration

**Answer:** b
**Explanation:** When pods can't communicate across nodes with Weave Net:
1. Check Weave Net logs first: `kubectl logs -n kube-system weave-net-1abc2 weave`
2. Look for:
   - Peer connection issues
   - IPAM conflicts
   - Encryption problems
   - MTU misconfigurations

### Question 17
You're troubleshooting CNI issues and see this in kubelet logs:
```log
failed to set up pod "nginx-deployment-66b6c48dd5-abcd" network: error getting ClusterInformation: Get "https://10.96.0.1:443/apis/crd.projectcalico.org/v1/clusterinformations/default": dial tcp 10.96.0.1:443: i/o timeout
```
What is the most likely issue?

a) Calico CRDs are not installed
b) API server is unreachable
c) Pod network configuration is incorrect
d) CNI binary is missing

**Answer:** a
**Explanation:** This error indicates that Calico Custom Resource Definitions (CRDs) are missing. Resolution steps:
1. Verify CRD installation:
```bash
kubectl get crd | grep calico
```
2. Install Calico CRDs if missing:
```bash
kubectl apply -f https://docs.projectcalico.org/manifests/crds.yaml
```
3. Verify Calico operator status
4. Check API server connectivity

### Question 18
Given this MTU-related CNI configuration:
```yaml
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  calicoNetwork:
    mtu: 1440
```
Pods are experiencing packet fragmentation. What could be the cause?

a) MTU is too high
b) MTU is too low
c) Incorrect CNI plugin
d) Network policy blocking traffic

**Answer:** b
**Explanation:** MTU issues often cause packet fragmentation. Troubleshooting steps:
1. Check overlay network requirements:
   - VXLAN typically needs 50 bytes overhead
   - IPsec needs additional 30-32 bytes
2. Calculate correct MTU:
   - Base MTU (usually 1500)
   - Subtract overlay overhead
3. Common MTU values:
   - Standard: 1500
   - VXLAN: 1450
   - IPsec: 1420

### Question 19
Examine this CNI troubleshooting pod:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cni-debug
spec:
  hostNetwork: true
  containers:
  - name: debug
    image: nicolaka/netshoot
    securityContext:
      privileged: true
    volumeMounts:
    - name: cni-config
      mountPath: /etc/cni/net.d
  volumes:
  - name: cni-config
    hostPath:
      path: /etc/cni/net.d
```
Why is hostNetwork: true necessary?

a) To access node network directly
b) To bypass CNI configuration
c) To enable privileged mode
d) To mount host volumes

**Answer:** a
**Explanation:** hostNetwork: true is required because:
1. It allows the pod to use the node's network namespace
2. Enables direct access to node networking
3. Necessary for debugging CNI issues
4. Allows inspection of CNI configuration without CNI plugin interference

### Question 20
Your cluster uses Flannel CNI and pods report duplicate IP addresses. What should you check?

a) IPAM configuration
b) kube-controller-manager status
c) Pod CIDR ranges
d) Service CIDR ranges

**Answer:** c
**Explanation:** Duplicate IP addresses with Flannel usually indicate overlapping Pod CIDR ranges. Resolution steps:
1. Check node Pod CIDR allocation:
```bash
kubectl get nodes -o jsonpath='{.items[*].spec.podCIDR}'
```
2. Verify Flannel configuration:
```bash
kubectl get cm -n kube-system kube-flannel-cfg -o yaml
```
3. Ensure each node has a unique Pod CIDR
4. Check for IPAM conflicts in Flannel logs

## Section 8: Service Mesh Concepts

### Question 21
Given this Istio VirtualService configuration:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews-route
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        user-agent:
          exact: "mobile"
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v1
```
What happens to requests with a "mobile" user-agent header?

a) They are blocked
b) They are routed to v2
c) They are routed to v1
d) They are load balanced between v1 and v2

**Answer:** b
**Explanation:** The VirtualService configuration:
1. Matches requests with user-agent "mobile"
2. Routes matched requests to the v2 subset
3. All other requests go to v1 subset
4. Uses header-based routing for traffic splitting
5. Implements A/B testing based on user agent

### Question 22
In a service mesh architecture, what is the primary purpose of a sidecar proxy?

a) To provide storage for the main container
b) To handle inter-service communication
c) To manage container logs
d) To scale the application

**Answer:** b
**Explanation:** Sidecar proxy (e.g., Envoy) in a service mesh:
1. Handles all inter-service communication
2. Provides:
   - Traffic management
   - Security (mTLS)
   - Observability
   - Policy enforcement
3. Implements service mesh control plane decisions
4. Enables transparent networking features

### Question 23
Examine this Istio DestinationRule:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: my-service
spec:
  host: my-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 1024
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
```
What is the purpose of outlierDetection configuration?

a) To detect network latency
b) To implement circuit breaking
c) To monitor connection pools
d) To track load balancing

**Answer:** b
**Explanation:** OutlierDetection implements circuit breaking by:
1. Monitoring for consecutive 5xx errors
2. Ejecting failing endpoints temporarily
3. Implementing automatic service resilience
4. Key parameters:
   - consecutive5xxErrors: Number of errors before ejection
   - interval: How often to check for errors
   - baseEjectionTime: How long to eject the endpoint

### Question 24
You have implemented mutual TLS in your service mesh. Which statement is true?

a) Only the server needs a certificate
b) Only the client needs a certificate
c) Both client and server need certificates
d) No certificates are needed

**Answer:** c
**Explanation:** Mutual TLS (mTLS) in service mesh:
1. Requires certificates for both client and server
2. Provides:
   - Two-way authentication
   - Encryption of traffic
   - Identity verification
3. Implementation details:
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT
```

### Question 25
Given this Istio Gateway configuration:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: my-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: MUTUAL
      serverCertificate: /etc/certs/server.pem
      privateKey: /etc/certs/privatekey.pem
      caCertificates: /etc/certs/ca.pem
    hosts:
    - "*.example.com"
```
What type of TLS configuration is being used?

a) Simple TLS
b) Mutual TLS
c) Passthrough TLS
d) No TLS

**Answer:** b
**Explanation:** The Gateway uses Mutual TLS (mTLS) because:
1. tls.mode is set to MUTUAL
2. Requires:
   - Server certificate
   - Private key
   - CA certificates
3. Provides:
   - Client authentication
   - Server authentication
   - Encrypted communication

### Question 26
In a service mesh, what is the purpose of a ServiceEntry?

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: external-svc
spec:
  hosts:
  - api.external.com
  ports:
  - number: 443
    name: https
    protocol: HTTPS
  resolution: DNS
  location: MESH_EXTERNAL
```

a) To define internal services
b) To allow access to external services
c) To create service endpoints
d) To configure load balancing

**Answer:** b
**Explanation:** ServiceEntry:
1. Adds external services to the mesh's service registry
2. Enables:
   - Controlled access to external services
   - Application of mesh features to external traffic
   - Monitoring of external service calls
3. Configuration options:
   - DNS or static resolution
   - Location (internal/external)
   - Port and protocol definitions

### Question 27
What is the purpose of this Istio configuration?
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: fault-injection
spec:
  hosts:
  - my-service
  http:
  - fault:
      delay:
        percentage:
          value: 10
        fixedDelay: 5s
    route:
    - destination:
        host: my-service
```

a) To improve service performance
b) To test service resilience
c) To load balance traffic
d) To secure service communication

**Answer:** b
**Explanation:** This configuration implements fault injection:
1. Adds artificial delays to test service resilience
2. Key aspects:
   - Delays 10% of requests
   - 5-second fixed delay
   - Tests timeout handling
   - Verifies retry mechanisms
3. Used for:
   - Chaos engineering
   - Resilience testing
   - Timeout verification
   - Error handling validation

### Question 28
In a service mesh, what is the relationship between control plane and data plane?

a) They operate independently
b) Control plane configures data plane
c) Data plane manages control plane
d) They are the same component

**Answer:** b
**Explanation:** Service mesh architecture:
1. Control Plane:
   - Manages configuration
   - Handles service discovery
   - Implements policies
   - Distributes certificates
2. Data Plane:
   - Consists of proxies (sidecars)
   - Handles actual traffic
   - Enforces policies
   - Reports telemetry
3. Interaction:
   - Control plane pushes configuration to proxies
   - Proxies report metrics back to control plane
   - Real-time policy enforcement

## Section 9: Troubleshooting Scenarios

### Question 29
You observe the following pod status:
```bash
$ kubectl get pod web-app
NAME      READY   STATUS    RESTARTS   AGE
web-app   0/1     Pending   0          10m
```
Examining the pod events shows:
```bash
$ kubectl describe pod web-app
Events:
  Type     Reason             Age    From               Message
  ----     ------             ----   ----               -------
  Warning  FailedScheduling   5m     default-scheduler  0/3 nodes are available: 3 pod has unbound immediate PersistentVolumeClaims.
```
What is the most likely cause of this issue?

a) Network policy blocking pod creation
b) Insufficient node resources
c) Missing persistent volume
d) Container image not found

**Answer:** c
**Explanation:** Troubleshooting steps:
1. Check PVC status:
```bash
kubectl get pvc
kubectl describe pvc <pvc-name>
```
2. Verify PV availability:
```bash
kubectl get pv
```
3. Check storage class:
```bash
kubectl get storageclass
```
4. Resolution options:
   - Create required PV
   - Fix storage class provisioner
   - Modify PVC requirements

### Question 30
Given this service configuration:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  selector:
    app: backend
  ports:
  - port: 80
    targetPort: 8080
```
The service is not routing traffic. Running:
```bash
$ kubectl get endpoints backend-service
NAME             ENDPOINTS   AGE
backend-service  <none>     5m
```
What should you check first?

a) Service port configuration
b) Pod label matching
c) Network policy
d) Node port configuration

**Answer:** b
**Explanation:** No endpoints indicates a label mismatch. Troubleshooting steps:
1. Check pod labels:
```bash
kubectl get pods --show-labels | grep backend
```
2. Compare with service selector:
```bash
kubectl describe svc backend-service
```
3. Verify pod readiness:
```bash
kubectl get pods -l app=backend
```
4. Common fixes:
   - Correct pod labels
   - Update service selector
   - Check pod readiness probe

### Question 31
Examining CoreDNS logs shows:
```bash
$ kubectl logs -n kube-system coredns-74ff55c5b-abcd
[ERROR] plugin/errors: 2 "SERVFAIL" remote="10.244.0.15:60953"
```
And a pod shows:
```bash
$ kubectl exec -it test-pod -- nslookup kubernetes.default
;; connection timed out; no servers could be reached
```
What should you investigate?

a) Pod network connectivity
b) CoreDNS configuration
c) Service CIDR range
d) Node DNS settings

**Answer:** a
**Explanation:** DNS issues often indicate network connectivity problems. Investigation steps:
1. Check CoreDNS pods:
```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
```
2. Verify network policies:
```bash
kubectl get networkpolicy
```
3. Test pod DNS configuration:
```bash
kubectl exec test-pod -- cat /etc/resolv.conf
```
4. Check CNI plugin status:
```bash
kubectl get pods -n kube-system -l k8s-app=calico-node
```

### Question 32
Your ingress controller logs show:
```bash
SSL certificate error: certificate has expired
```
And the configuration is:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-ingress
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: tls-secret
```
What commands would help diagnose this?

a) kubectl get ingress
b) kubectl describe secret tls-secret
c) kubectl get pods
d) kubectl get services

**Answer:** b
**Explanation:** Certificate expiration requires checking the TLS secret. Troubleshooting steps:
1. Check secret details:
```bash
kubectl describe secret tls-secret
```
2. Examine certificate:
```bash
kubectl get secret tls-secret -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text
```
3. Verify ingress configuration:
```bash
kubectl describe ingress secure-ingress
```
4. Resolution steps:
   - Generate new certificate
   - Update secret
   - Verify ingress controller picks up changes

### Question 33
Pod logs show:
```bash
Error: dial tcp 10.96.0.1:443: i/o timeout
```
What troubleshooting steps should you take first?

a) Check pod IP configuration
b) Verify kube-apiserver status
c) Review network policies
d) Check DNS configuration

**Answer:** b
**Explanation:** This error indicates API server connectivity issues. Investigation steps:
1. Check API server status:
```bash
kubectl get componentstatuses
kubectl get pods -n kube-system | grep apiserver
```
2. Verify network connectivity:
```bash
curl -k https://10.96.0.1:443
```
3. Check kube-proxy:
```bash
kubectl get pods -n kube-system | grep kube-proxy
kubectl logs -n kube-system kube-proxy-xxxxx
```
4. Review service CIDR configuration

### Question 34
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
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          environment: production
```
Database pods are unreachable from production namespace. What should you verify?

a) Pod labels
b) Namespace labels
c) Port configuration
d) Protocol specification

**Answer:** b
**Explanation:** Network policy uses namespace selector. Verification steps:
1. Check namespace labels:
```bash
kubectl get namespace --show-labels
```
2. Verify policy application:
```bash
kubectl describe networkpolicy db-policy
```
3. Test connectivity:
```bash
kubectl run test-pod -n production --image=busybox -- sleep 3600
kubectl exec -it test-pod -n production -- wget -O- http://database-service
```
4. Common fixes:
   - Add missing namespace labels
   - Correct namespace selector
   - Verify CNI plugin supports network policies