from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import SVC, NetworkPolicy
from diagrams.k8s.group import NS
from diagrams.k8s.infra import Node

# Set diagram attributes
with Diagram("Lab 3: Network Policies", show=False, direction="TB", filename="ch06_lab03_network_policies"):
    
    # Create main cluster
    with Cluster("Kubernetes Cluster"):
        # Frontend Namespace
        with Cluster("Frontend Namespace"):
            frontend_ns = NS("frontend")
            frontend_pods = [
                Pod("frontend-pod-1\napp: frontend"),
                Pod("frontend-pod-2\napp: frontend")
            ]
            frontend_svc = SVC("frontend-service")
            
            # Frontend Network Policy
            frontend_policy = NetworkPolicy("frontend-policy\nallow-ingress")
            
            # Connect frontend components
            frontend_svc >> Edge(color="blue") >> frontend_pods
            frontend_policy >> Edge(color="green", style="dashed", label="allow 80,443") >> frontend_pods

        # Backend Namespace
        with Cluster("Backend Namespace"):
            backend_ns = NS("backend")
            backend_pods = [
                Pod("backend-pod-1\napp: backend"),
                Pod("backend-pod-2\napp: backend")
            ]
            backend_svc = SVC("backend-service")
            
            # Backend Network Policies
            default_deny = NetworkPolicy("default-deny-all")
            backend_policy = NetworkPolicy("backend-policy\nallow-from-frontend")
            
            # Connect backend components
            backend_svc >> Edge(color="blue") >> backend_pods
            default_deny >> Edge(color="red", style="bold", label="deny all") >> backend_pods
            backend_policy >> Edge(color="green", style="dashed", label="allow from frontend") >> backend_pods

        # Test Namespace
        with Cluster("Test Namespace"):
            test_ns = NS("test")
            test_pod = Pod("test-pod\napp: test")
            
            # Show blocked access
            test_pod >> Edge(color="red", style="dotted", label="blocked") >> backend_svc
            test_pod >> Edge(color="red", style="dotted", label="blocked") >> frontend_svc

        # Allowed Communication Paths
        frontend_pods[0] >> Edge(color="green", style="bold", label="allowed") >> backend_svc
        frontend_pods[1] >> Edge(color="green", style="bold", label="allowed") >> backend_svc 