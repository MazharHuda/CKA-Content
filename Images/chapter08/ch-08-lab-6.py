from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.podconfig import CM
from diagrams.k8s.compute import Pod
from diagrams.onprem.monitoring import Grafana
from diagrams.generic.storage import Storage
from diagrams.programming.flowchart import Document

# Set diagram attributes
with Diagram("Audit Logging Lab", show=False, direction="LR", filename="ch08_lab06_audit"):
    
    with Cluster("Kubernetes Cluster"):
        # API Server Configuration
        with Cluster("API Server Setup"):
            api = APIServer("kube-apiserver")
            policy = CM("audit-policy\n(Policy Configuration)")
            
            # Audit backends
            with Cluster("Audit Backends"):
                log_file = Storage("audit.log\n(Log Backend)")
                webhook = Pod("webhook-backend\n(Remote Logger)")
                
                # Show backend configurations
                api >> Edge(color="blue", style="bold", label="write") >> log_file
                api >> Edge(color="blue", style="bold", label="send") >> webhook
        
        # Audit Policy Rules
        with Cluster("Audit Policy Rules"):
            rules = [
                Document("Metadata Level\n(auth/authn)"),
                Document("Request Level\n(pod operations)"),
                Document("RequestResponse\n(configmaps/secrets)"),
                Document("None Level\n(health checks)")
            ]
            
            # Show policy application
            policy >> Edge(color="red", label="defines") >> rules
            rules >> Edge(color="red", style="dashed", label="applied to") >> api
        
        # Log Analysis
        with Cluster("Audit Analysis"):
            dashboard = Grafana("Audit Dashboard")
            
            with Cluster("Event Categories"):
                events = [
                    Document("Create Events"),
                    Document("Update Events"),
                    Document("Delete Events"),
                    Document("Auth Failures")
                ]
                
                # Show analysis flow
                log_file >> Edge(color="green", style="dotted", label="analyze") >> dashboard
                webhook >> Edge(color="green", style="dotted", label="analyze") >> dashboard
                dashboard >> Edge(color="orange", label="categorize") >> events
        
        # Policy Verification
        with Cluster("Verification"):
            verify = [
                Pod("Policy Validation"),
                Pod("Log Verification"),
                Pod("Event Analysis")
            ]
            
            # Show verification steps
            dashboard >> Edge(color="purple", style="bold", label="verify") >> verify 