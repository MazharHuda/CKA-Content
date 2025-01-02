from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.infra import Node
from diagrams.k8s.controlplane import APIServer
from diagrams.generic.os import Ubuntu
from diagrams.onprem.container import Docker
from diagrams.k8s.others import CRD

# Diagram 1: Node Maintenance Workflow
with Diagram("Node Maintenance Process", show=False, direction="TB", filename="ch10_lab02_node_maintenance"):
    
    with Cluster("Pre-maintenance Phase"):
        # Node inspection
        node_check = Node("Target Node")
        pod_list = Pod("Running Pods")
        scheduler = APIServer("Scheduler")
        
        # Show inspection flow
        node_check >> Edge(color="blue", label="1. Check Pods") >> pod_list
        scheduler >> Edge(color="blue", style="dashed", label="Schedule Pods") >> pod_list

    with Cluster("Maintenance Execution"):
        with Cluster("Step 1: Node Preparation"):
            drain = Node("Drain Node")
            other_nodes = [Node("Other Node 1"), 
                         Node("Other Node 2")]
            
            # Show pod migration
            drain >> Edge(color="red", label="2. Migrate Pods") >> other_nodes
        
        with Cluster("Step 2: System Maintenance"):
            system = Ubuntu("System Updates")
            kubelet = Docker("kubelet service")
            updates = CRD("System Packages")
            
            # Show maintenance tasks
            system >> Edge(color="orange", label="3. Stop") >> kubelet
            system >> Edge(color="orange", label="4. Update") >> updates
            updates >> Edge(color="orange", label="5. Start") >> kubelet

    with Cluster("Post-maintenance Phase"):
        node_ready = Node("Node Ready")
        verify = APIServer("Verification")
        new_pods = [Pod("New Pod 1"),
                   Pod("New Pod 2")]
        
        # Show node recovery
        node_ready >> Edge(color="green", label="6. Uncordon") >> verify
        verify >> Edge(color="green", label="7. Schedule") >> new_pods

# Diagram 2: Pod Migration Flow
with Diagram("Pod Migration During Maintenance", show=False, direction="LR", filename="ch10_lab02_pod_migration"):
    
    with Cluster("Original Node (Maintenance)"):
        orig_node = Node("Draining Node")
        orig_pods = [Pod("Original Pod 1"),
                    Pod("Original Pod 2"),
                    Pod("Original Pod 3")]
        
        orig_node >> Edge(color="red", style="bold", label="Drain") >> orig_pods

    with Cluster("Target Nodes"):
        target_nodes = [
            Node("Target Node 1"),
            Node("Target Node 2")
        ]
        new_pods = [Pod("Migrated Pod 1"),
                   Pod("Migrated Pod 2"),
                   Pod("Migrated Pod 3")]
        
        # Show pod redistribution
        for node in target_nodes:
            orig_pods >> Edge(color="blue", style="dashed", label="Migrate") >> node
            node >> Edge(color="green", label="Schedule") >> new_pods 