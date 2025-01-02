from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.infra import Node
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler
from diagrams.generic.database import SQL as Etcd
from diagrams.k8s.network import Service
from diagrams.onprem.network import Internet
from diagrams.generic.network import Switch
from diagrams.generic.os import Ubuntu

with Diagram("Multi-Node Kubernetes Cluster Setup", show=True, direction="TB", filename="ch03_lab01_cluster_setup"):
    
    # Network and Internet
    net = Internet("Internet")
    switch = Switch("Network\n10.0.0.0/24")
    
    # Control Plane Components
    with Cluster("Control Plane Node (Ubuntu 20.04)"):
        control_plane = Ubuntu("Control Plane\n2 CPU, 2GB RAM")
        api = APIServer("kube-apiserver")
        etcd = Etcd("etcd")
        controller = ControllerManager("controller-manager")
        scheduler = Scheduler("scheduler")
        
        # Control plane connections
        control_plane >> Edge(color="black") >> [api, etcd, controller, scheduler]
        api >> Edge(color="red") >> etcd
    
    # Worker Nodes
    with Cluster("Worker Nodes"):
        workers = [
            Node("Worker 1\n2 CPU, 2GB RAM"),
            Node("Worker 2\n2 CPU, 2GB RAM")
        ]
        
    # Network Connections
    net >> Edge(color="blue") >> switch
    switch >> Edge(color="green") >> control_plane
    switch >> Edge(color="green") >> workers
    
    # Control Plane to Worker Communication
    api >> Edge(color="red", style="dashed") >> workers