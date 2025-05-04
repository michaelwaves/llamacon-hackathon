'use client'

import { Card, CardContent } from '@/components/ui/card'
import { Button } from './ui/button'
import InterviewForm from './InterviewForm'
type KYCResult = {
    first_name: string
    last_name: string
    occupation: string
    image_filename: string
    image_content_type: string
    image_size_bytes: number
    kyc_result: {
        risk_score: string
        rationale: string
    }
}

function KYCResults({ data }: { data: KYCResult }) {
    const riskScore = parseFloat(data.kyc_result.risk_score)
    let scoreColor = 'text-green-600'
    if (riskScore > 75) scoreColor = 'text-red-600'
    else if (riskScore > 50) scoreColor = 'text-orange-500'
    console.log(data)
    return (
        <Card className="mt-6 p-6 shadow-md rounded-2xl border border-gray-200 bg-white">
            <CardContent className="space-y-4">
                <h2 className="text-xl font-semibold">KYC Results</h2>
                <p><strong>First Name:</strong> {data.first_name}</p>
                <p><strong>Last Name:</strong> {data.last_name}</p>
                <p><strong>Occupation:</strong> {data.occupation}</p>
                <p><strong>Image File:</strong> {data.image_filename}</p>
                <p><strong>File Size:</strong> {(data.image_size_bytes / 1024).toFixed(1)} KB</p>
                <p className={scoreColor}>
                    <strong>Risk Score:</strong> {riskScore}
                </p>
                <div>
                    <strong>Rationale:</strong>
                    <p className="mt-1 text-sm text-gray-700">{data.kyc_result.rationale}</p>
                </div>
                <div>
                    <InterviewForm />
                </div>
            </CardContent>
        </Card>
    )
}

export default KYCResults