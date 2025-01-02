from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import SVC
from diagrams.k8s.controlplane import API, CM, KProxy, Sched
from diagrams.k8s.group import NS
from diagrams.k8s.infra import ETCD, Node
from diagrams.onprem.container import Docker

graph_attr = {
    "fontsize": "30",
    "bgcolor": "#F0F8FF",  # Light blue background
    "margin": "-1.0,-1.0"
}

cluster_attr = {
    "bgcolor": "#E6F3FF",  # Lighter blue for clusters
    "pencolor": "#4682B4",  # Steel blue for borders
    "penwidth": "2.0"
}

with Diagram("Kubernetes Architecture", show=False, direction="TB", graph_attr=graph_attr, outformat="png"):
    with Cluster("Master", graph_attr=cluster_attr):
        master = Node("Master\nManage, Plan, Schedule, Monitor\nNodes")
        
        with Cluster("Control Plane", graph_attr={"bgcolor": "#E0FFEC"}):  # Light green for Control Plane
            api = API("kube-apiserver")
            etcd = ETCD("ETCD\nCLUSTER")
            scheduler = Sched("kube-scheduler")
            cm = CM("Kube\nController\nManager")
        
        master - Edge(color="#4682B4", style="solid") - api
        api - Edge(color="#4682B4", style="solid") - etcd
        api - Edge(color="#4682B4", style="solid") - scheduler
        api - Edge(color="#4682B4", style="solid") - cm
    
    with Cluster("Worker Nodes", graph_attr=cluster_attr):
        workers = [
            Node("Worker Node 1\nHost Application as Containers"),
            Node("Worker Node 2\nHost Application as Containers")
        ]
        
        for worker in workers:
            kubelet = Pod("kubelet")
            proxy = KProxy("Kube-proxy")
            cri = Docker("Container Runtime Engine")
            
            worker - Edge(color="#4682B4", style="solid") - kubelet
            worker - Edge(color="#4682B4", style="solid") - proxy
            worker - Edge(color="#4682B4", style="solid") - cri

    master >> Edge(color="#4682B4", style="solid", minlen="2") >> workers[0]
    api >> Edge(color="#4682B4", style="solid", minlen="2") >> workers[1]