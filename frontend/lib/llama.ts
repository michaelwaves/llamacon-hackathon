'use server'

export async function summarizeTranscript(transcript: any[]) {
    const apiKey = process.env.LLAMA_API_KEY;

    if (!apiKey) {
        throw new Error('LLAMA_API_KEY is not defined in environment variables');
    }

    const response = await fetch('https://api.llama.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            model: 'Llama-4-Maverick-17B-128E-Instruct-FP8',
            messages: [
                {
                    role: 'system',
                    content: 'You are a financial crime analyst assistant. Analyze the transcript and summarize any signs of money laundering, suspicious activity, or criminal intent. Be concise and factual.',
                },
                {
                    role: 'user',
                    content: `Here is the transcript:\n\n${JSON.stringify(transcript)}`,
                },
            ],
            max_tokens: 256,
        }),
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`LLaMA API error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    return data.choices?.[0]?.message?.content || 'No summary returned.';
}
