#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.infra import Master, Node
from diagrams.k8s.controlplane import API, Scheduler, ControllerManager
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.storage import PV
from diagrams.onprem.database import MongoDB  # For etcd representation
from diagrams.generic.storage import Storage
from diagrams.generic.network import Router
from diagrams.onprem.certificates import CertManager
from diagrams.onprem.monitoring import Grafana, Prometheus

# Enhanced graph attributes for better visualization
graph_attr = {
    "splines": "spline",
    "pad": "0.75",
    "nodesep": "1.2",
    "ranksep": "1.2",
    "fontsize": "45",
    "fontname": "sans-serif"
}

# Node attribute defaults
node_attr = {
    "fontsize": "14",
    "fontname": "sans-serif"
}

# Edge attribute defaults
edge_attr = {
    "fontsize": "12",
    "fontname": "sans-serif"
}

def create_k8s_maintenance_diagram():
    """Creates a comprehensive Kubernetes maintenance architecture diagram."""
    
    with Diagram(
        "Kubernetes Maintenance Architecture",
        show=False,
        direction="TB",
        filename="k8s_maintenance",
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr
    ):
        # External Load Balancer with HA Configuration
        lb = Router("External Load Balancer (HA)\nActive-Active Configuration")
        
        # Control Plane Components
        with Cluster("Control Plane - N+1 Rolling Upgrade Strategy"):
            # API Servers with version information
            api_servers = [
                API("API Server v1.26\n(Production)"),
                API("API Server v1.27\n(Canary)")
            ]
            
            # Core Components
            scheduler = Scheduler("kube-scheduler\nLeader Election Enabled")
            controller = ControllerManager("kube-controller-manager\nHA Mode")
            
            # etcd Cluster with HA Configuration
            with Cluster("etcd Cluster - Raft Consensus Protocol"):
                etcd_nodes = [
                    MongoDB("etcd-1 (Leader)\nQuorum Member"),
                    MongoDB("etcd-2 (Follower)\nQuorum Member"),
                    MongoDB("etcd-3 (Follower)\nQuorum Member")
                ]
                
                # etcd mesh topology
                for i in range(len(etcd_nodes)):
                    for j in range(i + 1, len(etcd_nodes)):
                        etcd_nodes[i] - Edge(
                            color="darkred",
                            style="solid",
                            label="Raft Protocol"
                        ) - etcd_nodes[j]
        
        # Certificate Management
        with Cluster("Certificate Lifecycle - cert-manager"):
            cert_manager = CertManager("cert-manager\nAutomatic Renewal")
            certs = [
                Storage("API Server Certs\n1 Year Validity"),
                Storage("Kubelet Certs\n1 Year Validity"),
                Storage("Client Certs\n1 Year Validity"),
                Storage("SA Keys\n90 Days Rotation")
            ]
            
            for cert in certs:
                cert_manager >> Edge(color="red", label="manages") >> cert
        
        # Observability Stack
        with Cluster("Observability Stack - HA Configuration"):
            prometheus = Prometheus("Prometheus\nHA Pair")
            grafana = Grafana("Grafana\nClustered")
            alerts = Pod("Alert Manager\nHA Mode")
            
            prometheus >> Edge(color="orange", label="metrics") >> grafana
            prometheus >> Edge(color="orange", label="alerts") >> alerts
        
        # Node Management
        with Cluster("Node Fleet Management - Kubernetes States"):
            nodes = [
                Node("Node 1\nReady"),
                Node("Node 2\nSchedulingDisabled"),
                Node("Node 3\nDraining"),
                Node("Node 4\nMaintenance")
            ]
            
            # Node Components
            with Cluster("Node-level Components"):
                kubelet = Pod("kubelet\nSelf-healing")
                runtime = Pod("Container Runtime\nContainerd")
                proxy = Pod("kube-proxy\nIPVS Mode")
                
                kubelet >> Edge(color="black", label="manages") >> runtime
                kubelet >> Edge(color="black", label="configures") >> proxy
        
        # Backup Systems
        with Cluster("Backup & Recovery - 3-2-1 Strategy"):
            backup_systems = [
                Storage("etcd Snapshots\nEncrypted"),
                Storage("Resource Backups\nVersioned"),
                Storage("Cert Backups\nSecure")
            ]
            restore = Pod("Recovery\nProcedures")
            
            for backup in backup_systems:
                backup >> Edge(
                    color="darkblue",
                    style="dashed",
                    label="periodic"
                ) >> restore
        
        # System Relationships
        lb >> Edge(color="black", style="bold", label="load balance") >> api_servers
        
        # Control plane connections
        for api in api_servers:
            api >> Edge(color="blue", label="coordinate") >> scheduler
            api >> Edge(color="blue", label="manage") >> controller
            api >> Edge(color="brown", label="store") >> etcd_nodes[0]
        
        # Node management
        for node in nodes:
            api_servers[0] >> Edge(color="green", label="control") >> node
        
        # Monitoring connections
        prometheus >> Edge(color="orange", style="dotted") >> nodes
        prometheus >> Edge(color="orange", style="dotted") >> api_servers
        prometheus >> Edge(color="orange", style="dotted") >> etcd_nodes

if __name__ == "__main__":
    create_k8s_maintenance_diagram()