import { Inter } from 'next/font/google'
import './globals.css'
import { Sidebar } from '@/layout/Sidebar'
import { Header } from '@/layout/Header'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'LLMObs Platform',
  description: 'Modular observability platform for LLM applications',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="flex h-screen bg-gray-100">
          <Sidebar />
          <div className="flex-1 flex flex-col overflow-hidden">
            <Header />
            <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100">
              <div className="container mx-auto px-6 py-8">
                {children}
              </div>
            </main>
          </div>
        </div>
      </body>
    </html>
  )
}
