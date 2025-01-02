from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.storage import PV, PVC, SC
from diagrams.onprem.network import Nginx
from diagrams.generic.storage import Storage
from diagrams.k8s.controlplane import API

# Set diagram attributes
with Diagram("Lab 3: Dynamic Volume Provisioning", show=False, direction="TB", filename="ch07_lab03_dynamic_provisioning"):
    
    # Storage Backend
    with Cluster("Storage Infrastructure"):
        storage = Storage("SSD Storage\nBackend")
        
        # Storage Class Definition
        with Cluster("Storage Class Configuration"):
            sc = SC("fast-storage\nProvisioner: k8s.io/minikube-hostpath\nType: ssd")
    
    # Control Plane
    with Cluster("Control Plane"):
        api = API("API Server")
        
    # Dynamic Provisioning Flow
    with Cluster("Dynamic Provisioning"):
        # PVC requesting storage
        pvc = PVC("dynamic-pvc\n1Gi\nReadWriteOnce")
        
        # Dynamically created PV
        pv = PV("auto-pv\n1Gi")
        
        # Show provisioning flow
        sc >> Edge(color="blue", 
                  style="bold", 
                  label="manages") >> storage
        
        pvc >> Edge(color="red", 
                   style="dashed", 
                   label="requests") >> sc
        
        api >> Edge(color="brown", 
                   style="dotted", 
                   label="triggers provisioning") >> sc
        
        sc >> Edge(color="green", 
                  style="bold", 
                  label="creates") >> pv
        
        pv >> Edge(color="orange", 
                  style="bold", 
                  label="binds") >> pvc
    
    # Application using PVC
    with Cluster("Application"):
        pod = Pod("app-pod")
        nginx = Nginx("nginx-container")
        
        # Show application relationships
        pod >> Edge(color="black", 
                   style="dotted") >> nginx
        
        pvc >> Edge(color="purple", 
                   style="dashed", 
                   label="mounts") >> nginx 