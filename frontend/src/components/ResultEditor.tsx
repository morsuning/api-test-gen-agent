import React from 'react';
import { Copy, FileCode, ListChecks } from 'lucide-react';
import { cn } from '../utils';

interface GenerateResult {
    generated_code: Record<string, string>;
    test_plan: Array<{
        id: string;
        name: string;
        description: string;
        type: string;
        endpoint: string;
        method: string;
    }>;
}

interface ResultEditorProps {
    result: GenerateResult | null;
    selectedCaseId: string | null;
    onCaseSelect: (id: string) => void;
    isGenerating: boolean;
}

const ResultEditor: React.FC<ResultEditorProps> = ({ result, selectedCaseId, onCaseSelect, isGenerating }) => {
    if (isGenerating) {
        return (
            <div className="flex-1 bg-white rounded-xl border border-slate-200 shadow-sm p-8 flex flex-col items-center justify-center text-slate-500 min-h-[500px]">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                <p className="text-lg font-medium text-slate-700">正在生成测试用例...</p>
                <p className="text-sm mt-2">AI 正在分析接口并编写代码，这可能需要几十秒。</p>
            </div>
        );
    }

    if (!result) {
        return (
            <div className="flex-1 bg-white rounded-xl border border-slate-200 shadow-sm p-8 flex flex-col items-center justify-center text-slate-400 min-h-[500px]">
                <FileCode className="w-16 h-16 mb-4 opacity-20" />
                <p className="text-lg font-medium text-slate-500">等待生成结果</p>
                <p className="text-sm mt-1">请上传文件配置后点击生成</p>
            </div>
        );
    }

    const selectedCode = selectedCaseId && result.generated_code[selectedCaseId]
        ? result.generated_code[selectedCaseId]
        : Object.values(result.generated_code)[0] || "// No code generated";

    // Set default selection if none
    if (!selectedCaseId && result.test_plan.length > 0) {
        // Ideally this side effect should be in parent or useEffect, 
        // but purely for display fallback it's okay.
    }

    return (
        <div className="flex-1 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col h-[calc(100vh-120px)] overflow-hidden">
            <div className="flex h-full">
                {/* Left Sidebar: Test Plan List */}
                <div className="w-1/3 border-r border-slate-200 flex flex-col bg-slate-50">
                    <div className="p-4 border-b border-slate-200 bg-white">
                        <h3 className="font-semibold text-slate-800 flex items-center gap-2">
                            <ListChecks className="w-4 h-4 text-blue-600" />
                            测试用例列表 ({result.test_plan.length})
                        </h3>
                    </div>
                    <div className="overflow-y-auto flex-1 p-2 space-y-2">
                        {result.test_plan.map((item) => (
                            <button
                                key={item.id}
                                onClick={() => onCaseSelect(item.id)}
                                className={cn(
                                    "w-full text-left p-3 rounded-lg text-sm border transition-all",
                                    selectedCaseId === item.id || (!selectedCaseId && result.test_plan[0].id === item.id)
                                        ? "bg-white border-blue-500 shadow-sm ring-1 ring-blue-500"
                                        : "bg-transparent border-transparent hover:bg-slate-200"
                                )}
                            >
                                <div className="font-medium text-slate-900 truncate">{item.name}</div>
                                <div className="flex items-center gap-2 mt-1">
                                    <span className={cn(
                                        "px-1.5 py-0.5 rounded text-[10px] font-medium uppercase tracking-wider",
                                        item.method === "GET" ? "bg-blue-100 text-blue-700" :
                                            item.method === "POST" ? "bg-green-100 text-green-700" :
                                                item.method === "PUT" ? "bg-orange-100 text-orange-700" :
                                                    item.method === "DELETE" ? "bg-red-100 text-red-700" :
                                                        "bg-slate-100 text-slate-700"
                                    )}>
                                        {item.method}
                                    </span>
                                    <span className="text-xs text-slate-500 truncate flex-1">{item.endpoint}</span>
                                </div>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Right Content: Code Editor View */}
                <div className="flex-1 flex flex-col bg-[#1e1e1e] text-white">
                    <div className="flex items-center justify-between px-4 py-3 border-b border-[#333] bg-[#252526]">
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 rounded-full bg-red-500"></div>
                            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                            <div className="w-3 h-3 rounded-full bg-green-500"></div>
                            <span className="ml-2 text-xs text-gray-400 font-mono">Generated Code</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <button
                                onClick={() => navigator.clipboard.writeText(selectedCode)}
                                className="p-1.5 hover:bg-[#333] rounded text-gray-400 hover:text-white transition-colors"
                                title="Copy"
                            >
                                <Copy className="w-4 h-4" />
                            </button>
                        </div>
                    </div>
                    <div className="flex-1 overflow-auto p-4 font-mono text-sm leading-relaxed">
                        <pre className="whitespace-pre-wrap break-all text-gray-300">
                            {selectedCode}
                        </pre>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResultEditor;
