"use client";
import { useState } from "react";

const PERSPECTIVES = ["Scientific", "Philosophical", "Economic", "Cultural", "Historical", "Ethical"];

interface Perspective { name: string; view: string; confidence: number; }
interface AnalysisResult { perspectives?: Perspective[]; agreements?: string[]; conflicts?: string[]; synthesis?: string; }

export default function ConsiliencePage() {
  const [topic, setTopic] = useState("");
  const [selected, setSelected] = useState<string[]>(["Scientific", "Philosophical", "Economic"]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");

  function togglePerspective(p: string) {
    setSelected((prev) => prev.includes(p) ? prev.filter((x) => x !== p) : [...prev, p]);
  }

  async function analyze() {
    if (!topic.trim() || selected.length < 2) return;
    setLoading(true); setError("");
    try {
      const res = await fetch("/api/analyze", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ topic, perspectives: selected }) });
      const data = await res.json();
      if (data.error) setError(data.error); else setResult(data as AnalysisResult);
    } catch (e) { setError(String(e)); }
    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-white p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-sky-300 mb-2">Consilience</h1>
          <p className="text-slate-500">Multi-perspective analysis — see any topic through different lenses simultaneously</p>
        </div>
        <div className="mb-4">
          <label className="block text-sm text-slate-400 mb-2">Topic or Question</label>
          <input className="w-full bg-[#111118] border border-sky-900 rounded-lg px-4 py-3 text-white placeholder-slate-600 focus:outline-none focus:border-sky-600" placeholder="e.g. Universal Basic Income, Quantum Computing, Gene editing..." value={topic} onChange={(e) => setTopic(e.target.value)} />
        </div>
        <div className="mb-6">
          <label className="block text-sm text-slate-400 mb-2">Perspectives (select 2+)</label>
          <div className="flex flex-wrap gap-2">
            {PERSPECTIVES.map((p) => (
              <button key={p} onClick={() => togglePerspective(p)} className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${selected.includes(p) ? "bg-sky-800 text-sky-200 border border-sky-600" : "bg-[#111118] text-slate-400 border border-slate-700 hover:border-sky-800"}`}>{p}</button>
            ))}
          </div>
        </div>
        <button onClick={analyze} disabled={loading || !topic.trim() || selected.length < 2} className="px-6 py-2 bg-sky-700 hover:bg-sky-600 disabled:opacity-40 text-white rounded-lg text-sm font-medium transition-colors mb-6">{loading ? "Analyzing..." : "Analyze"}</button>
        {error && <div className="p-4 bg-red-900/30 border border-red-700 rounded-lg text-red-400 text-sm mb-4">{error}</div>}
        {result?.perspectives && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 gap-3">
              {result.perspectives.map((p) => (
                <div key={p.name} className="bg-[#111118] border border-sky-900/40 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sky-300 font-semibold text-sm">{p.name}</span>
                    <span className="text-slate-400 text-xs">{p.confidence}% confidence</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full mb-3 overflow-hidden">
                    <div className="h-full bg-sky-600 rounded-full" style={{ width: `${p.confidence}%` }} />
                  </div>
                  <p className="text-slate-300 text-sm">{p.view}</p>
                </div>
              ))}
            </div>
            {(result.agreements || result.conflicts) && (
              <div className="grid grid-cols-2 gap-4">
                {result.agreements && (
                  <div className="bg-[#111118] border border-green-900/40 rounded-xl p-4">
                    <h3 className="text-green-400 font-semibold text-sm mb-3">Areas of Agreement</h3>
                    <ul className="space-y-2">{result.agreements.map((a, i) => <li key={i} className="text-slate-300 text-sm flex gap-2"><span className="text-green-600">+</span>{a}</li>)}</ul>
                  </div>
                )}
                {result.conflicts && (
                  <div className="bg-[#111118] border border-red-900/40 rounded-xl p-4">
                    <h3 className="text-red-400 font-semibold text-sm mb-3">Points of Conflict</h3>
                    <ul className="space-y-2">{result.conflicts.map((c, i) => <li key={i} className="text-slate-300 text-sm flex gap-2"><span className="text-red-600">×</span>{c}</li>)}</ul>
                  </div>
                )}
              </div>
            )}
            {result.synthesis && (
              <div className="bg-[#111118] border border-sky-700/40 rounded-xl p-4">
                <h3 className="text-sky-300 font-semibold text-sm mb-2">Synthesis</h3>
                <p className="text-slate-300 text-sm">{result.synthesis}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
