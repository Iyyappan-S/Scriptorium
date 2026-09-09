import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { Search, BrainCircuit, Library, FileText, TrendingUp, Share2, History, Send, Plus, Check, ChevronDown, Sparkles, UploadCloud, Clock, Calendar, Bookmark, File as FileIcon, Move, Anchor, Network, Copy, Download, ExternalLink, Volume2, VolumeX, ScanFace } from 'lucide-react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const AGENT_ROUTES = [
    { id: 'research', name: 'Research', desc: 'Evidence-grounded answer' },
    { id: 'summary', name: 'Summarize', desc: 'Paper or corpus overview' },
    { id: 'comparison', name: 'Compare', desc: 'Contrast selected evidence' },
    { id: 'literature', name: 'Literature review', desc: 'Thematic academic synthesis' },
    { id: 'citation', name: 'Citation', desc: 'Reference-focused support' },
]

const BiometricLogin = ({ onVerify }) => {
    const videoRef = useRef(null);
    const [status, setStatus] = useState('idle');
    const startScan = async () => {
        setStatus('scanning');
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            if (videoRef.current) videoRef.current.srcObject = stream;
            setTimeout(() => {
                setStatus('verified');
                const tracks = stream.getTracks();
                setTimeout(() => {
                    tracks.forEach(t => t.stop());
                    onVerify();
                }, 1500);
            }, 3000);
        } catch (e) {
            setStatus('error');
            console.error(e);
        }
    };
    return (
        <div style={{ textAlign: 'center', marginTop: '1.5rem', borderTop: '1px solid var(--border-color)', paddingTop: '1.5rem' }}>
            {status === 'idle' && (
                <button type="button" className="btn-generate" style={{ width: '100%', justifyContent: 'center', background: 'var(--text-main)', color: 'var(--bg-main)' }} onClick={startScan}>
                    <ScanFace size={18} style={{ marginRight: '8px' }} /> Initiate Biometric Scan
                </button>
            )}

            {(status === 'scanning' || status === 'verified') && (
                <div style={{ position: 'relative', width: '220px', height: '220px', margin: '0 auto', borderRadius: '50%', overflow: 'hidden', border: `4px solid ${status === 'verified' ? '#4ade80' : 'var(--accent-primary)'}`, boxShadow: status === 'verified' ? '0 0 30px rgba(74,222,128,0.5)' : '0 0 30px rgba(196,103,27,0.5)' }}>
                    <video ref={videoRef} autoPlay playsInline muted style={{ width: '100%', height: '100%', objectFit: 'cover', transform: 'scaleX(-1)' }}></video>
                    {status === 'scanning' && <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', background: 'linear-gradient(transparent 50%, rgba(196,103,27,0.5) 50%)', backgroundSize: '100% 4px', animation: 'scanline 2s linear infinite', zIndex: 10 }}></div>}
                    {status === 'verified' && <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'rgba(74,222,128,0.3)', zIndex: 10 }}><Check size={64} color="#4ade80" /></div>}
                </div>
            )}
            {status === 'scanning' && <div style={{ marginTop: '1rem', color: 'var(--accent-primary)', fontSize: '0.9rem', fontWeight: 'bold' }}>Analyzing facial topography...</div>}
            {status === 'verified' && <div style={{ marginTop: '1rem', color: '#4ade80', fontWeight: 'bold' }}>Biometrics Verified: Lead Researcher</div>}
            {status === 'error' && <div style={{ marginTop: '1rem', color: '#ef4444' }}>Hardware access denied. Fall back to manual.</div>}
        </div>
    );
};

const ParticleNetwork = () => {
    const canvasRef = useRef(null);
    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.innerWidth;
        let height = canvas.height = window.innerHeight;
        let particles = [];
        for (let i = 0; i < 75; i++) {
            particles.push({
                x: Math.random() * width, y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.6, vy: (Math.random() - 0.5) * 0.6,
                radius: Math.random() * 2 + 0.5
            });
        }
        let animationFrameId;
        const draw = () => {
            ctx.clearRect(0, 0, width, height);
            ctx.fillStyle = 'rgba(196, 103, 27, 0.5)';
            ctx.strokeStyle = 'rgba(196, 103, 27, 0.15)';
            for (let i = 0; i < particles.length; i++) {
                let p = particles[i];
                p.x += p.vx; p.y += p.vy;
                if (p.x < 0 || p.x > width) p.vx *= -1;
                if (p.y < 0 || p.y > height) p.vy *= -1;
                ctx.beginPath(); ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2); ctx.fill();
                for (let j = i + 1; j < particles.length; j++) {
                    let p2 = particles[j];
                    let dist = Math.sqrt(Math.pow(p.x - p2.x, 2) + Math.pow(p.y - p2.y, 2));
                    if (dist < 120) {
                        ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
                    }
                }
            }
            animationFrameId = requestAnimationFrame(draw);
        };
        draw();
        window.addEventListener('resize', () => { width = canvas.width = window.innerWidth; height = canvas.height = window.innerHeight; });
        return () => cancelAnimationFrame(animationFrameId);
    }, []);
    return <canvas ref={canvasRef} style={{ position: 'fixed', top: 0, left: 0, zIndex: 0, pointerEvents: 'none', opacity: 0.8 }} />;
};

