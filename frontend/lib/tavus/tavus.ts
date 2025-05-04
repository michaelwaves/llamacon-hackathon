"use server";

export async function createConversation() {
    const apiEndpoint = "https://tavusapi.com/v2/conversations";
    const apiKey = process.env.TAVUS_API_KEY; // Store API key securely

    if (!apiKey) {
        throw new Error("Missing API Key");
    }

    const body = {
        replica_id: "rb17cf590e15",
        callback_url: "https://kyc.info/webhook",
        conversation_name: "A Reference for a Founder",
        conversational_context: `
        Keep response short and snappy. You are interviewing Michael. 
        This is a reference check for Alex. Ask him: Did you work with Alex Chan at Shopify? 
        What was your experience with him, specifically his strengths, growth areas, work style, 
        and any challenges? Were there any key behaviors or decision-making traits that stood out? 
        If you had to pick five team members, would Alex be one of them?`,
        custom_greeting: "Hey there!",
        properties: {
            max_call_duration: 60,
            participant_left_timeout: 30,
            participant_absent_timeout: 30,
            enable_recording: true,
            enable_transcription: true,
            language: "english",
        },
    };

    const response = await fetch(apiEndpoint, {
        method: "POST",
        headers: {
            "x-api-key": apiKey,
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });

    if (!response.ok) {
        console.error(await response.json())
        throw new Error(`Error creating conversation: ${response.statusText}`);
    }

    const data = await response.json();
    return data.conversation_url;
}

export async function endConversation(conversationId: string) {
    const apiEndpoint = `https://tavusapi.com/v2/conversations/${conversationId}/end`;
    const apiKey = process.env.TAVUS_API_KEY; // Store API key securely

    if (!apiKey) {
        throw new Error("Missing API Key");
    }

    const response = await fetch(apiEndpoint, {
        method: "POST",
        headers: {
            "x-api-key": apiKey,
        },
    });

    if (!response.ok) {
        throw new Error(`Error ending conversation: ${response.statusText}`);
    }

    return null;
}

export async function getTranscript(conversationId: string) {
    const apiEndpoint = `https://tavusapi.com/v2/conversations/${conversationId}?verbose=true`;
    const apiKey = process.env.TAVUS_API_KEY; // Store API key securely

    if (!apiKey) {
        throw new Error("Missing API Key");
    }

    const response = await fetch(apiEndpoint, {
        method: "GET",
        headers: {
            "x-api-key": apiKey,
        },
    });

    if (!response.ok) {
        throw new Error(`Error fetching conversation: ${response.statusText}`);
    }

    return await response.json();
}