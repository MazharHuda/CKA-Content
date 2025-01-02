from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC, Ingress
from diagrams.k8s.infra import Node
from diagrams.k8s.podconfig import CM
from diagrams.onprem.network import Internet

# Set diagram attributes
with Diagram("Kubernetes Networking and Services Lab", show=False, direction="LR", filename="ch02_lab03_networking"):
    
    # External Access
    inet = Internet("External\nTraffic")

    # Create Service Types
    with Cluster("Service Layer"):
        clusterip = SVC("ClusterIP\nService")
        nodeport = SVC("NodePort\nService")
        lb = SVC("LoadBalancer\nService")

    # Create Application Pods
    with Cluster("Application Pods"):
        pods = [
            Pod("nginx-pod-1"),
            Pod("nginx-pod-2"),
            Pod("nginx-pod-3")
        ]

    # Create Test Pod
    with Cluster("Test Environment"):
        test_pod = Pod("test-pod\n(busybox)")
        
    # Show traffic flow
    inet >> Edge(color="blue", style="bold") >> nodeport
    inet >> Edge(color="blue", style="bold") >> lb
    
    # Service to Pod communication
    clusterip >> Edge(color="red") >> pods
    nodeport >> Edge(color="green") >> pods
    lb >> Edge(color="orange") >> pods
    
    # Test pod connections
    test_pod >> Edge(color="purple", style="dashed") >> clusterip
    test_pod >> Edge(color="purple", style="dashed") >> nodeport