from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC, Ingress
from diagrams.k8s.infra import Node
from diagrams.k8s.controlplane import APIServer, KProxy
from diagrams.onprem.network import Internet
from diagrams.onprem.client import Users
from diagrams.k8s.group import NS

# Diagram 1: Multi-cluster Architecture
with Diagram("Multi-cluster Architecture", show=True, direction="TB", filename="ch05_lab06_multicluster"):
    
    users = Users("Global Users")
    glb_ingress = Ingress("Global Load Balancer")
    
    with Cluster("Multi-cluster Environment"):
        # Cluster 1
        with Cluster("Cluster 1 (US Region)"):
            api1 = APIServer("API Server 1")
            with Cluster("Worker Nodes"):
                node1 = Node("worker1-us")
                node2 = Node("worker2-us")
                pods1 = [Pod("pod-us-1"),
                        Pod("pod-us-2")]
                
                # Connect nodes to pods
                node1 >> pods1[0]
                node2 >> pods1[1]
            
        # Cluster 2
        with Cluster("Cluster 2 (EU Region)"):
            api2 = APIServer("API Server 2")
            with Cluster("Worker Nodes"):
                node3 = Node("worker1-eu")
                node4 = Node("worker2-eu")
                pods2 = [Pod("pod-eu-1"),
                        Pod("pod-eu-2")]
                
                # Connect nodes to pods
                node3 >> pods2[0]
                node4 >> pods2[1]
        
        # Traffic flow
        users >> glb_ingress
        glb_ingress >> Edge(color="blue", label="route") >> [api1, api2]

# Diagram 2: Active-Active Pattern
with Diagram("Active-Active Multi-cluster Pattern", show=True, direction="LR", filename="ch05_lab06_active_active"):
    
    inet = Internet("Internet Traffic")
    
    with Cluster("Global Load Balancing"):
        gslb = Ingress("Global Service LB")
        
        with Cluster("Active Cluster 1"):
            svc1 = SVC("service-c1")
            deploy1 = Deploy("app-c1")
            pods_c1 = [Pod("pod-c1-1"),
                      Pod("pod-c1-2")]
            
            # Connect components
            deploy1 >> pods_c1
            pods_c1[0] >> svc1
            
        with Cluster("Active Cluster 2"):
            svc2 = SVC("service-c2")
            deploy2 = Deploy("app-c2")
            pods_c2 = [Pod("pod-c2-1"),
                      Pod("pod-c2-2")]
            
            # Connect components
            deploy2 >> pods_c2
            pods_c2[0] >> svc2
        
        # Traffic distribution
        inet >> gslb
        gslb >> Edge(color="blue", label="50%") >> svc1
        gslb >> Edge(color="green", label="50%") >> svc2

# Diagram 3: Disaster Recovery Pattern
with Diagram("Disaster Recovery Pattern", show=True, direction="TB", filename="ch05_lab06_dr"):
    
    with Cluster("Multi-Region Deployment"):
        # Primary Region
        with Cluster("Primary Region (Active)"):
            primary_ns = NS("prod-primary")
            primary_api = APIServer("Primary API")
            primary_proxy = KProxy("kube-proxy")
            
            with Cluster("Primary Workloads"):
                primary_deploy = Deploy("app-primary")
                primary_pods = [Pod("pod-p-1"),
                              Pod("pod-p-2")]
                primary_svc = SVC("service-primary")
                
                # Connect primary components
                primary_deploy >> primary_pods
                primary_pods[0] >> primary_svc
        
        # DR Region
        with Cluster("DR Region (Standby)"):
            dr_ns = NS("prod-dr")
            dr_api = APIServer("DR API")
            dr_proxy = KProxy("kube-proxy")
            
            with Cluster("DR Workloads"):
                dr_deploy = Deploy("app-dr")
                dr_pods = [Pod("pod-dr-1"),
                          Pod("pod-dr-2")]
                dr_svc = SVC("service-dr")
                
                # Connect DR components
                dr_deploy >> dr_pods
                dr_pods[0] >> dr_svc
        
        # Replication and failover
        primary_api >> Edge(color="blue", style="dashed", label="replicate") >> dr_api
        primary_svc >> Edge(color="red", style="dotted", label="failover") >> dr_svc 