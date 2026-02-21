import React from "react";

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

interface TodoCardProps {
    todo: Todo;
    user: User | null;
    onDelete: (id: number) => void;
    onToggleComplete: (id: number, currentTodo: Todo) => void;
}

export const TodoCard: React.FC<TodoCardProps> = ({ todo, user, onDelete, onToggleComplete }) => {
    return (
        <div
            className={`group relative bg-slate-900/60 backdrop-blur-xl border rounded-2xl p-6 transition-all duration-300 hover:shadow-2xl hover:-translate-y-1 overflow-hidden flex flex-col
        ${todo.Complete ? 'border-emerald-500/20 hover:border-emerald-500/40 opacity-80' : 'border-slate-800 hover:border-indigo-500/40 hover:shadow-indigo-500/10'}
      `}
        >
            {/* Priority Indicator Top Bar */}
            <div className={`absolute top-0 left-0 w-full h-1 
        ${todo.Priority >= 5 ? 'bg-gradient-to-r from-red-500 to-rose-400' :
                    todo.Priority >= 3 ? 'bg-gradient-to-r from-amber-500 to-yellow-400' :
                        'bg-gradient-to-r from-blue-500 to-indigo-400'}
      `}></div>

            <div className="flex justify-between items-start mb-4">
                <div className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold
          ${todo.Complete ? 'bg-emerald-500/10 text-emerald-400' : 'bg-slate-800 text-slate-300'}
        `}>
                    {todo.Complete ? (
                        <><span className="w-1.5 h-1.5 bg-emerald-400 rounded-full mr-2"></span>Completed</>
                    ) : (
                        <><span className="w-1.5 h-1.5 bg-slate-400 rounded-full mr-2 animate-pulse"></span>In Progress</>
                    )}
                </div>

                <div className="flex items-center gap-2">
                    <span className="text-xs font-medium text-slate-500 bg-slate-800/50 px-2 py-1 rounded border border-slate-700/50 shadow-sm">
                        Pri: {todo.Priority}
                    </span>
                    <button
                        onClick={() => onDelete(todo.ID)}
                        className="opacity-0 group-hover:opacity-100 transition-opacity p-1.5 text-slate-400 hover:text-red-400 hover:bg-red-400/10 rounded-lg"
                        title="Delete Task"
                    >
                        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                    </button>
                </div>
            </div>

            <div className="flex-grow">
                <h3 className={`text-lg font-bold mb-2 transition-colors ${todo.Complete ? 'text-slate-400 line-through decoration-slate-600' : 'text-white'}`}>
                    {todo.Title}
                </h3>
                <p className="text-sm text-slate-400 line-clamp-3 mb-6 leading-relaxed">
                    {todo.Description || "No description provided."}
                </p>
            </div>

            <div className="mt-auto pt-4 border-t border-slate-800/80 flex justify-between items-center">
                <div className="flex -space-x-2">
                    <div className="w-8 h-8 rounded-full border-2 border-slate-900 bg-indigo-500 flex items-center justify-center text-xs font-bold text-white shadow-sm" title={user?.username}>
                        {user?.username?.charAt(0).toUpperCase()}
                    </div>
                </div>
                {!todo.Complete && (
                    <button 
                        onClick={() => onToggleComplete(todo.ID, todo)}
                        className="text-sm font-semibold text-indigo-400 hover:text-indigo-300 transition-colors flex items-center gap-1.5 group/btn"
                    >
                        <span className="group-hover/btn:-translate-y-0.5 transition-transform">Done</span>
                        <svg className="w-4 h-4 group-hover/btn:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                    </button>
                )}
                {todo.Complete && (
                    <div className="text-sm font-semibold text-emerald-500 flex items-center gap-1.5 bg-emerald-500/10 px-2 py-1 rounded-md">
                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span>Finished</span>
                    </div>
                )}
            </div>
        </div>
    );
};