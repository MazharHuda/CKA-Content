from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.rbac import Role, RoleBinding, User, Group
from diagrams.k8s.compute import Pod
from diagrams.k8s.group import NS
from diagrams.k8s.controlplane import APIServer

# Set diagram attributes
with Diagram("RBAC Configuration Lab", show=False, direction="TB", filename="ch08_lab02_rbac"):
    
    # API Server as the central authority
    with Cluster("Kubernetes Control Plane"):
        api = APIServer("kube-apiserver")
    
    # Development Namespace
    with Cluster("Development Namespace"):
        ns = NS("development")
        
        # RBAC Components
        with Cluster("RBAC Configuration"):
            role = Role("pod-manager\n[pods, pods/log]")
            binding = RoleBinding("pod-manager-binding")
            user = User("john")
            
            # Define allowed actions
            with Cluster("Allowed Actions"):
                actions = [
                    Pod("get"),
                    Pod("list"),
                    Pod("watch"),
                    Pod("create"),
                    Pod("update"),
                    Pod("delete")
                ]
            
            # Show RBAC relationships
            user >> Edge(color="blue", label="bound to") >> binding
            binding >> Edge(color="green", label="references") >> role
            role >> Edge(color="orange", label="allows") >> actions
    
    # Authorization Flow
    with Cluster("Authorization Process"):
        auth_check = Pod("Authorization Check")
        api >> Edge(color="red", style="dashed", label="1. Verify") >> auth_check
        auth_check >> Edge(color="red", style="dashed", label="2. Check") >> role
        
    # Namespace Scope
    ns - Edge(color="black", style="dotted", label="scoped to") - role

    # API Server Authorization
    api >> Edge(color="darkgreen", style="bold", label="3. Enforce") >> ns 