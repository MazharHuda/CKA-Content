from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.infra import Node, Master
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.logging import Loki
from diagrams.k8s.podconfig import ConfigMap
from diagrams.onprem.queue import Kafka
from diagrams.generic.storage import Storage
from diagrams.generic.database import SQL
from diagrams.onprem.network import Internet

with Diagram("Kubernetes Monitoring Architecture", show=False, direction="TB"):
    # Application Layer
    with Cluster("Applications"):
        apps = [Pod("App 1"), Pod("App 2"), Pod("App 3")]
    
    # Metrics Collection
    with Cluster("Metrics Collection"):
        with Cluster("Node Level"):
            node = Node("Worker Node")
            node_exporter = Pod("Node Exporter")
            metrics_server = Master("Metrics Server")
            node >> node_exporter >> metrics_server
        
        with Cluster("Pod Level"):
            pod_metrics = Pod("Pod Metrics")
            custom_metrics = Pod("Custom Metrics")
    
    # Monitoring Stack
    with Cluster("Metrics & Logging"):
        prometheus = Prometheus("Prometheus")
        loki = Loki("Log Aggregator")
        tsdb = SQL("Time Series DB")
        elastic = SQL("Elasticsearch")
        
        prometheus >> tsdb
        
        with Cluster("Alert Management"):
            alert_mgr = ConfigMap("Alert Manager")
            rules = Storage("Alert Rules")
            prometheus >> alert_mgr
            rules >> alert_mgr
    
    # Log Storage
    with Cluster("Log Storage"):
        kibana = Internet("Kibana")
        kafka = Kafka("Log Buffer")
        
        loki >> elastic >> kibana
        kafka >> elastic
    
    # Visualization
    with Cluster("Dashboards"):
        grafana = Grafana("Grafana")
        dashboards = Storage("Dashboards")
        
        prometheus >> grafana
        elastic >> grafana
        grafana >> dashboards
    
    # Application Flows
    for app in apps:
        app >> pod_metrics
        app >> custom_metrics
        app >> loki
        app >> kafka
    
    pod_metrics >> prometheus
    custom_metrics >> prometheus
    node_exporter >> prometheus
    
    # Alerts
    notifications = Internet("Notifications")
    alert_mgr >> notifications
    
    # Scaling
    with Cluster("Scaling"):
        hpa = ConfigMap("HPA")
        vpa = ConfigMap("VPA")
        
        metrics_server >> [hpa, vpa]
        for app in apps:
            hpa >> app
            vpa >> app