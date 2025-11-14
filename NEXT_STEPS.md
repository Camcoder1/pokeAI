# 🎯 Next Steps - Deployment Checklist

Your Pokemon TCG Market Analyst application is ready to deploy! Follow these steps to get it live on AWS.

## ✅ What's Been Completed

- ✅ Full-stack serverless application built
- ✅ Backend API with Pokemon TCG analysis logic
- ✅ React frontend with modern UI
- ✅ AWS SAM infrastructure configuration
- ✅ GitHub Actions CI/CD pipeline
- ✅ Comprehensive documentation
- ✅ Code pushed to https://github.com/Camcoder1/pokeAI

## 🚀 Quick Deploy (5 Minutes)

### Option 1: Automated Deployment via GitHub Actions (Recommended)

1. **Add GitHub Secrets**

   Go to: https://github.com/Camcoder1/pokeAI/settings/secrets/actions

   Add these secrets:
   ```
   Name: AWS_ACCESS_KEY_ID
   Value: [Your AWS Access Key ID provided separately]

   Name: AWS_SECRET_ACCESS_KEY
   Value: [Your AWS Secret Access Key provided separately]

   Name: POKEMON_TCG_API_KEY (optional)
   Value: [Get free key from pokemontcg.io]
   ```

   **Note**: AWS credentials have been provided to you separately for security. Never commit credentials to Git!

2. **Trigger Deployment**

   The GitHub Action will automatically deploy when you push to `main`, or you can:
   - Go to: https://github.com/Camcoder1/pokeAI/actions
   - Click "Deploy Pokemon TCG Analyst to AWS"
   - Click "Run workflow"

   Wait 5-10 minutes for deployment to complete!

3. **Get Your URLs**

   Check the GitHub Actions output for:
   - Frontend URL: `http://pokemon-tcg-analyst-XXXX.s3-website-us-east-1.amazonaws.com`
   - API URL: `https://xxxx.execute-api.us-east-1.amazonaws.com/prod/`

### Option 2: Manual Deployment (Local)

1. **Install Prerequisites**
   ```bash
   # AWS CLI
   # Download from: https://aws.amazon.com/cli/

   # AWS SAM CLI
   # Download from: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
   ```

2. **Configure AWS Credentials**
   ```bash
   aws configure
   # Enter the credentials provided above
   ```

3. **Run Deployment Script**
   ```bash
   cd pokeAI
   chmod +x deploy.sh
   ./deploy.sh
   ```

## 📊 Cost Monitoring Setup

### Set Up Budget Alert (Important!)

1. Go to AWS Console → Billing → Budgets
2. Create budget: https://console.aws.amazon.com/billing/home#/budgets/create
3. Set threshold: **$50/month**
4. Add your email for alerts

### Check Current Costs

```bash
aws ce get-cost-and-usage \
  --time-period Start=$(date -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost"
```

## 🔒 Security Best Practices

### 1. Rotate AWS Credentials (Recommended)

After initial deployment, create new credentials:

```bash
# Create new access key in AWS Console
# Update GitHub Secrets
# Delete old credentials
```

### 2. Get Pokemon TCG API Key

Free tier: 1000 requests/day
- Sign up: https://pokemontcg.io
- Get API key
- Add to GitHub Secrets as `POKEMON_TCG_API_KEY`
- Redeploy

### 3. Enable CloudWatch Alarms

Monitor Lambda errors and high costs:
- Lambda errors > 10/5min
- DynamoDB throttling
- Estimated charges > $40

## 🧪 Testing Your Deployment

### 1. Test Backend API

```bash
# Get your API URL from deployment output
API_URL="https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod"

# Test sets endpoint
curl "${API_URL}/sets"

# Test analysis
curl -X POST "${API_URL}/analyze" \
  -H "Content-Type: application/json" \
  -d '{"set_name": "151", "product_name": "151 Booster Box"}'
```

### 2. Test Frontend

Open your frontend URL in browser:
1. Select "151" from the dropdown
2. Enter "151 Booster Box"
3. Click "Analyze Product"
4. Verify you see results with EV breakdown and recommendation

### 3. Check DynamoDB

```bash
# Verify table exists
aws dynamodb describe-table --table-name pokemon-tcg-analytics

# Check for data
aws dynamodb scan --table-name pokemon-tcg-analytics --max-items 5
```

## 🎨 Customization Ideas

### 1. Add Custom Domain

- Register domain in Route 53
- Create SSL certificate in ACM
- Configure API Gateway custom domain
- Update frontend with new API URL

### 2. Enable CloudFront CDN

Uncomment CloudFront section in `template.yaml` and redeploy for:
- Faster global performance
- HTTPS support
- Custom domain support

### 3. Add Email Alerts

Integrate with SNS to email when:
- Product EV exceeds threshold
- Price drops detected
- New trending products

### 4. Enhanced Analytics

- Historical price trends
- ROI tracking over time
- Portfolio management
- Graded card value (PSA/BGS)

## 🐛 Troubleshooting

### GitHub Actions Fails

**Problem**: "Error: Credentials could not be loaded"

**Solution**:
- Verify GitHub Secrets are set correctly
- Check AWS credentials are valid
- Ensure IAM user has required permissions

### Frontend Shows Network Error

**Problem**: API calls fail with CORS error

**Solution**:
```bash
# Check API Gateway CORS settings
# Verify API URL is correct in frontend build
# Check browser console for specific error
```

### Lambda Timeout

**Problem**: Analysis takes too long

**Solution**: Increase timeout in `template.yaml`:
```yaml
Globals:
  Function:
    Timeout: 60  # Increase from 30
```

Then redeploy.

## 📚 Documentation

- **README.md** - Project overview and quickstart
- **DEPLOYMENT.md** - Detailed deployment guide
- **Backend API**: `backend/app.py` - Main application logic
- **Frontend**: `frontend/src/` - React components

## 🎯 Success Criteria

Your deployment is successful when:

- [ ] GitHub Actions workflow completes without errors
- [ ] Frontend URL loads in browser
- [ ] Can select a set and analyze a product
- [ ] Results display with EV breakdown and recommendation
- [ ] DynamoDB table contains analysis data
- [ ] Monthly cost estimate < $50

## 🎉 You're All Set!

Once deployed, you can:
1. Share the frontend URL with others
2. Analyze any Pokemon TCG sealed product
3. View trending analyses
4. Monitor costs in AWS Billing console
5. Make updates via Git push (auto-deploys)

## 💡 Tips for Success

1. **Start with Popular Sets**: Try "151", "Obsidian Flames", or "Paldean Fates"
2. **Get API Key**: Free Pokemon TCG API key for better rate limits
3. **Monitor Costs**: Check AWS billing weekly
4. **Share Results**: Export analyses for investment decisions
5. **Contribute**: Add features and submit PRs!

## 📧 Need Help?

- **GitHub Issues**: https://github.com/Camcoder1/pokeAI/issues
- **AWS Support**: Use AWS Support Center
- **Documentation**: Check README.md and DEPLOYMENT.md

---

**Happy deploying! 🚀**
