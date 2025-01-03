from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.rbac import Role, RoleBinding, ServiceAccount, Group
from diagrams.k8s.infra import Master, Node
from diagrams.k8s.network import NetworkPolicy
from diagrams.k8s.podconfig import Secret, ConfigMap
from diagrams.k8s.controlplane import ControllerManager
from diagrams.onprem.security import Vault
from diagrams.onprem.network import Internet
from diagrams.generic.storage import Storage
from diagrams.generic.os import Windows

with Diagram("Kubernetes Security Architecture", show=False, direction="TB"):
    # External Access
    with Cluster("External Access"):
        users = Internet("Users/Services")
    
    # Authentication Layer
    with Cluster("Authentication"):
        auth_methods = [
            Group("X.509\nCertificates"),
            ServiceAccount("Service\nAccounts"),
            Group("OIDC")
        ]
    
    # API Server Security
    with Cluster("API Server Security"):
        api = Master("API Server")
        admission = ControllerManager("Admission\nControllers")
        audit = Storage("Audit Logs")
        etcd = Storage("etcd\n(Encrypted)")
        
        api >> admission
        api >> audit
        api >> etcd
    
    # Authorization Layer
    with Cluster("RBAC"):
        roles = [Role("Role"), Role("ClusterRole")]
        bindings = [RoleBinding("RoleBinding"), RoleBinding("ClusterRoleBinding")]
        
        roles[0] >> bindings[0]
        roles[1] >> bindings[1]
    
    # Pod Security
    with Cluster("Pod Security"):
        sec_context = ConfigMap("Security\nContext")
        pod_security = ConfigMap("Pod Security\nStandards")
        
        with Cluster("Workload"):
            app1 = Pod("App 1")
            app2 = Pod("App 2")
            
            sec_context >> app1
            sec_context >> app2
            pod_security >> app1
            pod_security >> app2
    
    # Network Security
    with Cluster("Network Security"):
        netpol = NetworkPolicy("Network\nPolicies")
        
        with Cluster("Pod Communication"):
            pod1 = Pod("Pod 1")
            pod2 = Pod("Pod 2")
            netpol >> pod1
            netpol >> pod2
    
    # Secret Management
    with Cluster("Secret Management"):
        k8s_secrets = Secret("K8s Secrets")
        ext_secrets = Vault("External\nSecrets")
        
        with Cluster("Secret Consumers"):
            secret_user1 = Pod("Secret\nConsumer 1")
            secret_user2 = Pod("Secret\nConsumer 2")
            
            k8s_secrets >> secret_user1
            k8s_secrets >> secret_user2
            ext_secrets >> secret_user1
            ext_secrets >> secret_user2
    
    # Node Security
    with Cluster("Node Security"):
        node = Node("Worker Node")
        node_auth = ServiceAccount("Node\nAuthorizer")
        runtime = ConfigMap("Runtime\nSecurity")
        
        node >> node_auth
        node_auth >> api
        runtime >> node
    
    # Flow Connections
    users >> auth_methods[0]
    users >> auth_methods[1]
    users >> auth_methods[2]
    
    for auth in auth_methods:
        auth >> api
    
    api >> bindings[0]
    api >> bindings[1]
    
    # Policy Enforcement
    with Cluster("Policy Enforcement"):
        policy = ConfigMap("Security\nPolicies")
        scanner = Windows("Security\nScanner")
        
        policy >> app1
        policy >> app2
        policy >> pod1
        policy >> pod2
        policy >> node
        
        scanner >> app1
        scanner >> app2
        scanner >> pod1
        scanner >> pod2