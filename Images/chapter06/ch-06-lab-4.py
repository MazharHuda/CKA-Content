from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import SVC
from diagrams.k8s.infra import Node
from diagrams.k8s.group import NS

# Set diagram attributes
with Diagram("Lab 4: DNS and Service Discovery", show=False, direction="TB", filename="ch06_lab04_dns"):
    
    # Create DNS Infrastructure
    with Cluster("DNS Infrastructure (kube-system)"):
        coredns_pods = [
            Pod("coredns-pod-1"),
            Pod("coredns-pod-2")
        ]
        kubedns_svc = SVC("kube-dns\nService")
        
        # Connect DNS components
        coredns_pods >> Edge(color="blue", style="bold") >> kubedns_svc

    # Create Application Namespaces
    with Cluster("Application Namespaces"):
        # Production Namespace
        with Cluster("Production Namespace"):
            prod_ns = NS("prod")
            prod_svc = SVC("web-service.prod\nClusterIP")
            prod_pods = [
                Pod("web-pod-1\nnginx"),
                Pod("web-pod-2\nnginx")
            ]
            
            # Connect service to pods
            prod_svc >> Edge(color="green") >> prod_pods

        # Development Namespace
        with Cluster("Development Namespace"):
            dev_ns = NS("dev")
            dev_svc = SVC("web-service.dev\nClusterIP")
            dev_pods = [
                Pod("web-pod-1\nnginx"),
                Pod("web-pod-2\nnginx")
            ]
            
            # Connect service to pods
            dev_svc >> Edge(color="green") >> dev_pods

        # Test Pod for DNS Resolution
        test_pod = Pod("dns-test-pod\nbusybox")

        # Show DNS Resolution Paths
        kubedns_svc >> Edge(color="orange", style="dashed", label="resolve") >> prod_svc
        kubedns_svc >> Edge(color="orange", style="dashed", label="resolve") >> dev_svc

        # Show DNS Query Paths
        test_pod >> Edge(color="blue", style="dotted", label="nslookup\nweb-service.prod") >> kubedns_svc
        test_pod >> Edge(color="blue", style="dotted", label="nslookup\nweb-service.dev") >> kubedns_svc

        # Show Custom DNS Config
        with Cluster("Custom DNS Configuration"):
            custom_pod = Pod("custom-dns-pod\ndnsPolicy: None")
            
            # Show custom DNS settings
            custom_pod >> Edge(color="red", style="bold", label="8.8.8.8") >> test_pod
            custom_pod >> Edge(color="purple", style="dashed", label="custom\nsearch paths") >> kubedns_svc