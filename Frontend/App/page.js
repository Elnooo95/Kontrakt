'use client'
import Link from 'next/link'

export default function Home() {
  return (
    <main className="max-w-3xl mx-auto p-6">
      <header className="mb-8">
        <h1 className="text-3xl font-bold">AI-kontraktsförklarare</h1>
        <p className="text-sm text-gray-600 mt-2">Förklarar avtal på enkel svenska med varningsflaggor. <strong>Ej juridisk rådgivning.</strong></p>
      </header>

      <div className="space-x-3">
        <Link href="/register" className="px-4 py-2 bg-black text-white rounded">Skapa konto</Link>
        <Link href="/login" className="px-4 py-2 border rounded">Logga in</Link>
      </div>

      <section className="mt-10">
        <h2 className="text-xl font-semibold mb-2">Så funkar det</h2>
        <ol className="list-decimal ml-6 space-y-1">
          <li>Ladda upp ditt PDF- eller TXT-kontrakt</li>
          <li>Få en kort förklaring, viktiga belopp/datum och varningsflaggor</li>
          <li>Ställ frågor – svar endast utifrån dokumentet</li>
        </ol>
      </section>
    </main>
  )
}
