from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.rbac import User
from diagrams.generic.storage import Storage
from diagrams.programming.language import Python
from diagrams.onprem.client import Client

# Set diagram attributes
with Diagram("Certificate Management and TLS Lab", show=False, direction="LR", filename="ch08_lab01_certificates"):
    
    # Create main components
    with Cluster("Certificate Management Process"):
        # User/Client components
        with Cluster("Client Side"):
            user = User("john")
            key = Storage("john.key\n(Private Key)")
            csr = Storage("john.csr\n(Certificate\nSigning Request)")
            cert = Storage("john.crt\n(Signed\nCertificate)")
            
            # Show key and CSR generation flow
            user >> Edge(label="1. Generate") >> key
            key >> Edge(label="2. Create CSR") >> csr
        
        # Kubernetes API Server components
        with Cluster("Kubernetes Cluster"):
            api = APIServer("kube-apiserver")
            
            with Cluster("Certificate Processing"):
                csr_obj = Storage("CSR Object")
                approved_csr = Storage("Approved CSR")
                
                # Show CSR approval flow
                csr_obj >> Edge(label="4. Approve") >> approved_csr
        
        # Show complete certificate flow
        csr >> Edge(label="3. Submit") >> csr_obj
        approved_csr >> Edge(label="5. Download") >> cert
        
        # Final verification
        verify = Client("Certificate\nVerification")
        cert >> Edge(label="6. Verify") >> verify 