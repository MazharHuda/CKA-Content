from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.storage import Vol
from diagrams.k8s.podconfig import Secret
from diagrams.k8s.group import NS

# Set diagram attributes
with Diagram("Pod Security Context Lab", show=False, direction="TB", filename="ch08_lab03_security_context"):
    
    # Create main cluster
    with Cluster("Kubernetes Cluster"):
        # Pod Security Context
        with Cluster("Pod with Security Context"):
            # Pod level security context
            with Cluster("Pod Security Settings"):
                pod = Pod("security-context-demo")
                
                with Cluster("Pod Level Context"):
                    pod_security = [
                        Pod("runAsUser: 1000"),
                        Pod("runAsGroup: 3000"),
                        Pod("fsGroup: 2000")
                    ]
                    
                    # Show pod level security settings
                    pod >> Edge(color="blue", style="bold", label="Pod Security") >> pod_security
            
            # Container level security context
            with Cluster("Container Security Settings"):
                container = Pod("sec-ctx-demo\n(busybox container)")
                
                with Cluster("Container Level Context"):
                    container_security = [
                        Pod("allowPrivilegeEscalation: false"),
                        Pod("capabilities: drop [ALL]")
                    ]
                    
                    # Show container level security settings
                    container >> Edge(color="red", style="bold", label="Container Security") >> container_security
            
            # Volume mount with security context
            with Cluster("Volume Security"):
                volume = Vol("sec-storage\n(emptyDir)")
                
                # Show volume relationships
                volume >> Edge(color="green", style="dashed", label="Mounted with fsGroup") >> pod
                volume >> Edge(color="green", style="dashed", label="ReadOnly Mount") >> container
            
            # Security verification
            with Cluster("Security Verification"):
                verify = [
                    Pod("id command\n(UID/GID check)"),
                    Pod("ls -l /data\n(Permission check)")
                ]
                
                # Show verification steps
                container >> Edge(color="orange", style="dotted", label="Verify") >> verify

    # Show container to pod relationship
    pod >> Edge(color="purple", style="bold", label="Contains") >> container 