from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.infra import Master, Node
from diagrams.k8s.controlplane import API, Scheduler, ControllerManager
from diagrams.k8s.compute import Pod, Deploy, ReplicaSet
from diagrams.k8s.network import SVC, NetworkPolicy, Ingress
from diagrams.k8s.storage import PV, PVC, StorageClass
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.network import Internet
from diagrams.onprem.database import MongoDB, Cassandra  # Using Cassandra for logs
from diagrams.onprem.compute import Server
from diagrams.onprem.client import Client
from diagrams.k8s.others import CRD

# Enhanced graph attributes
graph_attr = {
    "splines": "spline",
    "pad": "0.75",
    "nodesep": "1.0",
    "ranksep": "1.0"
}

with Diagram(
    "Kubernetes Troubleshooting Architecture",
    show=False,
    direction="TB",
    filename="ch12_troubleshooting",
    graph_attr=graph_attr
):
    # Monitoring & Logging Stack
    with Cluster("Observability & Diagnostics"):
        monitor = Prometheus("Metrics\nCollection")
        logs = Cassandra("Log\nAggregation")  # Using Cassandra instead of Elasticsearch
        visualizer = Grafana("Monitoring\nDashboards")
        log_collector = Pod("Log\nCollector")
        
        # Tool relationships
        monitor >> Edge(color="orange", label="metrics") >> visualizer
        logs >> Edge(color="orange", label="logs") >> visualizer
        log_collector >> Edge(color="orange", label="collect") >> logs
    
    # Control Plane Troubleshooting
    with Cluster("Control Plane Diagnostics"):
        api = API("API Server\nHealth & Logs")
        etcd = MongoDB("etcd\nHealth & Backup")
        controller = ControllerManager("Controller Manager\nStatus")
        sched = Scheduler("Scheduler\nDiagnostics")
        
        # Control plane monitoring
        monitor >> Edge(color="red", style="dashed", label="monitor") >> [api, etcd, controller, sched]
    
    # Node Troubleshooting
    with Cluster("Node Diagnostics"):
        nodes = [
            Node("Node 1\nKubelet & Runtime"),
            Node("Node 2\nResource Usage"),
            Node("Node 3\nConnectivity")
        ]
        
        # Node monitoring
        for node in nodes:
            monitor >> Edge(color="blue", style="dashed", label="metrics") >> node
            log_collector >> Edge(color="blue", style="dotted", label="logs") >> node
    
    # Pod Troubleshooting
    with Cluster("Pod & Workload Diagnostics"):
        with Cluster("Common Issues"):
            pods = [
                Pod("Image Pull\nIssues"),
                Pod("Resource\nConstraints"),
                Pod("Liveness/Readiness\nProbes")
            ]
            
            # Pod monitoring
            for pod in pods:
                monitor >> Edge(color="green", style="dashed", label="metrics") >> pod
                log_collector >> Edge(color="green", style="dotted", label="logs") >> pod
    
    # Network Troubleshooting
    with Cluster("Network Diagnostics"):
        net = Internet("Network\nConnectivity")
        service = SVC("Service\nEndpoints")
        netpol = NetworkPolicy("Network\nPolicies")
        ingress = Ingress("Ingress\nRouting")
        
        # Network relationships
        net >> Edge(color="brown", label="traffic") >> service
        netpol >> Edge(color="brown", style="dashed", label="control") >> service
        ingress >> Edge(color="brown", label="route") >> service
    
    # Storage Troubleshooting
    with Cluster("Storage Diagnostics"):
        sc = StorageClass("Storage\nClass")
        pv = PV("PV\nStatus")
        pvc = PVC("PVC\nBinding")
        
        # Storage relationships
        pvc >> Edge(color="purple", label="bind") >> pv
        sc >> Edge(color="purple", style="dashed", label="provision") >> pv
    
    # Application Troubleshooting
    with Cluster("Application Diagnostics"):
        apps = [
            Server("App 1\nLogs & Events"),
            Server("App 2\nMetrics"),
            Server("App 3\nTracing")
        ]
        
        # Application monitoring
        for app in apps:
            app >> Edge(color="black", style="dotted", label="logs") >> log_collector
            app >> Edge(color="black", style="dashed", label="metrics") >> monitor
    
    # Debug Tools & Utilities
    with Cluster("Debugging Toolkit"):
        debug_tools = [
            Client("Network\nDebug Tools"),
            Client("DNS\nUtils"),
            Client("Storage\nUtils")
        ]
        debug_pod = Pod("Debug\nContainer")
        
        # Debug connections
        for tool in debug_tools:
            tool >> Edge(color="red", style="bold", label="use") >> debug_pod
        debug_pod >> Edge(color="red", style="bold", label="debug") >> [net, service, pv]