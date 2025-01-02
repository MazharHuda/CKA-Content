from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deploy, RS
from diagrams.k8s.network import SVC
from diagrams.k8s.clusterconfig import HPA
from diagrams.onprem.monitoring import Prometheus
from diagrams.programming.framework import Flask
from diagrams.generic.device import Mobile

# Diagram 1: Manual Scaling
with Diagram("Manual Scaling Process", show=False, direction="TB", filename="ch05_lab03_manual_scaling"):
    
    with Cluster("Manual Scale Operation"):
        # Deployment and ReplicaSet
        deploy = Deploy("web-app")
        rs = RS("ReplicaSet")
        
        # Original pods
        with Cluster("Original Scale (replicas: 2)"):
            pods_orig = [Pod("pod-1"),
                        Pod("pod-2")]
        
        # Scaled pods
        with Cluster("Scaled Up (replicas: 5)"):
            pods_scaled = [Pod("pod-1"), Pod("pod-2"),
                         Pod("pod-3"), Pod("pod-4"),
                         Pod("pod-5")]
        
        # Show scaling flow
        deploy >> rs
        rs >> Edge(color="blue", label="kubectl scale --replicas=2") >> pods_orig[0]
        for pod in pods_orig[1:]:
            pods_orig[0] - pod
            
        rs >> Edge(color="green", label="kubectl scale --replicas=5") >> pods_scaled[0]
        for pod in pods_scaled[1:]:
            pods_scaled[0] - pod

# Diagram 2: Horizontal Pod Autoscaling
with Diagram("Horizontal Pod Autoscaling", show=False, direction="LR", filename="ch05_lab03_hpa"):
    
    # Monitoring components
    metrics = Prometheus("Metrics Server")
    
    with Cluster("HPA Configuration"):
        hpa = HPA("HPA\nmin: 2, max: 10\ntarget CPU: 80%")
        
        with Cluster("Dynamic Scaling"):
            # Application deployment
            app_deploy = Deploy("web-app")
            app_svc = SVC("web-service")
            
            # Pod states
            with Cluster("Pod Scaling States"):
                min_pods = [Pod("pod-1"),
                           Pod("pod-2")]
                
                scaled_pods = [Pod("pod-1"), Pod("pod-2"),
                             Pod("pod-3"), Pod("pod-4"),
                             Pod("pod-5"), Pod("pod-6")]
            
            # Show autoscaling process
            metrics >> Edge(color="red", label="monitor") >> hpa
            hpa >> Edge(color="blue", label="scale") >> app_deploy
            
            # Connect deployment to first pod in each state, then chain the rest
            app_deploy >> Edge(color="green") >> min_pods[0]
            for pod in min_pods[1:]:
                min_pods[0] - pod
                
            app_deploy >> Edge(color="green") >> scaled_pods[0]
            for pod in scaled_pods[1:]:
                scaled_pods[0] - pod
                
            # Connect service to pods
            app_svc >> Edge(color="orange", style="dashed") >> min_pods[0]
            app_svc >> Edge(color="orange", style="dashed") >> scaled_pods[0]

# Diagram 3: Load Testing and Scaling
with Diagram("Load Testing and Scaling Response", show=False, direction="TB", filename="ch05_lab03_load_test"):
    
    with Cluster("Load Test Environment"):
        # Load generators
        clients = [Mobile("client-1"),
                  Mobile("client-2"),
                  Mobile("client-3")]
        
        with Cluster("Application Under Test"):
            # Application components
            app = Flask("web-app")
            hpa_config = HPA("HPA Config")
            metrics_server = Prometheus("Metrics Server")
            
            # Pod scaling stages
            with Cluster("Scaling Stages"):
                stage1 = [Pod("pod-1"), Pod("pod-2")]
                stage2 = [Pod("pod-1"), Pod("pod-2"),
                         Pod("pod-3"), Pod("pod-4")]
                stage3 = [Pod("pod-1"), Pod("pod-2"),
                         Pod("pod-3"), Pod("pod-4"),
                         Pod("pod-5"), Pod("pod-6")]
            
            # Show test flow
            clients[0] >> Edge(color="red", label="generate load") >> app
            for client in clients[1:]:
                client >> app
                
            metrics_server >> Edge(color="blue", label="monitor") >> app
            metrics_server >> Edge(color="green", label="report") >> hpa_config
            
            # Connect HPA to first pod in each stage, then chain the rest
            hpa_config >> Edge(color="orange", label="scale") >> stage1[0]
            for pod in stage1[1:]:
                stage1[0] - pod
                
            hpa_config >> Edge(color="orange", label="scale") >> stage2[0]
            for pod in stage2[1:]:
                stage2[0] - pod
                
            hpa_config >> Edge(color="orange", label="scale") >> stage3[0]
            for pod in stage3[1:]:
                stage3[0] - pod 