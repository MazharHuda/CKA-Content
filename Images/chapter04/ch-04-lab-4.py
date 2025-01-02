from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.storage import Vol
from diagrams.programming.language import Bash
from diagrams.programming.framework import Flask
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.network import Nginx
from diagrams.k8s.network import Service

with Diagram("Advanced Pod Patterns", show=False, direction="TB", filename="ch04_lab04_pod_patterns"):
    
    # Init Container Pattern
    with Cluster("Init Container Pattern"):
        init_pod = Pod("Pod: init-demo")
        init_container = Bash("Init Container\nService Check")
        main_app = Nginx("Main App\nNginx")
        
        # Show initialization flow
        init_container >> Edge(color="red", style="bold", label="1. Check Service") >> main_app
        init_pod >> Edge(color="blue", style="dotted") >> [init_container, main_app]

    # Sidecar Pattern
    with Cluster("Sidecar Pattern"):
        # Main container and sidecar
        main_container = Flask("Main App\nNginx")
        sidecar = Grafana("Sidecar\nLog Shipper")
        shared_vol = Vol("Shared Volume\nemptyDir")
        
        # Show data flow
        main_container >> Edge(color="blue", style="bold", label="write logs") >> shared_vol
        shared_vol >> Edge(color="green", style="bold", label="read logs") >> sidecar
        
        # Pod grouping
        with Cluster("Pod: sidecar-demo"):
            sidecar_pod = Pod("pod")
            sidecar_pod >> Edge(color="black", style="dotted") >> [main_container, sidecar]

    # Ambassador Pattern
    with Cluster("Ambassador Pattern"):
        app = Flask("Main App")
        ambassador = Nginx("Ambassador\nProxy")
        external_svc = Service("External\nService")
        
        # Show proxy flow
        with Cluster("Pod: ambassador-demo"):
            ambassador_pod = Pod("pod")
            ambassador_pod >> Edge(color="black", style="dotted") >> [app, ambassador]
            app >> Edge(color="orange", style="bold", label="local request") >> ambassador
            ambassador >> Edge(color="green", style="bold", label="external request") >> external_svc