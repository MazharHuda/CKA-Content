from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC, Ingress
from diagrams.k8s.podconfig import CM
from diagrams.onprem.network import Internet
from diagrams.onprem.monitoring import Prometheus
from diagrams.k8s.clusterconfig import HPA

# Diagram 1: A/B Testing Pattern
with Diagram("A/B Testing Deployment Pattern", show=True, direction="TB", filename="ch05_lab05_ab_testing"):
    
    with Cluster("A/B Testing Setup"):
        # External Traffic
        users = Internet("Users")
        ingress = Ingress("Ingress Controller")
        
        with Cluster("Version A (75%)"):
            deploy_a = Deploy("app-version-a")
            pods_a = [Pod("pod-a-1"), 
                     Pod("pod-a-2"),
                     Pod("pod-a-3")]
            
        with Cluster("Version B (25%)"):
            deploy_b = Deploy("app-version-b")
            pods_b = [Pod("pod-b-1")]
            
        # Traffic flow
        users >> ingress
        ingress >> Edge(color="blue", style="bold", label="75%") >> pods_a[0]
        ingress >> Edge(color="green", style="bold", label="25%") >> pods_b[0]
        
        # Connect remaining pods
        for pod in pods_a[1:]:
            pods_a[0] - pod

# Diagram 2: Shadow Deployment
with Diagram("Shadow Deployment Pattern", show=True, direction="LR", filename="ch05_lab05_shadow"):
    
    with Cluster("Shadow Testing Environment"):
        # Production traffic
        prod_traffic = Internet("Production\nTraffic")
        
        with Cluster("Production Service"):
            prod_svc = SVC("prod-service")
            prod_deploy = Deploy("prod-app")
            prod_pods = [Pod("prod-1"),
                        Pod("prod-2")]
            
        with Cluster("Shadow Service"):
            shadow_svc = SVC("shadow-service")
            shadow_deploy = Deploy("shadow-app")
            shadow_pods = [Pod("shadow-1"),
                         Pod("shadow-2")]
            
        # Traffic mirroring
        prod_traffic >> prod_svc
        prod_svc >> Edge(color="blue", label="real traffic") >> prod_pods[0]
        prod_svc >> Edge(color="red", style="dashed", label="mirrored") >> shadow_pods[0]
        
        # Connect remaining pods
        for pod in prod_pods[1:]:
            prod_pods[0] - pod
        for pod in shadow_pods[1:]:
            shadow_pods[0] - pod

# Diagram 3: Feature Toggle Pattern
with Diagram("Feature Toggle Deployment", show=True, direction="TB", filename="ch05_lab05_feature_toggle"):
    
    with Cluster("Feature Toggle Implementation"):
        # Configuration
        config = CM("Feature Flags")
        metrics = Prometheus("Feature Metrics")
        
        with Cluster("Application Deployment"):
            deploy = Deploy("application")
            
            with Cluster("Feature States"):
                # Feature A enabled
                feature_a = [Pod("pod-a-1"),
                           Pod("pod-a-2")]
                
                # Feature B enabled
                feature_b = [Pod("pod-b-1"),
                           Pod("pod-b-2")]
                
                # Both features
                feature_ab = [Pod("pod-ab-1"),
                            Pod("pod-ab-2")]
            
            # Configuration flow
            config >> Edge(color="blue", label="toggle") >> deploy
            deploy >> Edge(color="green") >> feature_a[0]
            deploy >> Edge(color="red") >> feature_b[0]
            deploy >> Edge(color="orange") >> feature_ab[0]
            
            # Connect remaining pods in each feature group
            for pod in feature_a[1:]:
                feature_a[0] - pod
            for pod in feature_b[1:]:
                feature_b[0] - pod
            for pod in feature_ab[1:]:
                feature_ab[0] - pod
            
            # Metrics collection
            metrics >> Edge(color="purple", style="dotted") >> [feature_a[0], feature_b[0], feature_ab[0]] 