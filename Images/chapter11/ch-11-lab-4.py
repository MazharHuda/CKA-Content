from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.storage import PV, PVC, SC
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.infra import Node
from diagrams.generic.storage import Storage
from diagrams.k8s.others import CRD

# Diagram 1: Custom Storage Class Implementation
with Diagram("Custom Storage Class Configuration", show=False, direction="TB", filename="ch11_lab04_storage_class"):
    
    with Cluster("Storage Infrastructure"):
        storage = Storage("GCE SSD\nStorage Backend")
        
        with Cluster("Storage Class Definition"):
            sc = SC("fast-ssd\nProvisioner: gce-pd\nType: pd-ssd")
            params = CRD("Parameters:\n- fstype: ext4\n- replication: none")
            
            # Show configuration
            storage >> Edge(color="blue", label="provides") >> sc
            params >> Edge(color="red", label="configures") >> sc
    
    with Cluster("Storage Consumption"):
        pvc = PVC("Application PVC\nstorageClass: fast-ssd")
        pv = PV("Dynamic PV\nType: SSD")
        pod = Pod("Application Pod")
        
        # Show provisioning flow
        sc >> Edge(color="green", label="provisions") >> pv
        pvc >> Edge(color="orange", label="binds") >> pv
        pod >> Edge(color="blue", label="mounts") >> pvc

# Diagram 2: Volume Snapshot Management
with Diagram("Volume Snapshot Workflow", show=False, direction="TB", filename="ch11_lab04_snapshots"):
    
    with Cluster("Source Volume"):
        source_pv = PV("Source PV")
        source_pvc = PVC("Source PVC")
        source_pod = Pod("Source Pod")
        
        # Show source relationships
        source_pvc >> Edge(color="blue") >> source_pv
        source_pod >> Edge(color="blue") >> source_pvc
    
    with Cluster("Snapshot Operation"):
        snapshot_class = SC("Snapshot Class")
        snapshot = CRD("Volume Snapshot")
        snapshot_content = CRD("Snapshot Content")
        
        # Show snapshot creation
        source_pvc >> Edge(color="red", label="1. Create") >> snapshot
        snapshot >> Edge(color="green", label="2. Reference") >> snapshot_class
        snapshot >> Edge(color="orange", label="3. Generate") >> snapshot_content
    
    with Cluster("Restore Operation"):
        new_pvc = PVC("Restored PVC")
        new_pv = PV("Restored PV")
        new_pod = Pod("Restored Pod")
        
        # Show restore flow
        snapshot >> Edge(color="blue", label="4. Restore") >> new_pvc
        new_pvc >> Edge(color="green", label="5. Provision") >> new_pv
        new_pod >> Edge(color="orange", label="6. Mount") >> new_pvc

# Diagram 3: Advanced Storage Features
with Diagram("Advanced Storage Features", show=False, direction="LR", filename="ch11_lab04_advanced"):
    
    with Cluster("Storage Management"):
        with Cluster("Volume Expansion"):
            pvc_resize = PVC("Resizable PVC")
            storage_expand = Storage("Expanded Storage")
            
            # Show expansion
            pvc_resize >> Edge(color="blue", label="expand") >> storage_expand
        
        with Cluster("Volume Modes"):
            block_vol = PV("Block Volume")
            fs_vol = PV("Filesystem Volume")
            
            # Show different modes
            block_vol >> Edge(color="red", label="raw") >> Pod("Block Pod")
            fs_vol >> Edge(color="green", label="mounted") >> Pod("FS Pod")
        
        with Cluster("Access Modes"):
            rwx_pv = PV("RWX Volume")
            rwo_pv = PV("RWO Volume")
            
            # Show access patterns
            rwx_pv >> Edge(color="orange", label="shared") >> [Pod("Pod 1"), Pod("Pod 2")]
            rwo_pv >> Edge(color="blue", label="exclusive") >> Pod("Single Pod") 