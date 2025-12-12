import React, { useCallback } from 'react';
import { UploadCloud, FileJson, FileType, X } from 'lucide-react';


interface UploadSectionProps {
  onFileSelect: (content: string, filename: string) => void;
  selectedFile: { name: string; size: number } | null;
  onClear: () => void;
}

const UploadSection: React.FC<UploadSectionProps> = ({ onFileSelect, selectedFile, onClear }) => {
  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    processFile(file);
  }, [onFileSelect]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = (file: File) => {
    if (!file) return;

    // Simple validation
    if (!file.name.endsWith('.json') && !file.name.endsWith('.yaml') && !file.name.endsWith('.yml')) {
      alert("Please upload a JSON or YAML file.");
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      onFileSelect(content, file.name);
    };
    reader.readAsText(file);
  };

  return (
    <div className="w-full">
      <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
        <FileJson className="w-5 h-5 text-blue-600" />
        OpenAPI 文档上传
      </h2>

      {!selectedFile ? (
        <div
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          className="border-2 border-dashed border-slate-300 rounded-lg p-8 text-center hover:border-blue-500 hover:bg-blue-50 transition-colors cursor-pointer relative"
        >
          <input
            type="file"
            accept=".json,.yaml,.yml"
            onChange={handleFileChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
          <div className="flex flex-col items-center justify-center text-slate-500">
            <UploadCloud className="w-12 h-12 mb-3 text-slate-400" />
            <p className="font-medium text-slate-700">点击或拖拽文件到这里</p>
            <p className="text-sm mt-1">支持 JSON 或 YAML 格式</p>
          </div>
        </div>
      ) : (
        <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-blue-100 p-2 rounded">
              <FileType className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <p className="font-medium text-slate-900">{selectedFile.name}</p>
              <p className="text-xs text-slate-500">{(selectedFile.size / 1024).toFixed(1)} KB</p>
            </div>
          </div>
          <button
            onClick={onClear}
            className="p-1 hover:bg-slate-200 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-slate-500" />
          </button>
        </div>
      )}
    </div>
  );
};

export default UploadSection;
