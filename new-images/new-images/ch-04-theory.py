from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy
from diagrams.k8s.network import SVC, NetworkPolicy
from diagrams.k8s.storage import Vol
from diagrams.k8s.infra import Node
from diagrams.k8s.podconfig import Secret, CM
from diagrams.k8s.compute import Cronjob as HPA
from diagrams.onprem.analytics import Spark
from diagrams.onprem.monitoring import Prometheus, Grafana, Datadog
from diagrams.onprem.network import Nginx, Haproxy
from diagrams.programming.framework import Spring

with Diagram("Pod Orchestration Architecture", show=False, direction="TB", filename="ch04_pod_orchestration"):
   
   with Cluster("Node Resources"):
       node = Node("Worker Node")
       
       with Cluster("Resource Allocation"):
           resources = [
               Pod("Guaranteed QoS\nRequests=Limits"),
               Pod("Burstable QoS\nRequests<Limits"),
               Pod("BestEffort QoS\nNo Requests/Limits")
           ]

   with Cluster("Multi-Container Pod Patterns"):
       with Cluster("Sidecar Pattern"):
           main_app = Spring("Main App")
           sidecar = Grafana("Logging Sidecar")
           shared_vol = Vol("Shared Volume")
           
           main_app >> Edge(color="blue") >> shared_vol
           sidecar >> Edge(color="blue", style="dashed") >> shared_vol

       with Cluster("Ambassador Pattern"):
           app = Nginx("Application")
           ambassador = Haproxy("Ambassador Proxy")
           
           app >> Edge(color="red") >> ambassador

       with Cluster("Adapter Pattern"):
           source = Spark("Source App")
           adapter = Prometheus("Format Adapter")
           
           source >> Edge(color="green") >> adapter

   with Cluster("Security Configuration"):
       sec_pod = Pod("Secure Pod")
       net_policy = NetworkPolicy("Network Policy")
       sec_context = Secret("Security Context")
       
       sec_context >> Edge(color="red", style="bold") >> sec_pod
       net_policy >> Edge(color="orange", style="bold") >> sec_pod

   with Cluster("Pod Lifecycle"):
       init_container = Pod("Init Container")
       main_container = Pod("Main Container")
       probe = HPA("Health Probe")
       
       init_container >> Edge(color="blue", style="bold") >> main_container
       probe >> Edge(color="green", style="dashed") >> main_container

   with Cluster("Scheduling Controls"):
       with Cluster("Affinity Rules"):
           node_affinity = Pod("Node Affinity")
           pod_affinity = Pod("Pod Affinity")
           
           node_affinity >> Edge(color="purple") >> node
           pod_affinity >> Edge(color="purple", style="dashed") >> node

       with Cluster("Taints & Tolerations"):
           tolerating_pod = Pod("Tolerating Pod")
           
           tolerating_pod >> Edge(color="brown", style="bold") >> node

   with Cluster("Pod Configuration"):
       config = CM("ConfigMap")
       storage = Vol("Storage Volume")
       
       config >> Edge(color="darkgreen") >> main_container
       storage >> Edge(color="darkgreen") >> main_container

   node >> Edge(color="black", style="dotted") >> resources