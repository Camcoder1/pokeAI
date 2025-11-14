import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import AnalysisResults from './components/AnalysisResults';
import TrendingProducts from './components/TrendingProducts';
import SetSelector from './components/SetSelector';

// API endpoint - will be replaced with actual API Gateway URL after deployment
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-api-gateway-url.execute-api.us-east-1.amazonaws.com/prod';

function App() {
  const [sets, setSets] = useState([]);
  const [selectedSet, setSelectedSet] = useState('');
  const [productName, setProductName] = useState('');
  const [sealedPrice, setSealedPrice] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);
  const [trending, setTrending] = useState([]);

  // Load sets on mount
  useEffect(() => {
    loadSets();
    loadTrending();
  }, []);

  const loadSets = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/sets`);
      setSets(response.data.sets || []);
    } catch (err) {
      console.error('Failed to load sets:', err);
    }
  };

  const loadTrending = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/trending`);
      setTrending(response.data.trending || []);
    } catch (err) {
      console.error('Failed to load trending:', err);
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const payload = {
        set_name: selectedSet,
        product_name: productName || `${selectedSet} Booster Box`,
        sealed_price: sealedPrice ? parseFloat(sealedPrice) : null
      };

      const response = await axios.post(`${API_BASE_URL}/analyze`, payload);
      setAnalysis(response.data);

      // Refresh trending
      loadTrending();
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSetChange = (e) => {
    const setName = e.target.value;
    setSelectedSet(setName);
    // Auto-populate product name
    if (setName && !productName) {
      setProductName(`${setName} Booster Box`);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>⚡ Pokémon TCG Market Analyst</h1>
        <p className="subtitle">AI-Powered Open vs Hold vs Resell Analysis</p>
      </header>

      <div className="container">
        <div className="main-content">
          {/* Analysis Form */}
          <div className="card form-card">
            <h2>Analyze Sealed Product</h2>

            <form onSubmit={handleAnalyze}>
              <div className="form-group">
                <label htmlFor="set-select">Select Set:</label>
                <select
                  id="set-select"
                  value={selectedSet}
                  onChange={handleSetChange}
                  required
                  disabled={loading}
                >
                  <option value="">-- Choose a Set --</option>
                  {sets.map(set => (
                    <option key={set.id} value={set.name}>
                      {set.name} ({set.series})
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="product-name">Product Name:</label>
                <input
                  id="product-name"
                  type="text"
                  placeholder="e.g., 151 Booster Box"
                  value={productName}
                  onChange={(e) => setProductName(e.target.value)}
                  required
                  disabled={loading}
                />
                <small>e.g., "Booster Box", "Elite Trainer Box (ETB)", "Booster Bundle"</small>
              </div>

              <div className="form-group">
                <label htmlFor="sealed-price">Sealed Price (Optional):</label>
                <input
                  id="sealed-price"
                  type="number"
                  step="0.01"
                  placeholder="Auto-estimated if left blank"
                  value={sealedPrice}
                  onChange={(e) => setSealedPrice(e.target.value)}
                  disabled={loading}
                />
                <small>Leave blank to use estimated market price</small>
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading || !selectedSet}
              >
                {loading ? '🔍 Analyzing...' : '🚀 Analyze Product'}
              </button>
            </form>

            {error && (
              <div className="error-message">
                <strong>Error:</strong> {error}
              </div>
            )}
          </div>

          {/* Analysis Results */}
          {analysis && (
            <AnalysisResults analysis={analysis} />
          )}

          {/* Trending Products */}
          {trending.length > 0 && (
            <TrendingProducts
              trending={trending}
              onSelect={(item) => {
                setSelectedSet(item.set_name);
                setProductName(item.product_name);
              }}
            />
          )}
        </div>
      </div>

      <footer className="App-footer">
        <p>
          Data sourced from{' '}
          <a href="https://pokemontcg.io" target="_blank" rel="noopener noreferrer">
            Pokémon TCG API
          </a>
          {' '}and TCGPlayer
        </p>
        <p className="disclaimer">
          ⚠️ Disclaimer: This tool provides estimates based on current market data and community averages.
          Actual results may vary. Not financial advice.
        </p>
      </footer>
    </div>
  );
}

export default App;
