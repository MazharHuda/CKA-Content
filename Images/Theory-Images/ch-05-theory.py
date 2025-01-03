from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy, RS, StatefulSet
from diagrams.k8s.network import SVC, Ingress, NetworkPolicy
from diagrams.k8s.podconfig import CM, Secret
from diagrams.k8s.infra import Node, ETCD
from diagrams.k8s.clusterconfig import HPA
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.network import Internet, Istio
from diagrams.onprem.database import MySQL
from diagrams.programming.framework import Spring

with Diagram("Enhanced Application Lifecycle Management", show=False, direction="TB"):
   
   # External Access Layer
   users = Internet("Users")
   ingress = Ingress("Global Ingress")
   
   with Cluster("Service Mesh Layer"):
       mesh = Istio("Service Mesh")
       global_lb = SVC("Global Load Balancer")
       
   with Cluster("Multi-Cluster Deployment"):
       with Cluster("Cluster A (Active)"):
           # Deployment Strategies
           with Cluster("Advanced Deployments"):
               # A/B Testing
               with Cluster("A/B Testing"):
                   ab_svc = SVC("A/B Router")
                   version_a = Pod("Version A")
                   version_b = Pod("Version B")
               
               # Feature Flags
               with Cluster("Feature Flags"):
                   ff_config = CM("Feature Flags")
                   ff_pod = Pod("Feature Enabled App")
               
               # Canary
               with Cluster("Canary"):
                   canary_svc = SVC("Traffic Split")
                   prod = Pod("Production (90%)")
                   canary = Pod("Canary (10%)")
               
               # Blue/Green
               with Cluster("Blue/Green"):
                   bg_svc = SVC("B/G Switch")
                   blue = Pod("Blue")
                   green = Pod("Green")
           
           # Configuration & Health
           with Cluster("Platform Services"):
               config = CM("ConfigMap")
               secret = Secret("Secrets")
               health = SVC("Health Monitor")
               
               probes = [
                   Pod("Liveness"),
                   Pod("Readiness"), 
                   Pod("Startup")
               ]
           
           # Data Layer A
           with Cluster("Data Layer Primary"):
               db_primary = StatefulSet("Primary DB")
               backup = Pod("Backup")

       with Cluster("Cluster B (Passive)"):
           with Cluster("Failover Components"):
               passive_svc = SVC("Passive Service")
               passive_pods = [Pod("Standby Pod")]
               
           # Data Layer B    
           with Cluster("Data Layer Secondary"):
               db_replica = StatefulSet("Replica DB")
               recovery = Pod("Recovery")
   
   with Cluster("Observability"):
       metrics = Prometheus("Metrics")
       monitoring = Grafana("Monitoring")
       
       with Cluster("Auto Scaling"):
           hpa = HPA("HPA")
           scaled_deploy = Deploy("Scaled Apps")
           replicas = [Pod("Pod 1"), Pod("Pod 2"), Pod("Pod 3")]

   # Traffic Flow
   users >> ingress >> mesh >> global_lb
   
   # Service Mesh Routing
   global_lb >> ab_svc >> [version_a, version_b]
   global_lb >> canary_svc >> [prod, canary] 
   global_lb >> bg_svc >> [blue, green]
   
   # Data Replication
   db_primary >> Edge(color="red") >> db_replica
   
   # Configuration Flow
   config >> Edge(color="blue") >> ff_pod
   ff_config >> Edge(color="blue") >> ff_pod
   
   # Monitoring
   metrics >> monitoring
   metrics >> hpa >> scaled_deploy >> replicas
   
   # Health Checks
   health >> Edge(color="green") >> probes