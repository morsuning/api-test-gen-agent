import React, { useState, useEffect } from 'react';
import { Settings, Code2, BrainCircuit, Key, Server, Cpu, Save, X } from 'lucide-react';
import { cn } from '../utils';
import axios from 'axios';

interface ConfigPanelProps {
    language: string;
    setLanguage: (lang: string) => void;
    tier: string;
    setTier: (tier: string) => void;
    // Provider removed, now generic
    baseUrl: string;
    setBaseUrl: (url: string) => void;
    apiKey: string;
    setApiKey: (key: string) => void;
    modelName: string;
    setModelName: (name: string) => void;
    includeBoundary: boolean;
    setIncludeBoundary: (val: boolean) => void;
    includeNegative: boolean;
    setIncludeNegative: (val: boolean) => void;
    isGenerating: boolean;
    onGenerate: () => void;
    canGenerate: boolean;
}

const ConfigPanel: React.FC<ConfigPanelProps> = ({
    language, setLanguage,
    tier, setTier,
    baseUrl, setBaseUrl,
    apiKey, setApiKey,
    modelName, setModelName,
    includeBoundary, setIncludeBoundary,
    includeNegative, setIncludeNegative,
    isGenerating, onGenerate, canGenerate
}) => {
    const [showSettings, setShowSettings] = useState(false);
    const [isSaving, setIsSaving] = useState(false);

    // Load settings on mount
    useEffect(() => {
        const fetchSettings = async () => {
            try {
                const res = await axios.get(`http://127.0.0.1:8000/api/v1/settings?_t=${new Date().getTime()}`);
                if (res.data) {
                    if (res.data.base_url) setBaseUrl(res.data.base_url);
                    if (res.data.api_key) setApiKey(res.data.api_key);
                    if (res.data.model_name) setModelName(res.data.model_name);
                    // Set language only if valid, otherwise keep default (curl)
                    if (res.data.language && ['go', 'java', 'curl'].includes(res.data.language)) {
                        setLanguage(res.data.language);
                    }
                }
            } catch (e) {
                console.error("Failed to load settings", e);
            }
        };
        fetchSettings();
    }, []); // Run once on mount

    const handleSaveSettings = async () => {
        setIsSaving(true);
        try {
            await axios.post('http://127.0.0.1:8000/api/v1/settings', {
                base_url: baseUrl,
                api_key: apiKey,
                model_name: modelName,
                language: language
            });
            setShowSettings(false);
        } catch (e) {
            alert("Failed to save settings");
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="w-full bg-white/70 backdrop-blur-xl rounded-2xl border border-white/20 shadow-xl relative group">
            {/* Background Effects Wrapper - Clips only the blobs */}
            <div className="absolute inset-0 overflow-hidden rounded-2xl -z-10 bg-white/40">
                <div className="absolute top-0 right-0 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none" />
                <div className="absolute bottom-0 left-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -ml-16 -mb-16 pointer-events-none" />
            </div>

            <div className="p-6 relative">
                <h2 className="text-xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent mb-6 flex items-center justify-between">
                    <span className="flex items-center gap-2">
                        <BrainCircuit className="w-6 h-6 text-indigo-600" />
                        配置中心
                    </span>
                    <button
                        onClick={() => setShowSettings(!showSettings)}
                        className="p-2 rounded-full hover:bg-slate-100 transition-colors text-slate-500 hover:text-indigo-600"
                        title="模型设置"
                    >
                        <Settings className="w-5 h-5" />
                    </button>
                </h2>

                {/* Settings Modal/Overlay - Fixed Position to break out of container */}
                {showSettings && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
                        {/* Backdrop */}
                        <div
                            className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity"
                            onClick={() => setShowSettings(false)}
                        />

                        {/* Modal Content */}
                        <div className="relative w-full max-w-md bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/20 p-6 animate-in zoom-in-95 duration-200">
                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2">
                                    <Settings className="w-5 h-5 text-indigo-600" /> 模型接入配置
                                </h3>
                                <button onClick={() => setShowSettings(false)} className="p-1.5 hover:bg-slate-100 text-slate-400 hover:text-slate-600 rounded-full transition-colors">
                                    <X className="w-5 h-5" />
                                </button>
                            </div>

                            <div className="space-y-4">
                                <div>
                                    <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
                                        <Server className="w-3 h-3 inline mr-1" />Base URL
                                    </label>
                                    <input
                                        type="text"
                                        value={baseUrl}
                                        onChange={(e) => setBaseUrl(e.target.value)}
                                        placeholder="https://api.openai.com/v1"
                                        className="w-full rounded-lg border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all text-sm py-2 px-3 font-mono"
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
                                        <Key className="w-3 h-3 inline mr-1" />API Key
                                    </label>
                                    <input
                                        type="password"
                                        value={apiKey}
                                        onChange={(e) => setApiKey(e.target.value)}
                                        placeholder="sk-..."
                                        className="w-full rounded-lg border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all text-sm py-2 px-3 font-mono"
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
                                        <Cpu className="w-3 h-3 inline mr-1" />Model Name
                                    </label>
                                    <input
                                        type="text"
                                        value={modelName}
                                        onChange={(e) => setModelName(e.target.value)}
                                        placeholder="gpt-4, qwen-max, etc"
                                        className="w-full rounded-lg border-slate-200 bg-slate-50 focus:bg-white focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all text-sm py-2 px-3 font-mono"
                                    />
                                </div>
                            </div>

                            <button
                                onClick={handleSaveSettings}
                                disabled={isSaving}
                                className="mt-6 w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium shadow-lg shadow-indigo-500/20 active:scale-[0.98] transition-all flex items-center justify-center gap-2"
                            >
                                {isSaving ? '保存中...' : <><Save className="w-4 h-4" /> 保存并生效</>}
                            </button>
                        </div>
                    </div>
                )}

                <div className="space-y-6">
                    {/* Language Selection */}
                    <div className="group/input">
                        <label className="block text-sm font-medium text-slate-700 mb-2 flex items-center gap-2 group-focus-within/input:text-indigo-600 transition-colors">
                            <Code2 className="w-4 h-4" />
                            目标语言 (Target Language)
                        </label>
                        <div className="relative">
                            <select
                                value={language}
                                onChange={(e) => setLanguage(e.target.value)}
                                className="w-full appearance-none rounded-xl border-slate-200 bg-slate-50/50 hover:bg-white focus:bg-white shadow-sm focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 py-3 px-4 text-slate-700 transition-all cursor-pointer"
                                disabled={isGenerating}
                            >
                                <option value="go">Go (Golang)</option>
                                <option value="java">Java</option>
                                <option value="curl">cURL (Shell)</option>
                            </select>
                            <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
                            </div>
                        </div>
                    </div>

                    {/* Generic Tier Selection */}
                    <div>
                        <label className="block text-sm font-medium text-slate-700 mb-3 flex items-center gap-2">
                            <BrainCircuit className="w-4 h-4" />
                            处理策略 (Strategy)
                        </label>
                        <div className="grid grid-cols-2 gap-3">
                            <button
                                onClick={() => setTier('high')}
                                disabled={isGenerating}
                                className={cn(
                                    "p-3 rounded-xl border text-left transition-all duration-300 relative overflow-hidden group hover:shadow-md",
                                    tier === 'high'
                                        ? "border-indigo-500 bg-indigo-50/50 ring-2 ring-indigo-500/20"
                                        : "border-slate-200 bg-white hover:border-indigo-300"
                                )}
                            >
                                <div className={cn("font-bold text-sm mb-1", tier === 'high' ? "text-indigo-700" : "text-slate-700")}>深度思考 (Deep)</div>
                                <div className="text-xs text-slate-500 leading-relaxed">
                                    完整推理，适合复杂逻辑。
                                    <br />
                                    <span className="opacity-75">推荐使用 &gt;200B 参数的推理型大模型。</span>
                                </div>
                                {tier === 'high' && <div className="absolute top-0 right-0 p-1"><div className="w-2 h-2 bg-indigo-500 rounded-full shadow-lg shadow-indigo-500/50"></div></div>}
                            </button>
                            <button
                                onClick={() => setTier('low')}
                                disabled={isGenerating}
                                className={cn(
                                    "p-3 rounded-xl border text-left transition-all duration-300 relative overflow-hidden group hover:shadow-md",
                                    tier === 'low'
                                        ? "border-indigo-500 bg-indigo-50/50 ring-2 ring-indigo-500/20"
                                        : "border-slate-200 bg-white hover:border-indigo-300"
                                )}
                            >
                                <div className={cn("font-bold text-sm mb-1", tier === 'low' ? "text-indigo-700" : "text-slate-700")}>快速响应 (Fast)</div>
                                <div className="text-xs text-slate-500 leading-relaxed">
                                    结构化输出，速度优先。
                                    <br />
                                    <span className="opacity-75">适合简单 CRUD 或原型。</span>
                                </div>
                                {tier === 'low' && <div className="absolute top-0 right-0 p-1"><div className="w-2 h-2 bg-indigo-500 rounded-full shadow-lg shadow-indigo-500/50"></div></div>}
                            </button>
                        </div>
                    </div>

                    {/* Options */}
                    <div className="bg-slate-50/50 p-4 rounded-xl border border-slate-100">
                        <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">生成选项 (Options)</label>
                        <div className="space-y-3">
                            <label className="flex items-center gap-3 cursor-pointer group">
                                <div className="relative flex items-center">
                                    <input
                                        type="checkbox"
                                        checked={includeNegative}
                                        onChange={(e) => setIncludeNegative(e.target.checked)}
                                        disabled={isGenerating}
                                        className="peer h-5 w-5 cursor-pointer appearance-none rounded-md border border-slate-300 transition-all checked:border-indigo-600 checked:bg-indigo-600 focus:ring-2 focus:ring-indigo-500/20"
                                    />
                                    <div className="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-white opacity-0 transition-opacity peer-checked:opacity-100">
                                        <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                    </div>
                                </div>
                                <span className="text-sm text-slate-600 group-hover:text-slate-900 transition-colors">包含逆向测试 (Negative/400)</span>
                            </label>
                            <label className="flex items-center gap-3 cursor-pointer group">
                                <div className="relative flex items-center">
                                    <input
                                        type="checkbox"
                                        checked={includeBoundary}
                                        onChange={(e) => setIncludeBoundary(e.target.checked)}
                                        disabled={isGenerating}
                                        className="peer h-5 w-5 cursor-pointer appearance-none rounded-md border border-slate-300 transition-all checked:border-indigo-600 checked:bg-indigo-600 focus:ring-2 focus:ring-indigo-500/20"
                                    />
                                    <div className="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-white opacity-0 transition-opacity peer-checked:opacity-100">
                                        <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                    </div>
                                </div>
                                <span className="text-sm text-slate-600 group-hover:text-slate-900 transition-colors">包含边界测试 (Boundary)</span>
                            </label>
                        </div>
                    </div>

                    {/* Generate Button */}
                    <button
                        onClick={onGenerate}
                        disabled={!canGenerate || isGenerating}
                        className={cn(
                            "w-full py-4 px-4 rounded-xl font-bold text-white shadow-lg shadow-indigo-500/20 transition-all flex items-center justify-center gap-2 transform active:scale-[0.98]",
                            !canGenerate || isGenerating
                                ? 'bg-slate-300 cursor-not-allowed shadow-none'
                                : 'bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 hover:shadow-indigo-500/40'
                        )}
                    >
                        {isGenerating ? (
                            <><div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" /> 正在生成中...</>
                        ) : (
                            <><BrainCircuit className="w-5 h-5" /> 开始生成测试计划</>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ConfigPanel;
