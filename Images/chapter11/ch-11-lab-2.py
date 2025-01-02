from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.infra import Node
from diagrams.k8s.controlplane import Scheduler
from diagrams.k8s.podconfig import CM
from diagrams.k8s.others import CRD

# Diagram 1: Topology Spread Constraints
with Diagram("Topology Spread Constraints", show=False, direction="TB", filename="ch11_lab02_topology_spread"):
    
    with Cluster("Zone A"):
        zone_a = Node("Zone: us-east-1a")
        pods_a = [
            Pod("web-1\napp=web"),
            Pod("web-2\napp=web")
        ]
        zone_a >> Edge(color="blue") >> pods_a

    with Cluster("Zone B"):
        zone_b = Node("Zone: us-east-1b")
        pods_b = [
            Pod("web-3\napp=web")
        ]
        zone_b >> Edge(color="blue") >> pods_b

    with Cluster("Zone C"):
        zone_c = Node("Zone: us-east-1c")
        pods_c = [
            Pod("web-4\napp=web")
        ]
        zone_c >> Edge(color="blue") >> pods_c

    # Show scheduling constraints
    scheduler = Scheduler("kube-scheduler")
    scheduler >> Edge(color="red", label="maxSkew: 1") >> [zone_a, zone_b, zone_c]

# Diagram 2: Node Affinity Rules
with Diagram("Node Affinity Configuration", show=False, direction="LR", filename="ch11_lab02_node_affinity"):
    
    with Cluster("Node Pool"):
        nodes = [
            Node("GPU Node\ngpu-type=nvidia-tesla"),
            Node("Memory Node\nmem-type=high"),
            Node("Standard Node")
        ]
    
    with Cluster("Workload Placement"):
        gpu_pod = Pod("GPU Workload\nrequiredDuringScheduling:\n  gpu-type=nvidia-tesla")
        mem_pod = Pod("Memory Intensive\npreferredDuringScheduling:\n  mem-type=high")
        
        # Show affinity rules
        gpu_pod >> Edge(color="red", style="bold", label="required") >> nodes[0]
        mem_pod >> Edge(color="blue", style="dashed", label="preferred") >> nodes[1]

# Diagram 3: Advanced Scheduling Strategy
with Diagram("Advanced Scheduling Strategy", show=False, direction="TB", filename="ch11_lab02_strategy"):
    
    with Cluster("Scheduling Configuration"):
        config = CM("Scheduling Policy")
        rules = CRD("Custom Rules")
        
        # Show configuration flow
        config >> Edge(color="green") >> rules
    
    with Cluster("Pod Distribution"):
        with Cluster("High-Priority Workloads"):
            critical = Deploy("Critical Apps")
            gpu = Deploy("GPU Workloads")
            
            # Show priority placement
            rules >> Edge(color="red", label="guaranteed") >> [critical, gpu]
        
        with Cluster("Standard Workloads"):
            standard = Deploy("Standard Apps")
            batch = Deploy("Batch Jobs")
            
            # Show flexible placement
            rules >> Edge(color="blue", label="best-effort") >> [standard, batch]
    
    with Cluster("Resource Optimization"):
        metrics = CRD("Node Metrics")
        placement = Scheduler("Placement Decision")
        
        # Show decision flow
        metrics >> Edge(color="orange", label="influence") >> placement
        placement >> Edge(color="green", label="optimize") >> [critical, standard] 