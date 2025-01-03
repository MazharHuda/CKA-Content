from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler
from diagrams.k8s.compute import Pod
from diagrams.k8s.infra import Node, ETCD
from diagrams.onprem.network import HAProxy
from diagrams.generic.network import Switch
from diagrams.onprem.client import Client
from diagrams.k8s.others import CRD
from diagrams.k8s.podconfig import Secret
from diagrams.k8s.rbac import RB, Role

with Diagram("Kubernetes High Availability Cluster Setup", show=False, direction="TB", filename="ch03_ha_cluster_setup"):
    client = Client("External\nClients")
    
    with Cluster("Load Balancer"):
        lb = HAProxy("HAProxy\nLoad Balancer\n(TCP/6443)")
    
    with Cluster("Cluster Network"):
        net = Switch("Internal Network\n192.168.1.0/24")
    
    with Cluster("Control Plane HA Setup"):
        control_planes = []
        for i in range(3):
            with Cluster(f"Control Plane Node {i+1}"):
                cert = Secret("certificates")
                rbac = Role("RBAC")
                
                api = APIServer(f"kube-apiserver\n192.168.1.1{i}")
                etcd = ETCD(f"etcd\n192.168.1.1{i}:2379")
                ctrl = ControllerManager("controller-manager")
                sched = Scheduler("scheduler")
                
                cert >> Edge(color="purple") >> api
                rbac >> Edge(color="orange") >> api
                api >> Edge(color="red", style="bold") >> etcd
                api >> Edge(color="blue") >> ctrl
                api >> Edge(color="green") >> sched
                
                if i > 0:
                    etcd >> Edge(color="brown", style="dashed") >> control_planes[i-1]
                
                control_planes.append(api)

    with Cluster("Worker Nodes"):
        workers = []
        for i in range(3):
            with Cluster(f"Worker Node {i+1}"):
                worker = Node(f"worker-{i+1}")
                worker_cert = Secret("node-cert")
                pods = [Pod("pod-1"), Pod("pod-2")]
                
                worker_cert >> Edge(color="purple") >> worker
                worker - Edge(color="black", style="dotted") - pods
                workers.append(worker)

    client >> Edge(color="brown", style="bold") >> lb
    lb >> Edge(color="brown", style="bold") >> net
    
    for cp in control_planes:
        net >> Edge(color="blue", style="dashed") >> cp
    
    for worker in workers:
        net >> Edge(color="green", style="dashed") >> worker
        worker >> Edge(color="red", style="dotted", label="reports status") >> net
