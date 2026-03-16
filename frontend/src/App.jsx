import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [stage, setStage] = useState('');
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  const [showReviews, setShowReviews] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    setLoading(true);
    setResult(null);
    setStage('Stage 1: Getting responses from council members...');

    try {
      const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      setResult(data);
      setStage('');
    } catch (error) {
      console.error('Error:', error);
      alert('Error communicating with the council. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🧠 Consilience</h1>
        <p>Where AI minds converge to answer your hardest questions</p>
      </header>

      <div className="container">
        <form onSubmit={handleSubmit} className="query-form">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask your question..."
            className="query-input"
            disabled={loading}
          />
          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Processing...' : 'Ask Council'}
          </button>
        </form>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>{stage}</p>
          </div>
        )}

        {result && (
          <>
            <div className="section">
              <h2>📝 Stage 1: Individual Responses</h2>
              <div className="tabs">
                {result.stage1_responses.map((resp, idx) => (
                  <button
                    key={idx}
                    className={`tab ${activeTab === idx ? 'active' : ''}`}
                    onClick={() => setActiveTab(idx)}
                  >
                    {resp.model_name}
                  </button>
                ))}
              </div>
              <div className="tab-content">
                {result.stage1_responses[activeTab] && (
                  <div className="response">
                    <h3>{result.stage1_responses[activeTab].model_name}</h3>
                    <p>{result.stage1_responses[activeTab].response}</p>
                  </div>
                )}
              </div>
            </div>

            <div className="section">
              <h2>
                🔍 Stage 2: Peer Reviews
                <button 
                  className="toggle-btn"
                  onClick={() => setShowReviews(!showReviews)}
                >
                  {showReviews ? 'Hide' : 'Show'} Reviews
                </button>
              </h2>
              {showReviews && (
                <div className="reviews-grid">
                  {result.stage2_reviews.map((review, idx) => (
                    <div key={idx} className="review-card">
                      <h4>{review.model_name}</h4>
                      <p>{review.review}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="section final-answer">
              <h2>👑 Stage 3: Chairman's Final Answer</h2>
              <div className="final-content">
                <p>{result.stage3_final}</p>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
