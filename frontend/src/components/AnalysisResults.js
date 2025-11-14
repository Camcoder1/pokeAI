import React from 'react';
import './AnalysisResults.css';

const AnalysisResults = ({ analysis }) => {
  const getRecommendationClass = (recommendation) => {
    if (recommendation.includes('OPEN')) return 'recommendation-open';
    if (recommendation.includes('HOLD')) return 'recommendation-hold';
    if (recommendation.includes('RESELL')) return 'recommendation-resell';
    return '';
  };

  const getConfidenceColor = (score) => {
    if (score >= 80) return '#4caf50';
    if (score >= 60) return '#ff9800';
    return '#f44336';
  };

  return (
    <div className="analysis-results">
      <div className="card">
        <h2>📊 Analysis Results</h2>

        {/* Product Info */}
        <div className="product-info">
          <h3>{analysis.product_name}</h3>
          <p className="set-name">{analysis.set_name}</p>
        </div>

        {/* Recommendation */}
        <div className={`recommendation-badge ${getRecommendationClass(analysis.recommendation)}`}>
          <div className="recommendation-text">{analysis.recommendation}</div>
          <div className="confidence-score" style={{ color: getConfidenceColor(analysis.confidence_score) }}>
            Confidence: {analysis.confidence_score}%
          </div>
        </div>

        {/* Pricing Table */}
        <div className="pricing-table">
          <h3>💰 Pricing Summary</h3>
          <table>
            <tbody>
              <tr>
                <td>Sealed Box Cost:</td>
                <td className="price">${analysis.pricing.sealed_box_cost.toFixed(2)}</td>
              </tr>
              <tr>
                <td>Market Value (Sealed):</td>
                <td className="price">${analysis.pricing.market_value_sealed.toFixed(2)}</td>
              </tr>
              <tr>
                <td>Expected Value (Open):</td>
                <td className="price highlight">${analysis.pricing.expected_value_open.toFixed(2)}</td>
              </tr>
              <tr>
                <td>Projected 6mo Price:</td>
                <td className="price">${analysis.pricing.projected_6mo_sealed.toFixed(2)}</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* ROI Comparison */}
        <div className="roi-section">
          <h3>📈 ROI Comparison</h3>
          <div className="roi-grid">
            <div className="roi-card">
              <div className="roi-label">If You Open</div>
              <div className="roi-amount" style={{ color: analysis.roi.open.percent > 0 ? '#4caf50' : '#f44336' }}>
                ${analysis.roi.open.amount.toFixed(2)}
              </div>
              <div className="roi-percent">
                {analysis.roi.open.percent > 0 ? '+' : ''}{analysis.roi.open.percent.toFixed(1)}%
              </div>
            </div>

            <div className="roi-card">
              <div className="roi-label">If You Hold (6mo)</div>
              <div className="roi-amount" style={{ color: analysis.roi.hold_6mo.percent > 0 ? '#4caf50' : '#f44336' }}>
                ${analysis.roi.hold_6mo.amount.toFixed(2)}
              </div>
              <div className="roi-percent">
                {analysis.roi.hold_6mo.percent > 0 ? '+' : ''}{analysis.roi.hold_6mo.percent.toFixed(1)}%
              </div>
            </div>

            <div className="roi-card">
              <div className="roi-label">If You Resell Now</div>
              <div className="roi-amount" style={{ color: analysis.roi.resell_now.percent > 0 ? '#4caf50' : '#f44336' }}>
                ${analysis.roi.resell_now.amount.toFixed(2)}
              </div>
              <div className="roi-percent">
                {analysis.roi.resell_now.percent > 0 ? '+' : ''}{analysis.roi.resell_now.percent.toFixed(1)}%
              </div>
            </div>
          </div>
        </div>

        {/* Top Contributing Cards */}
        {analysis.ev_breakdown && analysis.ev_breakdown.top_cards && analysis.ev_breakdown.top_cards.length > 0 && (
          <div className="top-cards-section">
            <h3>💎 Top Value Cards (Contributing ≥5% to EV)</h3>
            <div className="cards-grid">
              {analysis.ev_breakdown.top_cards.slice(0, 10).map((card, idx) => (
                <div key={idx} className="card-item">
                  {card.image && (
                    <img src={card.image} alt={card.name} className="card-image" />
                  )}
                  <div className="card-details">
                    <div className="card-name">{card.name}</div>
                    <div className="card-rarity">{card.rarity}</div>
                    <div className="card-price">${card.price.toFixed(2)}</div>
                    <div className="card-ev">EV: ${card.ev_contribution.toFixed(2)}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Assumptions */}
        <div className="assumptions-section">
          <h3>ℹ️ Assumptions & Data Sources</h3>
          <ul>
            <li>Packs per box: {analysis.assumptions.packs_per_box}</li>
            <li>Pull rates: {analysis.assumptions.pull_rates}</li>
            <li>Min card value included: ${analysis.assumptions.min_card_value}</li>
            <li>Hold projection period: {analysis.assumptions.hold_period}</li>
            <li>Sealed appreciation estimate: {analysis.assumptions.appreciation_estimate}</li>
          </ul>
          <div className="api-sources">
            <strong>API Sources:</strong>
            <ul>
              {analysis.api_sources.map((source, idx) => (
                <li key={idx}>{source}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisResults;
