import React from 'react'
import Header from '../src/components/Header'

const communities = [
  {
    id: 1,
    title: 'Photography Enthusiasts',
    description:
      'Connect with fellow photographers, share tips, and explore new techniques. All skill levels welcome!',
    image: '/sample.jpg',
  },
  {
    id: 2,
    title: 'Board Game Masters',
    description:
      'Gather for epic board game nights, discover new releases, and challenge your strategic thinking.',
    image: '/sample.jpg',
  },
  {
    id: 3,
    title: 'Creative Writers Guild',
    description:
      'Join a supportive community of writers. Share your stories, get feedback, and find inspiration.',
    image: '/sample.jpg',
  },
  {
    id: 4,
    title: 'Outdoor Adventurers',
    description:
      'Explore hiking trails, plan camping trips, and connect with nature lovers.',
    image: '/sample.jpg',
  },
  {
    id: 5,
    title: 'Culinary Explorers',
    description:
      'Share recipes, discover new cuisines, and master cooking techniques with fellow foodies.',
    image: '/sample.jpg',
  },
  {
    id: 6,
    title: 'DIY Craft Collective',
    description:
      'Unleash your creativity with DIY projects, crafting workshops, and handmade goods exchange.',
    image: '/sample.jpg',
  },
]

const LandingPage: React.FC = () => {
  return (
    <div className="landing-page">
      {/* Header */}
      <Header />

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <div className="hero-text">
            <h2 className="hero-title">Discover Your Community</h2>
            <p className="hero-description">
              HobbyRoom connects you with like-minded individuals through shared
              passions. Explore diverse groups, join exciting events, and find
              your tribe.
            </p>
            <button className="cta-button">Explore Communities</button>
          </div>
          <div className="hero-image">
            <img
              src="/sample.jpg"
              alt="People reading together"
              className="hero-img"
            />
          </div>
        </div>
      </section>

      {/* Communities Section */}
      <section className="communities">
        <div className="communities-content">
          <h2 className="communities-title">Explore Popular Communities</h2>
          <div className="communities-grid">
            {communities.map(community => (
              <div key={community.id} className="community-card">
                <img
                  src={community.image}
                  alt={community.title}
                  className="community-image"
                />
                <div className="community-content">
                  <h3 className="community-title">{community.title}</h3>
                  <p className="community-description">
                    {community.description}
                  </p>
                  <button className="join-button">Join</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <p>&copy; 2024 HobbyRoom. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage
