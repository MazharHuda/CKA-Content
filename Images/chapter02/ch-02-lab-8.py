from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.rbac import Role, RoleBinding, User, Group, ClusterRole, ClusterRoleBinding
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import NetworkPolicy
from diagrams.k8s.podconfig import Secret
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.infra import Node

# Set diagram attributes
with Diagram("Kubernetes Security Implementation Lab", show=False, direction="TB", filename="ch02_lab08_security"):
    
    # API Server and Authentication
    with Cluster("Authentication & Authorization"):
        api = APIServer("kube-apiserver")
        
        # RBAC Components
        with Cluster("RBAC Configuration"):
            role = Role("pod-reader")
            c_role = ClusterRole("cluster-admin")
            binding = RoleBinding("pod-reader-binding")
            c_binding = ClusterRoleBinding("cluster-admin-binding")
            
            # Users and Groups
            user = User("dev-user")
            group = Group("dev-team")
            
            # Show RBAC relationships
            user >> Edge(color="blue") >> binding >> role
            group >> Edge(color="blue") >> c_binding >> c_role
    
    # Workload Security
    with Cluster("Secure Workloads"):
        with Cluster("Production Namespace"):
            # Pod with Security Context
            secure_pod = Pod("secure-pod")
            secret = Secret("app-secrets")
            
            # Network Policy
            net_policy = NetworkPolicy("pod-network-policy")
            
            # Show security relationships
            secret >> Edge(color="red", style="dashed") >> secure_pod
            net_policy >> Edge(color="orange", style="dotted") >> secure_pod
            
    # Node Security
    with Cluster("Node Security"):
        node = Node("worker-node")
        
        # Show node authorization
        api >> Edge(color="green") >> node
        node >> Edge(color="green", style="dashed") >> secure_pod