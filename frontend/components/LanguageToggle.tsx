/**
 * Language Toggle Component
 * 
 * Switches between English and Urdu with RTL support
 */

"use client";

import { useState, useEffect } from "react";
import { Globe } from "lucide-react";
import {
    Locale,
    getStoredLocale,
    setStoredLocale,
    localeNames,
    supportedLocales,
    getDirection
} from "@/lib/i18n";

interface LanguageToggleProps {
    onLocaleChange?: (locale: Locale) => void;
}

export default function LanguageToggle({ onLocaleChange }: LanguageToggleProps) {
    const [locale, setLocale] = useState<Locale>('en');
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        const stored = getStoredLocale();
        setLocale(stored);
        // Apply stored locale on mount
        document.documentElement.dir = getDirection(stored);
        document.documentElement.lang = stored;
    }, []);

    const handleLocaleChange = (newLocale: Locale) => {
        setLocale(newLocale);
        setStoredLocale(newLocale);
        setIsOpen(false);

        // Update document direction for RTL
        document.documentElement.dir = getDirection(newLocale);
        document.documentElement.lang = newLocale;

        // Apply Urdu font if needed
        if (newLocale === 'ur') {
            document.body.style.fontFamily = "'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', serif";
        } else {
            document.body.style.fontFamily = "";
        }

        onLocaleChange?.(newLocale);

        // Force re-render by refreshing
        window.location.reload();
    };

    return (
        <div className="relative">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                aria-label="Change language"
            >
                <Globe className="h-5 w-5 text-gray-600 dark:text-gray-300" />
                <span className="text-sm font-medium">{localeNames[locale]}</span>
            </button>

            {isOpen && (
                <div className="absolute top-full mt-1 right-0 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 py-1 min-w-[120px] z-50">
                    {supportedLocales.map((loc) => (
                        <button
                            key={loc}
                            onClick={() => handleLocaleChange(loc)}
                            className={`w-full px-4 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors ${locale === loc ? 'bg-primary/10 text-primary' : ''
                                } ${loc === 'ur' ? 'font-urdu text-right' : ''}`}
                            dir={getDirection(loc)}
                        >
                            {localeNames[loc]}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}
