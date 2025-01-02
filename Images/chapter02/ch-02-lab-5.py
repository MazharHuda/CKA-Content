from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.storage import PV, PVC, SC
from diagrams.k8s.compute import Pod
from diagrams.k8s.infra import Node
from diagrams.generic.storage import Storage  # Using generic storage instead of NFS

# Set diagram attributes
with Diagram("Kubernetes Storage Configuration Lab", show=False, direction="TB", filename="ch02_lab05_storage"):
    
    # Storage Class Definition
    with Cluster("Storage Classes"):
        sc = SC("standard-sc")
        
    # Storage Backend
    with Cluster("Storage Backend"):
        storage = Storage("Storage Server")  # Using generic storage icon
        
    # Persistent Volumes
    with Cluster("Persistent Volumes"):
        pv1 = PV("nfs-pv\n1Gi")
        pv2 = PV("hostpath-pv\n1Gi")
        
    # Persistent Volume Claims
    with Cluster("Persistent Volume Claims"):
        pvc1 = PVC("task-pvc")
        pvc2 = PVC("data-pvc")
        
    # Application Pods
    with Cluster("Application Pods"):
        pod1 = Pod("nginx-pod")
        pod2 = Pod("mysql-pod")
        
    # Show relationships
    sc >> Edge(color="blue") >> pv1
    storage >> Edge(color="red") >> pv1
    
    # PV to PVC binding
    pv1 >> Edge(color="green") >> pvc1
    pv2 >> Edge(color="green") >> pvc2
    
    # Pod volume mounts
    pvc1 >> Edge(color="orange") >> pod1
    pvc2 >> Edge(color="orange") >> pod2