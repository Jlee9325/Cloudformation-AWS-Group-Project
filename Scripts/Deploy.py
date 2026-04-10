# deploy.py - deploys my CloudFormation stack
# Usage:
#   python scripts/deploy.py deploy
#   python scripts/deploy.py destroy

import sys
import boto3

STACK_NAME = "MyVPCStack"
TEMPLATE_FILE = "cloudformation/vpc-web-db.yaml"
KEY_NAME = "twotier-key"   # change this to your key pair name
REGION = "us-east-1"

cf = boto3.client("cloudformation", region_name=REGION)


def deploy():
    # read the template file
    with open(TEMPLATE_FILE) as f:
        template = f.read()

    print("Creating stack...")
    cf.create_stack(
        StackName=STACK_NAME,
        TemplateBody=template,
        Parameters=[
            {"ParameterKey": "KeyName", "ParameterValue": KEY_NAME}
        ]
    )

    # wait for it to finish
    print("Waiting for stack to finish (this takes a few minutes)...")
    waiter = cf.get_waiter("stack_create_complete")
    waiter.wait(StackName=STACK_NAME)
    print("Done!")

    # print the web server IP
    result = cf.describe_stacks(StackName=STACK_NAME)
    outputs = result["Stacks"][0]["Outputs"]
    for o in outputs:
        print(o["OutputKey"], "=", o["OutputValue"])


def destroy():
    print("Deleting stack...")
    cf.delete_stack(StackName=STACK_NAME)
    waiter = cf.get_waiter("stack_delete_complete")
    waiter.wait(StackName=STACK_NAME)
    print("Stack deleted")


if sys.argv[1] == "deploy":
    deploy()
elif sys.argv[1] == "destroy":
    destroy()
else:
    print("Use 'deploy' or 'destroy'")