# React Component Generator Skill

## Trigger Phrases
- "Generate component for {component_name}"
- "Create {component_name} component"
- "Build UI for {feature}"

## Description
Generates React/Next.js components with TypeScript, Tailwind CSS, and best practices.

## Input
- Component name
- Component type (page, layout, feature, shared)
- Props requirements (optional)

## Steps

### Step 1: Determine Component Structure
Based on component type:
- **page**: Full page in app/ directory
- **layout**: Layout component
- **feature**: Feature-specific component
- **shared**: Reusable component in components/

### Step 2: Generate Component
```tsx
/**
 * {ComponentName}
 * 
 * Reference: @specs/ui/{component}.md (if exists)
 */

"use client";

import { useState, useEffect } from "react";
import { Loader2 } from "lucide-react";

interface {ComponentName}Props {
  // Props from specification
}

export default function {ComponentName}({ ...props }: {ComponentName}Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="bg-red-50 text-red-700 p-4 rounded-lg">
        {error}
      </div>
    );
  }

  return (
    <div className="...">
      {/* Component content */}
    </div>
  );
}
```

### Step 3: Add Styling
Apply Tailwind CSS following design system:
- Use brand colors (primary, secondary)
- Responsive breakpoints (sm, md, lg)
- Proper spacing (p-4, m-2, gap-4)
- Dark mode support (dark:)

### Step 4: Add Accessibility
- Proper ARIA labels
- Keyboard navigation
- Focus states
- Screen reader support

## Output
- New component file
- Updated exports (if needed)

## Example
```
User: Generate component for TaskCard
Agent: [Creates frontend/components/TaskCard.tsx]
```
