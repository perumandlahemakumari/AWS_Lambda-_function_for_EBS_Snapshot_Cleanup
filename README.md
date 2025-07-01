# 🧹 AWS Lambda for EBS Snapshot Cleanup (Cost Optimization)

This project contains a Python 3.13 AWS Lambda function that automatically **deletes unused EBS snapshots** to help reduce unnecessary storage costs.

---

## 🚀 Features

- Checks all EBS snapshots owned by the account
- Verifies if the snapshot is linked to an active EC2 instance
- Deletes snapshots that:
  - Are not linked to any volume
  - Are linked to a volume not attached to any running EC2 instance
  - Are linked to deleted volumes

---

## 🛠️ Setup Instructions

### 1. **Prepare Lambda Environment**

- Go to AWS Console → Lambda → Create Function
- Choose:
  - Runtime: `Python 3.13`
  - Function name: `cost-optimization-ebs-snapshot`
  - Execution role: Create a new role with basic Lambda permissions

---

### 2. **Add Code**

- Copy the Python code from [`lambda_function.py`](./lambda_function.py)

---

### 3. **Set IAM Permissions**

- Go to IAM → Roles → Select your Lambda Role → Add the following inline policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeSnapshots",
        "ec2:DeleteSnapshot",
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes"
      ],
      "Resource": "*"
    }
  ]
}
```

---

### 4. **Test the Lambda Function**

- In the Lambda console, use the "Test" tab and click:
  - Create new test event (no need to modify the default JSON)
  - Click **Test** to verify output in the logs

---

### 5. **Automate Using CloudWatch Events**

- Go to CloudWatch → Rules → Create Rule
- Choose:
  - Event Source: `Schedule`
  - Example: `rate(1 day)`
- Target:
  - Lambda Function: `cost-optimization-ebs-snapshot`

> This ensures your cleanup runs automatically every day.

---

## 🧪 Deployment from GitHub

If you want to automate deployment via GitHub:

- Clone the repo
- Push your `lambda_function.py` and `README.md`
- Use AWS CLI or Terraform for deployment

---

## 📒 Notes from Setup

- Use `describe snapshots`, `describe volumes`, `describe instances` via Boto3
- Test code from GitHub directly
- Create IAM policies → Attach → Add Permissions → Save
- Ensure timeout is set (e.g., 10s)
- Use CloudWatch Events for daily triggers
- Snapshot deletion should only happen when volume is not active or volume is deleted

---

## ✅ To-Do

- [ ] Add CloudFormation or Terraform automation
- [ ] Add SNS notification after cleanup
- [ ] Add dry-run mode

---

## 🧠 Author

Built for cost optimization on AWS using Lambda + Python 3.13 + Boto3.

Feel free to fork, star, and contribute 🤝
