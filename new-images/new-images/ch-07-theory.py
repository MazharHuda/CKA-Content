from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.storage import PV, PVC, SC
from diagrams.k8s.controlplane import ControllerManager
from diagrams.onprem.compute import Server
from diagrams.programming.framework import Django

with Diagram("Kubernetes Storage Architecture", show=False, direction="TB"):
    # Applications Layer
    with Cluster("Applications"):
        apps = [Django("App 1"), Django("App 2"), Django("App 3")]
    
    # Pod Layer
    with Cluster("Pod Layer"):
        pods = [Pod("Pod 1"), Pod("Pod 2"), Pod("Pod 3")]
    
    # Storage Abstraction (PVC)
    with Cluster("Storage Abstraction\nPVC"):
        pvcs = [PVC("PVC 1\nRWO"), PVC("PVC 2\nRWX"), PVC("PVC 3\nROX")]
    
    # Storage Classes
    with Cluster("Storage Classes"):
        sc_standard = SC("Standard\nStorage")
        sc_fast = SC("Fast\nStorage")
    
    # Storage Provisioner
    with Cluster("Storage Provisioners"):
        csi = ControllerManager("CSI\nController")
    
    # Storage Backend
    with Cluster("Storage Backend"):
        # Persistent Volumes
        with Cluster("Persistent Volumes"):
            pvs = [
                PV("PV 1\nLocal"),
                PV("PV 2\nNFS"),
                PV("PV 3\nCloud")
            ]
        
        # Storage Providers
        with Cluster("Storage Providers"):
            providers = [
                Server("Local\nStorage"),
                Server("NFS\nServer"),
                Server("Cloud\nStorage")
            ]
        
        # Backup & Recovery
        with Cluster("Backup & Recovery"):
            backup = [
                Server("Volume\nSnapshots"),
                Server("Backup\nStorage")
            ]
    
    # Connections
    for i in range(3):
        apps[i] >> pods[i] >> pvcs[i]
        pvs[i] >> providers[i]
        pvs[i] >> backup[0]
    
    pvcs[0] >> sc_fast
    pvcs[1:] >> sc_standard
    
    sc_standard >> csi
    sc_fast >> csi
    
    for pv in pvs:
        csi >> pv
    
    backup[0] >> backup[1]