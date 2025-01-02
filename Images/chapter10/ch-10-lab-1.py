from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler, KProxy
from diagrams.k8s.compute import Pod
from diagrams.k8s.infra import Node, Master
from diagrams.k8s.storage import PV
from diagrams.generic.storage import Storage
from diagrams.onprem.container import Docker
from diagrams.k8s.others import CRD

# Diagram 1: Cluster Upgrade Process Flow
with Diagram("Cluster Upgrade Process Flow", show=False, direction="TB", filename="ch10_lab01_upgrade_process"):
    
    with Cluster("Pre-upgrade Phase"):
        version_check = APIServer("Version Check")
        health_check = Pod("Cluster Health")
        backup = Storage("ETCD Backup")
        
        # Pre-upgrade checks flow
        version_check >> Edge(color="blue", label="1. verify") >> health_check
        health_check >> Edge(color="blue", label="2. backup") >> backup

    with Cluster("Control Plane Upgrade"):
        with Cluster("Step 1: Preparation"):
            master = Master("Control Plane Node")
            drain = Node("Drain Node")
            etcd = CRD("ETCD")
            
            # Preparation flow
            master >> Edge(color="red", label="3. drain") >> drain
            master - Edge(color="red", style="dotted") - etcd
        
        with Cluster("Step 2: Component Upgrades"):
            kubeadm = Docker("kubeadm upgrade")
            kubelet = Pod("kubelet")
            kubectl = Pod("kubectl")
            
            # Upgrade sequence
            kubeadm >> Edge(color="green", label="4. upgrade") >> kubelet
            kubeadm >> Edge(color="green", label="5. upgrade") >> kubectl

        with Cluster("Step 3: Verification"):
            api = APIServer("API Server")
            verify = Pod("Version Verification")
            uncordon = Node("Uncordon Node")
            
            # Verification flow
            api >> Edge(color="orange", label="6. verify") >> verify
            verify >> Edge(color="blue", label="7. uncordon") >> uncordon

# Diagram 2: Component Dependencies
with Diagram("Upgrade Component Dependencies", show=False, direction="LR", filename="ch10_lab01_dependencies"):
    
    with Cluster("Control Plane Components"):
        api_server = APIServer("API Server")
        controller = ControllerManager("Controller Manager")
        scheduler = Scheduler("Scheduler")
        proxy = KProxy("kube-proxy")
        
        # Control plane dependencies
        api_server >> Edge(color="red", style="bold") >> [controller, scheduler]
        api_server >> Edge(color="red", style="dashed") >> proxy

    with Cluster("Node Components"):
        node = Node("Worker Node")
        kubelet_comp = Pod("kubelet")
        container_runtime = Docker("Container Runtime")
        
        # Node component dependencies
        node >> Edge(color="blue") >> kubelet_comp
        kubelet_comp >> Edge(color="blue", style="dashed") >> container_runtime
        
    # Cross-component relationships
    api_server >> Edge(color="green", style="dotted", label="API Communication") >> kubelet_comp