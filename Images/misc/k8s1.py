from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import Ing, SVC
from diagrams.k8s.storage import PV, PVC
from diagrams.k8s.infra import Master, Node

with Diagram("Kubernetes Cluster Architecture", show=False):
    ing = Ing("Ingress")

    with Cluster("Kubernetes Cluster"):
        master = Master("Master Node")

        with Cluster("Worker Nodes"):
            workers = [Node("Worker 1"),
                       Node("Worker 2"),
                       Node("Worker 3")]

        with Cluster("Deployments"):
            deployments = [Deploy("Deployment 1"),
                           Deploy("Deployment 2")]

        with Cluster("Services"):
            svc = SVC("ClusterIP")

        with Cluster("Pods"):
            pods = [Pod("Pod 1"),
                    Pod("Pod 2"),
                    Pod("Pod 3")]

        storage = PV("Persistent Volume")
        claim = PVC("PV Claim")

    ing >> master
    master >> workers[0]
    master >> deployments[0]
    deployments[0] >> svc >> pods[0]
    
    for worker in workers:
        worker >> Edge(color="brown", style="dotted") >> pods

    storage - claim
    claim >> pods[0]