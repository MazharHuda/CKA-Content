from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.storage import PV, PVC, SC
from diagrams.k8s.compute import Pod, StatefulSet
from diagrams.k8s.infra import Node
from diagrams.generic.storage import Storage

# Set diagram attributes
with Diagram("Comprehensive Storage Management Lab", show=False, direction="TB", filename="ch02_lab07_storage"):
    
    # Storage Infrastructure
    with Cluster("Storage Infrastructure"):
        storage_backend = Storage("Storage Backend")
        
        with Cluster("Storage Classes"):
            sc_fast = SC("fast-storage\nSSD")
            sc_standard = SC("standard-storage\nHDD")
        
        # Show backend relationships
        storage_backend >> Edge(color="darkgreen") >> [sc_fast, sc_standard]
    
    # Persistent Volumes Layer
    with Cluster("Persistent Volumes"):
        pv_fast = PV("fast-pv-1\n10Gi")
        pv_standard = PV("standard-pv-1\n100Gi")
        
        # Storage class to PV relationships
        sc_fast >> Edge(color="blue") >> pv_fast
        sc_standard >> Edge(color="blue") >> pv_standard
    
    # Application Layer
    with Cluster("Application Workloads"):
        # StatefulSet with storage
        with Cluster("Database StatefulSet"):
            sts = StatefulSet("db-statefulset")
            
            # Create individual pods and PVCs
            db_pod0 = Pod("db-0")
            db_pod1 = Pod("db-1")
            db_pod2 = Pod("db-2")
            
            db_pvc0 = PVC("db-pvc-0")
            db_pvc1 = PVC("db-pvc-1")
            db_pvc2 = PVC("db-pvc-2")
            
            # Show StatefulSet relationships
            sts >> Edge(color="red") >> [db_pod0, db_pod1, db_pod2]
            
            # Connect PVCs to their respective pods
            db_pvc0 >> Edge(color="orange") >> db_pod0
            db_pvc1 >> Edge(color="orange") >> db_pod1
            db_pvc2 >> Edge(color="orange") >> db_pod2
            
            # Connect PV to PVCs
            pv_fast >> Edge(color="green") >> [db_pvc0, db_pvc1, db_pvc2]
        
        # Standard Pod with storage
        with Cluster("Web Application"):
            web_pod = Pod("web-pod")
            web_pvc = PVC("web-pvc")
            
            # Show web pod relationships
            web_pvc >> Edge(color="orange") >> web_pod
            pv_standard >> Edge(color="green") >> web_pvc