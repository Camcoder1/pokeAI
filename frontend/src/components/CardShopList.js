import React, { useState } from 'react';
import './CardShopList.css';

const CardShopList = ({ cards, setName }) => {
  const [sortBy, setSortBy] = useState('price'); // price, ev, name
  const [filterRarity, setFilterRarity] = useState('all');
  const [showOnlyHighValue, setShowOnlyHighValue] = useState(false);

  if (!cards || cards.length === 0) {
    return null;
  }

  // Get unique rarities
  const rarities = ['all', ...new Set(cards.map(c => c.rarity))];

  // Filter and sort cards
  let displayCards = [...cards];

  // Filter by rarity
  if (filterRarity !== 'all') {
    displayCards = displayCards.filter(c => c.rarity === filterRarity);
  }

  // Filter high value only
  if (showOnlyHighValue) {
    displayCards = displayCards.filter(c => c.price >= 5.0);
  }

  // Sort
  displayCards.sort((a, b) => {
    switch (sortBy) {
      case 'price':
        return b.price - a.price;
      case 'ev':
        return b.ev_contribution - a.ev_contribution;
      case 'name':
        return a.name.localeCompare(b.name);
      default:
        return 0;
    }
  });

  const handlePrint = () => {
    window.print();
  };

  const handleExport = () => {
    const csvContent = [
      ['Card Name', 'Rarity', 'Price', 'Pull Rate', 'EV Contribution', 'Set Number'],
      ...displayCards.map(card => [
        card.name,
        card.rarity,
        `$${card.price.toFixed(2)}`,
        `1/${Math.round(1/card.pull_rate)} packs`,
        `$${card.ev_contribution.toFixed(2)}`,
        card.set_number
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${setName.replace(/\s+/g, '_')}_card_list.csv`;
    a.click();
  };

  return (
    <div className="card-shop-list">
      <div className="card">
        <div className="card-shop-header">
          <h2>💎 Card Shop Reference List - {setName}</h2>
          <p className="card-shop-subtitle">
            {displayCards.length} valuable cards • Perfect for in-store hunting
          </p>
        </div>

        {/* Controls */}
        <div className="card-shop-controls no-print">
          <div className="control-group">
            <label>Sort by:</label>
            <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
              <option value="price">Price (High to Low)</option>
              <option value="ev">EV Contribution</option>
              <option value="name">Name (A-Z)</option>
            </select>
          </div>

          <div className="control-group">
            <label>Filter:</label>
            <select value={filterRarity} onChange={(e) => setFilterRarity(e.target.value)}>
              {rarities.map(r => (
                <option key={r} value={r}>
                  {r === 'all' ? 'All Rarities' : r}
                </option>
              ))}
            </select>
          </div>

          <div className="control-group checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={showOnlyHighValue}
                onChange={(e) => setShowOnlyHighValue(e.target.checked)}
              />
              Only show $5+ cards
            </label>
          </div>

          <div className="control-group action-buttons">
            <button onClick={handlePrint} className="btn-print">
              🖨️ Print List
            </button>
            <button onClick={handleExport} className="btn-export">
              📄 Export CSV
            </button>
          </div>
        </div>

        {/* Card Grid */}
        <div className="card-shop-grid">
          {displayCards.map((card, idx) => (
            <div key={idx} className="shop-card-item">
              <div className="shop-card-image-container">
                {card.image ? (
                  <img
                    src={card.image}
                    alt={card.name}
                    className="shop-card-image"
                    loading="lazy"
                  />
                ) : (
                  <div className="shop-card-placeholder">No Image</div>
                )}
                <div className="shop-card-number">#{card.set_number}</div>
              </div>

              <div className="shop-card-details">
                <div className="shop-card-name">{card.name}</div>
                <div className="shop-card-rarity">{card.rarity}</div>

                <div className="shop-card-stats">
                  <div className="shop-stat">
                    <span className="shop-stat-label">Market Price:</span>
                    <span className="shop-stat-value price-highlight">
                      ${card.price.toFixed(2)}
                    </span>
                  </div>

                  <div className="shop-stat">
                    <span className="shop-stat-label">Pull Rate:</span>
                    <span className="shop-stat-value">
                      1 in {Math.round(1/card.pull_rate)} packs
                    </span>
                  </div>

                  <div className="shop-stat">
                    <span className="shop-stat-label">EV per Box:</span>
                    <span className="shop-stat-value">
                      ${card.ev_contribution.toFixed(2)}
                    </span>
                  </div>
                </div>

                {card.price >= 10 && (
                  <div className="shop-card-badge high-value">High Value!</div>
                )}
                {card.price >= 50 && (
                  <div className="shop-card-badge chase-card">Chase Card!</div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Summary Stats */}
        <div className="card-shop-summary no-print">
          <h3>Quick Stats</h3>
          <div className="summary-grid">
            <div className="summary-item">
              <div className="summary-label">Total Cards Shown:</div>
              <div className="summary-value">{displayCards.length}</div>
            </div>
            <div className="summary-item">
              <div className="summary-label">Highest Value:</div>
              <div className="summary-value">
                ${Math.max(...displayCards.map(c => c.price)).toFixed(2)}
              </div>
            </div>
            <div className="summary-item">
              <div className="summary-label">Cards Over $10:</div>
              <div className="summary-value">
                {displayCards.filter(c => c.price >= 10).length}
              </div>
            </div>
            <div className="summary-item">
              <div className="summary-label">Cards Over $50:</div>
              <div className="summary-value">
                {displayCards.filter(c => c.price >= 50).length}
              </div>
            </div>
          </div>
        </div>

        {/* Mobile tip */}
        <div className="mobile-tip no-print">
          💡 <strong>Tip:</strong> Bookmark this page on your phone to use at card shops!
        </div>
      </div>
    </div>
  );
};

export default CardShopList;
