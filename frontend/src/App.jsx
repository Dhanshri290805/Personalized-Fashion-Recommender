import { useState } from 'react'
import axios from 'axios'
import { ThumbsUp, ThumbsDown, Sparkles, Shirt } from 'lucide-react'
import './index.css'

const API_BASE = 'http://localhost:8000/api'
const IMAGE_BASE = 'http://localhost:8000/'

function App() {
  const [preferences, setPreferences] = useState({
    category: '',
    color: '',
    style: '',
    occasion: '',
    budget: '',
    gender: ''
  })
  
  const [recommendations, setRecommendations] = useState([])
  const [outfit, setOutfit] = useState(null)
  const [loading, setLoading] = useState(false)
  const [loadingText, setLoadingText] = useState('')
  const [errorMsg, setErrorMsg] = useState('')

  const handleChange = (e) => {
    setPreferences({ ...preferences, [e.target.name]: e.target.value })
  }

  const getRecommendations = async () => {
    setLoading(true)
    setLoadingText('Finding the best fashion recommendations...')
    setErrorMsg('')
    try {
      const prefs = { ...preferences, budget: preferences.budget ? parseFloat(preferences.budget) : null }
      const res = await axios.post(`${API_BASE}/recommend`, prefs)
      if (res.data.recommendations && res.data.recommendations.length > 0) {
        setRecommendations(res.data.recommendations)
        setOutfit(null)
      } else {
        setErrorMsg('No recommendations found for your preferences.')
        setRecommendations([])
      }
    } catch (err) {
      console.error(err)
      setErrorMsg('Backend is not running. Please start the backend server.')
    }
    setLoading(false)
  }

  const generateOutfit = async () => {
    setLoading(true)
    setLoadingText('Creating your personalized outfit...')
    setErrorMsg('')
    try {
      const prefs = { ...preferences, budget: preferences.budget ? parseFloat(preferences.budget) : null }
      const res = await axios.post(`${API_BASE}/outfit`, prefs)
      if (res.data && Object.keys(res.data).length > 0) {
        setOutfit(res.data)
        if (prefs.budget && res.data.total_price > prefs.budget) {
          setErrorMsg('No complete outfit found within your budget. Showing the closest available option.')
        }
        setRecommendations([])
      } else {
        setErrorMsg('No complete outfit found within your preferences.')
        setOutfit(null)
      }
    } catch (err) {
      console.error(err)
      setErrorMsg('Backend is not running. Please start the backend server.')
    }
    setLoading(false)
  }

  const handleFeedback = async (itemId, type) => {
    try {
      await axios.post(`${API_BASE}/feedback`, {
        item_id: itemId,
        user_id: 1, // dummy user
        feedback_type: type
      })
      alert(`Feedback recorded: ${type}`)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="container">
      <header>
        <h1>Personalized Fashion Recommender</h1>
        <p>AI-Based Personalized Clothing & Outfit Recommendations</p>
      </header>

      <div className="form-container">
        <div className="form-grid">
          <div className="form-group">
            <label>Gender</label>
            <select name="gender" onChange={handleChange} value={preferences.gender}>
              <option value="">Any</option>
              <option value="Men">Men</option>
              <option value="Women">Women</option>
              <option value="Unisex">Unisex</option>
            </select>
          </div>
          <div className="form-group">
            <label>Category</label>
            <select name="category" onChange={handleChange} value={preferences.category}>
              <option value="">Any</option>
              <option value="T-shirt">T-shirt</option>
              <option value="Shirt">Shirt</option>
              <option value="Jeans">Jeans</option>
              <option value="Trousers">Trousers</option>
              <option value="Dress">Dress</option>
              <option value="Shoes">Shoes</option>
            </select>
          </div>
          <div className="form-group">
            <label>Preferred Color</label>
            <select name="color" onChange={handleChange} value={preferences.color}>
              <option value="">Any</option>
              <option value="Black">Black</option>
              <option value="White">White</option>
              <option value="Blue">Blue</option>
              <option value="Red">Red</option>
            </select>
          </div>
          <div className="form-group">
            <label>Style</label>
            <select name="style" onChange={handleChange} value={preferences.style}>
              <option value="">Any</option>
              <option value="Casual">Casual</option>
              <option value="Formal">Formal</option>
              <option value="Streetwear">Streetwear</option>
              <option value="Party">Party</option>
            </select>
          </div>
          <div className="form-group">
            <label>Occasion</label>
            <select name="occasion" onChange={handleChange} value={preferences.occasion}>
              <option value="">Any</option>
              <option value="College">College</option>
              <option value="Office">Office</option>
              <option value="Party">Party</option>
              <option value="Gym">Gym</option>
            </select>
          </div>
          <div className="form-group">
            <label>Max Budget (₹)</label>
            <input type="number" name="budget" onChange={handleChange} value={preferences.budget} placeholder="e.g. 3000" />
          </div>
        </div>
        
        <div className="actions">
          <button className="btn-primary" onClick={getRecommendations} disabled={loading}>
            <Shirt size={20} /> Recommend Fashion
          </button>
          <button className="btn-secondary" onClick={generateOutfit} disabled={loading}>
            <Sparkles size={20} /> Generate Outfit
          </button>
        </div>
        {loading && <div className="loading-state">{loadingText}</div>}
        {errorMsg && <div className="error-state" style={{color: 'red', marginTop: '1rem', textAlign: 'center'}}>{errorMsg}</div>}
      </div>

      {recommendations.length > 0 && (
        <div>
          <h2 className="section-title">Top Recommendations</h2>
          <div className="recommendations-grid">
            {recommendations.map(item => (
              <div key={item.item_id} className="card">
                <div className="card-img-wrapper">
                  <img src={`${IMAGE_BASE}${item.image_path}`} alt={item.item_name} />
                </div>
                <div className="card-content">
                  <div className="card-title">{item.item_name}</div>
                  <div className="card-details">
                    <span>Category: {item.category}</span>
                    <span>Style: {item.style}</span>
                    <span>Occasion: {item.occasion}</span>
                  </div>
                  <div className="card-price">₹{item.price}</div>
                  <div className="card-score">Recommendation: {Math.round(item.recommendation_score)}%</div>
                  <div className="card-actions">
                    <button className="btn-icon" onClick={() => handleFeedback(item.item_id, 'liked')}>
                      <ThumbsUp size={18} /> Like
                    </button>
                    <button className="btn-icon" onClick={() => handleFeedback(item.item_id, 'disliked')}>
                      <ThumbsDown size={18} /> Dislike
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {outfit && (
        <div className="outfit-container">
          <h2 className="section-title">Your Personalized Outfit</h2>
          
          {outfit.outfit_image && (
            <div className="generated-outfit-image" style={{ textAlign: 'center', marginBottom: '2rem' }}>
              <h3 style={{ marginBottom: '1rem' }}>Generated Outfit Image</h3>
              <img 
                src={`${IMAGE_BASE.replace(/\/$/, '')}${outfit.outfit_image}`} 
                alt="Generated Outfit" 
                style={{ maxWidth: '100%', maxHeight: '600px', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', objectFit: 'contain' }} 
              />
            </div>
          )}

          <h3 style={{ textAlign: 'center', marginBottom: '1.5rem' }}>Outfit Details</h3>
          <div className="outfit-scores">
            <div className="score-badge">
              <div className="score-value">{outfit.compatibility_score}%</div>
              <div className="score-label">Compatibility Score</div>
            </div>
            <div className="score-badge">
              <div className="score-value">{outfit.personalization_score}%</div>
              <div className="score-label">Personalization Score</div>
            </div>
          </div>
          
          <div className="outfit-total" style={{textAlign: 'center', fontSize: '1.2rem', fontWeight: 'bold', margin: '1rem 0'}}>
            Total Price: ₹{outfit.total_price}
          </div>
          
          <div className="outfit-items">
            {['top', 'bottom', 'shoes', 'accessory'].map(type => (
              outfit[type] && outfit[type].item_id && (
                <div key={type} className="outfit-item">
                  <div className="outfit-item-type">{type.toUpperCase()}</div>
                  <div className="card">
                    <div className="card-img-wrapper" style={{ height: '200px' }}>
                      <img src={`${IMAGE_BASE}${outfit[type].image_path}`} alt={outfit[type].item_name} />
                    </div>
                    <div className="card-content" style={{ padding: '1rem' }}>
                      <div className="card-title" style={{ fontSize: '1rem' }}>{outfit[type].item_name}</div>
                      <div className="card-price" style={{ fontSize: '1rem', marginBottom: 0 }}>₹{outfit[type].price}</div>
                    </div>
                  </div>
                </div>
              )
            ))}
          </div>
          
          <div style={{ marginTop: '2rem', textAlign: 'center' }}>
            <button className="btn-secondary" onClick={generateOutfit} disabled={loading}>
              <Sparkles size={20} /> Regenerate Outfit
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
