# Chapter 12: Troubleshooting - Practice Questions

## Control Plane Troubleshooting

1. You notice the API server is not responding. Which commands would you use to investigate the issue? (Choose all that apply)
   ```
   a) kubectl get componentstatuses
   b) systemctl status kube-apiserver
   c) journalctl -u kube-apiserver
   d) kubectl logs kube-apiserver
   ```

2. During a certificate audit, you need to check the expiration date of the API server certificate. Write the command to view the certificate details.

<details>
<summary>Show answers</summary>

1. Correct answers: a, b, c
   - These commands help check the API server status and logs
   - `kubectl logs kube-apiserver` won't work as API server runs as a system service

2. Command:
   ```bash
   sudo openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout
   ```
</details>

## Node Troubleshooting

3. A node is showing `NotReady` status. List three things you should check and the commands to investigate them.

4. Which command would you use to check if kubelet is running properly on a node?
   ```
   a) service kubelet status
   b) systemctl status kubelet
   c) kubectl get kubelet
   d) ps aux | grep kubelet
   ```

<details>
<summary>Show answers</summary>

3. Three things to check:
   - Kubelet status: `systemctl status kubelet`
   - Node resources: `df -h`, `free -m`, `top`
   - Node connectivity: `ping <node-ip>`, `telnet <node-ip> 6443`

4. Correct answer: b
   - `systemctl status kubelet` is the proper way to check systemd service status
</details>

## Pod Troubleshooting

5. A pod is stuck in `Pending` state. What are the possible causes and commands to investigate? List at least three.

6. You need to check the logs of a crashed container that has restarted. What command would you use?
   ```
   a) kubectl logs <pod-name>
   b) kubectl logs <pod-name> --previous
   c) kubectl describe pod <pod-name>
   d) kubectl get logs <pod-name>
   ```

<details>
<summary>Show answers</summary>

5. Possible causes and investigation commands:
   - Insufficient resources: `kubectl describe node`
   - PVC not bound: `kubectl get pvc`
   - Node selector/affinity issues: `kubectl describe pod`
   - Resource quotas: `kubectl describe quota`

6. Correct answer: b
   - `--previous` flag shows logs from the previous container instance
</details>

## Network Troubleshooting

7. How would you verify if a service is properly resolving through DNS? Write the command using a test pod.

8. You suspect network policies are blocking traffic to a pod. What steps would you take to troubleshoot this? List the commands.

<details>
<summary>Show answers</summary>

7. Command:
   ```bash
   kubectl run test-dns --image=busybox:1.28 -- nslookup <service-name>.<namespace>.svc.cluster.local
   ```

8. Steps and commands:
   ```bash
   # Check existing network policies
   kubectl get networkpolicy
   
   # Describe the network policy
   kubectl describe networkpolicy
   
   # Test connectivity with a debug pod
   kubectl run test-connectivity --image=busybox:1.28 -it --rm -- wget -O- <service-ip>
   ```
</details>

## Storage Troubleshooting

9. A pod can't mount its persistent volume. List the troubleshooting steps and commands you would use to investigate.

10. Which command would you use to check if a PersistentVolumeClaim is bound to a PersistentVolume?
    ```
    a) kubectl get pv,pvc
    b) kubectl describe pvc
    c) kubectl get storage
    d) kubectl get volumes
    ```

<details>
<summary>Show answers</summary>

9. Troubleshooting steps:
   ```bash
   # Check PVC status
   kubectl get pvc
   
   # Check PV status
   kubectl describe pv
   
   # Check storage class
   kubectl get sc
   
   # Check pod events
   kubectl describe pod <pod-name>
   ```

10. Correct answers: a, b
    - Both commands provide information about PV-PVC binding status
</details>

## Resource Troubleshooting

11. How would you identify if nodes are under resource pressure? Write two commands.

12. A pod is being OOMKilled. What steps would you take to investigate and resolve this issue?

<details>
<summary>Show answers</summary>

11. Commands:
    ```bash
    kubectl top nodes
    kubectl describe node | grep Pressure
    ```

12. Investigation steps:
    - Check current resource usage:
      ```bash
      kubectl top pod <pod-name> --containers
      ```
    - Review pod resource limits:
      ```bash
      kubectl describe pod <pod-name> | grep -A 5 Limits
      ```
    - Adjust memory limits in pod specification
    - Monitor pod behavior after adjustment
</details>

## General Troubleshooting

13. During an incident, what commands would you use to collect comprehensive cluster state information?

14. You need to debug a pod that's not starting. Put the following troubleshooting steps in the correct order:
    ```
    a) Check pod logs
    b) Check node capacity
    c) Get pod description
    d) Check pod status
    ```

<details>
<summary>Show answers</summary>

13. Commands to collect cluster state:
    ```bash
    # Get all resources
    kubectl get all --all-namespaces -o yaml > cluster_state.yaml
    
    # Get events
    kubectl get events --sort-by=.metadata.creationTimestamp > events.txt
    
    # Get logs
    kubectl logs <pod-name> > pod_logs.txt
    ```

14. Correct order:
    1. d) Check pod status (`kubectl get pods`)
    2. c) Get pod description (`kubectl describe pod`)
    3. a) Check pod logs (`kubectl logs`)
    4. b) Check node capacity (`kubectl describe node`)
</details>

## Additional Scenario-based Questions

16. The cluster's control plane components are running as static pods. During maintenance, you notice that the scheduler pod isn't running. How would you troubleshoot this issue?

<details>
<summary>Show answers</summary>

