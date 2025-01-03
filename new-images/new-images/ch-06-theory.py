from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.network import SVC, Ingress, NetworkPolicy
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.infra import Node
from diagrams.onprem.network import Internet
from diagrams.k8s.podconfig import ConfigMap
from diagrams.k8s.group import NS
from diagrams.generic.network import Switch, Firewall
from diagrams.k8s.compute import Pod

with Diagram("Kubernetes Networking Architecture", show=False, direction="TB"):
    # External Traffic
    inet = Internet("External\nTraffic")
    
    # Load Balancing Layer
    with Cluster("Load Balancing"):
        lb = ConfigMap("Cloud\nLoad Balancer")
        ingress = Ingress("Ingress\nController")
    
    # Service Layer
    with Cluster("Service Layer"):
        external_svc = SVC("LoadBalancer\nService")
        nodeport_svc = SVC("NodePort\nService")
        clusterip_svc = SVC("ClusterIP\nService")
    
    # Network Policies
    with Cluster("Network Policies"):
        policies = NetworkPolicy("Network\nSecurity")
        netpol = NetworkPolicy("Network\nPolicies")
    
    # Pod Networking
    with Cluster("Pod Networking"):
        # Node 1
        with Cluster("Node 1"):
            node1 = Node("Worker\nNode 1")
            with Cluster("Pod 1"):
                pod1 = Pod("Container 1")
                pod2 = Pod("Container 2")
            
            with Cluster("Pod 2"):
                pod3 = Pod("Container 3")
                pod4 = Pod("Container 4")
        
        # Node 2
        with Cluster("Node 2"):
            node2 = Node("Worker\nNode 2")
            with Cluster("Pod 3"):
                pod5 = Pod("Container 5")
                pod6 = Pod("Container 6")
    
    # CNI Layer
    with Cluster("CNI Network"):
        cni = Switch("CNI Plugin")
        overlay = Switch("Overlay\nNetwork")
    
    # Traffic Flow
    inet >> lb >> ingress >> external_svc
    external_svc >> nodeport_svc >> clusterip_svc
    
    # Policy Enforcement
    policies - netpol
    netpol >> Edge(color="red", style="dashed") >> pod1
    netpol >> Edge(color="red", style="dashed") >> pod3
    netpol >> Edge(color="red", style="dashed") >> pod5
    
    # Container Communication
    pod1 >> Edge(color="brown", style="dotted") >> pod2
    pod3 >> Edge(color="brown", style="dotted") >> pod4
    pod5 >> Edge(color="brown", style="dotted") >> pod6
    
    # Node Networking
    node1 >> Edge(color="darkblue") >> cni
    node2 >> Edge(color="darkblue") >> cni
    cni >> Edge(color="darkblue", style="dashed") >> overlay
    
    # Service to Pod Routing
    clusterip_svc >> Edge(color="green") >> pod1
    clusterip_svc >> Edge(color="green") >> pod3
    clusterip_svc >> Edge(color="green") >> pod5