from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler
from diagrams.k8s.infra import Node
from diagrams.k8s.podconfig import CM, Secret
from diagrams.k8s.others import CRD

# Set diagram attributes
with Diagram("Basic Kubernetes Troubleshooting Flow", show=False, direction="LR", filename="chapter01_lab04"):
    # Control Plane Components for Troubleshooting
    with Cluster("Control Plane Troubleshooting"):
        api = APIServer("kube-apiserver")
        controller = ControllerManager("kube-controller-manager")
        scheduler = Scheduler("kube-scheduler")
        
        # Show control plane relationships
        api >> Edge(color="red", style="dashed", label="1. Check Logs") >> controller
        api >> Edge(color="red", style="dashed", label="2. Check Status") >> scheduler

    # Node Level Troubleshooting
    with Cluster("Node Troubleshooting"):
        node = Node("worker-node")
        with Cluster("Pod Issues"):
            pod = Pod("failing-pod")
            config = CM("pod-config")
            secret = Secret("pod-secret")

            # Pod troubleshooting flow
            pod >> Edge(color="red", label="3. Check Events") >> config
            pod >> Edge(color="red", label="4. Check Secrets") >> secret

    # Service Level Troubleshooting
    with Cluster("Service Troubleshooting"):
        svc = SVC("service")
        ep = CRD("endpoints")
        
        # Service troubleshooting flow
        svc >> Edge(color="red", label="5. Check Endpoints") >> ep
        svc >> Edge(color="red", label="6. Verify Selectors") >> pod

    # Cross-component relationships
    api >> Edge(color="blue", style="dotted", label="7. API Responses") >> node
    node >> Edge(color="blue", style="dotted", label="8. Node Status") >> api