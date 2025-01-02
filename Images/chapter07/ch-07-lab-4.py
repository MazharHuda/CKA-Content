from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.storage import PV, PVC, SC
from diagrams.k8s.controlplane import API
from diagrams.k8s.infra import Node
from diagrams.generic.storage import Storage
from diagrams.onprem.monitoring import Grafana

# Set diagram attributes
with Diagram("Lab 4: Storage Troubleshooting Scenarios", show=False, direction="TB", filename="ch07_lab04_troubleshooting"):
    
    # Control Plane
    with Cluster("Control Plane"):
        api = API("API Server")
        
        # Events and Logs
        with Cluster("Diagnostics"):
            events = Grafana("Events & Logs")
            api >> Edge(color="red", 
                       style="bold", 
                       label="collect") >> events
    
    # Storage Infrastructure
    with Cluster("Storage Layer"):
        storage = Storage("Physical Storage")
        node = Node("Worker Node")
        
        # Storage components
        pv = PV("PV Status")
        pvc = PVC("PVC Status")
        sc = SC("StorageClass")
        
        # Infrastructure relationships
        storage >> Edge(color="brown", 
                       style="dashed", 
                       label="provides") >> node
        node >> Edge(color="brown", 
                    style="dashed", 
                    label="hosts") >> pv
    
    # Troubleshooting Flows
    with Cluster("Troubleshooting Paths"):
        # PVC Binding Issues
        with Cluster("Scenario 1: PVC Binding"):
            pvc >> Edge(color="red", 
                       style="bold", 
                       label="1. Check Status") >> events
            pvc >> Edge(color="orange", 
                       style="dotted", 
                       label="2. Verify Binding") >> pv
            sc >> Edge(color="blue", 
                      style="dashed", 
                      label="3. Check Provisioner") >> pv
        
        # Volume Mount Problems
        with Cluster("Scenario 2: Volume Mounts"):
            pod = Pod("Problem Pod")
            
            pod >> Edge(color="purple", 
                       style="bold", 
                       label="4. Check Events") >> events
            pod >> Edge(color="green", 
                       style="dashed", 
                       label="5. Verify Mounts") >> pvc
            node >> Edge(color="black", 
                        style="dotted", 
                        label="6. Check Node Storage") >> pod 