import React from 'react';
import './SetSelector.css';

const SetSelector = ({ sets, selectedSet, onSelectSet }) => {
  return (
    <div className="set-selector">
      <h3>Select a Set</h3>
      <div className="sets-grid">
        {sets.map((set) => (
          <div
            key={set.id}
            className={`set-card ${selectedSet === set.name ? 'selected' : ''}`}
            onClick={() => onSelectSet(set.name)}
            role="button"
            tabIndex={0}
          >
            {set.logo && (
              <img src={set.logo} alt={set.name} className="set-logo" />
            )}
            <div className="set-info">
              <div className="set-name">{set.name}</div>
              <div className="set-series">{set.series}</div>
              <div className="set-details">
                {set.total_cards} cards • {new Date(set.release_date).getFullYear()}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SetSelector;
