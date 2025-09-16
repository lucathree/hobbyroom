'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { authApi } from '../services/api'

interface User {
  email: string
  sub: string
  iat: number
  exp: number
  persona: any
  affiliated_gatherings: any
}

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (token: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

// JWT decode function (simple base64 decode)
const decodeJWT = (token: string): User | null => {
  try {
    const parts = token.split('.')
    if (parts.length !== 3) {
      return null
    }

    const payload = parts[1]
    // Add padding if needed
    const paddedPayload =
      payload + '=='.substring(0, (4 - (payload.length % 4)) % 4)
    const decoded = atob(paddedPayload)
    const user = JSON.parse(decoded)

    return {
      email: user.sub, // 'sub' field contains the email
      sub: user.sub,
      iat: user.iat,
      exp: user.exp,
      persona: user.persona,
      affiliated_gatherings: user.affiliated_gatherings,
    }
  } catch (error) {
    console.error('Error decoding JWT:', error)
    return null
  }
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check for existing token on mount
    const token = authApi.getToken()
    if (token) {
      const decodedUser = decodeJWT(token)
      if (decodedUser) {
        // Check if token is expired
        const currentTime = Date.now() / 1000
        if (decodedUser.exp > currentTime) {
          setUser(decodedUser)
        } else {
          // Token expired, remove it
          authApi.logout()
        }
      }
    }
    setIsLoading(false)
  }, [])

  const login = (token: string) => {
    authApi.setToken(token)
    const decodedUser = decodeJWT(token)
    if (decodedUser) {
      setUser(decodedUser)
    }
  }

  const logout = () => {
    authApi.logout()
    setUser(null)
  }

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
