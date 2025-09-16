import Providers from './providers'
import '../src/styles/index.css'
import '../src/styles/landing.css'
import '../src/styles/login.css'

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
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
