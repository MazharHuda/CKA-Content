from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.infra import Node
from diagrams.k8s.controlplane import Scheduler

with Diagram("Pod Scheduling and Placement", show=False, direction="TB", filename="ch04_lab02_pod_scheduling"):
    
    scheduler = Scheduler("kube-scheduler")
    
    # Node Selection
    with Cluster("Node Selection"):
        # Nodes with labels
        worker1 = Node("worker1\ndisk=ssd")
        worker2 = Node("worker2\ndisk=hdd")
        
        # Pod with nodeSelector
        pod_ssd = Pod("nginx-ssd\nnodeSelector:\ndisk=ssd")
        
        # Show node selection
        scheduler >> Edge(color="blue", style="bold", label="nodeSelector") >> pod_ssd
        pod_ssd >> Edge(color="green", style="bold") >> worker1

    # Node Affinity
    with Cluster("Node Affinity"):
        # Nodes for affinity
        perf_node = Node("worker3\ndisk=ssd\nperformance=high")
        
        # Pod with node affinity
        affinity_pod = Pod("pod-with-node-affinity\nrequired: disk=ssd\npreferred: performance=high")
        
        # Show affinity rules
        scheduler >> Edge(color="red", style="dashed", label="required") >> affinity_pod
        affinity_pod >> Edge(color="orange", style="bold", label="preferred") >> perf_node

    # Taints and Tolerations
    with Cluster("Taints and Tolerations"):
        # Tainted node
        tainted_node = Node("worker4\nTaint: app=critical:NoSchedule")
        
        # Pods with/without tolerations
        tolerating_pod = Pod("critical-app\nToleration: app=critical")
        regular_pod = Pod("regular-app\nNo toleration")
        
        # Show taint/toleration relationships
        scheduler >> Edge(color="purple", style="bold", label="tolerates") >> tolerating_pod
        tolerating_pod >> Edge(color="green", style="bold") >> tainted_node
        scheduler >> Edge(color="red", style="dotted", label="blocked") >> regular_pod
        regular_pod >> Edge(color="red", style="dotted") >> tainted_node 