16. Troubleshooting steps:
    1. Check static pod manifests:
       ```bash
       ls -l /etc/kubernetes/manifests/kube-scheduler.yaml
       ```
    
    2. Check scheduler pod status:
       ```bash
       kubectl get pods -n kube-system | grep scheduler
       ```
    
    3. Check kubelet status and logs:
       ```bash
       systemctl status kubelet
       journalctl -u kubelet | grep scheduler
       ```
    
    4. Verify scheduler manifest:
       ```bash
       cat /etc/kubernetes/manifests/kube-scheduler.yaml
       ```
    
    5. Check scheduler container logs:
       ```bash
       crictl logs <scheduler-container-id>
       ```
</details>

17. Your team reports that pods are being evicted frequently from a specific node. What could be the causes and how would you investigate?

<details>
<summary>Show answers</summary>

17. Investigation approach:
    1. Check node conditions:
       ```bash
       kubectl describe node <node-name> | grep Conditions -A 5
       ```
    
    2. Check resource usage:
       ```bash
       kubectl top node <node-name>
       ```
    
    3. Review eviction events:
       ```bash
       kubectl get events --field-selector involvedObject.kind=Pod,reason=Evicted
       ```
    
    4. Check node pressure thresholds:
       ```bash
       kubectl describe node <node-name> | grep -A 5 Allocatable
       ```
    
    Common causes:
    - Memory pressure
    - Disk pressure
    - PID pressure
    - Node cordoned for maintenance
</details>

18. ETCD cluster is reporting high latency. What steps would you take to diagnose and resolve this issue?

<details>
<summary>Show answers</summary>

18. Troubleshooting steps:
    1. Check ETCD metrics:
       ```bash
       ETCDCTL_API=3 etcdctl \
       --endpoints=https://127.0.0.1:2379 \
       --cacert=/etc/kubernetes/pki/etcd/ca.crt \
       --cert=/etc/kubernetes/pki/etcd/server.crt \
       --key=/etc/kubernetes/pki/etcd/server.key \
       endpoint status --write-out=table
       ```
    
    2. Monitor ETCD performance:
       ```bash
       ETCDCTL_API=3 etcdctl check perf
       ```
    
    3. Check disk latency:
       ```bash
       iostat -x 1
       ```
    
    4. Review ETCD logs:
       ```bash
       kubectl logs -n kube-system etcd-master -f
       ```
    
    Possible solutions:
    - Optimize disk I/O
    - Increase resource limits
    - Defragment ETCD database
    - Use SSD storage
</details>

19. A StatefulSet's pods are not getting scheduled despite available resources. What could be the potential issues?

<details>
<summary>Show answers</summary>

19. Investigation steps:
    1. Check StatefulSet status:
       ```bash
       kubectl describe statefulset <statefulset-name>
       ```
    
    2. Verify PVC creation:
       ```bash
       kubectl get pvc -l app=<statefulset-name>
       ```
    
    3. Check storage class:
       ```bash
       kubectl get storageclass
       kubectl describe storageclass <storage-class-name>
       ```
    
    4. Review pod anti-affinity rules:
       ```bash
       kubectl get statefulset <name> -o yaml | grep -A 10 affinity
       ```
    
    Potential issues:
    - Storage class issues
    - PVC binding problems
    - Pod anti-affinity constraints
    - Volume zone restrictions
</details>

20. Your cluster's CNI plugin is malfunctioning. How would you troubleshoot network connectivity issues between pods?

<details>
<summary>Show answers</summary>

20. Troubleshooting approach:
    1. Check CNI configuration:
       ```bash
       ls /etc/cni/net.d/
       cat /etc/cni/net.d/10-flannel.conflist  # or your CNI config
       ```
    
    2. Verify CNI pods:
       ```bash
       kubectl get pods -n kube-system -l k8s-app=flannel  # or your CNI
       ```
    
    3. Test pod connectivity:
       ```bash
       # Create test pods
       kubectl run test-pod1 --image=busybox --command -- sleep 3600
       kubectl run test-pod2 --image=busybox --command -- sleep 3600
       
       # Test connectivity
       kubectl exec test-pod1 -- ping <test-pod2-ip>
       ```
    
    4. Check CNI logs:
       ```bash
       kubectl logs -n kube-system <cni-pod-name>
       ```
    
    Common issues:
    - Misconfigured CNI
    - Network policy conflicts
    - MTU issues
    - Routing problems
</details>

21. During a production incident, you notice that some pods are stuck in "Terminating" state. What steps would you take to investigate and resolve this?

<details>
<summary>Show answers</summary>

21. Resolution steps:
    1. Check pod status and details:
       ```bash
       kubectl describe pod <pod-name>
       ```
    
    2. Check for finalizers:
       ```bash
       kubectl get pod <pod-name> -o yaml | grep finalizers -A 5
       ```
    
    3. Force delete if necessary:
       ```bash
       kubectl delete pod <pod-name> --grace-period=0 --force
       ```
    
    4. Check node status:
       ```bash
       kubectl describe node <node-name>
       ```
    
    Common causes:
    - Stuck finalizers
    - Node issues
    - Volume unmounting problems
    - CNI cleanup issues
</details>

22. Your cluster's monitoring system alerts that the API server is experiencing high latency. How would you investigate and resolve this issue?

<details>
<summary>Show answers</summary>

22. Investigation approach:
    1. Check API server metrics:
       ```bash
       curl -k https://localhost:6443/metrics | grep apiserver_request_duration_seconds
       ```
    
    2. Review API server logs:
       ```bash
       kubectl logs -n kube-system kube-apiserver-master -f
       ```
    
    3. Check etcd performance:
       ```bash
       ETCDCTL_API=3 etcdctl check perf
       ```
    
    4. Monitor system resources:
       ```bash
       top
       iostat -x 1
       ```
    
    Possible solutions:
    - Scale API server resources
    - Optimize etcd
    - Review expensive API calls
    - Implement API priority and fairness
</details>
