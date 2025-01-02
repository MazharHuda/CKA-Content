from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import SVC
from diagrams.k8s.infra import Node
from diagrams.onprem.network import Internet
from diagrams.generic.network import Switch

# Set diagram attributes
with Diagram("Lab 1: Pod Networking Architecture", show=False, direction="TB", filename="ch06_lab01_pod_networking"):
    
    # Create Internet/External Access
    inet = Internet("External\nNetwork")

    # Create Node Network
    with Cluster("Kubernetes Cluster Network"):
        # Create Node 1
        with Cluster("Node 1"):
            switch1 = Switch("Node Network")
            pods1 = [
                Pod("pod-a\nnetshoot"),
                Pod("pod-b\nnginx")
            ]
            
            # Connect pods to node network
            switch1 >> Edge(color="blue", style="bold") >> pods1[0]
            switch1 >> Edge(color="blue", style="bold") >> pods1[1]

        # Create Node 2
        with Cluster("Node 2"):
            switch2 = Switch("Node Network")
            pods2 = [
                Pod("pod-c\nnginx"),
                Pod("pod-d\nnetshoot")
            ]
            
            # Connect pods to node network
            switch2 >> Edge(color="blue", style="bold") >> pods2[0]
            switch2 >> Edge(color="blue", style="bold") >> pods2[1]

        # Create DNS Service
        dns = SVC("kube-dns\nService")

        # Connect nodes to cluster network
        inet >> Edge(color="red", style="dashed") >> switch1
        inet >> Edge(color="red", style="dashed") >> switch2

        # Show DNS resolution paths
        dns >> Edge(color="green") >> pods1[0]
        dns >> Edge(color="green") >> pods1[1]
        dns >> Edge(color="green") >> pods2[0]
        dns >> Edge(color="green") >> pods2[1]

        # Show pod-to-pod communication
        pods1[0] >> Edge(color="orange", style="dotted") >> pods1[1]
        pods1[0] >> Edge(color="orange", style="dotted") >> pods2[0]
        pods2[1] >> Edge(color="orange", style="dotted") >> pods2[0] 