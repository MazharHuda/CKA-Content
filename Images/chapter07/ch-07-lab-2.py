from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.storage import PV, PVC
from diagrams.onprem.network import Nginx
from diagrams.generic.storage import Storage

# Set diagram attributes
with Diagram("Lab 2: PersistentVolumes and Claims", show=False, direction="TB", filename="ch07_lab02_pv_pvc"):
    
    # Host Storage
    with Cluster("Host System"):
        storage = Storage("Physical Storage\n/mnt/data")
    
    # PV and PVC Configuration
    with Cluster("Storage Configuration"):
        # Create PV
        pv = PV("task-pv\n2Gi\nReadWriteOnce")
        
        # Create PVC
        pvc = PVC("task-pvc\n1Gi\nReadWriteOnce")
        
        # Show PV-PVC binding
        storage >> Edge(color="brown", 
                       style="bold", 
                       label="provides") >> pv
        
        pv >> Edge(color="blue", 
                  style="bold", 
                  label="binds") >> pvc
    
    # Pod using PVC
    with Cluster("Application"):
        # Create Pod with nginx
        pod = Pod("task-pod")
        nginx = Nginx("nginx-container")
        
        # Show Pod composition and volume mounting
        pod >> Edge(color="black", 
                   style="dotted") >> nginx
        
        pvc >> Edge(color="green", 
                   style="dashed", 
                   label="mounts as /usr/share/nginx/html") >> nginx 