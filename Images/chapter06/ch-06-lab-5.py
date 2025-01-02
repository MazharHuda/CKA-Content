from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC, Ingress
from diagrams.k8s.infra import Node
from diagrams.onprem.network import Internet
from diagrams.onprem.client import Users

# Set diagram attributes
with Diagram("Lab 5: Ingress and Load Balancing", show=False, direction="TB", filename="ch06_lab05_ingress"):
    
    # External Access
    users = Users("External\nUsers")
    inet = Internet("External\nNetwork")

    with Cluster("Kubernetes Cluster"):
        # Ingress Layer
        with Cluster("Ingress Layer"):
            ingress = Ingress("nginx-ingress\n/app1 → app1-service\n/app2 → app2-service")
            ingress_controller = Deploy("nginx-ingress-controller")
            ingress_pods = [
                Pod("ingress-pod-1"),
                Pod("ingress-pod-2")
            ]
            
            # Connect ingress components
            ingress_controller >> Edge(color="black", style="dotted") >> ingress_pods
            ingress >> Edge(color="blue", style="bold") >> ingress_pods

        # Application 1
        with Cluster("App1 Namespace"):
            app1_svc = SVC("app1-service\nClusterIP")
            app1_deploy = Deploy("app1-deployment")
            app1_pods = [
                Pod("app1-pod-1\nnginx"),
                Pod("app1-pod-2\nnginx")
            ]
            
            # Connect app1 components
            app1_deploy >> Edge(color="black", style="dotted") >> app1_pods
            app1_svc >> Edge(color="green") >> app1_pods

        # Application 2
        with Cluster("App2 Namespace"):
            app2_svc = SVC("app2-service\nClusterIP")
            app2_deploy = Deploy("app2-deployment")
            app2_pods = [
                Pod("app2-pod-1\nnginx"),
                Pod("app2-pod-2\nnginx")
            ]
            
            # Connect app2 components
            app2_deploy >> Edge(color="black", style="dotted") >> app2_pods
            app2_svc >> Edge(color="green") >> app2_pods

        # Traffic Flow
        users >> Edge(color="red", style="bold") >> inet
        inet >> Edge(color="red", style="bold") >> ingress
        ingress_pods >> Edge(color="orange", label="/app1") >> app1_svc
        ingress_pods >> Edge(color="orange", label="/app2") >> app2_svc

        # Load Balancer
        with Cluster("Load Balancer"):
            lb_svc = SVC("ingress-service\nLoadBalancer")
            
            # Connect load balancer
            inet >> Edge(color="purple", style="bold") >> lb_svc
            lb_svc >> Edge(color="purple") >> ingress_pods 