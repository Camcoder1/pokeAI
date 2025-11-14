import React from 'react';
import './TrendingProducts.css';

const TrendingProducts = ({ trending, onSelect }) => {
  if (!trending || trending.length === 0) {
    return null;
  }

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp * 1000);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  const getROIClass = (roi) => {
    if (roi > 10) return 'roi-high';
    if (roi > 0) return 'roi-medium';
    return 'roi-low';
  };

  return (
    <div className="trending-products">
      <div className="card">
        <h2>🔥 Trending Analyses</h2>
        <p className="trending-subtitle">Recently analyzed products by the community</p>

        <div className="trending-list">
          {trending.map((item, idx) => (
            <div
              key={idx}
              className="trending-item"
              onClick={() => onSelect(item)}
              role="button"
              tabIndex={0}
            >
              <div className="trending-header">
                <div className="trending-product-name">{item.product_name}</div>
                <div className="trending-set">{item.set_name}</div>
              </div>

              <div className="trending-stats">
                <div className="stat">
                  <span className="stat-label">EV Open:</span>
                  <span className="stat-value">${item.ev_open?.toFixed(2) || 'N/A'}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Sealed:</span>
                  <span className="stat-value">${item.sealed_price?.toFixed(2) || 'N/A'}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">ROI:</span>
                  <span className={`stat-value ${getROIClass(item.roi_percent)}`}>
                    {item.roi_percent > 0 ? '+' : ''}{item.roi_percent?.toFixed(1) || '0'}%
                  </span>
                </div>
              </div>

              <div className="trending-recommendation">
                {item.recommendation}
              </div>

              {item.timestamp && (
                <div className="trending-timestamp">
                  {formatTimestamp(item.timestamp)}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TrendingProducts;
