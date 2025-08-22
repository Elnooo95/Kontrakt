'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const router = useRouter()
  const api = process.env.NEXT_PUBLIC_API_BASE_URL

  async function onSubmit(e) {
    e.preventDefault()
    setError(null)
    try {
      const res = await fetch(`${api}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      if (!res.ok) throw new Error('Kunde inte skapa konto')
      await res.json()
      router.push('/login')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <main className="max-w-md mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Skapa konto</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input className="border p-2 w-full" placeholder="E-post" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="border p-2 w-full" placeholder="Lösenord" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <button className="px-4 py-2 bg-black text-white rounded" type="submit">Skapa konto</button>
      </form>
      <p className="mt-3 text-sm">Har du redan konto? <a href="/login" className="underline">Logga in</a></p>
    </main>
  )
}
