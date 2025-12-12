import { useState } from 'react';
import axios from 'axios';
import UploadSection from './components/UploadSection';
import ConfigPanel from './components/ConfigPanel';
import ResultEditor from './components/ResultEditor';
import { Bot, Sparkles, Terminal } from 'lucide-react';

// API Base URL - In dev, Vite proxy might be better, but hardcoding for simplicity now
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

function App() {
  // State
  const [specContent, setSpecContent] = useState<string>('');
  const [fileName, setFileName] = useState<string | null>(null);

  const [language, setLanguage] = useState('curl');
  const [tier, setTier] = useState('high');
  // Provider logic removed, using direct model settings
  const [baseUrl, setBaseUrl] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [modelName, setModelName] = useState('');

  const [includeBoundary, setIncludeBoundary] = useState(false);
  const [includeNegative, setIncludeNegative] = useState(true);

  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [selectedCaseId, setSelectedCaseId] = useState<string | null>(null);

  const handleFileSelect = (content: string, name: string) => {
    setSpecContent(content);
    setFileName(name);
    setResult(null); // Clear previous results
  };

  const handleClearFile = () => {
    setSpecContent('');
    setFileName(null);
    setResult(null);
  };

  const handleGenerate = async () => {
    if (!specContent) return;

    setIsGenerating(true);
    setResult(null);

    try {
      const payload = {
        openapi_content: specContent,
        target_language: language,
        llm_config: {
          base_url: baseUrl || undefined,
          api_key: apiKey || undefined,
          model_name: modelName,
          tier: tier
        },
        include_boundary: includeBoundary,
        include_negative: includeNegative
      };

      const response = await axios.post(`${API_BASE_URL}/generate`, payload);

      if (response.data.status === 'completed') {
        setResult(response.data.result);
        if (response.data.result.test_plan.length > 0) {
          setSelectedCaseId(response.data.result.test_plan[0].id);
        }
      } else {
        alert(`Generation failed: ${response.data.error || 'Unknown error'}`);
      }
    } catch (error: any) {
      console.error('Error generating tests:', error);
      alert(`Error calling API: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="h-screen bg-[#F8F9FC] flex flex-col font-sans text-slate-900 selection:bg-indigo-100 selection:text-indigo-900 overflow-hidden">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200/60 flex items-center justify-between px-8 py-4 shrink-0 z-20 shadow-sm">
        <div className="flex items-center gap-4">
          <div className="bg-gradient-to-br from-indigo-600 to-blue-500 p-2.5 rounded-xl shadow-lg shadow-indigo-500/30">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-700 tracking-tight">API Auto-Test Agent</h1>
            <p className="text-xs font-medium text-slate-500 flex items-center gap-1.5">
              <Terminal className="w-3 h-3" />
              Intelligent Test Generation System
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2 bg-indigo-50 px-3 py-1.5 rounded-full border border-indigo-100">
          <Sparkles className="w-4 h-4 text-indigo-500" />
          <span className="text-xs font-semibold text-indigo-700">Powered by LangGraph</span>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 min-h-0 max-w-[1800px] w-full mx-auto p-8 flex gap-8">
        {/* Left Column: Input & Config */}
        <div className="w-[420px] flex flex-col gap-8 shrink-0 overflow-y-auto h-full pb-32">
          <UploadSection
            onFileSelect={handleFileSelect}
            selectedFile={fileName ? { name: fileName, size: specContent.length } : null}
            onClear={handleClearFile}
          />

          <ConfigPanel
            language={language} setLanguage={setLanguage}
            tier={tier} setTier={setTier}
            // New generic generic props
            baseUrl={baseUrl} setBaseUrl={setBaseUrl}
            apiKey={apiKey} setApiKey={setApiKey}
            modelName={modelName} setModelName={setModelName}
            includeBoundary={includeBoundary} setIncludeBoundary={setIncludeBoundary}
            includeNegative={includeNegative} setIncludeNegative={setIncludeNegative}
            isGenerating={isGenerating}
            onGenerate={handleGenerate}
            canGenerate={!!specContent}
          />
        </div>

        {/* Right Column: Results */}
        <div className="flex-1 flex flex-col min-w-0 bg-white/50 rounded-2xl border border-slate-200 shadow-sm backdrop-blur-sm overflow-hidden h-full">
          <ResultEditor
            result={result}
            selectedCaseId={selectedCaseId}
            onCaseSelect={setSelectedCaseId}
            isGenerating={isGenerating}
          />
        </div>
      </main>
    </div>
  );
}

export default App;
