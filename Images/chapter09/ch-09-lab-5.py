from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.podconfig import CM
from diagrams.onprem.monitoring import Prometheus
from diagrams.k8s.others import CRD

# Set diagram attributes
with Diagram("Custom Metrics Implementation", show=False, direction="LR", filename="ch09_lab05_custom_metrics"):
    
    # API Server and Core Components
    with Cluster("Control Plane"):
        api = APIServer("kube-apiserver")
        
        # Custom Metrics API
        with Cluster("Custom Metrics API"):
            metrics_api = CRD("Custom Metrics\nAPIService")
            adapter = Pod("Custom Metrics\nAdapter")
            
            # API registration
            adapter >> Edge(color="red", style="bold", label="register") >> metrics_api
            metrics_api >> Edge(color="red", style="dashed") >> api

    # Monitoring Infrastructure
    with Cluster("Monitoring Stack"):
        prometheus = Prometheus("Prometheus")
        
        # Application pods being monitored
        with Cluster("Application Metrics"):
            app = Deploy("Application")
            pods = [
                Pod("app-pod-1"),
                Pod("app-pod-2")
            ]
            
            # App manages pods
            app >> Edge(color="black", style="dotted") >> pods
            
            # Metrics service
            metrics_svc = SVC("metrics-service")
            pods >> Edge(color="blue", label="expose metrics") >> metrics_svc
        
        # ServiceMonitor
        servicemonitor = CRD("ServiceMonitor")
        metrics_svc >> Edge(color="green", label="scrape") >> servicemonitor
        servicemonitor >> Edge(color="green", label="configure") >> prometheus

    # HPA and Scaling
    with Cluster("Autoscaling"):
        hpa = Pod("HPA")
        scaling_config = CM("scaling-config")
        
        # HPA configuration
        scaling_config >> Edge(color="brown", style="dotted", label="configure") >> hpa
        
        # Metrics flow for scaling
        prometheus >> Edge(color="purple", label="provide metrics") >> adapter
        hpa >> Edge(color="orange", label="query") >> adapter
        hpa >> Edge(color="blue", style="bold", label="scale") >> app

    # Main metrics flow
    metrics_svc >> Edge(color="brown", label="collect") >> prometheus
    adapter >> Edge(color="black", style="dashed", label="query") >> prometheus 