/**
 * Voice Input Button Component
 * 
 * Provides voice-to-text input for task creation and chat
 * Supports English and Urdu voice commands
 */

"use client";

import { useState, useEffect } from "react";
import { Mic, MicOff, Loader2, AlertCircle } from "lucide-react";
import { useVoiceInput, voiceLanguages } from "@/hooks/useVoiceInput";
import { getStoredLocale, Locale } from "@/lib/i18n";

interface VoiceInputButtonProps {
    onTranscript: (text: string) => void;
    className?: string;
    size?: "sm" | "md" | "lg";
}

export default function VoiceInputButton({
    onTranscript,
    className = "",
    size = "md",
}: VoiceInputButtonProps) {
    const [locale, setLocale] = useState<Locale>("en");

    useEffect(() => {
        setLocale(getStoredLocale());
    }, []);

    const {
        isListening,
        isSupported,
        transcript,
        error,
        toggleListening,
    } = useVoiceInput({
        language: voiceLanguages[locale],
        continuous: false,
        interimResults: true,
        onResult: (text, isFinal) => {
            if (isFinal && text.trim()) {
                onTranscript(text.trim());
            }
        },
    });

    // Size classes
    const sizeClasses = {
        sm: "p-2",
        md: "p-3",
        lg: "p-4",
    };

    const iconSizes = {
        sm: "h-4 w-4",
        md: "h-5 w-5",
        lg: "h-6 w-6",
    };

    if (!isSupported) {
        return (
            <button
                disabled
                className={`${sizeClasses[size]} rounded-full bg-gray-100 text-gray-400 cursor-not-allowed ${className}`}
                title="Voice input not supported in this browser"
            >
                <MicOff className={iconSizes[size]} />
            </button>
        );
    }

    return (
        <div className="relative">
            <button
                onClick={toggleListening}
                className={`
          ${sizeClasses[size]} 
          rounded-full 
          transition-all 
          duration-200
          ${isListening
                        ? "bg-red-500 text-white animate-pulse shadow-lg shadow-red-500/50"
                        : "bg-gray-100 hover:bg-gray-200 text-gray-600"
                    }
          ${className}
        `}
                title={isListening ? "Stop recording" : "Start voice input"}
                aria-label={isListening ? "Stop recording" : "Start voice input"}
            >
                {isListening ? (
                    <Mic className={`${iconSizes[size]} animate-pulse`} />
                ) : (
                    <Mic className={iconSizes[size]} />
                )}
            </button>

            {/* Listening indicator */}
            {isListening && (
                <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 whitespace-nowrap">
                    <div className="flex items-center gap-1 text-xs text-red-500">
                        <Loader2 className="h-3 w-3 animate-spin" />
                        <span>{locale === "ur" ? "سن رہا ہے..." : "Listening..."}</span>
                    </div>
                </div>
            )}

            {/* Transcript preview */}
            {isListening && transcript && (
                <div className="absolute -bottom-16 left-1/2 -translate-x-1/2 whitespace-nowrap max-w-[200px]">
                    <div className="bg-gray-800 text-white text-xs px-3 py-1 rounded-full truncate">
                        {transcript}
                    </div>
                </div>
            )}

            {/* Error indicator */}
            {error && (
                <div className="absolute -bottom-8 left-1/2 -translate-x-1/2 whitespace-nowrap">
                    <div className="flex items-center gap-1 text-xs text-red-500">
                        <AlertCircle className="h-3 w-3" />
                        <span className="max-w-[150px] truncate">{error}</span>
                    </div>
                </div>
            )}
        </div>
    );
}
