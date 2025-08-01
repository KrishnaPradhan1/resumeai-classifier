import React from 'react';
import './styles/globals.css';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          ResumeAI Classifier
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Advanced AI-based resume classification system
        </p>
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md mx-auto">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            🚀 Deployment Successful!
          </h2>
          <p className="text-gray-600 mb-6">
            The frontend is now deployed and working. Backend integration coming soon!
          </p>
          <div className="space-y-2 text-sm text-gray-500">
            <p>✅ React 18 + TypeScript</p>
            <p>✅ Tailwind CSS</p>
            <p>✅ Vercel Deployment</p>
            <p>✅ Railway Backend</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 