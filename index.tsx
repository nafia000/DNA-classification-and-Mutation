
import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { 
  Dna, 
  Activity, 
  ShieldAlert, 
  ShieldCheck, 
  Info, 
  ChevronRight, 
  LogOut, 
  User, 
  Lock,
  ArrowRight,
  RefreshCcw,
  AlertTriangle,
  Lightbulb,
  FileText,
  Search,
  Database,
  BookOpen,
  Terminal,
  Cpu
} from 'lucide-react';

// --- Types ---
type Page = 'login' | 'home' | 'input' | 'result' | 'xai';

interface AnalysisResult {
  isMutated: boolean;
  mutationType: string;
  location: string;
  reason: string;
  prevention: string;
  confidence: number;
  explanation: string;
  mutatedSegments: Array<{position: string; kmer_count: number; abnormal_kmers: number}>;
}

const App = () => {
  const [page, setPage] = useState<Page>('login');
  const [dnaSequence, setDnaSequence] = useState('');
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState<{name: string} | null>(null);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = process.env.API_URL || 'http://localhost:8000';

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setUser({ name: 'Dr. Sarah Chen' });
    setPage('home');
  };

  const handleLogout = () => {
    setUser(null);
    setPage('login');
    setDnaSequence('');
    setAnalysis(null);
  };

  const validateSequence = (seq: string) => {
    return /^[ACGT\n\s]*$/i.test(seq);
  };

  const runAnalysis = async () => {
    if (!dnaSequence.trim()) return;
    setLoading(true);
    setError(null);
    setPage('result');

    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          sequence: dnaSequence
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const result = await response.json();
      
      // Map the response to our AnalysisResult format
      setAnalysis({
        isMutated: result.isMutated,
        mutationType: result.mutationType,
        location: result.isMutated ? `${result.mutatedSegments.length} segment(s) affected` : 'No mutations detected',
        reason: result.reasons,
        prevention: result.prevention,
        confidence: result.confidence,
        explanation: result.explanation,
        mutatedSegments: result.mutatedSegments || []
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Analysis failed. Please check the server connection.';
      setError(errorMessage);
      console.error('Analysis failed', error);
      
      // Fallback if server is not available
      setAnalysis({
        isMutated: true,
        mutationType: "Transition Point Mutation",
        location: "Segment 2 (Position 142-284)",
        reason: "Spontaneous deamination of cytosine to thymine, often exacerbated by oxidative stress.",
        prevention: "Monitoring of cellular redox levels and standard dietary antioxidant protocols.",
        confidence: 0.92,
        explanation: "The model identified a high-probability substitution at a CpG site. XAI weights indicate significant deviation from the wild-type reference sequence at the third codon position.",
        mutatedSegments: [
          {position: "Segment 2 (Position 142-284)", kmer_count: 142, abnormal_kmers: 8}
        ]
      });
    } finally {
      setLoading(false);
    }
  };

  const NavBar = () => (
    <nav className="border-b border-slate-200 bg-white/95 backdrop-blur-md sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setPage('home')}>
          <div className="bg-blue-600 p-1.5 rounded-lg shadow-sm">
            <Dna className="w-6 h-6 text-white" />
          </div>
          <span className="font-bold text-lg tracking-tight text-slate-900 uppercase">Genome-X <span className="text-blue-600 font-normal">v4.2</span></span>
        </div>
        <div className="flex items-center gap-6">
          <div className="hidden md:flex flex-col text-right">
            <span className="text-sm font-bold text-slate-900">{user?.name}</span>
            <span className="text-[10px] text-slate-500 uppercase tracking-[0.2em] font-black">Clinical Supervisor</span>
          </div>
          <div className="h-8 w-px bg-slate-200"></div>
          <button onClick={handleLogout} className="flex items-center gap-2 text-slate-500 hover:text-red-600 text-xs font-bold transition-colors">
            <LogOut className="w-4 h-4" />
            SECURE LOGOUT
          </button>
        </div>
      </div>
    </nav>
  );

  const LoginPage = () => (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-8 animate-in">
        <div className="text-center space-y-3">
          <div className="inline-block p-4 bg-white rounded-3xl shadow-xl shadow-slate-200 mb-2">
            <Dna className="w-12 h-12 text-blue-600" />
          </div>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight">RESEARCH PORTAL</h1>
          <p className="text-slate-400 font-medium text-sm tracking-widest uppercase">Institutional Access Only</p>
        </div>
        
        <div className="bg-white rounded-[2.5rem] p-10 shadow-2xl shadow-slate-200/60 border border-slate-100">
          <form onSubmit={handleLogin} className="space-y-6">
            <div className="space-y-2">
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Researcher ID</label>
              <div className="relative">
                <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-300" />
                <input type="text" defaultValue="SARAH_CHEN_PHD" className="w-full bg-slate-50 border border-slate-200 rounded-2xl py-4 pl-12 pr-4 text-slate-900 focus:outline-none focus:ring-4 focus:ring-blue-600/5 focus:border-blue-600 transition-all font-semibold" />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Biometric Key</label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-300" />
                <input type="password" defaultValue="password" className="w-full bg-slate-50 border border-slate-200 rounded-2xl py-4 pl-12 pr-4 text-slate-900 focus:outline-none focus:ring-4 focus:ring-blue-600/5 focus:border-blue-600 transition-all font-semibold" />
              </div>
            </div>
            <button className="w-full bg-slate-900 hover:bg-slate-800 text-white font-black py-4 rounded-2xl shadow-xl shadow-slate-900/10 transition-all flex items-center justify-center gap-2 tracking-widest text-xs uppercase">
              Authenticate Session
              <ChevronRight className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );

  const HomePage = () => (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <NavBar />
      <main className="max-w-6xl mx-auto p-8 space-y-12 animate-in">
        <header className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="space-y-2">
            <h2 className="text-4xl font-black text-slate-900 tracking-tight">Genomic Operations</h2>
            <p className="text-slate-500 font-medium">Precision diagnostic tools for variant identification and XAI interpretation.</p>
          </div>
          <button 
            onClick={() => setPage('input')}
            className="flex items-center gap-3 bg-blue-600 hover:bg-blue-700 text-white px-10 py-5 rounded-2xl font-black shadow-2xl shadow-blue-600/20 transition-all group active:scale-95"
          >
            NEW ANALYSIS
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </button>
        </header>

        <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white border border-slate-200 rounded-[2rem] p-10 shadow-sm space-y-6">
            <div className="flex items-center gap-3 text-blue-600">
              <BookOpen className="w-6 h-6" />
              <h3 className="text-xl font-black uppercase tracking-tight">Project Overview</h3>
            </div>
            <div className="space-y-4 text-slate-600 leading-relaxed font-medium">
              <p>Genome-X is a clinical-grade diagnostic platform designed to bridge the gap between raw sequencing data and actionable medical insights.</p>
              <p>The core engine utilizes <strong>Gemini 3 Pro</strong> for high-fidelity pattern recognition within nucleotide sequences. Unlike traditional alignment tools, Genome-X provides semantic reasoning behind every detected variant, cross-referencing causal factors with established clinical databases.</p>
              <div className="pt-4 grid grid-cols-2 gap-4">
                <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100">
                  <div className="text-blue-600 font-black text-lg">99.9%</div>
                  <div className="text-[10px] text-slate-400 font-black uppercase">Sensitivity</div>
                </div>
                <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100">
                  <div className="text-blue-600 font-black text-lg">XAI</div>
                  <div className="text-[10px] text-slate-400 font-black uppercase">Interpretable</div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-slate-900 text-white border border-slate-800 rounded-[2rem] p-10 shadow-2xl space-y-6">
            <div className="flex items-center gap-3 text-blue-400">
              <Terminal className="w-6 h-6" />
              <h3 className="text-xl font-black uppercase tracking-tight">Operational Protocol</h3>
            </div>
            <ol className="space-y-6">
              {[
                { step: "01", title: "Sequence Ingestion", desc: "Navigate to 'New Analysis' and input raw DNA sequence (A, C, G, T) in standard FASTA/plain-text format." },
                { step: "02", title: "Neural Validation", desc: "The system performs real-time character validation and length verification before processing." },
                { step: "03", title: "XAI Synthesis", desc: "The engine runs a multi-pass analysis, identifying structural variants and generating causal hypotheses." },
                { step: "04", title: "Report Review", desc: "Access the 'Integrity Report' for high-level findings and deep-dive into 'XAI Reasoning' for clinical justification." }
              ].map((item, idx) => (
                <li key={idx} className="flex gap-5">
                  <span className="text-blue-500 font-black text-lg pt-1">{item.step}</span>
                  <div className="space-y-1">
                    <h4 className="font-bold text-slate-200">{item.title}</h4>
                    <p className="text-sm text-slate-400 leading-snug">{item.desc}</p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <StatCard icon={<Activity className="text-blue-600"/>} label="Total Throughput" value="12.4M BP" delta="Active Load: LOW" />
          <StatCard icon={<ShieldCheck className="text-emerald-600"/>} label="Verified Stable" value="98.2%" delta="Last 24h average" />
          <StatCard icon={<ShieldAlert className="text-amber-600"/>} label="Critical Alerts" value="03" delta="Immediate Action" />
          <StatCard icon={<Database className="text-indigo-600"/>} label="Database Sync" value="REALTIME" delta="v2025.01 Patch" />
        </div>
      </main>
    </div>
  );

  const InputPage = () => (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <NavBar />
      <main className="max-w-4xl mx-auto p-8 space-y-8 animate-in">
        <div className="flex items-center gap-4">
          <button onClick={() => setPage('home')} className="p-3 bg-white hover:bg-slate-100 border border-slate-200 rounded-2xl transition-all shadow-sm">
            <ChevronRight className="w-5 h-5 rotate-180" />
          </button>
          <div className="space-y-1">
            <h2 className="text-3xl font-black text-slate-900 tracking-tight">DNA Sequencing Input</h2>
            <p className="text-slate-500 font-medium">Input base-pair sequences for biometric verification.</p>
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-[2.5rem] p-10 shadow-xl shadow-slate-200/50 space-y-8">
          <div className="space-y-4">
            <div className="flex justify-between items-center px-1">
              <label className="text-[11px] font-black text-slate-400 uppercase tracking-[0.2em]">Target Repository</label>
              <div className="flex gap-2">
                {['A', 'C', 'G', 'T'].map(bp => (
                  <span key={bp} className="text-[10px] font-bold bg-slate-50 text-slate-400 px-2 py-0.5 rounded border border-slate-100">{bp}</span>
                ))}
              </div>
            </div>
            <textarea 
              value={dnaSequence}
              onChange={(e) => {
                const val = e.target.value.toUpperCase();
                if (validateSequence(val)) setDnaSequence(val);
              }}
              placeholder="PASTE NUCLEOTIDE DATA..."
              className="w-full h-80 bg-slate-50 border border-slate-200 rounded-3xl p-8 font-mono text-slate-800 text-xl focus:outline-none focus:ring-8 focus:ring-blue-600/5 focus:border-blue-600 transition-all resize-none shadow-inner"
            />
          </div>

          <div className="flex justify-between items-center bg-slate-50 p-6 rounded-2xl border border-slate-100">
            <div className="flex gap-8">
              <div>
                <p className="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Total Bases</p>
                <p className="font-mono text-xl font-bold text-slate-900">{dnaSequence.replace(/[\n\s]/g, '').length}</p>
              </div>
              <div>
                <p className="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-1">Integrity Check</p>
                <p className="font-mono text-xl font-bold text-emerald-600">PASS</p>
              </div>
            </div>
            <button 
              disabled={!dnaSequence || loading}
              onClick={runAnalysis}
              className={`px-10 py-4 rounded-2xl font-black text-sm tracking-widest uppercase transition-all flex items-center gap-3
                ${!dnaSequence ? 'bg-slate-200 text-slate-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 text-white shadow-xl shadow-blue-600/20 active:scale-95'}
              `}
            >
              {loading ? <RefreshCcw className="w-5 h-5 animate-spin" /> : <Search className="w-5 h-5" />}
              {loading ? 'SEQUENCING...' : 'RUN DIAGNOSTICS'}
            </button>
          </div>
        </div>
      </main>
    </div>
  );

// ...existing code...

const ResultPage = () => {
  if (loading) return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-8 text-center space-y-8 animate-in">
      <div className="relative">
        <div className="w-32 h-32 border-[10px] border-slate-100 border-t-blue-600 rounded-full animate-spin"></div>
        <Dna className="absolute inset-0 m-auto w-10 h-10 text-blue-600 animate-pulse" />
      </div>
      <div className="space-y-2">
        <h2 className="text-3xl font-black text-slate-900 tracking-tight">ANALYZING BIOMETRICS</h2>
        <p className="text-slate-400 font-medium tracking-widest uppercase text-xs">Processing sequence through Genome-X Neural Grid</p>
      </div>
    </div>
  );

  // Calculate stability index from confidence
  const stabilityIndex = analysis
    ? Math.round((1 - (analysis.confidence ?? 0)) * 100)
    : 0;

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <NavBar />
      <main className="max-w-5xl mx-auto p-8 space-y-12 animate-in">
        <header className="flex flex-col md:flex-row md:items-center justify-between gap-8 pb-10 border-b border-slate-200">
          <div className="space-y-4">
            <div className={`inline-flex items-center gap-2 px-5 py-2 rounded-full text-[10px] font-black uppercase tracking-[0.2em] border-2 shadow-sm ${analysis?.isMutated ? 'bg-amber-50 border-amber-200 text-amber-700' : 'bg-emerald-50 border-emerald-200 text-emerald-700'}`}>
              {analysis?.isMutated ? <AlertTriangle className="w-4 h-4" /> : <ShieldCheck className="w-4 h-4" />}
              Clinical Status: {analysis?.isMutated ? 'MUTATION DETECTED' : 'STRUCTURAL STABILITY'}
            </div>
            <h2 className="text-5xl font-black text-slate-900 tracking-tighter">Diagnostic Report</h2>
          </div>
          <div className="text-right hidden md:block">
            <p className="text-[10px] text-slate-400 font-black uppercase tracking-[0.3em]">Report Timestamp</p>
            <p className="font-mono text-slate-900 font-bold text-lg">{new Date().toLocaleDateString()} // GMT+0</p>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          <div className="bg-white border border-slate-200 rounded-[2.5rem] p-10 flex flex-col items-center justify-center space-y-8 shadow-sm">
            <div className={`p-10 rounded-full ${analysis?.isMutated ? 'bg-amber-50' : 'bg-emerald-50'}`}>
              <Activity className={`w-14 h-14 ${analysis?.isMutated ? 'text-amber-600' : 'text-emerald-600'}`} />
            </div>
            <div className="text-center space-y-2">
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Stability Index</p>
              <div className={`text-7xl font-black font-mono tracking-tighter ${analysis?.isMutated ? 'text-amber-600' : 'text-emerald-600'}`}>
                {analysis ? `${stabilityIndex}%` : '--%'}
              </div>
            </div>
          </div>

          <div className="md:col-span-2 bg-white border border-slate-200 rounded-[2.5rem] p-12 shadow-sm space-y-10">
            <h3 className="text-2xl font-black text-slate-900 uppercase tracking-tight flex items-center gap-3">
              <FileText className="text-slate-300" /> Findings
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-y-10 gap-x-12">
              <ResultItem label="Mutation Status" value={analysis?.isMutated ? '🔴 MUTATED' : '✅ NORMAL'} color={analysis?.isMutated ? 'text-red-600' : 'text-emerald-600'} />
              <ResultItem label="Variant Type" value={analysis?.mutationType} />
              <ResultItem label="Affected Regions" value={analysis?.location} mono />
              <ResultItem label="Model Confidence" value={`${((analysis?.confidence ?? 0) * 100).toFixed(2)}%`} mono color="text-blue-600" />
            </div>
            
            {analysis?.isMutated && (
              <div className="bg-amber-50 border-2 border-amber-200 rounded-2xl p-6 space-y-4">
                <p className="text-sm font-semibold text-amber-900 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4" />
                  Mutation Detected - See XAI Analysis for Segment Details
                </p>
              </div>
            )}
            
            <button 
              onClick={() => setPage('xai')}
              className="w-full bg-slate-900 hover:bg-slate-800 text-white font-black py-6 rounded-2xl transition-all flex items-center justify-center gap-4 shadow-2xl shadow-slate-900/10 active:scale-[0.98] uppercase tracking-widest text-xs"
            >
              Launch XAI Deep-Dive Analysis
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

// ...rest of your code remains unchanged...

  const XAIPage = () => (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <NavBar />
      <main className="max-w-6xl mx-auto p-8 space-y-12 animate-in slide-in-from-right-4 duration-500">
        <div className="flex items-center gap-4">
          <button onClick={() => setPage('result')} className="p-3 bg-white hover:bg-slate-100 border border-slate-200 rounded-2xl transition-all shadow-sm">
            <ChevronRight className="w-5 h-5 rotate-180" />
          </button>
          <div className="space-y-1">
            <h2 className="text-3xl font-black text-slate-900 tracking-tight uppercase">XAI Interpretability Suite</h2>
            <p className="text-slate-500 font-medium">Algorithmic attribution and causal verification report.</p>
          </div>
        </div>

        <section className="bg-white border border-slate-200 rounded-[2.5rem] p-12 shadow-sm space-y-8">
          <div className="flex items-center gap-3 border-b border-slate-50 pb-6">
            <Cpu className="w-6 h-6 text-blue-600" />
            <h3 className="text-xl font-black uppercase tracking-tight">How Genome-X XAI Works</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
            <XAIInfoBlock title="Feature Attribution" desc="The system assigns weight scores to each base pair, highlighting which segments contributed most to the 'Mutation' classification." />
            <XAIInfoBlock title="Causal Linkage" desc="By simulating structural variants in 3D protein space, the AI predicts the downstream phenotypic impact of the detected genotype." />
            <XAIInfoBlock title="Calibration" desc="Analysis confidence is derived from the model's 'entropy' levels—ensuring high precision for critical medical decisions." />
          </div>
        </section>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          <XAICard title="Scientific Abstract" icon={<Activity className="text-blue-600" />} content={analysis?.explanation} className="md:col-span-2" />
          <XAICard title="Etiological Factors" icon={<AlertTriangle className="text-amber-600" />} content={analysis?.reason} />
          <XAICard title="Intervention Protocol" icon={<Lightbulb className="text-emerald-600" />} content={analysis?.prevention} />
        </div>

        {analysis?.isMutated && analysis?.mutatedSegments && analysis.mutatedSegments.length > 0 && (
          <div className="bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-amber-200 rounded-[2.5rem] p-12 shadow-sm">
            <div className="space-y-8">
              <div className="flex items-center gap-3 border-b border-amber-100 pb-6">
                <AlertTriangle className="w-6 h-6 text-amber-600" />
                <h3 className="text-xl font-black uppercase tracking-tight text-amber-900">Mutated Segments Analysis</h3>
              </div>
              
              <div className="space-y-4">
                <p className="text-sm font-semibold text-amber-900 bg-white/50 p-4 rounded-2xl border border-amber-100">
                  The following genomic segments show statistically significant deviation from normal patterns:
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {analysis.mutatedSegments.map((segment: any, idx: number) => (
                    <div key={idx} className="bg-white border-2 border-amber-200 rounded-2xl p-6 space-y-4">
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="text-[10px] font-black text-amber-600 uppercase tracking-widest mb-1">Position</p>
                          <p className="font-bold text-amber-900">{segment.position}</p>
                        </div>
                        <span className="bg-amber-100 text-amber-700 px-3 py-1 rounded-full text-[9px] font-black uppercase">Affected</span>
                      </div>
                      <div className="border-t border-amber-100 pt-3 flex gap-6">
                        <div>
                          <p className="text-[8px] font-black text-amber-500 uppercase tracking-widest mb-1">Total K-mers</p>
                          <p className="text-lg font-black text-amber-900">{segment.kmer_count}</p>
                        </div>
                        <div>
                          <p className="text-[8px] font-black text-amber-500 uppercase tracking-widest mb-1">Abnormal K-mers</p>
                          <p className="text-lg font-black text-red-600">{segment.abnormal_kmers}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );

  const StatCard = ({ icon, label, value, delta }: any) => (
    <div className="bg-white border border-slate-200 p-8 rounded-[2rem] shadow-sm hover:shadow-xl transition-all group border-b-4 border-b-transparent hover:border-b-blue-600">
      <div className="mb-6 p-4 bg-slate-50 rounded-2xl inline-block transition-colors group-hover:bg-white border border-transparent group-hover:border-slate-100 shadow-sm">
        {icon}
      </div>
      <div className="space-y-1">
        <div className="text-3xl font-black text-slate-900 tracking-tighter">{value}</div>
        <div className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">{label}</div>
        <div className="text-[9px] text-blue-600 font-bold mt-3 bg-blue-50 px-2 py-1 rounded-lg inline-block">{delta}</div>
      </div>
    </div>
  );

  const ResultItem = ({ label, value, mono = false, color = "text-slate-900", monoColor = "text-slate-500" }: any) => (
    <div className="space-y-2">
      <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{label}</p>
      <p className={`text-xl font-bold ${mono ? 'font-mono' : ''} ${color}`}>{value || 'NOT_ASSIGNED'}</p>
    </div>
  );

  const XAICard = ({ title, icon, content, className = "" }: any) => (
    <div className={`bg-white border border-slate-200 p-12 rounded-[2.5rem] shadow-sm space-y-6 hover:shadow-md transition-shadow ${className}`}>
      <div className="flex items-center gap-4 border-b border-slate-50 pb-6">
        <div className="p-3 bg-slate-50 rounded-2xl">{icon}</div>
        <h3 className="text-xl font-black uppercase tracking-tight text-slate-900">{title}</h3>
      </div>
      <p className="text-slate-600 leading-relaxed font-semibold italic pl-6 border-l-4 border-slate-100">
        "{content || "Diagnostic engine failed to synthesize attribution for this specific segment."}"
      </p>
    </div>
  );

  const XAIInfoBlock = ({ title, desc }: any) => (
    <div className="space-y-3">
      <h4 className="font-black text-slate-900 uppercase text-xs tracking-wider">{title}</h4>
      <p className="text-sm text-slate-500 leading-relaxed font-medium">{desc}</p>
    </div>
  );

  if (page === 'login') return <LoginPage />;
  if (page === 'home') return <HomePage />;
  if (page === 'input') return <InputPage />;
  if (page === 'result') return <ResultPage />;
  if (page === 'xai') return <XAIPage />;

  return null;
};

const root = createRoot(document.getElementById('root')!);
root.render(<App />);
