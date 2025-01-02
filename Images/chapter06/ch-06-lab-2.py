from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC
from diagrams.k8s.infra import Node
from diagrams.onprem.network import Internet
from diagrams.onprem.client import Users

# Set diagram attributes
with Diagram("Lab 2: Kubernetes Services Architecture", show=False, direction="TB", filename="ch06_lab02_services"):
    
    # External Users/Traffic
    users = Users("External\nUsers")
    inet = Internet("External\nNetwork")

    with Cluster("Kubernetes Cluster"):
        # Create Service Types
        with Cluster("Service Layer"):
            clusterip = SVC("ClusterIP Service\nweb-service\n(internal)")
            nodeport = SVC("NodePort Service\nweb-service-np\n(30080)")
            loadbalancer = SVC("LoadBalancer Service\nweb-service-lb")

        # Create Nodes
        with Cluster("Node Pool"):
            nodes = [
                Node("worker-node-1\nPort 30080"),
                Node("worker-node-2\nPort 30080")
            ]

        # Create Application Deployment and Pods
        with Cluster("Application Tier"):
            deploy = Deploy("web-app\nDeployment")
            pods = [
                Pod("web-pod-1\nnginx"),
                Pod("web-pod-2\nnginx"),
                Pod("web-pod-3\nnginx")
            ]
            
            # Deployment manages pods
            deploy >> Edge(color="black", style="dotted") >> pods

        # Test Pod for Internal Access
        test_pod = Pod("test-pod\nbusybox")

        # Service to Pod Connections
        clusterip >> Edge(color="blue", label="port 80") >> pods
        nodeport >> Edge(color="green", label="port 80") >> pods
        loadbalancer >> Edge(color="orange", label="port 80") >> pods

        # External Access Paths
        inet >> Edge(color="red", style="bold") >> loadbalancer
        inet >> Edge(color="red", style="bold") >> nodes
        nodes >> Edge(color="green") >> nodeport

        # Internal Access Path
        test_pod >> Edge(color="blue", style="dashed", label="internal") >> clusterip

        # User Traffic Flow
        users >> Edge(color="black", style="bold") >> inet

    # Add Legend Cluster
    with Cluster("Traffic Types"):
        with Cluster(""):
            # Empty cluster for legend formatting
            pass 