from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3

with Diagram("Web Service Architecture", show=False):
    with Cluster("AWS Cloud"):
        lb = ELB("Load Balancer")

        with Cluster("Auto Scaling Group"):
            web_servers = [EC2("Web Server 1"),
                           EC2("Web Server 2"),
                           EC2("Web Server 3")]

        db = RDS("Database")
        s3 = S3("Object Storage")

    lb >> web_servers
    web_servers >> db
    web_servers >> s3