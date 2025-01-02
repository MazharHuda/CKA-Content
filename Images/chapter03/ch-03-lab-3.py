from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.storage import PV, PVC, SC
from diagrams.k8s.compute import Pod
from diagrams.k8s.infra import Node
from diagrams.generic.storage import Storage
from diagrams.generic.os import Ubuntu

with Diagram("Kubernetes Storage Configuration", show=False, direction="TB", filename="ch03_lab03_storage_config"):
    
    # Storage Backend
    with Cluster("Storage Infrastructure"):
        storage = Storage("Local Storage\n/mnt/data")
        
        # Storage Classes
        with Cluster("Storage Classes"):
            sc_local = SC("local-storage\nNo Provisioner")
            
    # Worker Node
    with Cluster("Worker Node (Ubuntu 20.04)"):
        node = Ubuntu("Worker 1\n2 CPU, 2GB RAM")
        
        # Persistent Volumes
        with Cluster("Persistent Volumes"):
            pv = PV("local-pv\n10Gi\nRetain")
            
        # Node affinity connection
        node >> Edge(color="brown", style="dashed", label="nodeAffinity") >> pv
        
    # Application Layer
    with Cluster("Application Workloads"):
        # PVC and Pod
        pvc = PVC("app-pvc\n5Gi\nRWO")
        app_pod = Pod("app-pod")
        
        # Show volume binding
        pvc >> Edge(color="blue", label="uses") >> pv
        app_pod >> Edge(color="green", label="mounts") >> pvc
        
    # Storage class relationships
    sc_local >> Edge(color="red", style="dotted", label="manages") >> pv
    storage >> Edge(color="orange", label="provides") >> pv 