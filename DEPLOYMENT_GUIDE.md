# Pokemon TCG Analyst - Deployment Status & Guide

## Current Deployment

**Status**: IN PROGRESS
**Started**: 2025-11-14
**Expected Completion**: 5-10 minutes from start
**AWS Account**: 871104587854
**Region**: us-east-1

## Monitor Deployment

### GitHub Actions
Live deployment status:
https://github.com/Camcoder1/pokeAI/actions

### Check AWS Resources

```bash
# Quick status check
./check-deployment.sh

# Manual CloudFormation check
aws cloudformation describe-stacks \
    --stack-name pokemon-tcg-analyst \
    --region us-east-1 \
    --query 'Stacks[0].StackStatus'
```

## What's Being Deployed

### Backend (AWS Lambda)
- **Function Name**: pokemon-tcg-analyst-PokemonAnalyzerFunction-*
- **Runtime**: Python 3.11
- **Memory**: 512 MB
- **Timeout**: 30 seconds
- **Environment Variables**:
  - DYNAMODB_TABLE
  - POKEMON_TCG_API_KEY
  - CACHE_TTL

### Database (DynamoDB)
- **Table Name**: pokemon-tcg-analytics
- **Billing Mode**: Pay-per-request (on-demand)
- **Indexes**:
  - Primary: pk (hash), sk (range)
  - GSI: timestamp-index

### API (API Gateway)
- **Type**: REST API
- **Stage**: prod
- **CORS**: Enabled
- **Endpoints**:
  - POST /analyze
  - GET /analyze/{productId}
  - GET /sets
  - GET /trending

### Frontend (S3)
- **Bucket**: pokemon-tcg-analyst-871104587854
- **Website**: Enabled
- **Public Access**: Read-only

## After Deployment Completes

### 1. Get Your URLs

```bash
# API Endpoint
aws cloudformation describe-stacks \
    --stack-name pokemon-tcg-analyst \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
    --output text

# Frontend URL
aws cloudformation describe-stacks \
    --stack-name pokemon-tcg-analyst \
    --query 'Stacks[0].Outputs[?OutputKey==`FrontendURL`].OutputValue' \
    --output text
```

### 2. Test Backend API

```bash
# Replace with your actual API URL
API_URL="https://xxxxx.execute-api.us-east-1.amazonaws.com/prod/"

# Test sets endpoint
curl "${API_URL}sets" | jq '.'

# Test analysis
curl -X POST "${API_URL}analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "set_name": "151",
    "product_name": "151 Booster Box",
    "sealed_price": 120.00
  }' | jq '.'
```

### 3. Test Frontend

Open your frontend URL in browser:
```
http://pokemon-tcg-analyst-871104587854.s3-website-us-east-1.amazonaws.com
```

Try analyzing a product:
1. Select "151" from dropdown
2. Enter "151 Booster Box"
3. Click "Analyze Product"

### 4. Check DynamoDB

```bash
# Verify table exists
aws dynamodb describe-table \
    --table-name pokemon-tcg-analytics \
    --query 'Table.TableStatus'

# Check for data
aws dynamodb scan \
    --table-name pokemon-tcg-analytics \
    --max-items 5
```

## Cost Monitoring

### Set Up Budget Alert

1. Go to AWS Console → Billing → Budgets
2. Create budget: https://console.aws.amazon.com/billing/home#/budgets/create
3. Set threshold: $50/month
4. Add email for alerts

### Check Current Costs

```bash
# This month's costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --query 'ResultsByTime[0].Total.UnblendedCost.Amount' \
  --output text
```

### Expected Costs

**Monthly estimate: $5-15**

- Lambda: $0-2 (1M free requests)
- DynamoDB: $0-3 (25GB free)
- S3: $0-2 (5GB free)
- API Gateway: $0-3 (1M free)
- Data Transfer: $1-5

## Troubleshooting

### Deployment Fails

**Check GitHub Actions logs**:
https://github.com/Camcoder1/pokeAI/actions

Common issues:
- AWS credentials incorrect → Verify GitHub Secrets
- IAM permissions missing → Check user has CloudFormation access
- Stack already exists → Delete old stack first

### API Returns Errors

**Check Lambda logs**:
```bash
aws logs tail /aws/lambda/pokemon-tcg-analyst-PokemonAnalyzerFunction --follow
```

### Frontend Not Loading

**Check S3 bucket policy**:
```bash
aws s3api get-bucket-policy \
    --bucket pokemon-tcg-analyst-871104587854
```

**Verify website configuration**:
```bash
aws s3api get-bucket-website \
    --bucket pokemon-tcg-analyst-871104587854
```

## Next Steps After Deployment

### 1. Test Full Workflow

Analyze different products:
- 151 Booster Box
- Obsidian Flames Elite Trainer Box
- Paldean Fates Booster Bundle
- Shrouded Fable Booster Box

### 2. Review Analytics

```bash
# Check what's been analyzed
aws dynamodb scan \
    --table-name pokemon-tcg-analytics \
    --filter-expression "begins_with(pk, :pk)" \
    --expression-attribute-values '{":pk":{"S":"ANALYSIS"}}' \
    --max-items 10
```

### 3. Monitor Performance

```bash
# Lambda invocations
aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Invocations \
    --dimensions Name=FunctionName,Value=pokemon-tcg-analyst-PokemonAnalyzerFunction \
    --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
    --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
    --period 3600 \
    --statistics Sum
```

### 4. Share With Others

Once tested, share your frontend URL:
```
http://pokemon-tcg-analyst-871104587854.s3-website-us-east-1.amazonaws.com
```

## Update Application

### Via GitHub (Automatic)

```bash
# Make changes
cd S:\Code\pokeAI
# Edit files...
git add .
git commit -m "Update feature"
git push origin main

# GitHub Actions will auto-deploy
```

### Manual Deployment

```bash
cd S:\Code\pokeAI
./deploy.sh
```

## Cleanup (If Needed)

To completely remove the application:

```bash
# Delete CloudFormation stack
aws cloudformation delete-stack --stack-name pokemon-tcg-analyst

# Delete S3 bucket
aws s3 rb s3://pokemon-tcg-analyst-871104587854 --force
```

## Support

- **GitHub Issues**: https://github.com/Camcoder1/pokeAI/issues
- **AWS Support**: https://console.aws.amazon.com/support
- **Pokemon TCG API**: https://pokemontcg.io

---

**Deployment triggered!** Check back in 5-10 minutes.

Run `./check-deployment.sh` to monitor progress.
