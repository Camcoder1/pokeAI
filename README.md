# ⚡ Pokémon TCG Market Analyst

> AI-Powered analysis tool for Pokémon TCG sealed products: Should you **Open**, **Hold**, or **Resell**?

[![Deploy to AWS](https://github.com/Camcoder1/pokeAI/workflows/Deploy%20Pokemon%20TCG%20Analyst%20to%20AWS/badge.svg)](https://github.com/Camcoder1/pokeAI/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 What It Does

This tool helps you make data-driven decisions about Pokémon TCG sealed products by:

1. **Fetching Real Data** from Pokémon TCG API and TCGPlayer
2. **Calculating Expected Value (EV)** using actual pull rates and card prices
3. **Modeling ROI** for three scenarios: Opening, Holding, or Reselling
4. **Providing Recommendations** with confidence scores

### Example Analysis Output

```
┌─────────────────────────────────────────────┐
│ Product: 151 Booster Box                    │
│ Sealed Box Cost: $120.00                    │
│ Market Value (sealed): $125.00              │
│ Expected Value (open): $145.50              │
│                                              │
│ ROI if you OPEN:      +$25.50 (+21.3%)     │
│ ROI if you HOLD (6mo): +$18.00 (+15%)      │
│ ROI if you RESELL:     +$5.00 (+4.2%)      │
│                                              │
│ ✅ RECOMMENDATION: OPEN                     │
│ Confidence Score: 87%                        │
└─────────────────────────────────────────────┘
```

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │ ───▶ │ API Gateway  │ ───▶ │   Lambda    │
│  Frontend   │      │              │      │   (Python)  │
│   (S3)      │      └──────────────┘      └─────────────┘
└─────────────┘                                    │
                                                   ▼
                                            ┌─────────────┐
                                            │  DynamoDB   │
                                            │ (Analytics) │
                                            └─────────────┘
```

### AWS Services Used

- **Lambda** - Serverless compute for analysis logic
- **API Gateway** - REST API endpoints
- **DynamoDB** - Database for analytics and caching
- **S3** - Static website hosting for frontend
- **CloudFormation** - Infrastructure as Code (via SAM)

### Cost Estimate

**Expected Monthly Cost: $5-15** (well under $50 budget)

- Lambda: ~$0-5 (1M requests/month free tier)
- DynamoDB: ~$0-5 (25GB storage, 25 read/write units free)
- S3: ~$0-2 (5GB storage, 20K GET requests free)
- API Gateway: ~$0-3 (1M calls free for 12 months)

## 🚀 Quick Start

### Prerequisites

- **AWS Account** with credentials
- **AWS CLI** installed ([Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
- **AWS SAM CLI** installed ([Installation Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html))
- **Node.js 18+** and **Python 3.11+**

### 1. Clone the Repository

```bash
git clone https://github.com/Camcoder1/pokeAI.git
cd pokeAI
```

### 2. Set Up AWS Credentials

```bash
chmod +x setup-aws.sh
./setup-aws.sh
```

This will:
- Verify AWS CLI and SAM CLI installations
- Configure your AWS credentials
- Set up Pokemon TCG API key (optional)

### 3. Deploy to AWS

```bash
chmod +x deploy.sh
./deploy.sh
```

This will:
1. Install backend dependencies
2. Build and deploy the SAM application
3. Build and deploy the React frontend to S3
4. Output your application URLs

### 4. Access Your Application

After deployment, you'll see:

```
✅ Deployment complete!
Frontend URL: http://pokemon-tcg-analyst-XXXXXXXXXXXX.s3-website-us-east-1.amazonaws.com
API URL: https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/
```

Visit the **Frontend URL** in your browser!

## 🧪 Local Development

### Run Backend Locally

```bash
sam local start-api --port 3001
```

### Run Frontend Locally

```bash
cd frontend
REACT_APP_API_URL="http://localhost:3001" npm start
```

### Quick Local Test (Both)

```bash
chmod +x local-test.sh
./local-test.sh
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file (not committed to git):

```env
POKEMON_TCG_API_KEY=your_api_key_here
AWS_REGION=us-east-1
```

### Get Pokemon TCG API Key

1. Visit [pokemontcg.io](https://pokemontcg.io)
2. Sign up for a free API key
3. Add it to your `.env` file or GitHub Secrets

### GitHub Secrets (for CI/CD)

Add these to your GitHub repository secrets:

- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key
- `POKEMON_TCG_API_KEY` - Your Pokemon TCG API key (optional)

## 📊 Features

### Current Features

- ✅ Real-time card price fetching from TCGPlayer
- ✅ Expected value calculation with pull rates
- ✅ ROI comparison (Open vs Hold vs Resell)
- ✅ Trending products dashboard
- ✅ Historical analysis storage
- ✅ Confidence scoring
- ✅ Mobile-responsive UI
- ✅ Serverless architecture

### Planned Features

- [ ] Historical price trends and charts
- [ ] Graded card value calculations (PSA/BGS)
- [ ] Email alerts for price changes
- [ ] Multi-product comparison
- [ ] Advanced analytics dashboard
- [ ] Custom pull rate configuration

## 🎮 How to Use

1. **Select a Set** from the dropdown (e.g., "151", "Shrouded Fable")
2. **Enter Product Type** (e.g., "Booster Box", "Elite Trainer Box")
3. **Optionally Enter Sealed Price** (or let it auto-estimate)
4. **Click "Analyze Product"**
5. **Review the Results**:
   - EV breakdown by card rarity
   - Top value cards contributing to EV
   - ROI for each scenario
   - Final recommendation with confidence score

## 📈 Analytics

All analyses are stored in DynamoDB for future analytics:

- Product popularity trends
- EV trends over time
- Best ROI products
- Community recommendations

## 🛠️ API Endpoints

### `POST /analyze`

Analyze a sealed product.

**Request:**
```json
{
  "set_name": "151",
  "product_name": "151 Booster Box",
  "sealed_price": 120.00
}
```

**Response:**
```json
{
  "product_name": "151 Booster Box",
  "recommendation": "OPEN - Expected value significantly exceeds sealed price",
  "confidence_score": 87,
  "pricing": {
    "sealed_box_cost": 120.00,
    "expected_value_open": 145.50,
    ...
  },
  "roi": { ... },
  "ev_breakdown": { ... }
}
```

### `GET /sets`

List all available Pokemon TCG sets.

### `GET /trending`

Get trending analyses from the community.

### `GET /analyze/{productId}`

Retrieve a previous analysis by ID.

## 🔬 How It Works

### 1. Data Collection

- Fetches card list from Pokemon TCG API
- Gets current market prices from TCGPlayer
- Uses community-validated pull rates

### 2. EV Calculation

```python
EV = Σ (card_price × pull_probability × packs_per_box)
```

For each card:
- If price ≥ $0.40: Include in calculation
- Apply rarity-specific pull rates
- Multiply by 36 packs per box

### 3. ROI Modeling

**Open ROI**: `EV_open - sealed_price`
**Hold ROI**: `projected_6mo_price - sealed_price`
**Resell ROI**: `current_market_price - sealed_price`

### 4. Recommendation Logic

```
IF ev_open > sealed_price × 1.2 AND roi_open% > 20%
  → OPEN

ELSE IF sealed_price_trend_up AND ev_open < sealed_price
  → HOLD SEALED

ELSE IF sealed_price > ev_open × 1.3
  → RESELL SEALED NOW

ELSE
  → HOLD SEALED (marginal)
```

## 🔒 Security

- ✅ AWS credentials stored in GitHub Secrets
- ✅ API keys not committed to repository
- ✅ CORS configured for security
- ✅ DynamoDB encryption at rest
- ✅ IAM least-privilege policies

## 🐛 Troubleshooting

### Deployment Fails

1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify SAM is installed: `sam --version`
3. Check CloudFormation stack in AWS Console

### Frontend Can't Connect to API

1. Check API Gateway URL in browser
2. Verify CORS configuration in `template.yaml`
3. Check browser console for errors

### Rate Limiting

If you see rate limit errors:
1. Get a Pokemon TCG API key (free)
2. Add to `.env` or GitHub Secrets
3. Redeploy

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Credits

- **Pokemon TCG API** - [pokemontcg.io](https://pokemontcg.io)
- **TCGPlayer** - Market price data
- **Community Pull Rates** - Based on verified community data

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/Camcoder1/pokeAI/issues)
- **Email**: [Your email]

---

**⚠️ Disclaimer**: This tool provides estimates based on current market data and community averages. Actual results may vary. Pokemon card values fluctuate. This is not financial advice. Use at your own risk.

**🎮 Happy Collecting!**
