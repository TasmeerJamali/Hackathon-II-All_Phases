/**
 * ChatKit-style Chat Page
 * 
 * Reference: @specs/features/chatbot.md
 * Uses OpenAI ChatKit patterns for the chat interface
 */

"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Send, Loader2, ArrowLeft, MessageSquare, Bot, User } from "lucide-react";
import { api } from "@/lib/api";

interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
    timestamp: Date;
    toolCalls?: string[];
}

export default function ChatPage() {
    const router = useRouter();
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [conversationId, setConversationId] = useState<number | null>(null);
    const [userId, setUserId] = useState<string | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const storedUserId = localStorage.getItem("user_id");
        if (!storedUserId) {
            router.push("/login");
            return;
        }
        setUserId(storedUserId);
    }, [router]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const sendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || !userId || loading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: "user",
            content: input.trim(),
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        try {
            const response = await api.chat(userId, {
                conversation_id: conversationId || undefined,
                message: userMessage.content,
            });

            if (!conversationId) {
                setConversationId(response.conversation_id);
            }

            const assistantMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: "assistant",
                content: response.response,
                timestamp: new Date(),
                toolCalls: response.tool_calls,
            };

            setMessages((prev) => [...prev, assistantMessage]);
        } catch (err) {
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: "assistant",
                content: `Error: ${err instanceof Error ? err.message : "Failed to send message"}`,
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gradient-to-br from-gray-50 to-blue-50">
            {/* Header */}
            <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 px-4 py-3 flex items-center gap-4">
                <button
                    onClick={() => router.push("/dashboard")}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                    <ArrowLeft className="h-5 w-5 text-gray-600" />
                </button>
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-primary to-blue-600 rounded-full flex items-center justify-center">
                        <Bot className="h-5 w-5 text-white" />
                    </div>
                    <div>
                        <h1 className="font-semibold text-gray-900">Todo Assistant</h1>
                        <p className="text-xs text-gray-500">Powered by AI</p>
                    </div>
                </div>
            </header>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-full text-gray-500">
                        <MessageSquare className="h-16 w-16 mb-4 text-gray-300" />
                        <h2 className="text-xl font-medium mb-2">Start a conversation</h2>
                        <p className="text-sm text-center max-w-md">
                            Ask me to manage your tasks! Try saying:
                        </p>
                        <div className="mt-4 space-y-2 text-sm">
                            <p className="bg-white px-4 py-2 rounded-lg shadow-sm">"Add a task to buy groceries"</p>
                            <p className="bg-white px-4 py-2 rounded-lg shadow-sm">"What's pending?"</p>
                            <p className="bg-white px-4 py-2 rounded-lg shadow-sm">"Mark task 1 as done"</p>
                        </div>
                    </div>
                )}

                {messages.map((msg) => (
                    <div
                        key={msg.id}
                        className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                    >
                        <div
                            className={`max-w-[80%] rounded-2xl px-4 py-3 ${msg.role === "user"
                                    ? "bg-primary text-white rounded-br-md"
                                    : "bg-white shadow-sm border border-gray-100 rounded-bl-md"
                                }`}
                        >
                            <div className="flex items-center gap-2 mb-1">
                                {msg.role === "assistant" ? (
                                    <Bot className="h-4 w-4 text-primary" />
                                ) : (
                                    <User className="h-4 w-4" />
                                )}
                                <span className="text-xs opacity-70">
                                    {msg.role === "assistant" ? "Assistant" : "You"}
                                </span>
                            </div>
                            <p className="whitespace-pre-wrap text-sm">{msg.content}</p>
                            {msg.toolCalls && msg.toolCalls.length > 0 && (
                                <div className="mt-2 pt-2 border-t border-gray-100">
                                    <p className="text-xs text-gray-400">
                                        Actions: {msg.toolCalls.join(", ")}
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-white shadow-sm border border-gray-100 rounded-2xl rounded-bl-md px-4 py-3">
                            <div className="flex items-center gap-2">
                                <Loader2 className="h-4 w-4 animate-spin text-primary" />
                                <span className="text-sm text-gray-500">Thinking...</span>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="bg-white border-t border-gray-200 p-4">
                <form onSubmit={sendMessage} className="flex gap-3">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type a message..."
                        disabled={loading}
                        className="flex-1 px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all disabled:opacity-50"
                    />
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        className="px-6 py-3 bg-primary text-white rounded-xl hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                        {loading ? (
                            <Loader2 className="h-5 w-5 animate-spin" />
                        ) : (
                            <Send className="h-5 w-5" />
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
}
