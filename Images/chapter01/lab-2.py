from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, Deploy, RS
from diagrams.k8s.network import SVC
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.podconfig import CM, Secret
from diagrams.k8s.group import NS

# Set diagram attributes
with Diagram("Basic Kubernetes Operations Lab", show=False, direction="LR", filename="chapter01_lab02"):
    # Control Plane
    with Cluster("Control Plane"):
        api = APIServer("kube-apiserver")
        
    # Namespace Operations
    with Cluster("Namespace: my-namespace"):
        ns = NS("namespace")
        
        # Deployment and Pod Management
        with Cluster("Deployment Flow"):
            deploy = Deploy("nginx-deployment")
            rs = RS("ReplicaSet")
            pods = [Pod("nginx-pod-1"),
                   Pod("nginx-pod-2")]
            
            # Show deployment flow
            deploy >> rs >> pods
        
        # Service and Configuration
        svc = SVC("nginx-service")
        config = CM("nginx-config")
        
        # Show service connection
        pods >> svc
        config >> pods

    # Show API server control
    api >> deploy
    api >> svc
    api >> config
    api >> ns