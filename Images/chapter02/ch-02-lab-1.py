from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler
from diagrams.k8s.infra import Node
from diagrams.k8s.podconfig import CM
from diagrams.k8s.group import NS
from diagrams.k8s.others import CRD

# Set diagram attributes
with Diagram("Kubernetes Control Plane Components", show=False, direction="TB", filename="ch02_lab01_control_plane"):
    # Create API Server as central component
    with Cluster("Control Plane"):
        api = APIServer("kube-apiserver")
        etcd = CRD("etcd")
        scheduler = Scheduler("kube-scheduler")
        controller = ControllerManager("kube-controller-manager")

        # Show core component relationships
        api >> Edge(color="darkgreen", style="bold") >> etcd
        api >> Edge(color="blue") >> scheduler
        api >> Edge(color="red") >> controller

    # Worker Node Components
    with Cluster("Worker Node"):
        kubelet = Node("kubelet")
        
        # Show node-level monitoring
        kubelet >> Edge(color="darkblue", style="dashed", label="reports status") >> api
        api >> Edge(color="darkblue", style="dashed", label="sends instructions") >> kubelet

    # Component Health Checks
    with Cluster("Health Monitoring"):
        health = CM("Component Status")
        api >> Edge(color="green", style="dotted", label="health checks") >> health
        scheduler >> Edge(color="green", style="dotted") >> health
        controller >> Edge(color="green", style="dotted") >> health
        etcd >> Edge(color="green", style="dotted") >> health