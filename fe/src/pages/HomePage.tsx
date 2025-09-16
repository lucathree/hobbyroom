import React from 'react'

const HomePage: React.FC = () => {
  return (
    <div className="home-page">
      <header>
        <h1>HobbyRoom</h1>
        <p>취미 기반 모임을 만들고 참여하세요</p>
      </header>
      <main>
        <section>
          <h2>환영합니다!</h2>
          <p>
            HobbyRoom에서 당신의 취미를 공유하고 새로운 사람들과 만나보세요.
          </p>
        </section>
      </main>
    </div>
  )
}

export default HomePage
