# Chapter 3: Cluster Setup and Configuration

## 1. Kubernetes Cluster Architecture

### 1.1 Overview
A Kubernetes cluster consists of a control plane and worker nodes, forming a highly available and scalable container orchestration platform.

```ascii
┌─────────────────────────────────────────────────────────┐
│                  Kubernetes Cluster                      │
│                                                         │
│  ┌─────────────┐ ┌─────────────┐  ┌─────────────┐      │
│  │Control Plane│ │Control Plane│  │Control Plane│      │
│  │   Node 1    │ │   Node 2    │  │   Node 3    │      │
│  └─────────────┘ └─────────────┘  └─────────────┘      │
│         ▲              ▲               ▲                │
│         │              │               │                │
│         ▼              ▼               ▼                │
│  ┌─────────────┐ ┌─────────────┐  ┌─────────────┐      │
│  │Worker Node 1│ │Worker Node 2│  │Worker Node 3│      │
│  └─────────────┘ └─────────────┘  └─────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Control Plane Components Configuration

#### 1.2.1 API Server Configuration
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --advertise-address=192.168.1.10
    - --allow-privileged=true
    - --authorization-mode=Node,RBAC
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --enable-admission-plugins=NodeRestriction
    - --enable-bootstrap-token-auth=true
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
    - --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
    - --etcd-servers=https://127.0.0.1:2379
    - --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt
    - --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
    - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
    - --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
    image: k8s.gcr.io/kube-apiserver:v1.23.0
```

**Best Practices:**
1. Enable RBAC authorization
2. Configure appropriate admission controllers
3. Use secure communication (TLS)
4. Implement proper authentication methods
5. Set resource limits

**Common Pitfalls:**
- Insufficient security configuration
- Missing certificates
- Improper RBAC setup
- Resource constraints

#### 1.2.2 etcd Configuration
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: etcd
  namespace: kube-system
spec:
  containers:
  - command:
    - etcd
    - --advertise-client-urls=https://192.168.1.10:2379
    - --data-dir=/var/lib/etcd
    - --initial-cluster=master=https://192.168.1.10:2380
    - --initial-cluster-state=new
    - --listen-client-urls=https://127.0.0.1:2379
    - --listen-peer-urls=https://192.168.1.10:2380
    - --name=master
    image: k8s.gcr.io/etcd:3.5.1
```

### 1.3 High Availability Setup

```ascii
┌────────────────────────────────────────────────────┐
│                   Load Balancer                     │
│                   (HAProxy/LB)                      │
└───────────────┬────────────────┬──────────────────┘
                │                │
        ┌───────▼───────┐ ┌─────▼─────────┐
        │  API Server 1  │ │  API Server 2  │
        └───────┬───────┘ └─────┬─────────┘
                │               │
        ┌───────▼───────┐ ┌─────▼─────────┐
        │     etcd 1    │ │    etcd 2     │
        └───────────────┘ └───────────────┘
```

#### 1.3.1 Load Balancer Configuration (HAProxy Example)
```conf
frontend kubernetes
    bind *:6443
    mode tcp
    option tcplog
    default_backend kubernetes-master-nodes

backend kubernetes-master-nodes
    mode tcp
    balance roundrobin
    option tcp-check
    server master1 192.168.1.10:6443 check fall 3 rise 2
    server master2 192.168.1.11:6443 check fall 3 rise 2
```

[Continue with more sections...]