'use client'

import React from 'react'
import Link from 'next/link'
import { useAuth } from '../contexts/AuthContext'

const Header: React.FC = () => {
  const { user, isAuthenticated, logout, isLoading } = useAuth()

  const handleLogout = () => {
    logout()
    // Optionally redirect to login page
    window.location.href = '/'
  }

  return (
    <header className="header">
      <div className="header-content">
        <Link href="/" className="logo">
          🌟 HobbyRoom
        </Link>
        <nav className="nav">
          <a href="#" className="nav-link">
            Home
          </a>
          {isLoading ? (
            <div className="auth-loading">Loading...</div>
          ) : isAuthenticated && user ? (
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          ) : (
            <Link href="/login" className="login-btn">
              Login
            </Link>
          )}
        </nav>
      </div>
    </header>
  )
}

export default Header
