from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy, RS
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.group import NS
from diagrams.k8s.infra import Node
from diagrams.k8s.others import CRD
from diagrams.k8s.controlplane import Scheduler
from diagrams.onprem.monitoring import Prometheus

# Diagram 1: Pod Disruption Budget Implementation
with Diagram("Pod Disruption Budget Configuration", show=False, direction="TB", filename="ch11_lab05_pdb"):
    
    with Cluster("High Availability Setup"):
        with Cluster("Production Namespace"):
            ns = NS("production")
            
            # Application pods
            deploy = Deploy("critical-service")
            pods = [
                Pod("pod-1\napp=critical"),
                Pod("pod-2\napp=critical"),
                Pod("pod-3\napp=critical")
            ]
            
            # PDB configuration
            pdb = CRD("PodDisruptionBudget\nminAvailable: 2")
            
            # Show relationships
            deploy >> Edge(color="blue") >> pods
            pdb >> Edge(color="red", style="dashed", label="protect") >> pods

        with Cluster("Node Maintenance"):
            node = Node("Node for Maintenance")
            scheduler = Scheduler("kube-scheduler")
            
            # Show eviction protection
            node >> Edge(color="orange", label="drain") >> scheduler
            scheduler >> Edge(color="green", label="respect") >> pdb

# Diagram 2: Vertical Pod Autoscaling
with Diagram("Vertical Pod Autoscaling", show=False, direction="TB", filename="ch11_lab05_vpa"):
    
    with Cluster("Resource Management"):
        # Monitoring components
        metrics = Prometheus("Resource Metrics")
        vpa = CRD("VerticalPodAutoscaler")
        recommender = Pod("VPA Recommender")
        
        with Cluster("Application"):
            deployment = Deploy("Application")
            replicaset = RS("ReplicaSet")
            app_pods = [
                Pod("Pod 1\nCPU: 200m\nMem: 256Mi"),
                Pod("Pod 2\nCPU: 300m\nMem: 512Mi")
            ]
            
            # Show deployment structure
            deployment >> Edge(color="blue") >> replicaset >> Edge(color="blue") >> app_pods
        
        # Show VPA workflow
        metrics >> Edge(color="orange", label="collect") >> recommender
        recommender >> Edge(color="green", label="analyze") >> vpa
        vpa >> Edge(color="red", label="adjust") >> app_pods

# Diagram 3: Advanced Workload Strategy
with Diagram("Advanced Workload Strategy", show=False, direction="LR", filename="ch11_lab05_strategy"):
    
    with Cluster("Workload Management"):
        with Cluster("Resource Controls"):
            hpa = HPA("HorizontalPodAutoscaler")
            vpa_ctrl = CRD("VPA Controller")
            pdb_ctrl = CRD("PDB Controller")
            
            # Show control relationships
            metrics_server = Prometheus("Metrics Server")
            metrics_server >> Edge(color="blue") >> [hpa, vpa_ctrl]
        
        with Cluster("Application Tiers"):
            with Cluster("Critical Workloads"):
                critical = Deploy("Critical Apps")
                critical_pods = [Pod("Critical-1"), Pod("Critical-2")]
                
                # Critical tier management
                critical >> Edge(color="red") >> critical_pods
                pdb_ctrl >> Edge(color="red", style="dashed", label="protect") >> critical_pods
                vpa_ctrl >> Edge(color="orange", label="optimize") >> critical_pods
            
            with Cluster("Standard Workloads"):
                standard = Deploy("Standard Apps")
                standard_pods = [Pod("Standard-1"), Pod("Standard-2")]
                
                # Standard tier management
                standard >> Edge(color="blue") >> standard_pods
                hpa >> Edge(color="green", label="scale") >> standard_pods 