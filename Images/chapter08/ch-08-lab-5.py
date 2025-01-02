from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.podconfig import Secret, CM
from diagrams.k8s.group import NS
from diagrams.k8s.rbac import Role, RoleBinding, User
from diagrams.generic.storage import Storage

# Set diagram attributes
with Diagram("Secret Management Lab", show=False, direction="TB", filename="ch08_lab05_secrets"):
    
    with Cluster("Kubernetes Cluster"):
        # Secret Creation Methods
        with Cluster("Secret Creation"):
            literal_secret = Secret("db-creds\n(from-literal)")
            file_secret = Secret("db-creds-file\n(from-file)")
            yaml_secret = Secret("tls-secret\n(from-yaml)")
            
            # Secret sources
            with Cluster("Source Data"):
                literal_data = Storage("username=admin\npassword=secret")
                files = Storage("credentials.txt\ncert.pem")
                yaml = Storage("secret.yaml")
                
                # Show creation methods
                literal_data >> Edge(color="blue", label="kubectl create") >> literal_secret
                files >> Edge(color="blue", label="kubectl create") >> file_secret
                yaml >> Edge(color="blue", label="kubectl apply") >> yaml_secret
        
        # Secret Usage in Pods
        with Cluster("Secret Usage"):
            with Cluster("Application Pod"):
                app_pod = Pod("secure-app")
                
                # Secret mounting methods
                with Cluster("Mount Methods"):
                    env_vars = Pod("Environment\nVariables")
                    volume_mount = Pod("Volume\nMount")
                    
                    # Show usage methods
                    literal_secret >> Edge(color="green", style="dashed", label="as env") >> env_vars
                    file_secret >> Edge(color="red", style="dashed", label="as volume") >> volume_mount
                    
                    # Connect to pod
                    env_vars >> Edge(color="orange") >> app_pod
                    volume_mount >> Edge(color="orange") >> app_pod
        
        # Access Control
        with Cluster("Access Control"):
            user = User("app-user")
            role = Role("secret-reader")
            binding = RoleBinding("secret-binding")
            
            # Show RBAC for secrets
            user >> Edge(color="purple") >> binding
            binding >> Edge(color="purple") >> role
            role >> Edge(color="purple", style="dotted", label="read") >> [literal_secret, file_secret, yaml_secret]
        
        # Namespace Scope
        with Cluster("Namespace"):
            ns = NS("secure-ns")
            ns - Edge(color="black", style="dotted") - app_pod
            ns - Edge(color="black", style="dotted") - [literal_secret, file_secret, yaml_secret] 