from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import SVC, NetworkPolicy
from diagrams.k8s.group import NS
from diagrams.k8s.podconfig import CM

# Set diagram attributes
with Diagram("Network Policies and Pod Communication Lab", show=False, direction="TB", filename="ch02_lab04_network"):
    
    # Create Production Namespace
    with Cluster("Production Namespace"):
        prod_ns = NS("prod")
        
        # Frontend and Backend pods
        with Cluster("Frontend"):
            frontend = Pod("frontend\napp: web")
            
        with Cluster("Backend"):
            backend = Pod("backend\napp: db")
            backend_svc = SVC("backend-svc")
        
        # Network Policies
        default_deny = NetworkPolicy("default-deny")
        allow_frontend = NetworkPolicy("allow-frontend-to-backend")
        
        # Show policy relationships
        default_deny >> Edge(color="red", style="dashed", label="deny all") >> [frontend, backend]
        allow_frontend >> Edge(color="green", style="bold", label="allow 3306") >> backend
        
    # Create Development Namespace for testing
    with Cluster("Development Namespace"):
        dev_ns = NS("dev")
        test_pod = Pod("test-pod")
        
        # Show blocked access
        test_pod >> Edge(color="red", style="dotted", label="blocked") >> backend_svc

    # Service connections
    frontend >> Edge(color="blue") >> backend_svc >> backend