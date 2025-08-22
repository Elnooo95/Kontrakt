'use client'
export default function BillingPage(){
  async function createCheckout(){
    const token = localStorage.getItem('token')
    const api = process.env.NEXT_PUBLIC_API_BASE_URL
    const res = await fetch(`${api}/billing/create-checkout-session`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await res.json()
    if (data.url) window.location.href = data.url
    else alert('Stripe ej konfigurerat')
  }

  return (
    <main className="max-w-md mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Prenumeration</h1>
      <p className="text-sm text-gray-600 mb-4">Lås upp Pro-funktioner.</p>
      <button onClick={createCheckout} className="px-4 py-2 bg-black text-white rounded">Prenumerera</button>
    </main>
  )
}
