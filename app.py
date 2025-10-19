#!/usr/bin/env python3
import aws_cdk as cdk
from kendra_data_pipeline.kendra_crawler_stack import KendraCrawlerStack

app = cdk.App()
KendraCrawlerStack(app, "KendraCrawlerStack",
    env=cdk.Environment(account="689327566109", region="us-east-1")
)

app.synth()
