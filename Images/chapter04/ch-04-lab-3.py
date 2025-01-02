from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.controlplane import Scheduler
from diagrams.k8s.infra import Node
from diagrams.k8s.podconfig import CM

with Diagram("Resource Management and QoS", show=False, direction="TB", filename="ch04_lab03_resource_qos"):
    
    scheduler = Scheduler("kube-scheduler")
    
    # Resource Requests and Limits
    with Cluster("Resource Management"):
        # Resource configurations
        config = CM("Resource\nConfiguration")
        
        # Pods with different resource settings
        basic_pod = Pod("Basic Pod\nNo Requests/Limits")
        request_pod = Pod("Request Pod\nRequests Only\nCPU: 250m\nMem: 64Mi")
        limit_pod = Pod("Limited Pod\nRequests & Limits\nCPU: 500m/1\nMem: 128Mi/256Mi")
        
        # Show resource assignments
        config >> Edge(color="red", style="dotted") >> basic_pod
        config >> Edge(color="orange", style="bold", label="requests") >> request_pod
        config >> Edge(color="green", style="bold", label="limits") >> limit_pod

    # QoS Classes
    with Cluster("Quality of Service (QoS)"):
        # Different QoS class pods
        guaranteed = Pod("Guaranteed QoS\nRequests = Limits\nCPU: 500m\nMem: 128Mi")
        burstable = Pod("Burstable QoS\nRequests < Limits\nCPU: 250m/500m\nMem: 64Mi/128Mi")
        besteffort = Pod("BestEffort QoS\nNo Requests/Limits")
        
        # Node with resources
        worker = Node("Worker Node\nCPU: 2 cores\nMem: 4Gi")
        
        # Show QoS hierarchy and scheduling
        scheduler >> Edge(color="green", style="bold", label="high priority") >> guaranteed
        scheduler >> Edge(color="orange", style="bold", label="medium priority") >> burstable
        scheduler >> Edge(color="red", style="bold", label="low priority") >> besteffort
        
        # Show node assignment
        guaranteed >> Edge(color="blue") >> worker
        burstable >> Edge(color="blue") >> worker
        besteffort >> Edge(color="blue", style="dotted") >> worker 