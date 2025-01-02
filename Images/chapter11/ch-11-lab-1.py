from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.others import CRD
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.storage import PV
from diagrams.onprem.client import Client
from diagrams.k8s.rbac import User

# Diagram 1: CRD Creation Flow
with Diagram("CRD Creation Process", show=False, direction="TB", filename="ch11_lab01_crd_creation"):
    
    with Cluster("CRD Definition"):
        # CRD components
        crd_def = CRD("Backup CRD\nDefinition")
        api = APIServer("API Server")
        schema = CRD("OpenAPI Schema")
        
        # Show CRD registration
        crd_def >> Edge(color="blue", label="1. Register") >> api
        schema >> Edge(color="red", label="2. Validate") >> crd_def

    with Cluster("Custom Resource"):
        # CR components
        backup_cr = CRD("Backup CR\nInstance")
        validation = CRD("Schema\nValidation")
        storage = PV("Backup\nStorage")
        
        # Show CR creation flow
        api >> Edge(color="green", label="3. Enable") >> backup_cr
        backup_cr >> Edge(color="orange", label="4. Validate") >> validation
        backup_cr >> Edge(color="blue", label="5. Configure") >> storage

# Diagram 2: CRD Controller Flow
with Diagram("CRD Controller Operation", show=False, direction="TB", filename="ch11_lab01_controller"):
    
    with Cluster("Controller Components"):
        controller = Deploy("Backup Controller")
        watcher = Pod("Resource Watcher")
        reconciler = Pod("Reconciliation Loop")
        
        # Show controller operation
        controller >> Edge(color="red", label="1. Watch") >> watcher
        watcher >> Edge(color="blue", label="2. Detect") >> reconciler
    
    with Cluster("Resource Management"):
        cr_instance = CRD("Backup Resource")
        status = CRD("Status Update")
        backup_job = Pod("Backup Job")
        
        # Show reconciliation
        reconciler >> Edge(color="green", label="3. Process") >> cr_instance
        cr_instance >> Edge(color="orange", label="4. Create") >> backup_job
        backup_job >> Edge(color="blue", label="5. Update") >> status

# Diagram 3: CRD Interaction Model
with Diagram("CRD Interaction Model", show=False, direction="LR", filename="ch11_lab01_interaction"):
    
    with Cluster("User Interaction"):
        user = User("Cluster Admin")
        client = Client("kubectl")
        
        # User tools
        user >> Edge(color="blue", label="create/update") >> client
    
    with Cluster("API Layer"):
        api_server = APIServer("API Server")
        validation_webhook = Pod("Validation\nWebhook")
        
        # API handling
        client >> Edge(color="green", label="1. Request") >> api_server
        api_server >> Edge(color="red", label="2. Validate") >> validation_webhook
    
    with Cluster("Resource Handling"):
        custom_resource = CRD("Custom Resource")
        controller_pod = Pod("Controller")
        storage_backend = PV("Storage")
        
        # Resource flow
        api_server >> Edge(color="orange", label="3. Store") >> custom_resource
        controller_pod >> Edge(color="blue", label="4. Watch") >> custom_resource
        controller_pod >> Edge(color="green", label="5. Manage") >> storage_backend 