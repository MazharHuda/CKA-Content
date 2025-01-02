from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC
from diagrams.onprem.monitoring import Prometheus
from diagrams.programming.framework import Flask
from diagrams.k8s.controlplane import APIServer

# Diagram 1: Health Check Types
with Diagram("Kubernetes Health Check Types", show=False, direction="TB", filename="ch05_lab04_health_checks"):
    
    with Cluster("Pod Health Checks"):
        # API Server monitoring
        api = APIServer("API Server")
        
        with Cluster("Application Pod"):
            app = Flask("web-app")
            
            # Health check endpoints
            with Cluster("Health Probes"):
                liveness = Pod("Liveness Probe\n/health\nPort 8080")
                readiness = Pod("Readiness Probe\n/ready\nPort 8080")
                startup = Pod("Startup Probe\n/startup\nPort 8080")
            
            # Show probe relationships
            app >> Edge(color="green", style="bold", label="HTTP GET") >> liveness
            app >> Edge(color="blue", style="bold", label="TCP Socket") >> readiness
            app >> Edge(color="orange", style="bold", label="Exec Command") >> startup
            
            # API Server monitoring
            api >> Edge(color="red", label="monitor") >> [liveness, readiness, startup]

# Diagram 2: Probe Configuration Flow
with Diagram("Probe Configuration and Response", show=False, direction="LR", filename="ch05_lab04_probe_flow"):
    
    with Cluster("Health Check Configuration"):
        # Monitoring setup
        metrics = Prometheus("Metrics Collection")
        
        with Cluster("Pod Lifecycle States"):
            # Pod states based on probes
            healthy = Pod("Healthy Pod\nAll Probes OK")
            starting = Pod("Starting Pod\nInit Phase")
            failing = Pod("Failing Pod\nProbe Failed")
            
            # Service interaction
            svc = SVC("Application Service")
            
            # Show state transitions
            metrics >> Edge(color="green", label="success") >> healthy
            metrics >> Edge(color="yellow", label="initializing") >> starting
            metrics >> Edge(color="red", label="failure") >> failing
            
            # Service relationship
            svc >> Edge(color="blue", style="dashed", label="routes traffic") >> healthy
            svc >> Edge(color="red", style="dotted", label="no traffic") >> [starting, failing]

# Diagram 3: Probe Timing and Retry
with Diagram("Probe Timing and Retry Mechanism", show=False, direction="TB", filename="ch05_lab04_probe_timing"):
    
    with Cluster("Probe Lifecycle"):
        # Deployment controller
        deploy = Deploy("Application Deployment")
        
        with Cluster("Pod Probing Sequence"):
            # Probe timing stages
            with Cluster("Startup Phase"):
                init = Pod("Init Container")
                startup_check = Pod("Startup Probe\nTimeout: 30s")
            
            with Cluster("Runtime Phase"):
                runtime = Pod("Main Container")
                liveness_check = Pod("Liveness Probe\nPeriod: 10s")
                readiness_check = Pod("Readiness Probe\nPeriod: 5s")
            
            # Show timing sequence
            deploy >> Edge(color="black") >> init
            init >> Edge(color="orange", label="initialDelay: 5s") >> startup_check
            startup_check >> Edge(color="green", label="success") >> runtime
            
            # Runtime probes
            runtime >> Edge(color="blue", style="dashed", label="periodic") >> liveness_check
            runtime >> Edge(color="red", style="dashed", label="periodic") >> readiness_check
            
            # Failure handling
            liveness_check >> Edge(color="red", style="bold", label="restart") >> runtime
            readiness_check >> Edge(color="orange", style="bold", label="remove from service") >> runtime 