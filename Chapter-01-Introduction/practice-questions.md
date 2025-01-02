 Chapter 1: Practice Questions

 Section 1: Basic Concepts

1. What is Kubernetes?
   a) A container runtime
   b) A container orchestration platform
   c) A Linux distribution
   d) A virtual machine manager
   
   Answer: b
   Explanation: Kubernetes is a container orchestration platform that automates the deployment, scaling, and management of containerized applications.

2. Which component serves as the primary control plane for Kubernetes?
   a) kubelet
   b) etcd
   c) kube-apiserver
   d) kube-scheduler
   
   Answer: c
   Explanation: The kube-apiserver is the front-end for the Kubernetes control plane, handling all API requests and serving as the gateway for cluster management.

 Section 2: Architecture Components

3. Which of the following is NOT a control plane component?
   a) kube-apiserver
   b) kube-scheduler
   c) kubelet
   d) kube-controller-manager
   
   Answer: c
   Explanation: kubelet is a node component that runs on every worker node, not a control plane component.

4. What is the purpose of etcd in a Kubernetes cluster?
   a) Container runtime
   b) Network proxy
   c) Distributed key-value store
   d) Load balancer
   
   Answer: c
   Explanation: etcd is a consistent and highly-available key-value store used for all cluster data storage.

 Section 3: Node Components

5. Which component maintains network rules on nodes?
   a) kubelet
   b) kube-proxy
   c) flannel
   d) docker
   
   Answer: b
   Explanation: kube-proxy maintains network rules on nodes, enabling pod-to-pod communication and service access.

6. What is the primary responsibility of kubelet?
   a) Managing network rules
   b) Storing cluster data
   c) Ensuring containers are running in a Pod
   d) Scheduling pods on nodes
   
   Answer: c
   Explanation: kubelet ensures that containers are running in a Pod according to the PodSpec.

 Section 4: Basic Operations

7. Which command is used to view the status of nodes in a cluster?
   ```
   a) kubectl get pods
   b) kubectl get nodes
   c) kubectl get services
   d) kubectl get deployments
   ```
   Answer: b
   Explanation: 'kubectl get nodes' displays the status of all nodes in the cluster.

8. What tool is commonly used for local Kubernetes development?
   a) Docker Desktop
   b) Minikube
   c) VirtualBox
   d) VMware
   
   Answer: b
   Explanation: Minikube is a tool that makes it easy to run a single-node Kubernetes cluster locally.

 Section 5: Core Concepts

9. What is the smallest deployable unit in Kubernetes?
   a) Container
   b) Pod
   c) Service
   d) Deployment
   
   Answer: b
   Explanation: A Pod is the smallest deployable unit that can be created and managed in Kubernetes.

10. Which statement about Pods is correct?
    a) Pods can only contain one container
    b) Pods always run on multiple nodes
    c) Pods share network namespace between containers
    d) Pods cannot be scaled
    
    Answer: c
    Explanation: Containers within a Pod share the same network namespace, allowing them to communicate via localhost.

 Section 6: Scenario-based Questions

11. You need to set up a local development environment for Kubernetes. Which sequence of steps is correct?
    a) Install Docker → Install kubectl → Install Minikube → Start cluster
    b) Install Minikube → Install Docker → Start cluster → Install kubectl
    c) Install kubectl → Install Minikube → Start cluster → Install Docker
    d) Install Docker → Install Minikube → Install kubectl → Start cluster
    
    Answer: a
    Explanation: Docker should be installed first as a prerequisite, followed by kubectl for cluster management, then Minikube for local cluster creation.

12. A pod is stuck in 'Pending' state. What could be the cause?
    a) Image not found
    b) Insufficient cluster resources
    c) Network plugin not installed
    d) All of the above
    
    Answer: d
    Explanation: A pod can be stuck in 'Pending' state due to any of these reasons: missing images, insufficient resources, or network issues.

 Section 7: Advanced Concepts

13. What is the purpose of a namespace in Kubernetes?
    a) To isolate nodes
    b) To group container images
    c) To organize cluster resources
    d) To manage storage volumes
    
    Answer: c
    Explanation: Namespaces provide a mechanism for isolating groups of resources within a single cluster.

14. Which component is responsible for scheduling decisions?
    a) kubelet
    b) kube-scheduler
    c) kube-proxy
    d) controller-manager
    
    Answer: b
    Explanation: The kube-scheduler is responsible for deciding which node should run each pod.

15. What happens to pods when a node fails?
    a) They are automatically rescheduled on other nodes
    b) They continue running on the failed node
    c) They are permanently lost
    d) They enter a suspended state
    
    Answer: a
    Explanation: If the pods are managed by a controller (like a Deployment), they will be rescheduled on other available nodes.

 Practice Test Review Guidelines

1. For each question you got wrong:
   - Review the related concept in the documentation
   - Understand why the correct answer is right
   - Practice any related commands or operations

2. Key Areas to Focus:
   - Kubernetes architecture
   - Core components
   - Basic operations
   - Troubleshooting steps

3. Additional Resources:
   - Kubernetes official documentation
   - Community forums
   - Practice environments