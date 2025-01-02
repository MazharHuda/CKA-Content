from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC, NetworkPolicy, Ingress
from diagrams.k8s.group import NS
from diagrams.onprem.network import Internet
from diagrams.k8s.infra import Node
from diagrams.k8s.podconfig import CM

# Diagram 1: Network Policy Implementation
with Diagram("Network Policy Configuration", show=False, direction="TB", filename="ch11_lab03_network_policy"):
    
    with Cluster("Production Environment"):
        prod_ns = NS("production")
        
        with Cluster("Frontend Tier"):
            frontend = Pod("Frontend\nrole: frontend")
            frontend_svc = SVC("Frontend Service")
            
        with Cluster("API Tier"):
            api = Pod("API Service\napp: api")
            api_svc = SVC("API Service")
            
        with Cluster("Database Tier"):
            db = Pod("Database\napp: database")
            db_svc = SVC("DB Service")
            
        # Network Policies
        api_policy = NetworkPolicy("API Policy")
        db_policy = NetworkPolicy("DB Policy")
        
        # Show traffic flow with policies
        frontend >> Edge(color="green", label="allowed") >> api_svc >> api
        api >> Edge(color="green", label="allowed") >> db_svc >> db
        api_policy >> Edge(color="red", style="dashed", label="enforce") >> api
        db_policy >> Edge(color="red", style="dashed", label="enforce") >> db

# Diagram 2: Service Mesh Architecture
with Diagram("Service Mesh Integration", show=False, direction="LR", filename="ch11_lab03_service_mesh"):
    
    inet = Internet("External\nTraffic")
    
    with Cluster("Service Mesh"):
        with Cluster("Ingress Layer"):
            gateway = Ingress("Istio Gateway")
            vs = CM("Virtual Service")
        
        with Cluster("Service Layer"):
            reviews_v1 = Pod("Reviews v1")
            reviews_v2 = Pod("Reviews v2")
            reviews_svc = SVC("Reviews Service")
            
            # Traffic splitting
            vs >> Edge(color="blue", label="80%") >> reviews_v1
            vs >> Edge(color="orange", label="20%") >> reviews_v2
            reviews_svc >> Edge(color="green") >> [reviews_v1, reviews_v2]
        
        # External traffic flow
        inet >> Edge(color="black", style="bold") >> gateway >> vs

# Diagram 3: Advanced Network Configuration
with Diagram("Advanced Network Configuration", show=False, direction="TB", filename="ch11_lab03_advanced_config"):
    
    with Cluster("Network Infrastructure"):
        nodes = [Node("Worker Node 1"), Node("Worker Node 2")]
        
        with Cluster("CNI Configuration"):
            cni_config = CM("CNI Config")
            network_config = NetworkPolicy("Network Config")
            
            # Network configuration
            cni_config >> Edge(color="blue", label="configure") >> nodes
            network_config >> Edge(color="red", label="apply") >> nodes
    
    with Cluster("Pod Networking"):
        with Cluster("Pod-to-Pod Communication"):
            pod1 = Pod("Pod 1")
            pod2 = Pod("Pod 2")
            
            # Pod communication
            pod1 >> Edge(color="green", style="dashed", label="direct") >> pod2
        
        with Cluster("Service Discovery"):
            dns = SVC("CoreDNS")
            service = SVC("ClusterIP Service")
            
            # Service discovery
            pod1 >> Edge(color="orange", label="resolve") >> dns
            dns >> Edge(color="blue", label="route") >> service 