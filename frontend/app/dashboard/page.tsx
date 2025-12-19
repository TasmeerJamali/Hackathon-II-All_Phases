/**
 * Dashboard Page - Task Management
 * 
 * Reference: @specs/ui/pages.md
 * Reference: @specs/features/task-crud.md
 * 
 * Per AC-002.1: Display all tasks belonging to current user
 * Per AC-002.2: Show task ID, title, and status indicator
 * Per AC-002.3: Status shows ✅ for complete, ❌ for pending
 */

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
    Plus,
    CheckCircle2,
    Circle,
    Trash2,
    Edit2,
    LogOut,
    Loader2,
    Search,
    MessageCircle,
} from "lucide-react";
import { api, Task, CreateTaskInput } from "@/lib/api";

export default function DashboardPage() {
    const router = useRouter();
    const [tasks, setTasks] = useState<Task[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [userId, setUserId] = useState<string | null>(null);

    // Form state
    const [showForm, setShowForm] = useState(false);
    const [newTitle, setNewTitle] = useState("");
    const [newDescription, setNewDescription] = useState("");
    const [newPriority, setNewPriority] = useState<"high" | "medium" | "low">("medium");

    // Filter state
    const [filter, setFilter] = useState<"all" | "pending" | "completed">("all");
    const [search, setSearch] = useState("");

    useEffect(() => {
        const storedUserId = localStorage.getItem("user_id");
        if (!storedUserId) {
            router.push("/login");
            return;
        }
        setUserId(storedUserId);
    }, [router]);

    // Fetch tasks when userId changes
    useEffect(() => {
        if (userId) {
            fetchTasks();
        }
    }, [userId, filter, search]);

    const fetchTasks = async () => {
        if (!userId) return;

        setLoading(true);
        try {
            const options: { completed?: boolean; search?: string } = {};
            if (filter === "pending") options.completed = false;
            if (filter === "completed") options.completed = true;
            if (search) options.search = search;

            const data = await api.getTasks(userId, options);
            setTasks(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to fetch tasks");
        } finally {
            setLoading(false);
        }
    };

    const handleCreateTask = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!userId || !newTitle.trim()) return;

        try {
            const task: CreateTaskInput = {
                title: newTitle.trim(),
                description: newDescription.trim(),
                priority: newPriority,
            };
            await api.createTask(userId, task);
            setNewTitle("");
            setNewDescription("");
            setShowForm(false);
            fetchTasks();
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to create task");
        }
    };

    const handleToggleComplete = async (taskId: number) => {
        if (!userId) return;
        try {
            await api.toggleComplete(userId, taskId);
            fetchTasks();
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to update task");
        }
    };

    const handleDeleteTask = async (taskId: number) => {
        if (!userId) return;
        if (!confirm("Are you sure you want to delete this task?")) return;

        try {
            await api.deleteTask(userId, taskId);
            fetchTasks();
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to delete task");
        }
    };

    const handleLogout = () => {
        localStorage.removeItem("auth_token");
        localStorage.removeItem("user_id");
        router.push("/login");
    };

    const priorityBadge = (priority: string) => {
        const colors = {
            high: "bg-red-100 text-red-800",
            medium: "bg-yellow-100 text-yellow-800",
            low: "bg-green-100 text-green-800",
        };
        return colors[priority as keyof typeof colors] || colors.medium;
    };

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white shadow-sm">
                <div className="max-w-4xl mx-auto px-4 py-4 flex justify-between items-center">
                    <h1 className="text-2xl font-bold text-primary">Todo Evolution</h1>
                    <div className="flex items-center gap-4">
                        <button
                            onClick={() => router.push("/chat")}
                            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-lg hover:from-purple-600 hover:to-blue-600 transition-all shadow-sm"
                        >
                            <MessageCircle className="h-5 w-5" />
                            Chat with AI
                        </button>
                        <button
                            onClick={handleLogout}
                            className="flex items-center gap-2 text-gray-600 hover:text-gray-900"
                        >
                            <LogOut className="h-5 w-5" />
                            Logout
                        </button>
                    </div>
                </div>
            </header>

            <main className="max-w-4xl mx-auto px-4 py-8">
                {/* Error Message */}
                {error && (
                    <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                        {error}
                        <button onClick={() => setError("")} className="float-right">&times;</button>
                    </div>
                )}

                {/* Controls */}
                <div className="flex flex-col sm:flex-row gap-4 mb-6">
                    {/* Search */}
                    <div className="relative flex-1">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search tasks..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            className="pl-10 w-full rounded-lg border border-gray-300 px-3 py-2"
                        />
                    </div>

                    {/* Filter */}
                    <select
                        value={filter}
                        onChange={(e) => setFilter(e.target.value as typeof filter)}
                        className="rounded-lg border border-gray-300 px-3 py-2"
                    >
                        <option value="all">All Tasks</option>
                        <option value="pending">Pending</option>
                        <option value="completed">Completed</option>
                    </select>

                    {/* Add Button */}
                    <button
                        onClick={() => setShowForm(!showForm)}
                        className="flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        <Plus className="h-5 w-5" />
                        Add Task
                    </button>
                </div>

                {/* Add Task Form */}
                {showForm && (
                    <form
                        onSubmit={handleCreateTask}
                        className="mb-6 bg-white p-4 rounded-lg shadow-sm border"
                    >
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Title (required, 1-200 chars)
                                </label>
                                <input
                                    type="text"
                                    value={newTitle}
                                    onChange={(e) => setNewTitle(e.target.value)}
                                    maxLength={200}
                                    required
                                    className="w-full rounded-lg border border-gray-300 px-3 py-2"
                                    placeholder="Task title..."
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Description (optional, max 1000 chars)
                                </label>
                                <textarea
                                    value={newDescription}
                                    onChange={(e) => setNewDescription(e.target.value)}
                                    maxLength={1000}
                                    rows={3}
                                    className="w-full rounded-lg border border-gray-300 px-3 py-2"
                                    placeholder="Task description..."
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Priority
                                </label>
                                <select
                                    value={newPriority}
                                    onChange={(e) => setNewPriority(e.target.value as typeof newPriority)}
                                    className="rounded-lg border border-gray-300 px-3 py-2"
                                >
                                    <option value="high">High</option>
                                    <option value="medium">Medium</option>
                                    <option value="low">Low</option>
                                </select>
                            </div>
                        </div>
                        <div className="mt-4 flex gap-2">
                            <button
                                type="submit"
                                className="bg-primary text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                            >
                                Create Task
                            </button>
                            <button
                                type="button"
                                onClick={() => setShowForm(false)}
                                className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300"
                            >
                                Cancel
                            </button>
                        </div>
                    </form>
                )}

                {/* Task List */}
                {loading ? (
                    <div className="flex justify-center py-8">
                        <Loader2 className="h-8 w-8 animate-spin text-primary" />
                    </div>
                ) : tasks.length === 0 ? (
                    <div className="text-center py-12 text-gray-500">
                        No tasks found. Create your first task!
                    </div>
                ) : (
                    <div className="space-y-3">
                        {tasks.map((task) => (
                            <div
                                key={task.id}
                                className={`bg-white p-4 rounded-lg shadow-sm border flex items-start gap-4 ${task.completed ? "opacity-75" : ""
                                    }`}
                            >
                                {/* Toggle Complete - Per AC-002.3 */}
                                <button
                                    onClick={() => handleToggleComplete(task.id)}
                                    className="mt-1 flex-shrink-0"
                                >
                                    {task.completed ? (
                                        <CheckCircle2 className="h-6 w-6 text-green-500" />
                                    ) : (
                                        <Circle className="h-6 w-6 text-gray-400" />
                                    )}
                                </button>

                                {/* Task Details - Per AC-002.2 */}
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-2">
                                        <span className="text-xs text-gray-400">#{task.id}</span>
                                        <span className={`text-xs px-2 py-0.5 rounded-full ${priorityBadge(task.priority)}`}>
                                            {task.priority}
                                        </span>
                                    </div>
                                    <h3
                                        className={`font-medium ${task.completed ? "line-through text-gray-500" : ""
                                            }`}
                                    >
                                        {task.title}
                                    </h3>
                                    {task.description && (
                                        <p className="text-sm text-gray-600 mt-1">{task.description}</p>
                                    )}
                                    <p className="text-xs text-gray-400 mt-2">
                                        Created: {new Date(task.created_at).toLocaleDateString()}
                                    </p>
                                </div>

                                {/* Actions */}
                                <div className="flex gap-2">
                                    <button
                                        onClick={() => handleDeleteTask(task.id)}
                                        className="p-2 text-red-500 hover:bg-red-50 rounded"
                                    >
                                        <Trash2 className="h-5 w-5" />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}
