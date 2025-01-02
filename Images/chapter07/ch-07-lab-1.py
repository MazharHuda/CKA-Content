from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.storage import Vol
from diagrams.programming.language import Bash
from diagrams.onprem.network import Nginx

# Set diagram attributes
with Diagram("Lab 1: Pod Storage with EmptyDir", show=False, direction="TB", filename="ch07_lab01_emptydir"):
    
    # Create main Pod cluster
    with Cluster("shared-volume-pod"):
        # Create containers
        nginx = Nginx("container1\n(nginx)")
        busybox = Bash("container2\n(busybox)")
        
        # Create EmptyDir volume
        with Cluster("volumes"):
            emptydir = Vol("shared-data\n(emptyDir)")
        
        # Show volume mounts
        nginx >> Edge(color="blue", 
                     style="dashed", 
                     label="/data") >> emptydir
        
        busybox >> Edge(color="green", 
                       style="dashed", 
                       label="/data") >> emptydir
        
        # Show data flow for timestamp.txt
        busybox >> Edge(color="red", 
                       style="dotted", 
                       label="writes timestamp.txt") >> emptydir
        
        nginx >> Edge(color="orange", 
                     style="dotted", 
                     label="reads timestamp.txt") >> emptydir 