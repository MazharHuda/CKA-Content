from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.controlplane import APIServer, ControllerManager, Scheduler 
from diagrams.k8s.compute import Pod, Deploy, RS
from diagrams.k8s.network import SVC, Ingress
from diagrams.k8s.storage import PV, PVC
from diagrams.k8s.infra import Node
from diagrams.k8s.podconfig import CM, Secret
from diagrams.k8s.rbac import RB, Role, SA
from diagrams.k8s.others import CRD
from diagrams.generic.network import Firewall
from diagrams.onprem.network import Internet
from diagrams.k8s.clusterconfig import HPA as Etcd

with Diagram("Kubernetes Core Architecture", show=False, direction="TB", filename="ch02_core_architecture"):
   # Internet/External Access
   inet = Internet("External Traffic")
   
   # Control Plane Components
   with Cluster("Control Plane"):
       api = APIServer("kube-apiserver")
       etcd = Etcd("etcd") 
       ctrl_mgr = ControllerManager("controller-manager")
       sched = Scheduler("scheduler")
       metrics = CRD("metrics-server")
       
       api >> Edge(color="darkgreen", style="bold") >> etcd
       api >> Edge(color="blue") >> ctrl_mgr
       api >> Edge(color="red") >> sched
       metrics >> Edge(color="purple") >> api

   # Network Layer  
   with Cluster("Network Layer"):
       ingress = Ingress("ingress-controller")
       netpol = Firewall("network-policy")
       
       inet >> Edge(color="blue") >> ingress
   
   # Worker Node Components
   with Cluster("Worker Nodes"):
       with Cluster("Node 1"):
           node1 = Node("worker-1")
           pods1 = [Pod("pod-1"),
                   Pod("pod-2")]
           
       with Cluster("Node 2"):
           node2 = Node("worker-2") 
           pods2 = [Pod("pod-3"),
                   Pod("pod-4")]
           
       netpol >> Edge(color="red", style="dotted") >> pods1
       netpol >> Edge(color="red", style="dotted") >> pods2

   # Workload Management
   with Cluster("Workload Controllers"):
       deploy = Deploy("deployment")
       rs = RS("replicaset")
       svc = SVC("service")
       hpa = Deploy("hpa")
       
       deploy >> Edge(color="blue") >> rs
       rs >> Edge(color="blue") >> pods1
       rs >> Edge(color="blue") >> pods2
       svc >> Edge(color="red", style="dashed") >> pods1
       svc >> Edge(color="red", style="dashed") >> pods2
       hpa >> Edge(color="green") >> deploy
       metrics >> Edge(color="purple", style="dotted") >> hpa
       ingress >> Edge(color="blue") >> svc

   # Storage and Configuration
   with Cluster("Storage & Config"):
       pv = PV("persistent-volume")
       pvc = PVC("volume-claim")
       config = CM("configmap")
       secret = Secret("secrets")
       
       pvc >> Edge(color="brown") >> pv
       config >> Edge(color="green", style="dotted") >> pods1
       secret >> Edge(color="red", style="dotted") >> pods1

   # Security and RBAC
   with Cluster("Security & RBAC"):
       role = Role("role")
       rb = RB("role-binding")
       sa = SA("service-account")
       
       sa >> Edge(color="orange") >> rb
       rb >> Edge(color="orange") >> role
       role >> Edge(color="orange", style="dashed") >> api

   # API Server relationships
   api >> Edge(color="black", style="bold") >> node1
   api >> Edge(color="black", style="bold") >> node2
   node1 >> Edge(color="darkblue", style="dashed", label="reports status") >> api
   node2 >> Edge(color="darkblue", style="dashed", label="reports status") >> api