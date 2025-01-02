from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler
from diagrams.k8s.storage import PV, PVC
from diagrams.k8s.infra import Node
from diagrams.k8s.podconfig import CM, Secret

# Set diagram attributes
with Diagram("Kubernetes Troubleshooting Scenarios Lab", show=True, direction="TB", filename="ch02_lab09_troubleshooting"):
    
    # Control Plane Troubleshooting
    with Cluster("Control Plane Issues"):
        api = APIServer("API Server\nHealth Check")
        controller = ControllerManager("Controller Manager\nStatus")
        scheduler = Scheduler("Scheduler\nDiagnostics")
        
        # Show control plane relationships
        api >> Edge(color="red", style="dashed", label="1. Check Logs") >> controller
        api >> Edge(color="red", style="dashed", label="2. Verify Status") >> scheduler
    
    # Node Level Issues
    with Cluster("Node Problems"):
        node = Node("Worker Node")
        kubelet = Pod("kubelet\nStatus")
        
        # Show node diagnostics
        node >> Edge(color="orange", label="3. Check Health") >> kubelet
        kubelet >> Edge(color="orange", style="dashed", label="4. Report Status") >> api
    
    # Application Issues
    with Cluster("Application Troubleshooting"):
        deploy = Deploy("Deployment\nStatus")
        pod = Pod("Problem Pod")
        svc = SVC("Service\nEndpoints")
        config = CM("ConfigMap")
        secret = Secret("Secrets")
        
        # Show application diagnostics
        deploy >> Edge(color="blue", label="5. Check Rollout") >> pod
        svc >> Edge(color="green", label="6. Verify Endpoints") >> pod
        config >> Edge(color="purple", style="dotted") >> pod
        secret >> Edge(color="purple", style="dotted") >> pod
    
    # Storage Issues
    with Cluster("Storage Problems"):
        pv = PV("PV Status")
        pvc = PVC("PVC Binding")
        
        # Show storage diagnostics
        pvc >> Edge(color="brown", label="7. Check Binding") >> pv
        pv >> Edge(color="brown", style="dashed") >> pod