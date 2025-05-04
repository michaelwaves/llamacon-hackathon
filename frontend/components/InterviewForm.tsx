"use client"

import { Button } from "@/components/ui/button";
import { createConversation, endConversation, getTranscript } from "@/lib/tavus/tavus";
import { Check } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

function InterviewForm() {

    const [url, setUrl] = useState<string | null>(null);
    const [transcript, setTranscript] = useState<any>();
    const [conversationId, setConversationId] = useState<string | null>();
    const handleStartConversation = async () => {
        try {
            const res = await createConversation()
            window.open(res, "_blank", "noopener,noreferrer"); // Open in new tab
            setUrl(res)
            const convId = res.split("/").at(-1)
            setConversationId(convId)
            toast("Sucessfully created Conversation")
        } catch (e) {
            console.error(e)
            toast("Error creating conversation")
        }
    }

    const handleEndConversation = async () => {
        try {
            if (!url) {
                return
            }

            const res = await endConversation(conversationId ?? "")
            toast("Sucessfully ending Conversation")
        } catch (e) {
            console.error(e)
            toast("Error ending conversation")
        }
    }

    const handleSubmitConversation = async () => {
        const res = await getTranscript(conversationId ?? "")
        console.log(res)
        const index = res.events.findIndex((event: any) => event.event_type === "application.transcription_ready");

        let myTranscript;
        if (index !== -1) {
            myTranscript = res.events[index].properties.transcript;
            console.log(myTranscript);
            setTranscript(myTranscript);
        } else {
            console.log("No transcription event found");
            setTranscript("No transcription events found");
        }

        toast("Reference successfully submitted");



    }
    return (
        <div className="p-6 space-y-6">
            <div className="flex flex-wrap items-center gap-4">
                <Button onClick={handleStartConversation} className="bg-pink-500">Start Interview</Button>
                {url && (
                    <Button variant="destructive" onClick={handleEndConversation}>
                        End Call
                    </Button>
                )}
                <Button onClick={handleSubmitConversation}>Submit Interivew</Button>
            </div>
            {transcript && (
                <div className="flex items-center gap-2">
                    <Check className="w-5 h-5 text-green-500" />
                    <span className="text-green-500 font-medium">Successfully submitted</span>
                </div>
            )}
        </div>
    );
}

export default InterviewForm;