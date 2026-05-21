'use client'

import { useEffect, useState } from 'react'

interface Fruit {
    id: string
    name_en: string
    name_ko: string | null
    category: string
}

interface PairingResult {
    id: string
    compound_score: number
    shared_compounds: number
    predicted_sugar: number
    predicted_ph: number
    predicted_sweetness: number
    predicted_acidity: number
    predicted_bitterness: number
    predicted_creaminess: number
    predicted_juiciness: number
    predicted_richness: number
    predicted_freshness: number
}

export default function Home() {
    const [fruits, setFruits] = useState<Fruit[]>([])
    const [fruitA, setFruitA] = useState('')
    const [fruitB, setFruitB] = useState('')
    const [result, setResult] = useState<PairingResult | null>(null)
    const [loading, setLoading] = useState(false)
    const [ratioA, setRatioA] = useState(50)

    useEffect(() => {
        fetch('/api/fruits/')
            .then(res => res.json())
            .then(data => {
                const sorted = data.sort((a: Fruit, b: Fruit) =>
                    a.name_en.localeCompare(b.name_en)
                )
                setFruits(sorted)
            })
    }, [])

    const handlePairing = async () => {
        if (!fruitA || !fruitB) return
        setLoading(true)
        const res = await fetch('/api/fruits/pairing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                fruit_a_id: fruitA,
                fruit_b_id: fruitB,
                ratio_a: ratioA / 100,
                ratio_b: (100 - ratioA) / 100
            })
        })
        const data = await res.json()
        setResult(data)
        setLoading(false)
    }

    return (
        <main className="min-h-screen bg-pink-50 flex flex-col items-center justify-center p-8">
            <div className="text-center mb-12">
                <h1 className="text-4xl font-bold text-pink-400 mb-2">🍓 Dessert AI Lab</h1>
                <p className="text-pink-300 text-lg">과일 페어링 AI 서비스</p>
            </div>

            <div className="bg-white rounded-3xl shadow-lg p-8 w-full max-w-lg border border-pink-100">
                <h2 className="text-xl font-semibold text-pink-400 mb-6 text-center">🎀 과일 조합 만들기</h2>

                <div className="flex flex-col gap-4">
                    <div>
                        <label className="text-sm text-pink-300 mb-1 block">과일 A</label>
                        <select
                            className="w-full border border-pink-200 rounded-2xl px-4 py-3 text-gray-600 focus:outline-none focus:ring-2 focus:ring-pink-300"
                            value={fruitA}
                            onChange={e => { setFruitA(e.target.value); setResult(null) }}
                        >
                            <option value="">과일을 선택하세요</option>
                            {fruits.map(f => (
                                <option key={f.id} value={f.id}>
                                    {f.name_ko ? `${f.name_ko} (${f.name_en})` : f.name_en}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="text-center text-pink-300 text-2xl">+</div>

                    <div>
                        <label className="text-sm text-pink-300 mb-1 block">과일 B</label>
                        <select
                            className="w-full border border-pink-200 rounded-2xl px-4 py-3 text-gray-600 focus:outline-none focus:ring-2 focus:ring-pink-300"
                            value={fruitB}
                            onChange={e => { setFruitB(e.target.value); setResult(null) }}
                        >
                            <option value="">과일을 선택하세요</option>
                            {fruits.map(f => (
                                <option key={f.id} value={f.id}>
                                    {f.name_ko ? `${f.name_ko} (${f.name_en})` : f.name_en}
                                </option>
                            ))}
                        </select>
                    </div>

                    {fruitA && fruitB && (
                        <div className="bg-white rounded-2xl p-4 border border-pink-100">
                            <p className="text-sm text-pink-300 mb-2">혼합 비율</p>
                            <div className="flex items-center gap-3">
                <span className="text-xs text-pink-400 w-20 text-right truncate">
                  {fruits.find(f => f.id === fruitA)?.name_ko || fruits.find(f => f.id === fruitA)?.name_en}
                </span>
                                <span className="text-xs font-bold text-pink-400 w-8 text-center">{ratioA}%</span>
                                <input
                                    type="range"
                                    min="10"
                                    max="90"
                                    value={ratioA}
                                    onChange={e => setRatioA(Number(e.target.value))}
                                    className="flex-1 accent-pink-400"
                                />
                                <span className="text-xs font-bold text-pink-400 w-8 text-center">{100 - ratioA}%</span>
                                <span className="text-xs text-pink-400 w-20 truncate">
                  {fruits.find(f => f.id === fruitB)?.name_ko || fruits.find(f => f.id === fruitB)?.name_en}
                </span>
                            </div>
                        </div>
                    )}

                    <button
                        onClick={handlePairing}
                        disabled={loading || !fruitA || !fruitB}
                        className="mt-4 bg-pink-400 hover:bg-pink-500 text-white font-semibold py-3 rounded-2xl transition-colors disabled:opacity-50"
                    >
                        {loading ? '분석 중...' : '🍰 페어링 분석하기'}
                    </button>
                </div>

                {result && (
                    <div className="mt-8 bg-pink-50 rounded-2xl p-6 border border-pink-100">
                        <h3 className="text-center text-pink-400 font-semibold mb-4">✨ 페어링 결과</h3>

                        <div className="grid grid-cols-2 gap-4 mb-4">
                            <div className="bg-white rounded-2xl p-4 text-center border border-pink-100">
                                <p className="text-xs text-pink-300 mb-1">궁합 점수</p>
                                <p className="text-2xl font-bold text-pink-400">{result.compound_score}점</p>
                            </div>
                            <div className="bg-white rounded-2xl p-4 text-center border border-pink-100">
                                <p className="text-xs text-pink-300 mb-1">공유 화합물</p>
                                <p className="text-2xl font-bold text-pink-400">{result.shared_compounds}개</p>
                            </div>
                            <div className="bg-white rounded-2xl p-4 text-center border border-pink-100">
                                <p className="text-xs text-pink-300 mb-1">예측 당도</p>
                                <p className="text-2xl font-bold text-pink-400">
                                    {result.predicted_sugar ? `${result.predicted_sugar}g` : '-'}
                                </p>
                            </div>
                            <div className="bg-white rounded-2xl p-4 text-center border border-pink-100">
                                <p className="text-xs text-pink-300 mb-1">예측 산도</p>
                                <p className="text-2xl font-bold text-pink-400">
                                    {result.predicted_ph ? `pH ${result.predicted_ph}` : '-'}
                                </p>
                            </div>
                        </div>

                        {result.predicted_sweetness && (
                            <div className="bg-white rounded-2xl p-4 border border-pink-100">
                                <p className="text-sm text-pink-400 font-semibold mb-3">맛 프로파일 (1~10)</p>
                                <div className="flex flex-col gap-2">
                                    {[
                                        { label: '단맛', val: result.predicted_sweetness },
                                        { label: '산미', val: result.predicted_acidity },
                                        { label: '쓴맛', val: result.predicted_bitterness },
                                        { label: '크리미함', val: result.predicted_creaminess },
                                        { label: '과즙감', val: result.predicted_juiciness },
                                        { label: '풍미', val: result.predicted_richness },
                                        { label: '상큼함', val: result.predicted_freshness },
                                    ].map(item => (
                                        <div key={item.label} className="flex items-center gap-3">
                                            <span className="text-xs text-pink-300 w-16">{item.label}</span>
                                            <div className="flex-1 bg-pink-50 rounded-full h-2">
                                                <div
                                                    className="bg-pink-400 h-2 rounded-full transition-all"
                                                    style={{ width: `${((item.val || 0) / 10) * 100}%` }}
                                                />
                                            </div>
                                            <span className="text-xs text-pink-400 w-6 text-right">{item.val}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </main>
    )
}