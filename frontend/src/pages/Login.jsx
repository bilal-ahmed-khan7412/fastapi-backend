import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import './Login.css'

function Login({ onLogin }) {
  const [searchParams] = useSearchParams()
  const roleFromUrl = searchParams.get('role') || 'worker'
  
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    role: roleFromUrl
  })

  useEffect(() => {
    setFormData(prev => ({ ...prev, role: roleFromUrl }))
  }, [roleFromUrl])

  const handleSubmit = (e) => {
    e.preventDefault()
    
    // Simple validation (for prototype)
    if (formData.username && formData.password) {
      onLogin({
        username: formData.username,
        role: formData.role,
        id: Math.random().toString(36).substr(2, 9)
      })
    } else {
      alert('Please enter username and password')
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>Sealant Detection System</h1>
          <p>Please login to continue</p>
        </div>
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className={`role-badge role-badge-${formData.role}`}>
            <span className="role-icon">
              {formData.role === 'worker' ? '👷' : '👔'}
            </span>
            <div className="role-info">
              <span className="role-label">Logging in as</span>
              <span className="role-value">{formData.role.charAt(0).toUpperCase() + formData.role.slice(1)}</span>
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              placeholder="Enter your username"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              required
            />
          </div>

          <button type="submit" className="login-button">
            Login
          </button>
        </form>

        <div className="login-footer">
          <p>Use any credentials for prototype</p>
        </div>
      </div>
    </div>
  )
}

export default Login

