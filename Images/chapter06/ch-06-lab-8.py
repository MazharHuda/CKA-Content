from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, DaemonSet
from diagrams.k8s.network import SVC
from diagrams.k8s.infra import Node
from diagrams.k8s.group import NS
from diagrams.generic.network import Switch, Firewall
from diagrams.generic.os import LinuxGeneral
from diagrams.onprem.network import Internet

# Set diagram attributes
with Diagram("Lab 8: CNI Plugin Configuration", show=False, direction="TB", filename="ch06_lab08_cni"):
    
    # External Network
    inet = Internet("External\nNetwork")

    with Cluster("Kubernetes Cluster"):
        # CNI Infrastructure
        with Cluster("CNI Layer"):
            cni_daemon = DaemonSet("CNI Plugin\nDaemonSet")
            cni_config = LinuxGeneral("/etc/cni/net.d/\nConfiguration")
            
            # CNI Components
            with Cluster("CNI Components"):
                ipam = Switch("IPAM Plugin")
                routing = Switch("Routing Plugin")
                policy = Firewall("Network Policy\nEnforcement")
                
                # Connect CNI components
                cni_config >> Edge(color="black", style="bold") >> [ipam, routing, policy]
                cni_daemon >> Edge(color="blue", style="bold") >> [ipam, routing, policy]

        # Node Network Configuration
        with Cluster("Worker Nodes"):
            nodes = [
                Node("worker-1"),
                Node("worker-2")
            ]
            
            # Node CNI Components
            for node in nodes:
                node_cni = Switch(f"CNI on {node.label}")
                node >> Edge(color="black", style="dotted") >> node_cni
                cni_daemon >> Edge(color="blue", style="dashed") >> node_cni

        # Pod Network Example
        with Cluster("Pod Networking"):
            pods = [
                Pod("pod-1\nip: 10.244.1.2"),
                Pod("pod-2\nip: 10.244.2.3")
            ]
            
            # Show pod network configuration
            ipam >> Edge(color="red", style="bold", label="IP allocation") >> pods
            routing >> Edge(color="green", style="bold", label="route config") >> pods
            policy >> Edge(color="orange", style="dashed", label="policy enforcement") >> pods

        # Network Paths
        with Cluster("Network Paths"):
            # Pod to Pod Communication
            pods[0] >> Edge(color="purple", style="bold", label="pod-to-pod") >> pods[1]
            
            # External Communication
            inet >> Edge(color="brown", style="bold") >> routing
            pods >> Edge(color="brown", style="bold") >> inet

        # CNI Monitoring
        with Cluster("CNI Monitoring"):
            metrics_svc = SVC("cni-metrics-service")
            cni_daemon >> Edge(color="blue", style="dotted", label="metrics") >> metrics_svc

        # Add Legend
        with Cluster("Network Types"):
            with Cluster(""):
                # CNI Configuration (black)
                # IP Management (red)
                # Routing (green)
                # Policy (orange)
                # Pod Communication (purple)
                # External Traffic (brown)
                pass 