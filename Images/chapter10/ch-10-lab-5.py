from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler
from diagrams.k8s.compute import Pod
from diagrams.k8s.infra import Node
from diagrams.k8s.others import CRD
from diagrams.onprem.container import Docker
from diagrams.generic.os import Ubuntu
from diagrams.onprem.monitoring import Grafana

# Diagram 1: Node Troubleshooting Flow
with Diagram("Node Troubleshooting Process", show=False, direction="TB", filename="ch10_lab05_node_troubleshooting"):
    
    with Cluster("Node Investigation"):
        # Node components
        node = Node("Problem Node")
        kubelet = Docker("kubelet")
        system = Ubuntu("System Resources")
        logs = Grafana("System Logs")
        
        # Investigation flow
        node >> Edge(color="red", label="1. Check Status") >> kubelet
        node >> Edge(color="orange", label="2. Monitor") >> system
        kubelet >> Edge(color="blue", label="3. Analyze") >> logs

    with Cluster("Resource Analysis"):
        resources = [
            Pod("Resource Usage"),
            CRD("Disk Space"),
            CRD("Memory Stats")
        ]
        
        # Resource checks
        system >> Edge(color="green", style="dashed") >> resources

# Diagram 2: Control Plane Recovery Flow
with Diagram("Control Plane Recovery Process", show=False, direction="TB", filename="ch10_lab05_control_plane"):
    
    with Cluster("Control Plane Components"):
        api = APIServer("API Server")
        controller = ControllerManager("Controller Manager")
        scheduler = Scheduler("Scheduler")
        
        # Component relationships
        api >> Edge(color="red", style="bold") >> [controller, scheduler]
    
    with Cluster("Diagnostic Steps"):
        with Cluster("System Checks"):
            pod_status = Pod("Pod Status")
            manifests = CRD("Static Pod Manifests")
            logs_cp = Grafana("Component Logs")
            
            # Diagnostic flow
            api >> Edge(color="blue", label="1. Check") >> pod_status
            api >> Edge(color="orange", label="2. Verify") >> manifests
            [controller, scheduler] >> Edge(color="green", label="3. Analyze") >> logs_cp

# Diagram 3: Recovery Strategy
with Diagram("Recovery Strategy Overview", show=False, direction="LR", filename="ch10_lab05_recovery"):
    
    with Cluster("Problem Detection"):
        monitor = Grafana("Monitoring")
        alerts = CRD("Alerts")
        metrics = Pod("Metrics")
        
        # Detection flow
        monitor >> Edge(color="red", label="detect") >> alerts
        monitor >> Edge(color="orange", label="collect") >> metrics
    
    with Cluster("Recovery Actions"):
        with Cluster("Service Management"):
            services = Docker("System Services")
            resources = Ubuntu("Resource Management")
            verification = APIServer("Verification")
            
            # Recovery steps
            alerts >> Edge(color="blue", label="1. Restart") >> services
            metrics >> Edge(color="green", label="2. Optimize") >> resources
            [services, resources] >> Edge(color="orange", label="3. Verify") >> verification 