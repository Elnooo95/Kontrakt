'use client'
import { useEffect, useState } from 'react'

export default function Dashboard() {
  const [file, setFile] = useState(null)
  const [report, setReport] = useState(null)
  const [error, setError] = useState(null)

  const api = process.env.NEXT_PUBLIC_API_BASE_URL

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) window.location.href = '/login'
  }, [])

  async function upload(e) {
    e.preventDefault()
    setError(null)
    if (!file) return
    const token = localStorage.getItem('token')
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await fetch(`${api}/documents/upload`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: form
      })
      if (!res.ok) throw new Error('Uppladdning misslyckades')
      const data = await res.json()
      setReport(data.report)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <main className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Ditt konto</h1>
      <p className="text-sm text-gray-600">Ladda upp ett kontrakt (PDF eller TXT). <strong>Ej juridisk rådgivning.</strong></p>
      <form onSubmit={upload} className="my-4 flex items-center gap-3">
        <input type="file" accept=".pdf,.txt" onChange={e=>setFile(e.target.files?.[0] ?? null)} />
        <button className="px-4 py-2 bg-black text-white rounded">Analysera</button>
      </form>
      {error && <p className="text-red-600 text-sm">{error}</p>}
      {report && <ReportView report={report} />}
    </main>
  )
}

function ReportView({ report }) {
  return (
    <div className="bg-white shadow rounded p-4 space-y-4">
      <section>
        <h2 className="font-semibold">TL;DR</h2>
        <ul className="list-disc ml-5">{report.tldr?.map((p,i)=>(<li key={i}>{p}</li>))}</ul>
      </section>
      <section>
        <h2 className="font-semibold">Dina skyldigheter</h2>
        <ul className="list-disc ml-5">{report.skyldigheter_du?.map((p,i)=>(<li key={i}>{p}</li>))}</ul>
      </section>
      <section>
        <h2 className="font-semibold">Motpartens skyldigheter</h2>
        <ul className="list-disc ml-5">{report.skyldigheter_motpart?.map((p,i)=>(<li key={i}>{p}</li>))}</ul>
      </section>
      <section>
        <h2 className="font-semibold">Viktiga poster</h2>
        <ul className="list-disc ml-5">
          {report.viktiga_poster?.map((row, i)=>(
            <li key={i}><strong>{row.nyckel}:</strong> {Array.isArray(row.värden) ? row.värden.join(', ') : row.värden}</li>
          ))}
        </ul>
      </section>
      <section>
        <h2 className="font-semibold">Varningsflaggor</h2>
        <ul className="list-disc ml-5">
          {report.varningsflaggor?.map((r, i)=>(
            <li key={i}><span className="px-2 py-0.5 bg-yellow-100 rounded">{r.typ} – {r.klass}</span> <em className="text-gray-600">({r.varför})</em><br/><span className="text-xs text-gray-500">”{r.citat}”</span></li>
          ))}
        </ul>
      </section>
      <section>
        <h2 className="font-semibold">Citat</h2>
        <ol className="list-decimal ml-5">
          {report.citat?.map((c, i)=>(<li key={i}><span className="text-xs text-gray-500">Klausul {c.klausul}:</span> {c.text}</li>))}
        </ol>
      </section>
    </div>
  )
}
