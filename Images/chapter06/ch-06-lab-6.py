from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC, NetworkPolicy
from diagrams.k8s.infra import Node
from diagrams.k8s.group import NS
from diagrams.onprem.network import Internet
from diagrams.generic.network import Switch

# Set diagram attributes
with Diagram("Lab 6: Network Troubleshooting", show=False, direction="TB", filename="ch06_lab06_troubleshooting"):
    
    # External Network
    inet = Internet("External\nNetwork")

    with Cluster("Kubernetes Cluster"):
        # Network Infrastructure
        with Cluster("Network Infrastructure"):
            cni = Switch("CNI Plugin\n(Calico/Flannel)")
            node_network = Switch("Node Network")
            
            # Connect network components
            cni >> Edge(color="blue", style="bold") >> node_network

        # Test Namespace
        with Cluster("Network Test Namespace"):
            test_ns = NS("network-test")
            
            # Netshoot Pod for Diagnostics
            netshoot = Pod("netshoot\nNetwork Diagnostic Tools")
            
            # Test Web Service
            web_deploy = Deploy("web-test\nDeployment")
            web_svc = SVC("web-test-svc\nClusterIP")
            web_pods = [
                Pod("web-pod-1\nnginx"),
                Pod("web-pod-2\nnginx"),
                Pod("web-pod-3\nnginx")
            ]
            
            # Network Policy
            test_policy = NetworkPolicy("test-network-policy")

            # Connect components
            web_deploy >> Edge(color="black", style="dotted") >> web_pods
            web_svc >> Edge(color="green") >> web_pods
            test_policy >> Edge(color="red", style="dashed", label="policy rules") >> web_pods

        # Diagnostic Paths
        with Cluster("Diagnostic Actions"):
            # DNS Checks
            netshoot >> Edge(color="orange", style="bold", label="nslookup") >> web_svc
            
            # Connectivity Tests
            netshoot >> Edge(color="purple", style="bold", label="ping/wget") >> web_pods
            
            # Network Capture
            netshoot >> Edge(color="blue", style="dotted", label="tcpdump") >> node_network
            
            # Policy Verification
            netshoot >> Edge(color="red", style="dotted", label="verify") >> test_policy

        # External Access Testing
        inet >> Edge(color="orange", style="dashed", label="connectivity test") >> web_svc

        # MTU and Interface Checks
        with Cluster("Interface Diagnostics"):
            netshoot >> Edge(color="green", style="dashed", label="ip link\nnetstat -i") >> cni
            netshoot >> Edge(color="blue", style="dashed", label="MTU test") >> web_pods

        # Add Legend
        with Cluster("Diagnostic Types"):
            with Cluster(""):
                # DNS Checks (orange)
                # Connectivity Tests (purple)
                # Packet Capture (blue dotted)
                # Policy Verification (red)
                # Interface Checks (green)
                pass 