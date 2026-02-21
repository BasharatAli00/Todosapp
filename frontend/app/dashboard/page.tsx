"use client";

import React, { useEffect, useState } from "react";
import api from "../../lib/api";
import { Navbar } from "../../components/dashboard/Navbar";
import { StatCard } from "../../components/dashboard/StatCard";
import { TodoCard } from "../../components/dashboard/TodoCard";
import { CreateTodoModal } from "../../components/dashboard/createtodoModal";
// 1. THIS IS THE NEW IMPORT
import { AiChatWidget } from "../../components/dashboard/AiChatWidget"; 

interface User {
  username: string;
  user_id: number;
  user_role: string;
}

interface Todo {
  ID: number;
  Title: string;
  Description: string;
  Priority: number;
  Complete: boolean;
  Owner_id: number;
}

const DashboardPage = () => {
  const [user, setUser] = useState<User | null>(null);
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Fetch user info and todos
  useEffect(() => {
    const fetchUserAndTodos = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) {
        setError("You are not logged in");
        setLoading(false);
        return;
      }

      try {
        const userResp = await api.get("/auth/current_user", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUser(userResp.data);

        // Fetch todos
        const todosResp = await api.get("/todos/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setTodos(todosResp.data);
      } catch (err: any) {
        console.error(err);
        setError(err.response?.data?.detail || "Failed to fetch data");
      } finally {
        setLoading(false);
      }
    };

    fetchUserAndTodos();
  }, []);

  // Logout
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    window.location.href = "/login";
  };

  // Create Todo
  const handleCreateTodo = async (title: string, description: string, priority: number) => {
    const token = localStorage.getItem("access_token");
    const payload = {
      Title: title,
      Description: description,
      Priority: priority,
      Complete: false,
    };

    await api.post("/todos/todocreate", payload, {
      headers: { Authorization: `Bearer ${token}` },
    });

    // Refresh the todos list to get the newly created task with its ID from the database
    const todosResp = await api.get("/todos/", {
      headers: { Authorization: `Bearer ${token}` },
    });
    setTodos(todosResp.data);
  };

  // Toggle Complete (Update)
  const handleToggleComplete = async (id: number, currentTodo: Todo) => {
    const token = localStorage.getItem("access_token");
    try {
      // Optimistic UI update (feels instantly responsive)
      setTodos(todos.map((t) => (t.ID === id ? { ...t, Complete: true } : t)));

      await api.put(
        `/todos/todo/update/${id}`,
        {
          Title: currentTodo.Title,
          Description: currentTodo.Description,
          Priority: currentTodo.Priority,
          Complete: true,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
    } catch (err: any) {
      alert("Failed to update task status.");
      // Revert optimistic update on failure
      setTodos(todos.map((t) => (t.ID === id ? { ...t, Complete: false } : t)));
    }
  };

  // Delete todo
  const handleDelete = async (id: number) => {
    const token = localStorage.getItem("access_token");
    try {
      await api.delete(`/todos/delete_todo/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTodos(todos.filter((t) => t.ID !== id));
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to delete");
    }
  };

  // Stats calculation
  const totalTodos = todos.length;
  const completedTodos = todos.filter((t) => t.Complete).length;
  const pendingTodos = totalTodos - completedTodos;

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-slate-400 font-medium animate-pulse">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
        <div className="bg-slate-900 border border-red-500/30 p-8 rounded-2xl max-w-md w-full text-center">
          <div className="w-16 h-16 bg-red-500/10 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-white mb-2">Access Denied</h2>
          <p className="text-slate-400 mb-6">{error}</p>
          <button
            onClick={() => (window.location.href = "/login")}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 px-4 rounded-xl transition-all"
          >
            Return to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-indigo-500/30 relative overflow-hidden">
      {/* Background glow effects */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-[120px] pointer-events-none"></div>

      {/* Navbar Component */}
      <Navbar user={user} onLogout={handleLogout} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10 w-full">
        {/* Welcome Section */}
        <div className="mb-10 mt-4">
          <h1 className="text-3xl sm:text-4xl font-extrabold text-white mb-2 tracking-tight">
            Welcome back, <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">{user?.username}</span> 👋
          </h1>
          <p className="text-slate-400 text-lg">Here's an overview of your tasks for today.</p>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-10">
          <StatCard
            title="Total Tasks"
            value={totalTodos}
            colorTheme="blue"
            icon={
              <svg className="w-6 h-6 text-current" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            }
          />
          <StatCard
            title="Completed"
            value={completedTodos}
            colorTheme="emerald"
            icon={
              <svg className="w-6 h-6 text-current" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            }
          />
          <StatCard
            title="Pending"
            value={pendingTodos}
            colorTheme="amber"
            icon={
              <svg className="w-6 h-6 text-current" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            }
          />
        </div>

        {/* Todos Section Title */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            Your Tasks
            <span className="bg-indigo-500/20 text-indigo-300 text-xs font-semibold px-2.5 py-0.5 rounded-full">
              {todos.length}
            </span>
          </h2>
          <button
            onClick={() => setIsModalOpen(true)}
            className="bg-indigo-600 hover:bg-indigo-500 transition-colors text-white text-sm font-medium px-4 py-2 rounded-xl flex items-center gap-2 shadow-lg shadow-indigo-500/25"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Task
          </button>
        </div>

        {/* Todos List */}
        {todos.length === 0 ? (
          <div className="bg-slate-900/30 border border-dashed border-slate-700/50 rounded-3xl p-12 text-center flex flex-col items-center">
            <div className="w-20 h-20 bg-slate-800/80 rounded-full flex items-center justify-center mb-6 shadow-inner border border-white/5">
              <svg className="w-10 h-10 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-white mb-2">No tasks yet</h3>
            <p className="text-slate-400 max-w-md mx-auto mb-6">You're all caught up! Enjoy your free time or add a new task to get started on your next goal.</p>
            <button
              onClick={() => setIsModalOpen(true)}
              className="bg-white text-slate-900 hover:bg-slate-200 transition-colors font-semibold px-6 py-3 rounded-xl shadow-lg"
            >
              Create your first task
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {todos.map((todo) => (
              <TodoCard
                key={todo.ID}
                todo={todo}
                user={user}
                onDelete={handleDelete}
                onToggleComplete={handleToggleComplete}
              />
            ))}
          </div>
        )}
      </main>

      {/* Create Todo Modal */}
      <CreateTodoModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreateTodo}
      />

      {/* 2. THIS IS THE NEW WIDGET RENDERED AT THE BOTTOM */}
      <AiChatWidget />
      
    </div>
  );
};

export default DashboardPage;