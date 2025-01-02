from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.podconfig import CM, Secret
from diagrams.k8s.group import NS
from diagrams.k8s.rbac import Role, RoleBinding, User
from diagrams.onprem.vcs import Git
from diagrams.onprem.ci import Jenkins

# Diagram 1: ConfigMap Management
with Diagram("ConfigMap Management Strategy", show=False, direction="TB", filename="ch05_lab02_configmap"):
    
    with Cluster("Configuration Management"):
        # Version Control
        git = Git("Config Repository")
        ci = Jenkins("CI/CD Pipeline")
        
        # Environment Specific Configs
        with Cluster("Environment Configurations"):
            dev_cm = CM("dev-config")
            stage_cm = CM("stage-config")
            prod_cm = CM("prod-config")
            
            # Show config flow
            git >> Edge(color="blue", label="pull") >> ci
            ci >> Edge(color="green", label="apply") >> [dev_cm, stage_cm, prod_cm]
        
        # Application Deployments
        with Cluster("Application Deployments"):
            dev_deploy = Deploy("dev-app")
            stage_deploy = Deploy("stage-app")
            prod_deploy = Deploy("prod-app")
            
            # Connect configs to deployments
            dev_cm >> Edge(color="red", style="dotted") >> dev_deploy
            stage_cm >> Edge(color="red", style="dotted") >> stage_deploy
            prod_cm >> Edge(color="red", style="dotted") >> prod_deploy

# Diagram 2: Secret Management
with Diagram("Secret Management Strategy", show=False, direction="LR", filename="ch05_lab02_secrets"):
    
    with Cluster("Secret Management"):
        # RBAC Controls
        with Cluster("Access Control"):
            admin = User("admin")
            dev = User("developer")
            
            admin_role = Role("secret-admin")
            dev_role = Role("secret-reader")
            
            admin_binding = RoleBinding("admin-binding")
            dev_binding = RoleBinding("dev-binding")
            
            # Show RBAC relationships
            admin >> admin_binding >> admin_role
            dev >> dev_binding >> dev_role
        
        # Secrets by Environment
        with Cluster("Secure Configurations"):
            with Cluster("Development"):
                dev_secret = Secret("dev-secrets")
                dev_ns = NS("dev")
                
            with Cluster("Production"):
                prod_secret = Secret("prod-secrets")
                prod_ns = NS("prod")
            
            # Access control flows
            admin_role >> Edge(color="red", style="bold") >> [dev_secret, prod_secret]
            dev_role >> Edge(color="blue", style="dotted") >> dev_secret
            
            # Namespace associations
            dev_ns - Edge(color="black", style="dashed") - dev_secret
            prod_ns - Edge(color="black", style="dashed") - prod_secret

# Diagram 3: Configuration Update Flow
with Diagram("Configuration Update Process", show=False, direction="TB", filename="ch05_lab02_update_flow"):
    
    with Cluster("Configuration Update Workflow"):
        # Update Sources
        git_config = Git("Config Repository")
        ci_pipeline = Jenkins("CI Pipeline")
        
        with Cluster("Validation & Deployment"):
            # Validation steps
            config_test = Pod("config-test")
            validate = Pod("validation-job")
            
            # Application update
            deploy = Deploy("application")
            pods = [Pod("pod-1"),
                   Pod("pod-2"),
                   Pod("pod-3")]
            
            # Configuration objects
            new_config = CM("new-config")
            new_secret = Secret("new-secrets")
            
            # Show update flow
            git_config >> Edge(color="blue") >> ci_pipeline
            ci_pipeline >> Edge(color="green") >> config_test
            config_test >> Edge(color="green") >> validate
            validate >> Edge(color="green") >> [new_config, new_secret]
            
            # Application update flow
            deploy >> pods
            new_config >> Edge(color="red", style="dotted") >> pods
            new_secret >> Edge(color="red", style="dotted") >> pods 