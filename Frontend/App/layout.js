import './globals.css'

export const metadata = {
  title: 'AI-kontraktsförklarare',
  description: 'Förklarar kontrakt på enkel svenska. Ej juridisk rådgivning.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="sv">
      <body className="bg-gray-50 text-gray-900">{children}</body>
    </html>
  )
}
