import React from "react";

interface StatCardProps {
    title: string;
    value: number;
    icon: React.ReactNode;
    colorTheme: "blue" | "emerald" | "amber";
}

export const StatCard: React.FC<StatCardProps> = ({ title, value, icon, colorTheme }) => {
    const colorStyles = {
        blue: "bg-blue-500/10 text-blue-500",
        emerald: "bg-emerald-500/10 text-emerald-500",
        amber: "bg-amber-500/10 text-amber-500",
    };

    return (
        <div className="bg-slate-900/50 backdrop-blur-xl border border-white/5 p-6 rounded-2xl flex items-center gap-4 hover:bg-slate-900 transition-colors">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${colorStyles[colorTheme]}`}>
                {icon}
            </div>
            <div>
                <p className="text-sm font-medium text-slate-400 mb-1">{title}</p>
                <p className="text-3xl font-bold text-white">{value}</p>
            </div>
        </div>
    );
};
