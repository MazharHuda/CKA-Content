from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.infra import Node
from diagrams.k8s.controlplane import APIServer
from diagrams.onprem.monitoring import Prometheus, Grafana

# Set diagram attributes
with Diagram("Metrics Server Data Flow", show=False, direction="LR", filename="ch09_lab01_metrics_flow"):
    
    # Data Sources
    with Cluster("Metric Sources"):
        sources = [
            Node("Node Metrics\nCPU/Memory"),
            Pod("Pod Metrics\nResource Usage")
        ]
    
    # Metrics Collection
    with Cluster("Metrics Pipeline"):
        metrics_server = Pod("Metrics Server")
        api = APIServer("API Server")
        
        # Optional monitoring tools
        with Cluster("Monitoring Tools"):
            prometheus = Prometheus("Prometheus")
            grafana = Grafana("Grafana")
            
            # Monitoring flow
            api >> Edge(color="brown", style="dotted") >> prometheus
            prometheus >> Edge(color="brown", style="dotted") >> grafana
    
    # Data Flow
    sources >> Edge(color="blue", label="collect\n15s interval") >> metrics_server
    metrics_server >> Edge(color="green", label="aggregate") >> api
    
    # Query Flow
    with Cluster("Client Queries"):
        queries = [
            Pod("kubectl top nodes"),
            Pod("kubectl top pods"),
            Pod("HPA queries")
        ]
        
        # Query paths
        api >> Edge(color="red", style="dashed", label="serve metrics") >> queries 