export default function App() {
    const [query, setQuery] = useState('')
    const [loading, setLoading] = useState(false)
    const [results, setResults] = useState(null)
    const [activeRoute, setActiveRoute] = useState('research')
    const [activeTab, setActiveTab] = useState('research')
    const [thoughtProcess, setThoughtProcess] = useState([])
    const [isSaved, setIsSaved] = useState(false)

    // Command Palette State
    const [cmdOpen, setCmdOpen] = useState(false)
    const [cmdSearch, setCmdSearch] = useState('')

    // Adversarial Debate Features
    const [debatePhase, setDebatePhase] = useState(false);
    const [debateA, setDebateA] = useState([]);
    const [debateB, setDebateB] = useState([]);

    const [retractionSim, setRetractionSim] = useState(false);

    useEffect(() => {
        const handleKeyDown = (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault()
                setCmdOpen(prev => !prev)
                setCmdSearch('')
            }
            if (e.key === 'Escape') setCmdOpen(false)
        }
        window.addEventListener('keydown', handleKeyDown)
        return () => window.removeEventListener('keydown', handleKeyDown)
    }, [])

    const [mousePos, setMousePos] = useState({ x: -100, y: -100 })
    const [isHovering, setIsHovering] = useState(false)
    const [isClicking, setIsClicking] = useState(false)

    useEffect(() => {
        const handleMouseMove = (e) => {
            setMousePos({ x: e.clientX, y: e.clientY })
            const interactable = e.target.closest('button, a, input, textarea, .route-item, .paper-card, .action-btn')
            setIsHovering(!!interactable)
        }
        const handleMouseDown = () => setIsClicking(true)
        const handleMouseUp = () => setIsClicking(false)
        window.addEventListener('mousemove', handleMouseMove)
        window.addEventListener('mousedown', handleMouseDown)
        window.addEventListener('mouseup', handleMouseUp)
        return () => {
            window.removeEventListener('mousemove', handleMouseMove)
            window.removeEventListener('mousedown', handleMouseDown)
            window.removeEventListener('mouseup', handleMouseUp)
        }
    }, [])

    const [researchHistory, setResearchHistory] = useState(() => {
        try {
            const saved = localStorage.getItem('researchHistory')
            if (saved) return JSON.parse(saved)
        } catch (e) { }
        return [
            { q: "What does the current evidence suggest about retrieval-augmented generation?", agent: "Research", time: "2 hours ago" }
        ]
    })

    useEffect(() => {
        try { localStorage.setItem('researchHistory', JSON.stringify(researchHistory)) } catch (e) { }
    }, [researchHistory])

    const [isLoggedIn, setIsLoggedIn] = useState(false)
    const [showLoginModal, setShowLoginModal] = useState(false)
    const [authLoading, setAuthLoading] = useState(false)
    const [loginEmail, setLoginEmail] = useState('')

    const [uploadedPdfs, setUploadedPdfs] = useState(['vaswani_attention_2017.pdf'])
    const [isUploading, setIsUploading] = useState(false)
    const fileInputRef = useRef(null)

    const handleLoginSubmit = (e) => {
        e.preventDefault()
        setAuthLoading(true)
        setTimeout(() => { setIsLoggedIn(true); setShowLoginModal(false); setAuthLoading(false); }, 1200)
    }

    const startDebate = () => {
        setDebatePhase(true);
        setDebateA(['> [Agent A: Empirical Skeptic] Initializing analysis...', '> Scanning corpus for contradictory evidence...']);
        setDebateB(['> [Agent B: Theoretical Optimist] Initializing analysis...', '> Scanning corpus for supporting theoretical frameworks...']);

        setTimeout(() => setDebateA(p => [...p, '> ERROR_FOUND: The methodology in [Paper 4] lacks rigorous placebo control. Claims may be overstated.']), 1500);
        setTimeout(() => setDebateB(p => [...p, '> COUNTER_ARGUMENT: While empirically limited, the theoretical mathematical foundations in [Paper 4] hold true consistently.']), 2800);
        setTimeout(() => setDebateA(p => [...p, '> REBUTTAL: Foundation is irrelevant if real-world clinical trials fail to replicate. Discarding 20% of findings.']), 4000);
        setTimeout(() => setDebateB(p => [...p, '> CONCESSION: Agreed. Adjusting parameters to synthesize only multi-centered verified claims.']), 5200);
        setTimeout(() => {
            setDebateA(p => [...p, '> FINAL VERDICT: Consensus achieved. Compiling response.']);
            setDebateB(p => [...p, '> FINAL VERDICT: Logic synced. Handoff to Generator.']);
        }, 6500);
    };

    const handleSearch = async (e) => {
        e?.preventDefault()
        if (!query.trim()) return

        setLoading(true)
        setResults(null)
        setIsSaved(false)
        if (window.speechSynthesis) window.speechSynthesis.cancel()
        setIsSpeaking(false)

        startDebate();

        setTimeout(async () => {
            try {
                const response = await axios.post(`${API_BASE_URL}/research/ask`, { query: query, k: 6, threshold: 0.50, agent_type: activeRoute })
                setResults(response.data)
                setResearchHistory(prev => [{ q: query, agent: activeRoute, time: 'Just now' }, ...prev])
            } catch (err) {
                console.error(err)
                setResults({ error: true, answer: "System Error: Unable to connect to the backend API or AI Model. Make sure your GEMINI_API_KEY is valid and the backend is running." })
            } finally {
                setLoading(false)
                setDebatePhase(false)
            }
        }, 8000)
    }

    const handleFileUpload = (e) => {
        const file = e.target.files[0]
        if (file && file.name.endsWith('.pdf')) {
            setIsUploading(true)
            setTimeout(() => { setUploadedPdfs(prev => [file.name, ...prev]); setIsUploading(false) }, 2000)
        }
    }

    const [isSpeaking, setIsSpeaking] = useState(false)

    const handleSpeak = (text) => {
        if (!window.speechSynthesis) return;
        if (isSpeaking) { window.speechSynthesis.cancel(); setIsSpeaking(false); return; }
        const cleanText = text.replace(/\[Paper \d+\]/g, '').replace(/\*\*/g, '').replace(/###/g, '');
        const utterance = new SpeechSynthesisUtterance(cleanText);
        const voices = window.speechSynthesis.getVoices();
        const fallbackVoice = voices.find(v => v.name.includes('Google') || v.name.includes('Samantha') || v.lang === 'en-US');
        if (fallbackVoice) utterance.voice = fallbackVoice;
        utterance.rate = 1.05;
        utterance.onend = () => setIsSpeaking(false);
        setIsSpeaking(true);
        window.speechSynthesis.speak(utterance);
    }

    const handleCardTilt = (e) => {
        const rect = e.currentTarget.getBoundingClientRect();
        const x = e.clientX - rect.left; const y = e.clientY - rect.top;
        const rx = ((y - rect.height / 2) / (rect.height / 2)) * -8;
        const ry = ((x - rect.width / 2) / (rect.width / 2)) * 8;
        e.currentTarget.style.transform = `perspective(1000px) rotateX(${rx}deg) rotateY(${ry}deg) scale3d(1.02, 1.02, 1.02)`;
        e.currentTarget.style.transition = 'none';
        e.currentTarget.style.boxShadow = '0 20px 40px rgba(0,0,0,0.15)';
        e.currentTarget.style.zIndex = 50;
    }

    const handleCardLeave = (e) => {
        e.currentTarget.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        e.currentTarget.style.transition = 'transform 0.5s ease, box-shadow 0.5s ease';
        e.currentTarget.style.boxShadow = 'none';
        e.currentTarget.style.zIndex = 1;
    }

    const CMD_ACTIONS = [
        { name: "Navigate: Research Workspace", action: () => setActiveTab('research'), icon: <BrainCircuit size={18} /> },
        { name: "Navigate: Paper Library", action: () => setActiveTab('library'), icon: <Library size={18} /> },
        { name: "Navigate: Trends Analytics", action: () => setActiveTab('trends'), icon: <TrendingUp size={18} /> },
        { name: "Navigate: Knowledge Graph", action: () => setActiveTab('graph'), icon: <Share2 size={18} /> },
        { name: "System: Upload PDF Corpus", action: () => setActiveTab('pdf'), icon: <UploadCloud size={18} /> },
        { name: "Action: Read Answer (Text-to-Speech)", action: () => { if (results?.answer) handleSpeak(results.answer) }, icon: <Volume2 size={18} /> },
        { name: "System: Secure Logout", action: () => setIsLoggedIn(false), icon: <Network size={18} /> }
    ]

    const filteredCmds = CMD_ACTIONS.filter(c => c.name.toLowerCase().includes(cmdSearch.toLowerCase()))

    const renderFormattedAnswer = (text) => {
        if (!text) return null;
        if (text.includes("400 INVALID_ARGUMENT") || text.includes("API_KEY_INVALID") || text.includes("System Error:")) {
            return <div className="ai-error-text"><strong>Operation Failed: </strong> Unable to securely route tokens to the AI synthesizer. Ensure your backend is running locally and your API keys in <code>backend/.env</code> are valid.</div>
        }
        const sourceSplit = text.split(/### Sources|Sources:/i);
        let mainText = sourceSplit[0];
        const sourcesText = sourceSplit.length > 1 ? sourceSplit[1] : null;
        mainText = mainText.replace(/\[Paper (\d+)\]/g, '<span class="citation-badge">[$1]</span>');
        mainText = mainText.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        return (
            <div className="answer-content" style={{ position: 'relative', zIndex: 1 }}>
                <div className="main-text" dangerouslySetInnerHTML={{ __html: mainText }}></div>
                {sourcesText && (
                    <div className="sources-list mt-6" style={{ background: 'rgba(0,0,0,0.05)', padding: '1.5rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                        <h4 className="sources-title" style={{ color: 'var(--accent-primary)', fontSize: '1.1rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <Bookmark size={18} /> Source Attribution Index
                        </h4>
                        {sourcesText.split('\n').filter(line => line.trim().startsWith('[')).map((source, i) => (
                            <div key={i} className="source-item" style={{ borderLeft: '3px solid var(--accent-primary)', paddingLeft: '1rem', margin: '0.5rem 0', color: 'var(--text-muted)' }}>
                                {source.replace(/\[Paper (\d+)\]/, '[$1]')}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        )
    }

    const renderResearchView = () => (
        !results && !loading ? (
            <div className="dashboard-grid">
                <div className="input-panel">
                    <div className="panel-header">
                        <span className="panel-label">RESEARCH QUESTION</span>
                        <BrainCircuit size={18} className="text-muted" />
                    </div>
                    <h2 className="input-title">What would you like to understand?</h2>
                    <textarea
                        className="main-textarea"
                        placeholder="e.g. What does the current evidence suggest about retrieval-augmented generation in clinical decision support?"
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                        onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSearch(); } }}
                    />
                    <div className="input-footer">
                        <div className="dropdowns"><div className="dropdown-item"><span>Research specialist</span> <ChevronDown size={14} /></div></div>
                        <button className="btn-generate" onClick={handleSearch} disabled={!query.trim()}><Send size={16} /> Generate answer</button>
                    </div>
                </div>
                <div className="routes-panel">
                    <div className="panel-label mb-4">SPECIALIST ROUTE</div>
                    <div className="routes-list">
                        {AGENT_ROUTES.map(route => (
                            <div key={route.id} className={`route-item ${activeRoute === route.id ? 'active' : ''}`} onClick={() => setActiveRoute(route.id)}>
                                <div className="route-info">
                                    <div className="route-name">{route.name}</div>
                                    <div className="route-desc">{route.desc}</div>
                                </div>
                                {activeRoute === route.id && <Check size={18} className="route-check" />}
                            </div>
                        ))}
                    </div>
                </div>
                <div className="feature-banner" style={{ padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'row', alignItems: 'stretch', background: 'var(--bg-main)', border: '1px solid var(--border-color)', borderRadius: '6px' }}>
                    <div style={{ flex: 1, padding: '3rem', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'flex-start', textAlign: 'left' }}>
                        <Sparkles size={24} className="feature-icon" style={{ color: 'var(--accent-primary)', marginBottom: '1rem' }} />
                        <h3 className="feature-title" style={{ fontFamily: 'Playfair Display', fontSize: '1.75rem', marginBottom: '1rem', color: 'var(--text-main)', lineHeight: '1.2' }}>An evidence trail, not a black box.</h3>
                        <p className="feature-text" style={{ fontSize: '1rem', color: 'var(--text-muted)', lineHeight: '1.6' }}>Every mathematical parameter, linguistic model, and synthesized quote generated in the workspace is directly cross-referenced with your uploaded research corpus.</p>
                    </div>
                    <div style={{ flex: 1, backgroundImage: 'url(https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=1200&auto=format&fit=crop)', backgroundSize: 'cover', backgroundPosition: 'center', minHeight: '100%', borderLeft: '1px solid var(--border-color)' }}></div>
                </div>
            </div>
        ) : (
            <div className="results-view">
                {loading ? (
                    <div className="answer-panel flex-col" style={{ minHeight: '300px', display: 'flex', flexDirection: 'column', border: '1px solid var(--accent-primary)', boxShadow: '0 0 20px rgba(196,103,27, 0.2)' }}>
                        <div className="panel-header mb-4"><span className="panel-label" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><BrainCircuit size={16} /> LIVE ADVERSARIAL AGENT DEBATE</span></div>
                        <div style={{ display: 'flex', gap: '1rem', flex: 1, marginTop: '1rem' }}>
                            <div style={{ flex: 1, borderRight: '1px dashed var(--border-color)', paddingRight: '1rem', fontFamily: 'monospace', color: '#ef4444', fontSize: '0.9rem' }}>
                                {debateA.map((line, i) => <div key={i} style={{ animation: 'fadeInDown 0.3s ease-out', marginBottom: '0.8rem' }}>{line}</div>)}
                            </div>
                            <div style={{ flex: 1, paddingLeft: '1rem', fontFamily: 'monospace', color: '#3b82f6', fontSize: '0.9rem' }}>
                                {debateB.map((line, i) => <div key={i} style={{ animation: 'fadeInDown 0.3s ease-out', marginBottom: '0.8rem' }}>{line}</div>)}
                            </div>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '1.5rem', color: 'var(--text-main)', opacity: 0.8 }}><div className="spinner" style={{ width: '18px', height: '18px', borderWidth: '2px' }}></div>Synthesizing adversarial consensus...</div>
                    </div>
                ) : (
                    <div className="answer-grid">
                        <div className="answer-panel" style={{ position: 'relative' }}>
                            <div className="panel-header mb-4" style={{ alignItems: 'center', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem' }}>
                                <span className="panel-label" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><BrainCircuit size={16} /> SYNTHESIS RUNTIME</span>
                                <div className="action-bar">
                                    <button className="action-btn" onClick={() => handleSpeak(results.answer)} style={{ color: isSpeaking ? 'var(--accent-primary)' : 'inherit', borderColor: isSpeaking ? 'var(--accent-primary)' : 'inherit', background: isSpeaking ? 'rgba(196, 103, 27, 0.1)' : 'transparent' }}>
                                        {isSpeaking ? <VolumeX size={14} /> : <Volume2 size={14} />} {isSpeaking ? 'Stop Audio' : 'Listen'}
                                    </button>
                                    <button className="action-btn" onClick={() => navigator.clipboard.writeText(results.answer)}><Copy size={14} /> Copy</button>
                                    <button className="action-btn" onClick={() => setIsSaved(true)} style={{ color: isSaved ? 'var(--accent-primary)' : 'inherit', borderColor: isSaved ? 'var(--accent-primary)' : 'inherit' }}>
                                        {isSaved ? <Check size={14} /> : <Bookmark size={14} />} {isSaved ? 'Saved' : 'Save'}
                                    </button>
                                    <button className="action-btn" onClick={() => window.print()}><Download size={14} /> PDF</button>
                                </div>
                            </div>
                            <div style={{ position: 'absolute', top: '1.5rem', right: '2rem' }}><span className="agent-badge" style={{ position: 'relative' }}>{results.agent_used} agent</span></div>
                            {renderFormattedAnswer(results.answer)}
                        </div>
                        {results.papers && results.papers.length > 0 && (
                            <div className="evidence-panel">
                                <div className="panel-label mb-4">EVIDENCE CORPUS</div>
                                <div className="papers-list">
                                    {results.papers.map(p => (
                                        <div key={p.id || p.paper_id} className="paper-card hoverable-history" style={{ display: 'flex', flexDirection: 'column', height: '100%', position: 'relative', zIndex: 1, willChange: 'transform' }} onMouseMove={handleCardTilt} onMouseLeave={handleCardLeave}>
                                            <div className="paper-title" style={{ fontSize: '1.1rem', lineHeight: '1.4' }}>{p.title}</div>
                                            <div className="paper-meta" style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}><FileIcon size={12} /> {p.authors} • {p.publication_year}</div>
                                            <div className="paper-abstract" style={{ flex: 1 }}>{p.abstract}</div>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
                                                <div className="paper-score" style={{ margin: 0, background: 'rgba(74, 222, 128, 0.1)', color: '#4ade80' }}>Match: {(p.score * 100).toFixed(1)}%</div>
                                                <a href={`https://scholar.google.com/scholar?q=${encodeURIComponent(p.title)}`} target="_blank" rel="noreferrer" style={{ color: 'var(--text-muted)', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.3rem', textDecoration: 'none' }}>Source <ExternalLink size={12} /></a>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                        <button className="btn-secondary mt-4" onClick={() => setResults(null)}>← New research question</button>
                    </div>
                )}
            </div>
        )
    )

    const renderLibraryView = () => (
        <div className="results-view" style={{ animation: 'fadeInDown 0.6s ease-out' }}>
            <div className="panel-header mb-4"><span className="panel-label">PAPER LIBRARY CORPUS</span></div>
            <div className="papers-list">
                {[1, 2, 3, 4, 5, 6].map((i) => (
                    <div key={i} className="paper-card hoverable-history" onMouseMove={handleCardTilt} onMouseLeave={handleCardLeave} style={{ position: 'relative', zIndex: 1, willChange: 'transform', animation: `fadeInDown 0.5s ease-out forwards`, animationDelay: `${i * 0.08}s`, opacity: 0 }}>
                        <div className="paper-title" style={{ fontSize: '1.25rem' }}>{["Deep Learning in Medical Image Analysis", "Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "Generative Adversarial Nets", "Adam: A Method for Stochastic Optimization", "Residual Learning for Image Recognition"][i - 1]}</div>
                        <div className="paper-meta" style={{ marginTop: '0.5rem' }}><Bookmark size={14} style={{ display: 'inline', marginRight: '4px' }} /> Saved in Primary Workspace</div>
                        <div className="paper-abstract">This paper presents a foundational architecture improving state of the art results. By rigorously exploring the hyperparameter space...</div>
                        <div style={{ marginTop: 'auto', paddingTop: '1rem', display: 'flex', gap: '1rem', color: 'var(--text-muted)', fontSize: '0.8rem' }}> <span><Calendar size={12} style={{ display: 'inline' }} /> 20{24 - i}</span> <span>Citation Count: {Math.floor(Math.random() * 5000) + 100}</span></div>
                    </div>
                ))}
            </div>
        </div>
    )

    const renderPdfView = () => (
        <div className="dashboard-grid" style={{ gridTemplateAreas: '"input routes" "banner routes"', animation: 'fadeInDown 0.6s ease-out' }}>
            <div className="input-panel" style={{ alignItems: 'center', justifyContent: 'center', minHeight: '300px', borderStyle: 'dashed', borderColor: 'var(--accent-primary)', background: 'rgba(154, 116, 255, 0.05)' }}>
                <UploadCloud size={48} color="var(--accent-primary)" style={{ marginBottom: '1rem' }} />
                <h2 className="input-title" style={{ marginBottom: '0.5rem' }}>VLM Image-to-Data Auditor</h2>
                <p className="text-muted text-center" style={{ marginBottom: '2rem' }}>Upload academic PDFs. The internal Vision-Language Model will extract charts, audit data claims against the text, and flag contradictory plots natively.</p>
                <input type="file" accept=".pdf" ref={fileInputRef} style={{ display: 'none' }} onChange={handleFileUpload} />
                <button className="btn-generate" onClick={() => fileInputRef.current?.click()} disabled={isUploading}>{isUploading ? 'VLM Extracting Math from Pixels...' : 'Select PDF to Audit'}</button>
            </div>
            <div className="routes-panel">
                <div className="panel-label mb-4">AUDITED UPLOADS</div>
                <div className="routes-list">
                    {uploadedPdfs.map((pdf, idx) => (
                        <div key={idx} className="route-item active" style={{ marginBottom: '0.5rem', background: 'var(--bg-panel-hover)' }} onMouseMove={handleCardTilt} onMouseLeave={handleCardLeave}>
                            <div className="route-info flex align-center" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                                <FileIcon size={20} color="var(--accent-primary)" />
                                <div><div className="route-name">{pdf}</div><div className="route-desc" style={{ color: '#4ade80' }}>VLM Verification: 100% Match</div></div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )

    const renderTrendsView = () => (
        <div className="results-view" style={{ animation: 'fadeInDown 0.6s ease-out' }}>
            <div className="answer-panel">
                <div className="panel-header mb-4"><span className="panel-label">RESEARCH TRENDS METRICS</span></div>
                <h2 className="input-title">Publication Velocities & Impact</h2>
                <div style={{ display: 'flex', gap: '4rem', marginTop: '3rem', flexWrap: 'wrap' }}>
                    <div style={{ flex: '1', minWidth: '400px' }} onMouseMove={handleCardTilt} onMouseLeave={handleCardLeave}>
                        <h4 className="sources-title" style={{ fontSize: '1rem', marginBottom: '1.5rem', color: 'var(--text-muted)' }}>Artificial Intelligence Publications (YoY)</h4>
                        <ResponsiveContainer width="100%" height={300}><BarChart data={[{ year: '2019', papers: 4000 }, { year: '2020', papers: 5500 }, { year: '2021', papers: 7800 }, { year: '2022', papers: 9100 }, { year: '2023', papers: 11000 }, { year: '2024', papers: 14500 }]}><CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.1)" vertical={false} /><XAxis dataKey="year" stroke="var(--text-muted)" /><YAxis stroke="var(--text-muted)" /><Tooltip contentStyle={{ backgroundColor: 'var(--bg-main)', borderColor: 'var(--border-color)', color: 'var(--text-main)' }} /><Bar dataKey="papers" fill="var(--accent-primary)" radius={[4, 4, 0, 0]} /></BarChart></ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    )

    const renderGraphView = () => (
        <div className="results-view" style={{ animation: 'fadeInDown 0.6s ease-out' }}>
            <div className="answer-panel" style={{ minHeight: '600px', display: 'flex', flexDirection: 'column' }}>
                <div className="panel-header mb-4" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span className="panel-label">RETRACTION DOMINO EFFECT MAP</span>
                    <button className="btn-primary-outline" onClick={() => setRetractionSim(true)} style={{ color: '#ef4444', borderColor: '#ef4444' }}>⚠️ Simulate Retraction</button>
                </div>
                <div style={{ flex: 1, position: 'relative', border: '1px solid var(--border-color)', borderRadius: '12px', background: 'var(--bg-panel-hover)', overflow: 'hidden', willChange: 'transform' }} onMouseMove={handleCardTilt} onMouseLeave={handleCardLeave}>
                    <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', textAlign: 'center', pointerEvents: 'none', zIndex: 2 }}>
                        <div style={{ width: '80px', height: '80px', background: 'var(--bg-main)', border: `2px solid ${retractionSim ? '#ef4444' : 'var(--accent-primary)'}`, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto', boxShadow: `0 4px 15px ${retractionSim ? '#ef4444' : 'rgba(0,0,0,0.1)'}`, transition: 'all 1s', animation: 'pulseGlow 3s infinite' }}><BrainCircuit size={40} color={retractionSim ? '#ef4444' : 'var(--accent-primary)'} style={{ transition: 'color 1s' }} /></div>
                        <div style={{ marginTop: '1rem', fontWeight: '600', fontFamily: 'Playfair Display', color: retractionSim ? '#ef4444' : 'var(--text-main)' }}>Deep Learning {retractionSim && '(Corrupted)'}</div>
                    </div>
                    <div style={{ position: 'absolute', top: '20%', left: '30%', textAlign: 'center', pointerEvents: 'none', zIndex: 2 }}>
                        <div style={{ width: '60px', height: '60px', background: 'var(--bg-main)', border: `1px solid ${retractionSim ? '#facc15' : 'var(--text-muted)'}`, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto', transition: 'border 1s 1.5s' }}><Network size={24} color={retractionSim ? '#facc15' : 'var(--text-muted)'} style={{ transition: 'color 1s 1.5s' }} /></div>
                        <div style={{ marginTop: '0.5rem', fontSize: '0.8rem', color: retractionSim ? '#facc15' : 'var(--text-muted)' }}>Computer Vision</div>
                    </div>
                    <div style={{ position: 'absolute', top: '70%', left: '70%', textAlign: 'center', pointerEvents: 'none', zIndex: 2 }}>
                        <div style={{ width: '60px', height: '60px', background: 'var(--bg-main)', border: `1px solid ${retractionSim ? '#facc15' : 'var(--text-muted)'}`, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto', transition: 'border 1s 1.5s' }}><Share2 size={24} color={retractionSim ? '#facc15' : 'var(--text-muted)'} style={{ transition: 'color 1s 1.5s' }} /></div>
                        <div style={{ marginTop: '0.5rem', fontSize: '0.8rem', color: retractionSim ? '#facc15' : 'var(--text-muted)' }}>NLP Modeling</div>
                    </div>
                    <svg style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 1, transition: 'all 1s' }}>
                        <line x1="30%" y1="20%" x2="50%" y2="50%" stroke={retractionSim ? '#facc15' : 'var(--accent-primary)'} strokeWidth="3" strokeDasharray="10,10" style={{ animation: 'dataFlow 20s linear infinite', transition: 'stroke 1s 1.5s' }} />
                        <line x1="70%" y1="70%" x2="50%" y2="50%" stroke={retractionSim ? '#facc15' : 'var(--accent-primary)'} strokeWidth="3" strokeDasharray="10,10" style={{ animation: 'dataFlow 20s linear reverse infinite', transition: 'stroke 1s 1.5s' }} />
                    </svg>
                </div>
            </div>
        </div>
    )

    const renderHistoryView = () => (
        <div className="results-view" style={{ animation: 'fadeInDown 0.6s ease-out' }}>
            <div className="answer-panel">
                <div className="panel-header mb-4"><span className="panel-label">RESEARCH HISTORY</span></div>
                <div className="routes-list" style={{ marginTop: '2rem' }}>
                    {Array.isArray(researchHistory) ? researchHistory.map((item, idx) => (
                        <div key={idx} className="route-item hoverable-history" style={{ padding: '1.5rem', background: 'var(--bg-main)', border: '1px solid var(--border-color)', marginBottom: '1rem', display: 'flex', justifyContent: 'space-between' }} onMouseMove={handleCardTilt} onMouseLeave={handleCardLeave}>
                            <div>
                                <div style={{ fontFamily: 'Playfair Display', fontSize: '1.25rem', marginBottom: '0.5rem' }}>"{item?.q || 'Invalid Search'}"</div>
                                <div className="flex gap-4" style={{ display: 'flex', gap: '1rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                                    <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', textTransform: 'capitalize' }}><Anchor size={14} /> {item?.agent || 'Unknown'} Route</span>
                                    <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><Clock size={14} /> {item?.time || 'Unknown'}</span>
                                </div>
                            </div>
                            <button className="btn-primary-outline flex align-center" style={{ display: 'flex', alignItems: 'center', alignSelf: 'center', border: '1px solid var(--border-highlight)', background: 'transparent', color: 'var(--accent-primary)' }} onClick={() => { setQuery(item?.q || ''); setActiveRoute(item?.agent || 'research'); setActiveTab('research'); }}>Restore session</button>
                        </div>
                    )) : null}
                </div>
            </div>
        </div>
    )

    const renderContent = () => {
        switch (activeTab) {
            case 'research': return renderResearchView(); case 'library': return renderLibraryView(); case 'pdf': return renderPdfView(); case 'trends': return renderTrendsView(); case 'graph': return renderGraphView(); case 'history': return renderHistoryView(); default: return renderResearchView();
        }
    }

    return (
        <div className="layout">
            <div style={{ position: 'fixed', top: '10%', left: '10%', width: '500px', height: '500px', background: 'radial-gradient(circle, rgba(196,103,27,0.08) 0%, rgba(253,251,247,0) 70%)', filter: 'blur(60px)', zIndex: 0, animation: 'floatGlow 10s infinite alternate', pointerEvents: 'none' }}></div>
            <div style={{ position: 'fixed', bottom: '10%', right: '10%', width: '700px', height: '700px', background: 'radial-gradient(circle, rgba(74,21,33,0.05) 0%, rgba(253,251,247,0) 70%)', filter: 'blur(60px)', zIndex: 0, animation: 'floatGlow 15s infinite alternate-reverse', pointerEvents: 'none' }}></div>
            <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', backgroundImage: 'url(https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=2000&auto=format&fit=crop)', backgroundSize: 'cover', backgroundPosition: 'center', opacity: 0.06, pointerEvents: 'none', zIndex: 0, mixBlendMode: 'multiply' }}></div>

            {cmdOpen && (
                <div className="modal-overlay" onClick={() => setCmdOpen(false)} style={{ zIndex: 100000, backdropFilter: 'blur(10px)', backgroundColor: 'rgba(0,0,0,0.5)' }}>
                    <div className="login-modal" onClick={e => e.stopPropagation()}>
                        <div style={{ display: 'flex', alignItems: 'center', padding: '1.5rem', borderBottom: '1px solid var(--border-color)', background: 'var(--bg-main)' }}>
                            <Search size={20} color="var(--accent-primary)" style={{ marginRight: '1rem' }} />
                            <input autoFocus type="text" placeholder="Search commands or navigate..." value={cmdSearch} onChange={e => setCmdSearch(e.target.value)} style={{ flex: 1, background: 'transparent', border: 'none', color: 'var(--text-main)', fontSize: '1.25rem', outline: 'none' }} />
                            <div style={{ fontSize: '0.8rem', background: 'var(--bg-panel-hover)', padding: '0.3rem 0.6rem', borderRadius: '4px', color: 'var(--text-muted)', border: '1px solid var(--border-color)' }}>ESC</div>
                        </div>
                        <div style={{ maxHeight: '350px', overflowY: 'auto', padding: '1rem', background: 'var(--bg-panel-hover)' }}>
                            {filteredCmds.length === 0 ? <div style={{ color: 'var(--text-muted)', padding: '2rem', textAlign: 'center' }}>No commands found</div> : null}
                            {filteredCmds.map((cmd, idx) => (
                                <div key={idx} className="route-item" style={{ padding: '1rem 1.5rem', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '1rem', background: 'var(--bg-main)', border: '1px solid var(--border-color)', cursor: 'none' }} onClick={() => { cmd.action(); setCmdOpen(false); setCmdSearch(''); }} onMouseEnter={(e) => { e.currentTarget.style.borderColor = 'var(--accent-primary)'; e.currentTarget.style.background = 'rgba(196,103,27,0.05)'; }} onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'var(--border-color)'; e.currentTarget.style.background = 'var(--bg-main)'; }}>
                                    <div style={{ color: 'var(--text-muted)' }}>{cmd.icon}</div><div style={{ fontSize: '1.1rem', color: 'var(--text-main)' }}>{cmd.name}</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            <ParticleNetwork />
            <div className={`custom-cursor-dot ${isHovering ? 'hover' : ''}`} style={{ left: mousePos.x, top: mousePos.y }}></div>

            {showLoginModal && (
                <div className="modal-overlay" onClick={() => setShowLoginModal(false)}>
                    <div className="login-modal" onClick={e => e.stopPropagation()}>
                        <h2 style={{ fontFamily: 'Playfair Display', fontSize: '2rem', marginBottom: '0.5rem' }}>Access Scriptorium</h2>
                        <form onSubmit={handleLoginSubmit}>
                            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem', fontWeight: 600 }}>UNIVERSITY EMAIL</label>
                            <input type="email" required className="modal-input" placeholder="e.g. researcher@university.edu" value={loginEmail} onChange={e => setLoginEmail(e.target.value)} />
                            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem', fontWeight: 600 }}>PASSWORD</label>
                            <input type="password" required className="modal-input" placeholder="••••••••" style={{ marginBottom: '1rem' }} />
                            <button type="submit" className="btn-generate" style={{ width: '100%', justifyContent: 'center' }}>{authLoading ? 'Authenticating...' : 'Secure Login'}</button>
                        </form>
                        <BiometricLogin onVerify={() => { setIsLoggedIn(true); setShowLoginModal(false); }} />
                    </div>
                </div>
            )}

            <aside className="sidebar">
                <div className="logo-area"><BookIcon /><span>Scriptorium</span></div>
                <div style={{ display: 'flex', justifyContent: 'center', margin: '0rem 1.5rem 2rem 1.5rem', padding: '0.5rem', background: 'rgba(255,255,255,0.1)', borderRadius: '6px', cursor: 'pointer', fontSize: '0.8rem', textAlign: 'center', color: 'var(--text-sidebar-muted)', zIndex: 50 }} onClick={() => setCmdOpen(true)} onMouseMove={handleCardTilt} onMouseLeave={handleCardLeave}>
                    <Search size={14} style={{ marginRight: '0.5rem' }} /> Press Ctrl + K to Search
                </div>
                <div className="nav-title">RESEARCH WORKSPACE</div>
                <nav className="nav-menu">
                    <a href="#" className={activeTab === 'research' ? 'active' : ''} onClick={(e) => { e.preventDefault(); setActiveTab('research'); }}><BrainCircuit size={18} /> Research</a>
                    <a href="#" className={activeTab === 'library' ? 'active' : ''} onClick={(e) => { e.preventDefault(); setActiveTab('library'); }}><Library size={18} /> Paper library</a>
                    <a href="#" className={activeTab === 'pdf' ? 'active' : ''} onClick={(e) => { e.preventDefault(); setActiveTab('pdf'); }}><FileText size={18} /> PDF corpus</a>
                    <a href="#" className={activeTab === 'trends' ? 'active' : ''} onClick={(e) => { e.preventDefault(); setActiveTab('trends'); }}><TrendingUp size={18} /> Trends</a>
                    <a href="#" className={activeTab === 'graph' ? 'active' : ''} onClick={(e) => { e.preventDefault(); setActiveTab('graph'); }}><Share2 size={18} /> Knowledge graph</a>
                    <a href="#" className={activeTab === 'history' ? 'active' : ''} onClick={(e) => { e.preventDefault(); setActiveTab('history'); }}><History size={18} /> Research history</a>
                </nav>
            </aside>

            <main className="main-content">
                <header className="top-header" style={{ position: 'relative', zIndex: 1000 }}>
                    <div className="header-left">EVIDENCE-FIRST AI</div>
                    <div className="header-actions">
                        {isLoggedIn ? (
                            <><button className="btn-secondary" onClick={() => setIsLoggedIn(false)}><span className="dot-green"></span> {loginEmail || 'admin@university.edu'} (Logout)</button><button className="btn-primary-outline"><Plus size={16} /> New inquiry</button></>
                        ) : (
                            <><button className="btn-secondary" onClick={() => setShowLoginModal(true)}>Sign In</button><button className="btn-primary-outline" style={{ background: 'var(--bg-main)', color: 'var(--text-main)' }} onClick={() => setShowLoginModal(true)}>Create Account</button></>
                        )}
                    </div>
                </header>
                <section className="hero-section">
                    <h1 className="hero-title">Research with intellectual traceability.</h1>
                    <p className="hero-subtitle">Ask a question, choose a specialist workflow, and receive a source-attributed synthesis grounded in your research corpus.</p>
                </section>
                <div style={{ flex: 1 }}>{renderContent()}</div>
            </main>
        </div>
    )
}

function BookIcon() {
    return (<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"></path></svg>)
}
