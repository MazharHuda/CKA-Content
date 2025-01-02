from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.rbac import Role, RoleBinding, User, Group
from diagrams.k8s.compute import Pod
from diagrams.k8s.podconfig import Secret, CM
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.others import CRD

# Set diagram attributes
with Diagram("Kubernetes Security Implementation Lab", show=False, direction="TB", filename="ch02_lab06_security"):
    
    # API Server and Authentication
    with Cluster("Authentication & Authorization"):
        api = APIServer("kube-apiserver")
        user = User("app-user")
        group = Group("dev-group")
        
    # RBAC Configuration
    with Cluster("RBAC Components"):
        role = Role("app-role")
        binding = RoleBinding("app-rolebinding")
        
        # Show RBAC relationships
        user >> Edge(color="blue") >> binding
        group >> Edge(color="blue") >> binding
        binding >> Edge(color="green") >> role
        
    # Secure Workload
    with Cluster("Secure Application"):
        secret = Secret("app-secrets")
        config = CM("app-config")
        
        with Cluster("Pod Security"):
            pod = Pod("secure-pod")
            
            # Show security relationships
            secret >> Edge(color="red", style="dashed") >> pod
            config >> Edge(color="orange", style="dashed") >> pod
            
    # Authorization Flow
    api >> Edge(color="darkgreen", style="bold") >> role
    role >> Edge(color="darkgreen", style="bold") >> pod

# This diagram shows:
# Authentication and authorization flow
# RBAC component relationships
# Secret and ConfigMap usage
# Pod security context
# API server interactions