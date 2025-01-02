from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import SVC, NetworkPolicy
from diagrams.k8s.group import NS
from diagrams.onprem.network import Internet

# Set diagram attributes
with Diagram("Network Policies Lab", show=False, direction="TB", filename="ch08_lab04_network_policies"):
    
    # External Traffic
    inet = Internet("External Traffic")
    
    with Cluster("Kubernetes Cluster"):
        # Frontend Namespace
        with Cluster("Frontend Namespace"):
            frontend_ns = NS("frontend")
            
            # Frontend Components
            frontend_pods = [
                Pod("frontend-pod-1"),
                Pod("frontend-pod-2")
            ]
            frontend_svc = SVC("frontend-service")
            
            # Frontend Network Policy
            frontend_policy = NetworkPolicy("frontend-policy\nallow-ingress")
            
            # Show frontend relationships
            frontend_svc >> Edge(color="blue") >> frontend_pods
            frontend_policy >> Edge(color="green", style="dashed", label="allow 80,443") >> frontend_pods
            inet >> Edge(color="blue", style="bold") >> frontend_svc
        
        # Backend Namespace
        with Cluster("Backend Namespace"):
            backend_ns = NS("backend")
            
            # Backend Components
            backend_pods = [
                Pod("backend-pod-1"),
                Pod("backend-pod-2")
            ]
            backend_svc = SVC("backend-service")
            
            # Backend Network Policies
            default_deny = NetworkPolicy("default-deny-all")
            backend_policy = NetworkPolicy("backend-policy\nallow-from-frontend")
            
            # Show backend relationships
            backend_svc >> Edge(color="blue") >> backend_pods
            default_deny >> Edge(color="red", style="bold", label="deny all") >> backend_pods
            backend_policy >> Edge(color="green", style="dashed", label="allow from frontend") >> backend_pods
        
        # Cross-namespace communication
        frontend_pods >> Edge(color="orange", style="dotted", label="allowed") >> backend_svc
        
        # Test Pod for verification
        with Cluster("Test Namespace"):
            test_ns = NS("test")
            test_pod = Pod("test-pod")
            
            # Show blocked access
            test_pod >> Edge(color="red", style="bold", label="blocked") >> backend_svc 