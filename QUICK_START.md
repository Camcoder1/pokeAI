# Quick Start - Pokemon TCG Market Analyst

## Current Status

**GitHub Repository**: https://github.com/Camcoder1/pokeAI ✅
**GitHub Secrets**: Configured ✅
**Deployment**: IN PROGRESS ⏳

## What's Happening Now

Your Pokemon TCG Market Analyst is being deployed to AWS via GitHub Actions.

**Live Status**: https://github.com/Camcoder1/pokeAI/actions

The workflow is:
1. ✅ Checking out code
2. ⏳ Installing Python & Node.js
3. ⏳ Building backend Lambda function
4. ⏳ Deploying CloudFormation stack (this takes 3-5 minutes)
5. ⏳ Building React frontend
6. ⏳ Uploading to S3
7. ⏳ Running final tests

**Total time**: 5-10 minutes

## How to Check Status

### Option 1: GitHub Actions Web Interface

Go to: https://github.com/Camcoder1/pokeAI/actions

Look for the latest workflow run. You'll see:
- Yellow dot = Running
- Green check = Success
- Red X = Failed

### Option 2: Command Line

```bash
cd S:\Code\pokeAI

# Quick check
./check-deployment.sh

# Or manually
aws cloudformation describe-stacks \
    --stack-name pokemon-tcg-analyst \
    --region us-east-1
```

## Once Deployment Completes

### You'll Get These URLs

**API Endpoint**:
```
https://xxxxx.execute-api.us-east-1.amazonaws.com/prod/
```

**Frontend Website**:
```
http://pokemon-tcg-analyst-871104587854.s3-website-us-east-1.amazonaws.com
```

### Test Your Application

1. **Open Frontend URL** in your browser

2. **Select a Pokemon Set**:
   - Try "151" or "Obsidian Flames"

3. **Enter Product Details**:
   - Product: "151 Booster Box"
   - Price: Leave blank (auto-estimate) or enter your price

4. **Click "Analyze Product"**

5. **Review Results**:
   - Expected Value (EV) calculation
   - ROI comparison (Open/Hold/Resell)
   - Top value cards
   - Confidence score
   - Recommendation

### Test API Directly

```bash
# Get your API URL from deployment output
API_URL="https://xxxxx.execute-api.us-east-1.amazonaws.com/prod/"

# Test 1: Get all Pokemon TCG sets
curl "${API_URL}sets"

# Test 2: Analyze a product
curl -X POST "${API_URL}analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "set_name": "151",
    "product_name": "151 Booster Box",
    "sealed_price": 120.00
  }'

# Test 3: Get trending analyses
curl "${API_URL}trending"
```

## If Deployment Fails

### Check GitHub Actions Logs

1. Go to: https://github.com/Camcoder1/pokeAI/actions
2. Click on the failed workflow run
3. Click on "deploy-backend" or "deploy-frontend"
4. Read the error message

### Common Issues & Fixes

**Issue**: "Credentials could not be loaded"
**Fix**: Verify GitHub Secrets are set correctly at:
https://github.com/Camcoder1/pokeAI/settings/secrets/actions

**Issue**: "Stack already exists"
**Fix**: Delete old stack:
```bash
aws cloudformation delete-stack --stack-name pokemon-tcg-analyst
# Wait 2 minutes, then re-run deployment
```

**Issue**: "Insufficient IAM permissions"
**Fix**: Your AWS user needs these permissions:
- CloudFormation Full Access
- Lambda Full Access
- DynamoDB Full Access
- S3 Full Access
- API Gateway Administrator
- IAM Role Creation

### Manual Deployment (Backup)

If GitHub Actions fails, deploy manually:

```bash
cd S:\Code\pokeAI

# Option 1: Use deploy script
./deploy.sh

# Option 2: Manual SAM deployment
sam build
sam deploy \
    --stack-name pokemon-tcg-analyst \
    --capabilities CAPABILITY_IAM \
    --region us-east-1 \
    --resolve-s3 \
    --parameter-overrides PokemonTCGApiKey=YOUR_API_KEY
```

## What You're Getting

### Features

1. **Real Pokemon TCG Data**
   - 500+ sets from Pokemon TCG API
   - Live card prices from TCGPlayer
   - Community-validated pull rates

2. **EV Calculation**
   - Expected value per booster box
   - Card-by-card breakdown
   - Rarity-based probabilities

3. **ROI Analysis**
   - Open: Calculate EV vs box cost
   - Hold: Project 6-month appreciation
   - Resell: Current market markup

4. **Smart Recommendations**
   - AI-powered decision engine
   - Confidence scoring (1-100)
   - Historical trend analysis

5. **Analytics Dashboard**
   - Trending products
   - Community analyses
   - Historical data storage

### Architecture

```
User Browser
    ↓
React Frontend (S3)
    ↓
API Gateway
    ↓
Lambda Function (Python)
    ↓
┌─────────────┬──────────────┐
│  DynamoDB   │  Pokemon TCG │
│ (Analytics) │     API      │
└─────────────┴──────────────┘
```

### Cost

**Expected**: $5-15/month
**Maximum**: Set budget alert at $50/month

Breakdown:
- Lambda: ~$1-3
- DynamoDB: ~$1-3
- S3: ~$1-2
- API Gateway: ~$1-3
- Data Transfer: ~$1-4

**All services use free tier where available**

## Next Steps

### 1. Wait for Deployment (5-10 min)

Monitor at: https://github.com/Camcoder1/pokeAI/actions

### 2. Test Application

Use frontend URL to analyze products

### 3. Set Up Cost Monitoring

AWS Console → Billing → Budgets → Create ($50 threshold)

### 4. Get Pokemon TCG API Key (Optional)

Free key at https://pokemontcg.io for higher rate limits

### 5. Customize & Enhance

Ideas:
- Add more sets
- Historical price charts
- Email alerts
- Portfolio tracking
- Graded card values (PSA/BGS)

## Support Resources

- **GitHub Issues**: https://github.com/Camcoder1/pokeAI/issues
- **README**: S:\Code\pokeAI\README.md
- **Deployment Guide**: S:\Code\pokeAI\DEPLOYMENT.md
- **Pokemon TCG API Docs**: https://docs.pokemontcg.io

## Monitoring Commands

```bash
# Check deployment status
./check-deployment.sh

# View Lambda logs
aws logs tail /aws/lambda/pokemon-tcg-analyst-PokemonAnalyzerFunction --follow

# Check DynamoDB
aws dynamodb scan --table-name pokemon-tcg-analytics --max-items 5

# Monitor costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost"
```

---

**Deployment is running!** Check back in a few minutes.

Visit https://github.com/Camcoder1/pokeAI/actions to watch progress.
