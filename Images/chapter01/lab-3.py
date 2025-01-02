from diagrams import Diagram, Cluster
from diagrams.k8s.clusterconfig import Quota
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.group import NS
from diagrams.k8s.podconfig import Limits
from diagrams.k8s.rbac import Role, RoleBinding, User

# Set diagram attributes
with Diagram("Namespace and Resource Management Lab", show=False, direction="TB", filename="chapter01_lab03"):
    # Create main cluster
    with Cluster("Kubernetes Cluster"):
        # Development Namespace
        with Cluster("Development Namespace"):
            dev_ns = NS("dev")
            dev_quota = Quota("dev-quota")
            dev_limits = Limits("dev-limits")
            dev_pods = [Pod("dev-pod-1"),
                       Pod("dev-pod-2")]
            
            # Development namespace flow
            dev_ns >> dev_quota >> dev_pods
            dev_ns >> dev_limits >> dev_pods

        # Production Namespace
        with Cluster("Production Namespace"):
            prod_ns = NS("prod")
            prod_quota = Quota("prod-quota")
            prod_limits = Limits("prod-limits")
            prod_deploy = Deploy("prod-app")
            
            # Production namespace flow
            prod_ns >> prod_quota >> prod_deploy
            prod_ns >> prod_limits >> prod_deploy

        # RBAC Configuration
        with Cluster("RBAC"):
            dev_role = Role("dev-role")
            dev_binding = RoleBinding("dev-binding")
            dev_user = User("developer")
            
            # RBAC flow
            dev_user >> dev_binding >> dev_role
            dev_role >> dev_ns