from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.compute import Pod, Job
from diagrams.k8s.storage import PV
from diagrams.k8s.infra import Node
from diagrams.generic.storage import Storage
from diagrams.k8s.others import CRD
from diagrams.onprem.container import Docker

# Diagram 1: Backup Process Flow
with Diagram("Backup Process Flow", show=False, direction="TB", filename="ch10_lab03_backup"):
    
    with Cluster("Backup Process"):
        # Control Plane Components
        with Cluster("Control Plane"):
            api = APIServer("API Server")
            etcd = CRD("ETCD")
            
            # Show etcd connection
            api >> Edge(color="red", style="bold") >> etcd
        
        # Backup Components
        with Cluster("Backup Operation"):
            backup_job = Job("etcd-backup Job")
            snapshot = Storage("Snapshot File")
            volume = PV("Backup Volume")
            
            # Show backup flow
            backup_job >> Edge(color="blue", label="1. Create Snapshot") >> etcd
            backup_job >> Edge(color="green", label="2. Save") >> snapshot
            snapshot >> Edge(color="green", label="3. Store") >> volume

# Diagram 2: Restore Process Flow
with Diagram("Restore Process Flow", show=False, direction="TB", filename="ch10_lab03_restore"):
    
    with Cluster("Pre-restore Phase"):
        # Existing components
        api_server = APIServer("API Server")
        old_etcd = CRD("Current ETCD")
        
        # Show current state
        api_server >> Edge(color="red", style="bold") >> old_etcd
    
    with Cluster("Restore Operation"):
        # Restore components
        backup = Storage("Backup File")
        restore_dir = Storage("Restore Directory")
        new_etcd = CRD("New ETCD")
        
        # Show restore steps
        backup >> Edge(color="blue", label="1. Read Backup") >> restore_dir
        restore_dir >> Edge(color="blue", label="2. Initialize") >> new_etcd
        
        # Service management
        services = [
            Docker("kube-apiserver"),
            Docker("kubelet")
        ]
        
        # Show service operations
        for svc in services:
            svc >> Edge(color="orange", label="3. Restart") >> new_etcd
    
    with Cluster("Post-restore Verification"):
        verify = APIServer("API Verification")
        resources = [
            Pod("Pod Status"),
            CRD("Custom Resources")
        ]
        
        # Show verification flow
        new_etcd >> Edge(color="green", label="4. Verify") >> verify
        verify >> Edge(color="green", label="5. Check") >> resources

# Diagram 3: Backup Strategy Overview
with Diagram("Backup Strategy Overview", show=False, direction="LR", filename="ch10_lab03_strategy"):
    
    with Cluster("Backup Components"):
        # Backup targets
        etcd_data = CRD("ETCD Data")
        k8s_objects = Pod("K8s Objects")
        certs = Storage("Certificates")
        
        # Backup destinations
        with Cluster("Backup Storage"):
            local = Storage("Local Storage")
            remote = Storage("Remote Storage")
            
            # Show backup paths
            etcd_data >> Edge(color="blue", style="bold") >> local
            k8s_objects >> Edge(color="green", style="dashed") >> remote
            certs >> Edge(color="red", style="dotted") >> [local, remote] 