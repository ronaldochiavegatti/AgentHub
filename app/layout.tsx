import type { Metadata } from 'next'
import { GeistSans } from 'geist/font/sans'
import { GeistMono } from 'geist/font/mono'
import { Analytics } from '@vercel/analytics/next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AgentHub - Plataforma Inteligente de Automação',
  description: 'Uma Arquitetura Escalável para Agentes de IA Verticalizados - Especializada em automação contábil para MEI',
  keywords: 'Inteligência Artificial, Microsserviços, SaaS, Automação Contábil, MEI, RAG, OCR',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable}`}>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
