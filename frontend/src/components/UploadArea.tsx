import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface UploadAreaProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  onClear: () => void;
}

export const UploadArea: React.FC<UploadAreaProps> = ({ onFileSelect, selectedFile, onClear }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    multiple: false
  });

  return (
    <div className="w-full max-w-xl mx-auto">
      <AnimatePresence mode='wait'>
        {!selectedFile ? (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            key="dropzone"
            {...getRootProps()}
            className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors
              ${isDragActive ? 'border-primary bg-blue-50' : 'border-slate-300 hover:border-primary hover:bg-slate-50'}
            `}
          >
            <input {...getInputProps()} />
            <div className="flex flex-col items-center gap-4">
              <div className="p-4 bg-blue-100 text-primary rounded-full">
                <Upload size={32} />
              </div>
              <div>
                <p className="text-lg font-medium text-slate-700">
                  {isDragActive ? "Drop your resume here" : "Drag & drop your resume"}
                </p>
                <p className="text-sm text-slate-500 mt-1">Only PDF files are supported</p>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            key="preview"
            className="bg-white border rounded-xl p-6 shadow-sm flex items-center justify-between"
          >
            <div className="flex items-center gap-4">
              <div className="p-3 bg-red-100 text-red-600 rounded-lg">
                <FileText size={24} />
              </div>
              <div className="text-left">
                <p className="font-medium text-slate-900 truncate max-w-[200px]">{selectedFile.name}</p>
                <p className="text-sm text-slate-500">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            </div>
            <button 
              onClick={(e) => { e.stopPropagation(); onClear(); }}
              className="p-2 hover:bg-slate-100 rounded-full text-slate-500 hover:text-red-500 transition-colors"
            >
              <X size={20} />
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
