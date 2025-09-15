export interface User {
  id: string
  email: string
  isDeactivated: boolean
  createdAt: string
  updatedAt: string
}

export interface Persona {
  id: string
  userId: string
  name: string
  createdAt: string
  updatedAt: string
}

export interface Gathering {
  id: string
  name: string
  description: string
  createdAt: string
  updatedAt: string
}

export interface Affiliation {
  personaId: string
  gatheringId: string
  isLeader: boolean
  joinedAt: string
}

export interface Post {
  id: string
  gatheringId: string
  personaId: string
  title: string
  content: string
  createdAt: string
  updatedAt: string
}
