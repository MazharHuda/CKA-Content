from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.infra import Node
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler
from diagrams.generic.database import SQL as Etcd
from diagrams.onprem.network import HAProxy
from diagrams.generic.network import Switch
from diagrams.generic.os import Ubuntu

with Diagram("High Availability Kubernetes Control Plane", show=False, direction="TB", filename="ch03_lab02_ha_setup"):
    
    # Load Balancer
    lb = HAProxy("HAProxy\nLoad Balancer\n(6443)")
    
    # Network
    switch = Switch("Internal Network\n192.168.1.0/24")
    
    # Control Plane Nodes
    with Cluster("Control Plane Nodes"):
        control_planes = []
        for i in range(3):
            with Cluster(f"Control Plane {i+1}"):
                cp = Ubuntu(f"Master {i+1}\n2 CPU, 2GB RAM")
                api = APIServer("kube-apiserver")
                etcd = Etcd("etcd")
                controller = ControllerManager("controller-manager")
                scheduler = Scheduler("scheduler")
                
                # Control plane component connections
                cp >> Edge(color="black") >> [api, etcd, controller, scheduler]
                api >> Edge(color="red") >> etcd
                
                control_planes.extend([api])
    
    # Worker Nodes
    with Cluster("Worker Nodes"):
        workers = [
            Node("Worker 1\n2 CPU, 2GB RAM"),
            Node("Worker 2\n2 CPU, 2GB RAM")
        ]
    
    # Network Connections
    lb >> Edge(color="blue", style="bold") >> control_planes
    switch >> Edge(color="green") >> lb
    switch >> Edge(color="green") >> workers
    
    # Control Plane to Worker Communication
    for cp in control_planes:
        cp >> Edge(color="red", style="dashed") >> workers 