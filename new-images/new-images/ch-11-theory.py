from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.controlplane import API, Scheduler
from diagrams.k8s.network import SVC, NetworkPolicy
from diagrams.k8s.rbac import Role, RB, CRole
from diagrams.k8s.infra import Node
from diagrams.k8s.others import CRD
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.network import Istio
from diagrams.programming.framework import Flask
from diagrams.programming.language import Python

# Set diagram attributes
with Diagram("Advanced Kubernetes Concepts", show=False, direction="TB", filename="ch11_advanced_concepts"):
    
    # API Server and Extensions
    with Cluster("API Extension Layer"):
        api = API("API Server")
        
        with Cluster("Custom Resources"):
            crd = CRD("CRD")
            controller = Python("Custom\nController")
            custom_objects = [
                Pod("Custom\nObject 1"),
                Pod("Custom\nObject 2")
            ]
            
            # CRD relationships
            crd >> Edge(color="red") >> controller
            controller >> Edge(color="red") >> custom_objects
    
    # Advanced Scheduling
    with Cluster("Advanced Scheduling"):
        scheduler = Scheduler("Scheduler")
        
        with Cluster("Node Topology"):
            nodes = [
                Node("Zone A\nNode 1"),
                Node("Zone A\nNode 2"),
                Node("Zone B\nNode 1"),
                Node("Zone B\nNode 2")
            ]
            
            # Topology relationships
            scheduler >> Edge(color="blue") >> nodes
    
    # Service Mesh
    with Cluster("Service Mesh"):
        mesh = Istio("Service\nMesh")
        
        with Cluster("Mesh Services"):
            services = [
                SVC("Service 1"),
                SVC("Service 2"),
                SVC("Service 3")
            ]
            
            # Service mesh relationships
            mesh >> Edge(color="green") >> services
    
    # Advanced Security
    with Cluster("Security Controls"):
        with Cluster("RBAC"):
            roles = [
                Role("Role"),
                CRole("ClusterRole")
            ]
            bindings = [
                RB("RoleBinding"),
                RB("ClusterRoleBinding")
            ]
        
        with Cluster("Network Security"):
            netpol = NetworkPolicy("Network\nPolicy")
            secpol = NetworkPolicy("Security\nPolicy")
    
    # Advanced Workloads
    with Cluster("Advanced Workloads"):
        with Cluster("Applications"):
            apps = [Flask("App 1"), Flask("App 2")]
            
        with Cluster("Autoscaling"):
            vpa = Deploy("Vertical\nPod Autoscaler")
            pdb = Deploy("Pod Disruption\nBudget")
            
            # Autoscaling relationships
            vpa >> Edge(color="brown") >> apps
    
    # Monitoring
    with Cluster("Advanced Monitoring"):
        prometheus = Prometheus("Prometheus")
        grafana = Grafana("Grafana")
        metrics = [
            Pod("Custom\nMetrics"),
            Pod("Standard\nMetrics")
        ]
        
        # Monitoring relationships
        metrics >> Edge(color="orange") >> prometheus
        prometheus >> Edge(color="orange") >> grafana
    
    # System Relationships
    api >> Edge(color="black", style="bold") >> [crd, scheduler, mesh]
    netpol >> Edge(color="red", style="dashed") >> apps
    roles >> Edge(color="purple") >> bindings
    bindings >> Edge(color="purple", style="dashed") >> apps
    
    # Monitoring Coverage
    prometheus >> Edge(color="orange", style="dotted") >> [apps, services, nodes]