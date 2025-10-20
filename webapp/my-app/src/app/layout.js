import './globals.css'
import { Inter } from 'next/font/google'
import Chatbot from './components/Chatbot' // <-- 1. IMPORT THE COMPONENT

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Resource Connect',
  description: 'Connecting communities to resources.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
        <Chatbot /> {/* <-- 2. ADD THE COMPONENT HERE */}
      </body>
    </html>
  )
}
