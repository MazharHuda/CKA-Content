from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import SVC
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.client import Users
from diagrams.k8s.podconfig import Secret, CM

# Set diagram attributes
with Diagram("Grafana Dashboard Setup", show=False, direction="LR", filename="ch09_lab03_grafana"):
    
    # Data Sources
    with Cluster("Data Sources"):
        prometheus = Prometheus("Prometheus")
        
        # Prometheus targets
        with Cluster("Metrics Collection"):
            node_metrics = Pod("Node Metrics")
            pod_metrics = Pod("Pod Metrics")
            custom_metrics = Pod("Custom Metrics")
            
            # Collection flow
            metrics_group = [node_metrics, pod_metrics, custom_metrics]
            for metric in metrics_group:
                metric >> Edge(color="blue", style="dotted") >> prometheus

    # Grafana Setup
    with Cluster("Grafana Stack"):
        # Core components
        grafana = Grafana("Grafana Server")
        grafana_svc = SVC("grafana-service")
        
        # Configuration
        with Cluster("Grafana Config"):
            secret = Secret("grafana-secret")
            datasource = CM("datasource-config")
            dashboard_config = CM("dashboard-config")
            
            # Config relationships
            secret >> Edge(color="red", style="dashed", label="auth") >> grafana
            datasource >> Edge(color="brown", style="dotted", label="configure") >> grafana
            dashboard_config >> Edge(color="brown", style="dotted", label="configure") >> grafana

    # User Access
    with Cluster("User Interface"):
        users = Users("Administrators")
        
        # Dashboard types
        with Cluster("Dashboards"):
            cluster_dash = Pod("Cluster Metrics")
            pod_dash = Pod("Pod Metrics")
            custom_dash = Pod("Custom Metrics")
            
            # Dashboard grouping
            dashboards = [cluster_dash, pod_dash, custom_dash]
            for dash in dashboards:
                grafana >> Edge(color="green") >> dash

    # Main flows
    prometheus >> Edge(color="blue", label="metrics source") >> grafana
    grafana >> Edge(color="black") >> grafana_svc
    users >> Edge(color="orange", label="view/edit") >> grafana_svc 