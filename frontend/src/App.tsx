import React, { useState } from 'react';
import { UploadArea } from './components/UploadArea';
import { RoleSelector } from './components/RoleSelector';
import { ResultsDashboard } from './components/ResultsDashboard';
import { Chat } from './components/Chat';
import { Button } from './components/Button';
import { uploadResume, analyzeResume } from './services/api';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [file, setFile] = useState<File | null>(null);
  const [role, setRole] = useState<string>("");
  const [resumeData, setResumeData] = useState<any>(null);
  const [results, setResults] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async () => {
    if (!file) return;
    setIsLoading(true);
    setError(null);
    try {
      const data = await uploadResume(file);
      setResumeData(data.data);
      setStep(2);
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to upload resume");
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnalysis = async () => {
    if (!role || !resumeData) return;
    setIsLoading(true);
    setError(null);
    try {
      const data = await analyzeResume(resumeData, role);
      setResults(data);
      setStep(3);
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to analyze resume");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setStep(1);
    setFile(null);
    setRole("");
    setResults(null);
    setResumeData(null);
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-30">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-white font-bold">
              AI
            </div>
            <h1 className="font-bold text-xl text-slate-800 tracking-tight">ResumeReviewer</h1>
          </div>
          <a href="#" className="text-sm font-medium text-slate-600 hover:text-primary transition-colors">
            About
          </a>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-10">
        <AnimatePresence mode='wait'>
          {step === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="text-center space-y-8 py-10"
            >
              <div className="space-y-4 max-w-2xl mx-auto">
                <h2 className="text-4xl font-extrabold text-slate-900 leading-tight">
                  Optimize Your Resume for the <span className="text-primary">Perfect Role</span>
                </h2>
                <p className="text-lg text-slate-600">
                  Upload your PDF resume to get an instant ATS score, skill gap analysis, and personalized project recommendations using AI.
                </p>
              </div>

              <UploadArea 
                onFileSelect={setFile} 
                selectedFile={file} 
                onClear={() => setFile(null)} 
              />

              {error && (
                <div className="p-4 bg-red-50 text-red-600 rounded-lg max-w-md mx-auto">
                  {error}
                </div>
              )}

              <Button 
                onClick={handleFileUpload} 
                disabled={!file} 
                isLoading={isLoading}
                className="w-full max-w-xs text-lg py-3"
              >
                Continue to Role Selection
              </Button>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="text-center space-y-8"
            >
              <div className="space-y-2">
                <h2 className="text-3xl font-bold text-slate-900">Choose Your Target Role</h2>
                <p className="text-slate-600">Select the position you are targeting to get a tailored analysis.</p>
              </div>

              <RoleSelector selectedRole={role} onSelect={setRole} />

              {error && (
                <div className="p-4 bg-red-50 text-red-600 rounded-lg max-w-md mx-auto">
                  {error}
                </div>
              )}

              <div className="flex justify-center gap-4">
                <Button variant="secondary" onClick={() => setStep(1)}>Back</Button>
                <Button 
                  onClick={handleAnalysis} 
                  disabled={!role} 
                  isLoading={isLoading}
                  className="w-48"
                >
                  Analyze Resume
                </Button>
              </div>
            </motion.div>
          )}

          {step === 3 && results && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              <ResultsDashboard results={results} onReset={handleReset} />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Floating Chat Agent available in all steps */}
      <Chat context={results} />
    </div>
  );
}

export default App;