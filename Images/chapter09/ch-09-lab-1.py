from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.infra import Node
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.podconfig import CM
from diagrams.k8s.group import NS

# Set diagram attributes
with Diagram("Metrics Server Architecture", show=False, direction="TB", filename="ch09_lab01_metrics_server"):
    
    # API Server as central component
    with Cluster("Control Plane"):
        api = APIServer("kube-apiserver")
        
        # Metrics Server deployment
        with Cluster("kube-system namespace"):
            ns = NS("kube-system")
            metrics_server = Pod("metrics-server")
            config = CM("metrics-config")
            
            # Configuration relationship
            config >> Edge(color="brown", style="dotted", label="configure") >> metrics_server
    
    # Worker Nodes and Pods
    with Cluster("Worker Nodes"):
        # Create nodes individually for proper connection
        node1 = Node("worker-node-1")
        node2 = Node("worker-node-2")
        
        with Cluster("Application Pods"):
            # Create pods individually
            pod1 = Pod("app-pod-1")
            pod2 = Pod("app-pod-2")
            pod3 = Pod("app-pod-3")
            
            # Show pod placement - connect each node to pods
            node1 >> Edge(color="black", style="dotted") >> pod1
            node1 >> Edge(color="black", style="dotted") >> pod2
            node2 >> Edge(color="black", style="dotted") >> pod3
    
    # Metrics Collection Flow - connect to individual nodes and pods
    metrics_server >> Edge(color="blue", style="bold", label="collect metrics") >> node1
    metrics_server >> Edge(color="blue", style="bold", label="collect metrics") >> node2
    
    metrics_server >> Edge(color="green", style="bold", label="collect metrics") >> pod1
    metrics_server >> Edge(color="green", style="bold", label="collect metrics") >> pod2
    metrics_server >> Edge(color="green", style="bold", label="collect metrics") >> pod3
    
    # API Communication
    metrics_server >> Edge(color="red", style="dashed", label="store metrics") >> api
    api >> Edge(color="orange", label="kubectl top") >> metrics_server