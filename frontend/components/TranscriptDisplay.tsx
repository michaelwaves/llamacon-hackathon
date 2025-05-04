import { summarizeTranscript } from '@/lib/llama';
import React, { useEffect, useState } from 'react';

const roleColors = {
    user: 'bg-blue-100 text-blue-800',
    assistant: 'bg-green-100 text-green-800',
};

export default function TranscriptDisplay({ transcript }) {

    // Filter out 'system' messages
    const filteredTranscript = transcript.filter(entry => entry.role !== 'system');

    return (
        <div className="space-y-3 p-4 max-w-2xl mx-auto">
            {filteredTranscript.map((entry, index) => (
                <div
                    key={index}
                    className={`p-3 rounded-xl shadow-sm ${roleColors[entry.role] || 'bg-white'} whitespace-pre-wrap`}
                >
                    <div className="font-semibold capitalize mb-1 text-sm">
                        {entry.role}
                    </div>
                    <div>{entry.content}</div>
                </div>
            ))}
            <div>

            </div>
        </div>
    );
}
