# 🚀 Deployment Guide

Complete step-by-step deployment instructions for Pokemon TCG Market Analyst.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [AWS Configuration](#aws-configuration)
4. [Manual Deployment](#manual-deployment)
5. [Automated Deployment (CI/CD)](#automated-deployment-cicd)
6. [Verification](#verification)
7. [Updating the Application](#updating-the-application)
8. [Cost Monitoring](#cost-monitoring)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Tools

1. **AWS CLI**
   ```bash
   # Install on macOS
   brew install awscli

   # Install on Windows
   # Download from: https://aws.amazon.com/cli/

   # Install on Linux
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   ```

2. **AWS SAM CLI**
   ```bash
   # Install on macOS
   brew tap aws/tap
   brew install aws-sam-cli

   # Install on Windows
   # Download from: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

   # Install on Linux
   pip install aws-sam-cli
   ```

3. **Node.js 18+**
   ```bash
   # Check version
   node --version

   # Install via nvm (recommended)
   nvm install 18
   nvm use 18
   ```

4. **Python 3.11+**
   ```bash
   # Check version
   python3 --version

   # Install via pyenv (recommended)
   pyenv install 3.11
   pyenv global 3.11
   ```

### Required Accounts

1. **AWS Account** (Free tier available)
   - Sign up at [aws.amazon.com](https://aws.amazon.com)
   - Create IAM user with appropriate permissions

2. **Pokemon TCG API Key** (Optional but recommended)
   - Sign up at [pokemontcg.io](https://pokemontcg.io)
   - Get free API key from dashboard

## Initial Setup

### 1. Clone Repository

```bash
git clone https://github.com/Camcoder1/pokeAI.git
cd pokeAI
```

### 2. Run Setup Script

```bash
chmod +x setup-aws.sh
./setup-aws.sh
```

This script will:
- Verify AWS CLI and SAM CLI
- Configure AWS credentials
- Set up Pokemon TCG API key

### 3. Manual AWS Configuration (Alternative)

If the script doesn't work, configure manually:

```bash
aws configure
# AWS Access Key ID: AKIA4VUPBFBHN64MKHE5
# AWS Secret Access Key: [Your secret key]
# Default region: us-east-1
# Default output format: json
```

## AWS Configuration

### IAM Permissions Required

Your AWS user needs these permissions:
- `AWSLambda_FullAccess`
- `AmazonDynamoDBFullAccess`
- `AmazonS3FullAccess`
- `AmazonAPIGatewayAdministrator`
- `IAMFullAccess` (for creating roles)
- `CloudFormationFullAccess`

### Create IAM Policy (Least Privilege)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:*",
        "dynamodb:*",
        "s3:*",
        "apigateway:*",
        "cloudformation:*",
        "iam:CreateRole",
        "iam:PutRolePolicy",
        "iam:AttachRolePolicy",
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
```

## Manual Deployment

### Step 1: Deploy Backend

```bash
# Install dependencies
cd backend
pip install -r requirements.txt -t .
cd ..

# Build SAM application
sam build

# Deploy
sam deploy \
  --stack-name pokemon-tcg-analyst \
  --capabilities CAPABILITY_IAM \
  --region us-east-1 \
  --resolve-s3 \
  --parameter-overrides \
    PokemonTCGApiKey=YOUR_API_KEY_HERE
```

### Step 2: Get Backend URL

```bash
aws cloudformation describe-stacks \
  --stack-name pokemon-tcg-analyst \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
  --output text
```

Save this URL - you'll need it for frontend deployment.

### Step 3: Deploy Frontend

```bash
# Get AWS Account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Set API URL
export REACT_APP_API_URL="YOUR_API_URL_FROM_STEP_2"

# Build frontend
cd frontend
npm install
npm run build

# Deploy to S3
aws s3 sync build/ s3://pokemon-tcg-analyst-${AWS_ACCOUNT_ID}/ --delete

# Get frontend URL
echo "http://pokemon-tcg-analyst-${AWS_ACCOUNT_ID}.s3-website-us-east-1.amazonaws.com"
```

### Step 4: Automated Deployment Script

Or simply run:

```bash
chmod +x deploy.sh
./deploy.sh
```

## Automated Deployment (CI/CD)

### GitHub Actions Setup

1. **Add GitHub Secrets**

   Go to your repository → Settings → Secrets and Variables → Actions

   Add these secrets:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
   - `POKEMON_TCG_API_KEY`: Your Pokemon TCG API key (optional)

2. **Enable GitHub Actions**

   The workflow file is already configured at `.github/workflows/deploy.yml`

3. **Trigger Deployment**

   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

   This will automatically deploy to AWS!

## Verification

### 1. Test Backend API

```bash
# Get API URL
API_URL=$(aws cloudformation describe-stacks \
  --stack-name pokemon-tcg-analyst \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
  --output text)

# Test sets endpoint
curl "${API_URL}/sets"

# Test analysis endpoint
curl -X POST "${API_URL}/analyze" \
  -H "Content-Type: application/json" \
  -d '{"set_name": "151", "product_name": "151 Booster Box"}'
```

### 2. Test Frontend

Visit the frontend URL in your browser and:
1. Select a set from the dropdown
2. Enter a product name
3. Click "Analyze Product"
4. Verify results display correctly

### 3. Check DynamoDB

```bash
# List tables
aws dynamodb list-tables

# Scan analytics table
aws dynamodb scan --table-name pokemon-tcg-analytics --max-items 10
```

## Updating the Application

### Update Backend Code

```bash
# Make changes to backend/app.py
# Then redeploy
sam build
sam deploy --stack-name pokemon-tcg-analyst --capabilities CAPABILITY_IAM
```

### Update Frontend Code

```bash
# Make changes to frontend/src
# Then rebuild and deploy
cd frontend
npm run build
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws s3 sync build/ s3://pokemon-tcg-analyst-${AWS_ACCOUNT_ID}/ --delete
```

### Or Use Deploy Script

```bash
./deploy.sh
```

## Cost Monitoring

### Set Up Billing Alerts

1. Go to AWS Console → Billing → Budgets
2. Create a budget with $50 threshold
3. Add email alerts

### Monitor Costs

```bash
# Check current month costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --query "ResultsByTime[].Total.UnblendedCost.Amount"
```

### Cost Optimization Tips

1. **Use DynamoDB On-Demand**: Cheaper for low/variable traffic
2. **Enable S3 Lifecycle Policies**: Archive old logs
3. **Set Lambda Reserved Concurrency**: Prevent runaway costs
4. **Use CloudWatch Logs Retention**: Delete old logs after 7 days

## Troubleshooting

### Deployment Fails

**Problem**: `sam deploy` fails with access denied

**Solution**:
```bash
# Verify credentials
aws sts get-caller-identity

# Check IAM permissions
aws iam list-attached-user-policies --user-name YOUR_USERNAME
```

---

**Problem**: S3 bucket already exists

**Solution**:
```bash
# Use a unique bucket name
export BUCKET_SUFFIX=$(date +%s)
aws s3 mb s3://pokemon-tcg-analyst-${AWS_ACCOUNT_ID}-${BUCKET_SUFFIX}
```

### Frontend Issues

**Problem**: Frontend shows "Network Error" when calling API

**Solution**:
1. Check CORS configuration in `template.yaml`
2. Verify API Gateway URL is correct
3. Check browser console for CORS errors
4. Ensure API Gateway deployment is successful

---

**Problem**: React app shows blank page

**Solution**:
```bash
# Check S3 website configuration
aws s3 website s3://pokemon-tcg-analyst-${AWS_ACCOUNT_ID}/ \
  --index-document index.html \
  --error-document index.html
```

### Backend Issues

**Problem**: Lambda timeout errors

**Solution**:
Update timeout in `template.yaml`:
```yaml
Globals:
  Function:
    Timeout: 60  # Increase from 30
```

---

**Problem**: Pokemon TCG API rate limiting

**Solution**:
1. Get an API key from pokemontcg.io
2. Update deployment:
```bash
sam deploy --parameter-overrides PokemonTCGApiKey=YOUR_KEY
```

### Database Issues

**Problem**: DynamoDB read/write capacity errors

**Solution**:
Check and adjust capacity in AWS Console or switch to on-demand billing (already configured).

---

**Problem**: Analytics data not showing

**Solution**:
```bash
# Verify table exists
aws dynamodb describe-table --table-name pokemon-tcg-analytics

# Check for data
aws dynamodb scan --table-name pokemon-tcg-analytics --max-items 5
```

## Advanced Configuration

### Custom Domain Setup

1. Register domain in Route 53
2. Create SSL certificate in ACM
3. Update API Gateway with custom domain
4. Update CloudFront distribution (optional)

### Enable CloudFront (CDN)

Uncomment CloudFront section in `template.yaml` and redeploy.

### DynamoDB Backup

Enable point-in-time recovery:
```bash
aws dynamodb update-continuous-backups \
  --table-name pokemon-tcg-analytics \
  --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true
```

### CloudWatch Monitoring

Set up alarms:
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name pokemon-tcg-high-errors \
  --alarm-description "Alert on high Lambda errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold
```

## Cleanup (Tear Down)

To completely remove the application:

```bash
# Delete CloudFormation stack
aws cloudformation delete-stack --stack-name pokemon-tcg-analyst

# Delete S3 bucket
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws s3 rb s3://pokemon-tcg-analyst-${AWS_ACCOUNT_ID} --force

# Verify deletion
aws cloudformation describe-stacks --stack-name pokemon-tcg-analyst
# Should show: Stack with id pokemon-tcg-analyst does not exist
```

---

**Questions?** Open an issue on GitHub!
