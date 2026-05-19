'use client'

import { useEffect, useState } from 'react'

interface Fruit {
    id: string
    name_en: string
    category: string
}

interface PairingResult {
    id: string
    compound_score: number
    shared_compounds: number
    predicted_sugar: number
    predicted_ph: number
}

interface ValidationForm {
    tester_name: string
    sweetness: number
    sourness: number
    bitterness: number
    saltiness: number
    umami: number
    balance_score: number
    result: string
    memo: string
}

const defaultForm: ValidationForm = {
    tester_name: '',
    sweetness: 3,
    sourness: 3,
    bitterness: 3,
    saltiness: 3,
    umami: 3,
    balance_score: 3,
    result: '',
    memo: ''
}

const flavorItems = [
    { key: 'sweetness', label: '단맛' },
    { key: 'sourness', label: '신맛' },
    { key: 'bitterness', label: '쓴맛' },
    { key: 'saltiness', label: '짠맛' },
    { key: 'umami', label: '감칠맛' },
]

export default function FruitMatchValidate() {
    const [fruits, setFruits] = useState<Fruit[]>([])
    const [fruitA, setFruitA] = useState('')
    const [fruitB, setFruitB] = useState('')
    const [pairingResult, setPairingResult] = useState<PairingResult | null>(null)
    const [form, setForm] = useState<ValidationForm>(defaultForm)
    const [loading, setLoading] = useState(false)
    const [showPopup, setShowPopup] = useState(false)

    useEffect(() => {
        fetch('http://localhost:8000/fruits/')
            .then(res => res.json())
            .then(data => setFruits(data))
    }, [])

    const handlePairing = async () => {
        if (!fruitA || !fruitB) return
        setLoading(true)
        setPairingResult(null)
        setForm({ ...defaultForm, tester_name: form.tester_name })
        const res = await fetch('http://localhost:8000/fruits/pairing', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fruit_a_id: fruitA, fruit_b_id: fruitB })
        })
        const data = await res.json()
        setPairingResult(data)
        setLoading(false)
    }

    const handleSave = async () => {
        if (!pairingResult || !form.result) return
        await fetch('http://localhost:8000/validations/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                combination_id: pairingResult.id,
                ...form
            })
        })
        setShowPopup(true)
    }

    const handleConfirm = () => {
        setShowPopup(false)
        setFruitB('')
        setPairingResult(null)
        setForm({ ...defaultForm, tester_name: form.tester_name })
    }

    const handleScore = (key: string, value: number) => {
        setForm(prev => ({ ...prev, [key]: value }))
    }

    const fruitAName = fruits.find(f => f.id === fruitA)?.name_en
    const fruitBName = fruits.find(f => f.id === fruitB)?.name_en

    return (
        <main className="min-h-screen bg-pink-50 p-8">
            <div className="max-w-2xl mx-auto">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-pink-400 mb-2">🍓 과일 페어링 검증</h1>
                    <p className="text-pink-300">연구원 전용 맛 검증 입력 폼</p>
                </div>

                <div className="bg-white rounded-3xl shadow-lg p-8 border border-pink-100 flex flex-col gap-6">

                    {/* 테스터 이름 */}
                    <div>
                        <label className="text-sm text-pink-300 mb-1 block">테스터 이름</label>
                        <input
                            type="text"
                            className="w-full border border-pink-200 rounded-2xl px-4 py-3 text-gray-600 focus:outline-none focus:ring-2 focus:ring-pink-300"
                            placeholder="이름을 입력하세요"
                            value={form.tester_name}
                            onChange={e => setForm(prev => ({ ...prev, tester_name: e.target.value }))}
                        />
                    </div>

                    <div className="flex flex-col gap-4">
                        <div>
                            <label className="text-sm text-pink-300 mb-1 block">과일 A</label>
                            <select
                                className="w-full border border-pink-200 rounded-2xl px-4 py-3 text-gray-600 focus:outline-none focus:ring-2 focus:ring-pink-300"
                                value={fruitA}
                                onChange={e => { setFruitA(e.target.value); setPairingResult(null) }}
                            >
                                <option value="">과일을 선택하세요</option>
                                {fruits.map(f => (
                                    <option key={f.id} value={f.id}>{f.name_en}</option>
                                ))}
                            </select>
                        </div>

                        <div className="text-center text-pink-300 text-2xl">+</div>

                        <div>
                            <label className="text-sm text-pink-300 mb-1 block">과일 B</label>
                            <select
                                className="w-full border border-pink-200 rounded-2xl px-4 py-3 text-gray-600 focus:outline-none focus:ring-2 focus:ring-pink-300"
                                value={fruitB}
                                onChange={e => { setFruitB(e.target.value); setPairingResult(null) }}
                            >
                                <option value="">과일을 선택하세요</option>
                                {fruits.map(f => (
                                    <option key={f.id} value={f.id}>{f.name_en}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <button
                        onClick={handlePairing}
                        disabled={loading || !fruitA || !fruitB}
                        className="bg-pink-400 hover:bg-pink-500 text-white font-semibold py-3 rounded-2xl transition-colors disabled:opacity-50"
                    >
                        {loading ? '분석 중...' : '🍰 페어링 분석하기'}
                    </button>

                    {pairingResult && (
                        <>
                            <div className="bg-pink-50 rounded-2xl p-6 border border-pink-100">
                                <h3 className="text-center text-pink-400 font-semibold mb-4">
                                    ✨ {fruitAName} + {fruitBName}
                                </h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="bg-white rounded-2xl p-4 text-center border border-pink-100">
                                        <p className="text-xs text-pink-300 mb-1">궁합 점수</p>
                                        <p className="text-2xl font-bold text-pink-400">{pairingResult.compound_score}점</p>
                                    </div>
                                    <div className="bg-white rounded-2xl p-4 text-center border border-pink-100">
                                        <p className="text-xs text-pink-300 mb-1">공유 화합물</p>
                                        <p className="text-2xl font-bold text-pink-400">{pairingResult.shared_compounds}개</p>
                                    </div>
                                    <div className="bg-white rounded-2xl p-4 text-center border border-pink-100">
                                        <p className="text-xs text-pink-300 mb-1">예측 당도</p>
                                        <p className="text-2xl font-bold text-pink-400">
                                            {pairingResult.predicted_sugar ? `${pairingResult.predicted_sugar}g` : '-'}
                                        </p>
                                    </div>
                                    <div className="bg-white rounded-2xl p-4 text-center border border-pink-100">
                                        <p className="text-xs text-pink-300 mb-1">예측 산도</p>
                                        <p className="text-2xl font-bold text-pink-400">
                                            {pairingResult.predicted_ph ? `pH ${pairingResult.predicted_ph}` : '-'}
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <p className="text-sm text-pink-300 mb-3">맛 강도 (1~5점)</p>
                                <div className="flex flex-col gap-3">
                                    {flavorItems.map(item => (
                                        <div key={item.key} className="flex items-center justify-between">
                                            <span className="text-gray-600 w-16">{item.label}</span>
                                            <div className="flex gap-2">
                                                {[1, 2, 3, 4, 5].map(score => (
                                                    <button
                                                        key={score}
                                                        onClick={() => handleScore(item.key, score)}
                                                        className={`w-9 h-9 rounded-full text-sm font-semibold transition-colors
                              ${form[item.key as keyof ValidationForm] === score
                                                            ? 'bg-pink-400 text-white'
                                                            : 'bg-pink-50 text-pink-300 border border-pink-200 hover:bg-pink-100'
                                                        }`}
                                                    >
                                                        {score}
                                                    </button>
                                                ))}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* 밸런스 점수 */}
                            <div>
                                <p className="text-sm text-pink-300 mb-3">전체 밸런스 점수 (1~5점)</p>
                                <div className="flex gap-2">
                                    {[1, 2, 3, 4, 5].map(score => (
                                        <button
                                            key={score}
                                            onClick={() => handleScore('balance_score', score)}
                                            className={`w-9 h-9 rounded-full text-sm font-semibold transition-colors
                        ${form.balance_score === score
                                                ? 'bg-pink-400 text-white'
                                                : 'bg-pink-50 text-pink-300 border border-pink-200 hover:bg-pink-100'
                                            }`}
                                        >
                                            {score}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            {/* 최종 결과 */}
                            <div>
                                <p className="text-sm text-pink-300 mb-3">최종 평가</p>
                                <div className="flex gap-3">
                                    {['성공', '개선필요', '실패'].map(r => (
                                        <button
                                            key={r}
                                            onClick={() => setForm(prev => ({ ...prev, result: r }))}
                                            className={`flex-1 py-2 rounded-2xl text-sm font-semibold transition-colors
                        ${form.result === r
                                                ? 'bg-pink-400 text-white'
                                                : 'bg-pink-50 text-pink-300 border border-pink-200 hover:bg-pink-100'
                                            }`}
                                        >
                                            {r}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <div>
                                <label className="text-sm text-pink-300 mb-1 block">메모 (선택)</label>
                                <textarea
                                    className="w-full border border-pink-200 rounded-2xl px-4 py-3 text-gray-600 focus:outline-none focus:ring-2 focus:ring-pink-300 resize-none"
                                    rows={3}
                                    placeholder="추가 의견을 입력하세요"
                                    value={form.memo}
                                    onChange={e => setForm(prev => ({ ...prev, memo: e.target.value }))}
                                />
                            </div>

                            <button
                                onClick={handleSave}
                                disabled={!form.result}
                                className="bg-pink-400 hover:bg-pink-500 text-white font-semibold py-3 rounded-2xl transition-colors disabled:opacity-50"
                            >
                                ✅ 검증 결과 저장
                            </button>
                        </>
                    )}
                </div>
            </div>

            {showPopup && (
                <div className="fixed top-6 left-1/2 -translate-x-1/2 z-50">
                    <div className="bg-white rounded-3xl px-8 py-6 shadow-xl border border-pink-100 text-center">
                        <p className="text-2xl mb-2">🎀</p>
                        <h3 className="text-lg font-bold text-pink-400 mb-1">저장되었습니다!</h3>
                        <p className="text-pink-300 text-sm mb-4">{fruitAName} + {fruitBName} 검증 결과가 저장됐어요.</p>
                        <button
                            onClick={handleConfirm}
                            className="bg-pink-400 hover:bg-pink-500 text-white font-semibold py-2 px-8 rounded-2xl transition-colors"
                        >
                            확인
                        </button>
                    </div>
                </div>
            )}
        </main>
    )
}