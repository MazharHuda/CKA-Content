from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import SVC
from diagrams.k8s.storage import Vol
from diagrams.programming.framework import Flask
from diagrams.programming.language import Bash
from diagrams.onprem.monitoring import Grafana

with Diagram("Advanced Pod Configuration", show=False, direction="TB", filename="ch04_lab01_pod_config"):
    
    # Multi-container Pod
    with Cluster("Multi-Container Pod (web-app)"):
        # Main application container
        app = Flask("nginx\ncontainer")
        
        # Sidecar container
        sidecar = Bash("content-sync\ncontainer")
        
        # Shared volume
        volume = Vol("shared-data\nemptyDir")
        
        # Container relationships
        app >> Edge(color="blue", style="solid", label="reads") >> volume
        sidecar >> Edge(color="red", style="dashed", label="writes") >> volume

    # Health Checks Pod
    with Cluster("Health Checks Pod (health-check-demo)"):
        # Application with probes
        health_app = Grafana("nginx\ncontainer")
        
        # Health check endpoints
        with Cluster("Health Probes"):
            liveness = SVC("Liveness\n/\nPort 80")
            readiness = SVC("Readiness\n/\nPort 80")
            
            # Probe configurations
            health_app >> Edge(color="green", style="bold", label="every 3s") >> liveness
            health_app >> Edge(color="orange", style="bold", label="every 5s") >> readiness
            
            # Initial delays
            liveness >> Edge(color="brown", style="dotted", label="3s delay") >> health_app
            readiness >> Edge(color="purple", style="dotted", label="5s delay") >> health_app 