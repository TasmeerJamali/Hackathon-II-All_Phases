/**
 * Voice Commands Processor
 * 
 * Processes voice commands for task management
 * Supports both English and Urdu commands
 */

export interface VoiceCommand {
    action: "add" | "list" | "complete" | "delete" | "search" | "unknown";
    params: Record<string, string>;
    rawText: string;
}

// English command patterns
const englishPatterns = {
    add: [
        /^add (?:a )?task (?:to )?(.+)$/i,
        /^create (?:a )?task (?:for )?(.+)$/i,
        /^new task (.+)$/i,
        /^remind me to (.+)$/i,
        /^remember to (.+)$/i,
    ],
    list: [
        /^show (?:my )?tasks$/i,
        /^list (?:all )?tasks$/i,
        /^what(?:'s| is) pending\??$/i,
        /^what do i need to do\??$/i,
        /^show pending$/i,
        /^show completed$/i,
    ],
    complete: [
        /^(?:mark )?task (\d+) (?:as )?(?:complete|done)$/i,
        /^complete task (\d+)$/i,
        /^finish task (\d+)$/i,
        /^done with task (\d+)$/i,
    ],
    delete: [
        /^delete task (\d+)$/i,
        /^remove task (\d+)$/i,
        /^cancel task (\d+)$/i,
    ],
    search: [
        /^search (?:for )?(.+)$/i,
        /^find (.+)$/i,
        /^look for (.+)$/i,
    ],
};

// Urdu command patterns (using both Urdu script and romanized)
const urduPatterns = {
    add: [
        /^ٹاسک شامل کریں (.+)$/,
        /^نیا ٹاسک (.+)$/,
        /^یاد دہانی (.+)$/,
        /^task add karo (.+)$/i,
        /^naya task (.+)$/i,
    ],
    list: [
        /^ٹاسکس دکھائیں$/,
        /^سب ٹاسکس$/,
        /^کیا باقی ہے\??$/,
        /^tasks dikhao$/i,
        /^pending kya hai$/i,
    ],
    complete: [
        /^ٹاسک (\d+) مکمل کریں$/,
        /^task (\d+) complete karo$/i,
        /^task (\d+) ho gaya$/i,
    ],
    delete: [
        /^ٹاسک (\d+) حذف کریں$/,
        /^task (\d+) delete karo$/i,
        /^task (\d+) hatao$/i,
    ],
    search: [
        /^تلاش کریں (.+)$/,
        /^dhundo (.+)$/i,
        /^search karo (.+)$/i,
    ],
};

export function processVoiceCommand(text: string, locale: string = "en"): VoiceCommand {
    const patterns = locale === "ur" ? urduPatterns : englishPatterns;
    const normalizedText = text.toLowerCase().trim();

    // Check each action type
    for (const [action, actionPatterns] of Object.entries(patterns)) {
        for (const pattern of actionPatterns) {
            const match = normalizedText.match(pattern) || text.match(pattern);
            if (match) {
                return {
                    action: action as VoiceCommand["action"],
                    params: extractParams(action, match),
                    rawText: text,
                };
            }
        }
    }

    // Unknown command - might be a natural language request for AI chat
    return {
        action: "unknown",
        params: { text },
        rawText: text,
    };
}

function extractParams(action: string, match: RegExpMatchArray): Record<string, string> {
    switch (action) {
        case "add":
            return { title: match[1]?.trim() || "" };
        case "complete":
        case "delete":
            return { taskId: match[1] || "" };
        case "search":
            return { query: match[1]?.trim() || "" };
        case "list":
            if (match[0]?.includes("pending") || match[0]?.includes("باقی")) {
                return { status: "pending" };
            }
            if (match[0]?.includes("completed") || match[0]?.includes("مکمل")) {
                return { status: "completed" };
            }
            return { status: "all" };
        default:
            return {};
    }
}

// Voice feedback messages
export const voiceFeedback = {
    en: {
        taskAdded: "Task added successfully",
        taskCompleted: "Task marked as complete",
        taskDeleted: "Task deleted",
        listening: "I'm listening",
        notUnderstood: "I didn't understand that. Please try again.",
        error: "Sorry, something went wrong",
    },
    ur: {
        taskAdded: "ٹاسک شامل ہو گیا",
        taskCompleted: "ٹاسک مکمل ہو گیا",
        taskDeleted: "ٹاسک حذف ہو گیا",
        listening: "میں سن رہا ہوں",
        notUnderstood: "سمجھ نہیں آیا۔ دوبارہ کوشش کریں۔",
        error: "معذرت، کچھ غلط ہو گیا",
    },
};

// Text-to-speech for feedback
export function speakFeedback(message: string, locale: string = "en"): void {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
        const utterance = new SpeechSynthesisUtterance(message);
        utterance.lang = locale === "ur" ? "ur-PK" : "en-US";
        utterance.rate = 1;
        utterance.pitch = 1;
        window.speechSynthesis.speak(utterance);
    }
}
