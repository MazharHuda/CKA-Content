from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC
from diagrams.onprem.aggregator import Fluentd
from diagrams.generic.database import SQL as Elasticsearch
from diagrams.onprem.monitoring import Grafana as Kibana
from diagrams.k8s.storage import PV, PVC
from diagrams.k8s.infra import Node
from diagrams.k8s.podconfig import CM

# Set diagram attributes
with Diagram("Kubernetes Logging Architecture", show=False, direction="LR", filename="ch09_lab04_logging"):
    
    # Log Sources
    with Cluster("Log Sources"):
        with Cluster("Application Pods"):
            apps = [
                Pod("app-pod-1"),
                Pod("app-pod-2"),
                Pod("app-pod-3")
            ]
        
        with Cluster("System Components"):
            node = Node("Worker Node")
            system_logs = Pod("System Logs")
            
            # System logs flow
            node >> Edge(color="brown", style="dotted") >> system_logs

    # Log Collection
    with Cluster("Log Collection Layer"):
        # Fluentd DaemonSet
        with Cluster("Fluentd DaemonSet"):
            fluentd = Fluentd("Fluentd")
            fluentd_config = CM("fluentd-config")
            
            # Configuration relationship
            fluentd_config >> Edge(color="red", style="dotted", label="configure") >> fluentd
        
        # Log collection paths
        apps >> Edge(color="blue", label="container logs") >> fluentd
        system_logs >> Edge(color="blue", label="system logs") >> fluentd

    # Storage Layer
    with Cluster("Elasticsearch Cluster"):
        # Elasticsearch StatefulSet
        es_svc = SVC("elasticsearch-svc")
        with Cluster("Elasticsearch Nodes"):
            es_nodes = [
                Elasticsearch("es-node-1"),
                Elasticsearch("es-node-2"),
                Elasticsearch("es-node-3")
            ]
            
            # Storage for ES
            es_storage = [
                PV("es-pv-1"),
                PV("es-pv-2"),
                PV("es-pv-3")
            ]
            
            # Storage relationships
            for i in range(3):
                es_nodes[i] >> Edge(color="black", style="solid") >> es_storage[i]
        
        # Service relationship
        es_nodes >> Edge(color="green") >> es_svc

    # Visualization Layer
    with Cluster("Visualization"):
        kibana = Kibana("Kibana")
        kibana_svc = SVC("kibana-svc")
        
        # Service relationship
        kibana >> Edge(color="black") >> kibana_svc

    # Data Flow
    fluentd >> Edge(color="orange", label="forward logs") >> es_svc
    es_svc >> Edge(color="purple", label="query logs") >> kibana 