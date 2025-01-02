from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy, RS
from diagrams.k8s.network import SVC
from diagrams.onprem.network import Internet
from diagrams.k8s.podconfig import CM

# Diagram 1: Rolling Update Strategy
with Diagram("Rolling Update Deployment Strategy", show=False, direction="TB", filename="ch05_lab01_rolling_update"):
    
    with Cluster("Rolling Update Process"):
        # Original deployment
        with Cluster("Original (v1)"):
            deploy_v1 = Deploy("web-app:1.19")
            pods_v1 = [Pod("pod-v1-1"),
                      Pod("pod-v1-2"),
                      Pod("pod-v1-3")]
            deploy_v1 >> pods_v1

        # Updated deployment
        with Cluster("Updated (v2)"):
            deploy_v2 = Deploy("web-app:1.20")
            pods_v2 = [Pod("pod-v2-1"),
                      Pod("pod-v2-2"),
                      Pod("pod-v2-3")]
            deploy_v2 >> pods_v2

        # Service
        svc = SVC("web-service")
        
        # Show rolling update flow
        pods_v1 >> Edge(color="blue", style="bold") >> svc
        pods_v2 >> Edge(color="green", style="bold") >> svc

# Diagram 2: Blue-Green Deployment
with Diagram("Blue-Green Deployment Strategy", show=False, direction="LR", filename="ch05_lab01_blue_green"):
    
    inet = Internet("Users")
    
    with Cluster("Blue-Green Deployment"):
        # Blue environment
        with Cluster("Blue Environment"):
            blue_deploy = Deploy("web-blue")
            blue_pods = [Pod("blue-pod-1"),
                        Pod("blue-pod-2"),
                        Pod("blue-pod-3")]
            blue_deploy >> blue_pods

        # Green environment
        with Cluster("Green Environment"):
            green_deploy = Deploy("web-green")
            green_pods = [Pod("green-pod-1"),
                         Pod("green-pod-2"),
                         Pod("green-pod-3")]
            green_deploy >> green_pods

        # Service
        service = SVC("web-service")
        
        # Traffic flow
        inet >> service
        service >> Edge(color="blue", style="bold", label="current") >> blue_pods
        service >> Edge(color="green", style="dotted", label="ready") >> green_pods

# Diagram 3: Canary Deployment
with Diagram("Canary Deployment Strategy", show=False, direction="TB", filename="ch05_lab01_canary"):
    
    with Cluster("Canary Deployment"):
        # Main production deployment
        with Cluster("Production (90% traffic)"):
            prod_deploy = Deploy("web-main")
            prod_pods = [Pod("prod-1"), Pod("prod-2"),
                        Pod("prod-3"), Pod("prod-4"),
                        Pod("prod-5"), Pod("prod-6"),
                        Pod("prod-7"), Pod("prod-8"),
                        Pod("prod-9")]
            prod_deploy >> prod_pods

        # Canary deployment
        with Cluster("Canary (10% traffic)"):
            canary_deploy = Deploy("web-canary")
            canary_pod = Pod("canary-1")
            canary_deploy >> canary_pod

        # Service and config
        svc = SVC("web-service")
        config = CM("version-config")

        # Show traffic distribution
        prod_pods >> Edge(color="blue", style="bold", label="90%") >> svc
        canary_pod >> Edge(color="green", style="bold", label="10%") >> svc
        config >> Edge(color="red", style="dotted") >> [prod_deploy, canary_deploy] 