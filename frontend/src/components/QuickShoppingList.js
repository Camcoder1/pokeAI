import React, { useState } from 'react';
import './QuickShoppingList.css';

const QuickShoppingList = () => {
  const [checkedCards, setCheckedCards] = useState({});

  // Top chase cards to look for at card shops
  const topCards = [
    { name: 'Charizard ex (Special Illustration)', set: '151', price: 285, number: '199', rarity: 'SIR' },
    { name: 'Mew ex (Special Illustration)', set: '151', price: 175, number: '205', rarity: 'SIR' },
    { name: 'Mewtwo ex (Special Illustration)', set: '151', price: 140, number: '206', rarity: 'SIR' },
    { name: 'Charizard ex', set: '151', price: 45, number: '6', rarity: 'Double Rare' },
    { name: 'Mew ex', set: '151', price: 35, number: '151', rarity: 'Double Rare' },
    { name: 'Erika\'s Invitation (Full Art)', set: '151', price: 32, number: '196', rarity: 'Ultra Rare' },
    { name: 'Mewtwo ex', set: '151', price: 28, number: '150', rarity: 'Double Rare' },
    { name: 'Zapdos ex (Full Art)', set: '151', price: 18.50, number: '182', rarity: 'Ultra Rare' },
    { name: 'Moltres ex (Full Art)', set: '151', price: 15, number: '184', rarity: 'Ultra Rare' },
    { name: 'Pikachu (Illustration Rare)', set: '151', price: 12, number: '25', rarity: 'Illustration Rare' },
  ];

  const toggleCard = (index) => {
    setCheckedCards(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  const clearAll = () => {
    setCheckedCards({});
  };

  const checkedCount = Object.values(checkedCards).filter(Boolean).length;

  return (
    <div className="quick-shopping-list">
      <div className="card shopping-card">
        <div className="shopping-header">
          <div>
            <h2>🎯 Quick Shopping List</h2>
            <p className="shopping-subtitle">
              Top {topCards.length} cards to hunt for - Check them off as you find them!
            </p>
          </div>
          <div className="shopping-stats">
            <div className="stat-bubble">
              <span className="stat-number">{checkedCount}</span>
              <span className="stat-label">Found</span>
            </div>
            {checkedCount > 0 && (
              <button onClick={clearAll} className="btn-clear">
                Clear All
              </button>
            )}
          </div>
        </div>

        <div className="shopping-list-container">
          {topCards.map((card, idx) => (
            <div
              key={idx}
              className={`shopping-list-item ${checkedCards[idx] ? 'checked' : ''}`}
              onClick={() => toggleCard(idx)}
            >
              <div className="item-checkbox">
                <input
                  type="checkbox"
                  checked={checkedCards[idx] || false}
                  onChange={() => toggleCard(idx)}
                  onClick={(e) => e.stopPropagation()}
                />
              </div>

              <div className="item-rank">#{idx + 1}</div>

              <div className="item-details">
                <div className="item-name">{card.name}</div>
                <div className="item-meta">
                  <span className="item-set">{card.set}</span>
                  <span className="item-separator">•</span>
                  <span className="item-number">#{card.number}</span>
                  <span className="item-separator">•</span>
                  <span className="item-rarity">{card.rarity}</span>
                </div>
              </div>

              <div className="item-price">
                ${card.price.toFixed(card.price % 1 === 0 ? 0 : 2)}
              </div>
            </div>
          ))}
        </div>

        <div className="shopping-footer">
          <div className="total-value">
            <span className="total-label">Total Value:</span>
            <span className="total-amount">
              ${topCards.reduce((sum, card) => sum + card.price, 0).toFixed(0)}
            </span>
          </div>
          <div className="shopping-tip">
            💡 Tap cards to check them off as you find them at shops!
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuickShoppingList;
