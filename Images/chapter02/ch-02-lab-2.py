from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, RS, Deploy
from diagrams.k8s.network import SVC
from diagrams.k8s.podconfig import CM
from diagrams.k8s.group import NS

# Set diagram attributes
with Diagram("Basic Kubernetes Objects Lab", show=False, direction="TB", filename="ch02_lab02_basic_objects"):
    
    # Create Deployment Flow
    with Cluster("Deployment Flow"):
        deploy = Deploy("nginx-deployment")
        rs = RS("frontend-replicaset")
        pods = [
            Pod("nginx-pod-1"),
            Pod("nginx-pod-2"),
            Pod("nginx-pod-3")
        ]
        
        # Show deployment management
        deploy >> Edge(color="blue", style="bold") >> rs
        rs >> Edge(color="blue") >> pods

    # Service Layer
    with Cluster("Service Layer"):
        svc = SVC("frontend-service")
        
        # Show service relationship
        svc >> Edge(color="red", style="dashed") >> pods

    # Configuration
    with Cluster("Configuration"):
        config = CM("nginx-config")
        
        # Show config relationship
        config >> Edge(color="green", style="dotted") >> pods

    # Resource Management
    with Cluster("Resource Management"):
        ns = NS("development")
        
        # Show namespace scope
        ns - Edge(color="black", style="dashed") - deploy
        ns - Edge(color="black", style="dashed") - svc