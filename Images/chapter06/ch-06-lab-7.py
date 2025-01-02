from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy, StatefulSet
from diagrams.k8s.network import SVC
from diagrams.k8s.group import NS
from diagrams.onprem.client import Client
from diagrams.onprem.network import Internet

# Set diagram attributes
with Diagram("Lab 7: Advanced Service Configurations", show=False, direction="TB", filename="ch06_lab07_advanced_services"):
    
    # External Access
    clients = [
        Client("Client 1"),
        Client("Client 2")
    ]
    inet = Internet("External\nNetwork")

    with Cluster("Kubernetes Cluster"):
        # Session Affinity Service
        with Cluster("Session Affinity Example"):
            session_deploy = Deploy("session-app")
            session_svc = SVC("session-service\nsessionAffinity: ClientIP")
            session_pods = [
                Pod("session-pod-1\nnginx"),
                Pod("session-pod-2\nnginx"),
                Pod("session-pod-3\nnginx")
            ]
            
            # Connect session components
            session_deploy >> Edge(color="black", style="dotted") >> session_pods
            session_svc >> Edge(color="blue", style="bold", label="sticky session") >> session_pods
            
            # Show client affinity
            clients[0] >> Edge(color="red", style="bold") >> session_pods[0]
            clients[1] >> Edge(color="green", style="bold") >> session_pods[1]

        # Multi-Port Service
        with Cluster("Multi-Port Service"):
            multi_deploy = Deploy("multi-port-app")
            multi_svc = SVC("multi-port-service\nports: 80,443,9090")
            multi_pods = [
                Pod("multi-pod-1\nnginx+metrics"),
                Pod("multi-pod-2\nnginx+metrics")
            ]
            
            # Connect multi-port components
            multi_deploy >> Edge(color="black", style="dotted") >> multi_pods
            multi_svc >> Edge(color="orange", label="http:80") >> multi_pods
            multi_svc >> Edge(color="purple", label="https:443") >> multi_pods
            multi_svc >> Edge(color="brown", label="metrics:9090") >> multi_pods

        # Headless Service
        with Cluster("Headless Service"):
            stateful = StatefulSet("stateful-app")
            headless_svc = SVC("headless-service\nclusterIP: None")
            stateful_pods = [
                Pod("stateful-0\nDNS: pod-0.svc"),
                Pod("stateful-1\nDNS: pod-1.svc"),
                Pod("stateful-2\nDNS: pod-2.svc")
            ]
            
            # Connect headless components
            stateful >> Edge(color="black", style="dotted") >> stateful_pods
            headless_svc >> Edge(color="blue", style="dashed", label="DNS records") >> stateful_pods

            # Show direct DNS resolution
            inet >> Edge(color="green", style="dotted", label="pod-0.svc") >> stateful_pods[0]
            inet >> Edge(color="green", style="dotted", label="pod-1.svc") >> stateful_pods[1]
            inet >> Edge(color="green", style="dotted", label="pod-2.svc") >> stateful_pods[2]

        # Add Legend
        with Cluster("Service Types"):
            with Cluster(""):
                # Session Affinity (red/green)
                # Multi-Port (orange/purple/brown)
                # Headless DNS (blue dashed)
                pass 