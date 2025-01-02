from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.others import CRD
from diagrams.generic.storage import Storage
from diagrams.k8s.rbac import User, Group
from diagrams.k8s.infra import Master
from diagrams.onprem.client import Client

# Diagram 1: Certificate Management Flow
with Diagram("Certificate Management Process", show=False, direction="TB", filename="ch10_lab04_cert_management"):
    
    with Cluster("Certificate Infrastructure"):
        # Control plane certificates
        with Cluster("Control Plane Certificates"):
            api = APIServer("API Server")
            ca_cert = Storage("CA Certificate")
            server_cert = Storage("Server Certificates")
            client_cert = Storage("Client Certificates")
            
            # Show certificate relationships
            ca_cert >> Edge(color="red", label="signs") >> [server_cert, client_cert]
            server_cert >> Edge(color="blue", label="secures") >> api

    with Cluster("Certificate Operations"):
        # Certificate checking
        check = Client("Certificate Check")
        expiry = Storage("Expiration Status")
        renewal = Storage("Renewal Process")
        
        # Show operations flow
        check >> Edge(color="orange", label="1. Check") >> expiry
        expiry >> Edge(color="orange", label="2. Evaluate") >> renewal
        renewal >> Edge(color="green", label="3. Update") >> [server_cert, client_cert]

# Diagram 2: Certificate Signing Request Flow
with Diagram("CSR Process Flow", show=False, direction="TB", filename="ch10_lab04_csr_flow"):
    
    with Cluster("CSR Generation"):
        user = User("New User")
        key = Storage("Private Key")
        csr = CRD("Certificate\nSigning Request")
        
        # Show CSR creation
        user >> Edge(color="blue", label="1. Generate") >> key
        user >> Edge(color="blue", label="2. Create") >> csr

    with Cluster("CSR Processing"):
        api_server = APIServer("API Server")
        admin = User("Cluster Admin")
        signed_cert = Storage("Signed Certificate")
        
        # Show approval flow
        csr >> Edge(color="green", label="3. Submit") >> api_server
        admin >> Edge(color="red", label="4. Approve") >> api_server
        api_server >> Edge(color="green", label="5. Issue") >> signed_cert

# Diagram 3: Certificate Rotation Strategy
with Diagram("Certificate Rotation Strategy", show=False, direction="LR", filename="ch10_lab04_cert_rotation"):
    
    with Cluster("Certificate Lifecycle"):
        master = Master("Control Plane")
        
        with Cluster("Certificate States"):
            current = Storage("Active Certificates")
            new = Storage("New Certificates")
            backup = Storage("Backup Certificates")
        
        # Show rotation process
        current >> Edge(color="orange", label="1. Backup") >> backup
        master >> Edge(color="blue", label="2. Generate") >> new
        new >> Edge(color="green", label="3. Replace") >> current
        
        # Show verification
        verify = Client("Verification")
        current >> Edge(color="red", style="dotted", label="4. Verify") >> verify 