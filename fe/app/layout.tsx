import Providers from './providers'
import '../src/styles/index.css'

export const metadata = {
  title: 'Hobbyroom',
  description: 'Hobbyroom Frontend',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <div className="App">{children}</div>
        </Providers>
      </body>
    </html>
  )
}
