from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import Service, Ingress
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler
from diagrams.k8s.infra import Node
from diagrams.k8s.storage import PV
from diagrams.onprem.container import Docker

# Set diagram attributes
with Diagram("Kubernetes First Environment Setup", show=False, direction="TB", filename="chapter01_lab01"):
    # Control Plane Components
    with Cluster("Control Plane Node"):
        api = APIServer("kube-apiserver")
        etcd = PV("etcd")
        scheduler = Scheduler("kube-scheduler")
        controller = ControllerManager("kube-controller-manager")
        
        # Control plane component relationships
        api >> etcd
        api >> scheduler
        api >> controller

    # Worker Node Components
    with Cluster("Worker Node"):
        with Cluster("Node Components"):
            kubelet = Node("kubelet")
            docker = Docker("container runtime")
            
        with Cluster("Basic Workload"):
            pod = Pod("nginx-pod")
            svc = Service("nginx-service")

        # Worker node relationships
        kubelet >> docker
        docker >> pod
        pod << svc

    # Cross-cluster relationships
    api >> kubelet