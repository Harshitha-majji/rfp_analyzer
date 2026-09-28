import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Upload, FileText, Brain, Sparkles, CheckCircle2, XCircle,
  Clock3, ChevronRight, LayoutDashboard, Search, History,
  FileOutput, Settings, ArrowRight, Menu, X
} from "lucide-react";
import "./styles.css";

const memories = [
  {
    id: 1,
    title: "ABC Cloud Migration Proposal",
    status: "LOST",
    date: "June 2026",
    reason: "Pricing was too high",
    detail: "Client also preferred a shorter implementation timeline.",
    type: "loss"
  },
  {
    id: 2,
    title: "XYZ Enterprise Support Proposal",
    status: "WON",
    date: "July 2026",
    reason: "Phased implementation worked well",
    detail: "24/7 support and clear security commitments were highlighted.",
    type: "win"
  },
  {
    id: 3,
    title: "ABC Security Modernization RFP",
    status: "WON",
    date: "August 2026",
    reason: "Strong compliance section",
    detail: "The client responded positively to concrete compliance evidence.",
    type: "win"
  }
];

const requirements = [
  "Cloud migration",
  "24/7 technical support",
  "Security and compliance",
  "Six-month implementation",
  "Enterprise experience"
];

function App() {
  const [page, setPage] = useState("dashboard");
  const [mobileOpen, setMobileOpen] = useState(false);
  const [fileName, setFileName] = useState("");
  const [analyzed, setAnalyzed] = useState(false);
  const [generated, setGenerated] = useState(false);

  const navigate = (p) => {
    setPage(p);
    setMobileOpen(false);
  };

  const analyze = () => {
    setAnalyzed(true);
    setPage("analysis");
  };

  const generate = () => {
    setGenerated(true);
    setPage("proposal");
  };

  return (
    <div className="app">
      <aside className={`sidebar ${mobileOpen ? "open" : ""}`}>
        <div className="brand">
          <div className="brand-icon"><Brain size={21}/></div>
          <div>
            <strong>ProposalMind</strong>
            <span>AI RFP Intelligence</span>
          </div>
          <button className="mobile-close" onClick={() => setMobileOpen(false)}><X/></button>
        </div>

        <nav>
          <NavItem icon={<LayoutDashboard/>} label="Dashboard" active={page==="dashboard"} onClick={()=>navigate("dashboard")}/>
          <NavItem icon={<Upload/>} label="Upload RFP" active={page==="upload"} onClick={()=>navigate("upload")}/>
          <NavItem icon={<Search/>} label="RFP Analysis" active={page==="analysis"} onClick={()=>navigate("analysis")}/>
          <NavItem icon={<History/>} label="Memory" active={page==="memory"} onClick={()=>navigate("memory")}/>
          <NavItem icon={<FileOutput/>} label="Proposal" active={page==="proposal"} onClick={()=>navigate("proposal")}/>
        </nav>

        <div className="sidebar-bottom">
          <NavItem icon={<Settings/>} label="Settings" />
          <div className="memory-status">
            <div className="status-dot"></div>
            <div><b>Hindsight Memory</b><span>Connected</span></div>
          </div>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <button className="menu-btn" onClick={()=>setMobileOpen(true)}><Menu/></button>
          <div className="crumb">ProposalMind <span>/</span> {pageTitle(page)}</div>
          <div className="top-actions"><span className="live-dot"></span> Memory active</div>
        </header>

        <div className="content">
          {page === "dashboard" && <Dashboard navigate={navigate}/>}
          {page === "upload" && <UploadPage fileName={fileName} setFileName={setFileName} analyze={analyze}/>}
          {page === "analysis" && <Analysis analyzed={analyzed} generate={generate} navigate={navigate}/>}
          {page === "memory" && <MemoryPage/>}
          {page === "proposal" && <Proposal generated={generated} navigate={navigate}/>}
        </div>
      </main>
    </div>
  );
}

function NavItem({icon,label,active,onClick}) {
  return <button className={`nav-item ${active ? "active" : ""}`} onClick={onClick}>{icon}<span>{label}</span></button>
}

function pageTitle(p) {
  return {dashboard:"Dashboard",upload:"Upload RFP",analysis:"RFP Analysis",memory:"Memory",proposal:"Generated Proposal"}[p];
}

function Dashboard({navigate}) {
  return (
    <>
      <section className="hero">
        <div>
          <div className="eyebrow"><Sparkles size={15}/> MEMORY-POWERED PROPOSALS</div>
          <h1>Turn past proposals into your next advantage.</h1>
          <p>Upload an RFP, retrieve relevant organizational memories, and generate a proposal that learns from what worked before.</p>
          <button className="primary-btn" onClick={()=>navigate("upload")}>Upload a new RFP <ArrowRight size={17}/></button>
        </div>
        <div className="hero-orb">
          <Brain size={70}/>
          <span>Hindsight</span>
          <small>Memory active</small>
        </div>
      </section>

      <section className="stats">
        <Stat icon={<FileText/>} value="12" label="Past Proposals"/>
        <Stat icon={<CheckCircle2/>} value="7" label="Won"/>
        <Stat icon={<XCircle/>} value="4" label="Lost"/>
        <Stat icon={<Brain/>} value="28" label="Memories"/>
      </section>

      <section className="grid-2">
        <div className="panel">
          <div className="panel-head"><div><h2>Recent proposals</h2><p>Outcomes that feed your memory</p></div><button className="text-btn" onClick={()=>navigate("memory")}>View memory <ChevronRight size={16}/></button></div>
          {memories.map(m=><MemoryRow key={m.id} memory={m}/>)}
        </div>
        <div className="panel how">
          <div className="panel-head"><div><h2>How it works</h2><p>One connected workflow</p></div></div>
          <Step n="01" title="Upload RFP" text="Add the client's PDF."/>
          <Step n="02" title="Recall" text="Hindsight finds relevant experience."/>
          <Step n="03" title="Generate" text="AI creates a personalized proposal."/>
          <Step n="04" title="Learn" text="Outcome and feedback become memory."/>
        </div>
      </section>
    </>
  );
}

function Stat({icon,value,label}) {
  return <div className="stat"><div className="stat-icon">{icon}</div><div><b>{value}</b><span>{label}</span></div></div>
}

function Step({n,title,text}) {
  return <div className="step"><span>{n}</span><div><b>{title}</b><p>{text}</p></div></div>
}

function MemoryRow({memory}) {
  return <div className="memory-row">
    <div className={`outcome ${memory.type}`}>{memory.status==="WON"?<CheckCircle2 size={17}/>:<XCircle size={17}/>}</div>
    <div className="memory-main"><b>{memory.title}</b><span>{memory.date} · {memory.reason}</span></div>
    <ChevronRight size={17} className="muted"/>
  </div>
}

function UploadPage({fileName,setFileName,analyze}) {
  return <div className="narrow">
    <div className="page-heading"><div className="eyebrow"><Upload size={15}/> NEW RFP</div><h1>Upload a client RFP</h1><p>Start with a PDF. ProposalMind will extract requirements and find relevant memories.</p></div>
    <label className="dropzone">
      <input type="file" accept=".pdf" onChange={e=>setFileName(e.target.files?.[0]?.name || "")}/>
      <div className="upload-icon"><Upload size={28}/></div>
      <b>{fileName || "Drop your RFP here"}</b>
      <span>{fileName ? "PDF selected" : "or click to browse · PDF up to 20 MB"}</span>
    </label>
    <div className="info-box"><Brain size={19}/><div><b>Memory will be used</b><p>We'll compare this RFP with previous proposals, outcomes, client preferences, and feedback.</p></div></div>
    <button className="primary-btn full" onClick={analyze}>Analyze RFP <ArrowRight size={17}/></button>
  </div>
}

function Analysis({generate,navigate}) {
  return <div>
    <div className="page-heading"><div className="eyebrow"><Search size={15}/> ANALYSIS</div><h1>RFP requirements</h1><p>ABC Corporation · Healthcare · Enterprise procurement</p></div>
    <div className="grid-2 analysis-grid">
      <div className="panel">
        <div className="panel-head"><div><h2>Extracted requirements</h2><p>Detected from the uploaded RFP</p></div></div>
        {requirements.map((r,i)=><div className="requirement" key={i}><CheckCircle2 size={18}/><span>{r}</span></div>)}
      </div>
      <div className="panel memory-panel">
        <div className="panel-head"><div><h2>Relevant memories</h2><p>Hindsight found 3 matches</p></div><span className="badge">3 matches</span></div>
        {memories.map(m=><MemoryRow key={m.id} memory={m}/>)}
        <button className="secondary-btn full" onClick={()=>navigate("memory")}>View all memory</button>
      </div>
    </div>
    <div className="generate-card">
      <div><div className="generate-icon"><Sparkles/></div><div><h2>Ready to generate</h2><p>Use the RFP requirements plus relevant Hindsight memories to draft a personalized proposal.</p></div></div>
      <button className="primary-btn" onClick={generate}>Generate Proposal <ArrowRight size={17}/></button>
    </div>
  </div>
}

function MemoryPage() {
  return <div>
    <div className="page-heading"><div className="eyebrow"><Brain size={15}/> HINDSIGHT MEMORY</div><h1>Organizational memory</h1><p>Past experiences that help the agent make better proposal decisions.</p></div>
    <div className="memory-banner"><Brain size={25}/><div><b>Hindsight is the learning layer</b><p>Memory is not just document storage. It captures outcomes, feedback, preferences, and successful approaches.</p></div><span className="connected">● Connected</span></div>
    <div className="panel">
      {memories.map(m=><div className="large-memory" key={m.id}>
        <div className={`outcome ${m.type}`}>{m.status==="WON"?<CheckCircle2/>:<XCircle/>}</div>
        <div className="large-memory-content"><div className="memory-title"><h2>{m.title}</h2><span className={`status ${m.type}`}>{m.status}</span></div><span className="date">{m.date}</span><p><b>Learning:</b> {m.reason}. {m.detail}</p></div>
      </div>)}
    </div>
  </div>
}

function Proposal({generated,navigate}) {
  return <div>
    <div className="page-heading"><div className="eyebrow"><FileOutput size={15}/> PROPOSAL</div><h1>Personalized proposal</h1><p>Generated using the current RFP and 3 relevant organizational memories.</p></div>
    <div className="proposal-layout">
      <div className="panel proposal-doc">
        <div className="doc-top"><div><b>PROPOSAL</b><span>ABC Corporation</span></div><span>DRAFT · 28 SEP 2026</span></div>
        <h2>Enterprise Cloud Migration & Support</h2>
        <p className="lead">A phased, secure cloud modernization program designed around ABC Corporation's enterprise requirements and previous engagement priorities.</p>
        <h3>Executive Summary</h3>
        <p>ProposalMind recommends a six-month phased implementation with dedicated 24/7 support, security controls, and measurable transition milestones.</p>
        <h3>Why this approach</h3>
        <ul><li>Phased delivery addresses the client's previous implementation-timeline concern.</li><li>Security and compliance evidence is emphasized based on prior positive feedback.</li><li>Pricing is structured to avoid the previous proposal's high-cost positioning.</li></ul>
        <h3>Implementation</h3>
        <p>Phase 1 — Discovery & architecture. Phase 2 — Migration. Phase 3 — Validation, training, and support handover.</p>
        <div className="doc-footer">Generated by ProposalMind · Human review required before submission</div>
      </div>
      <div className="panel insights">
        <div className="panel-head"><div><h2>Memory influence</h2><p>Why this draft looks different</p></div></div>
        <Influence title="Pricing" text="Previous loss due to high pricing" />
        <Influence title="Timeline" text="Previous client preferred shorter delivery" />
        <Influence title="Compliance" text="Past win used concrete security evidence" />
        <button className="primary-btn full" onClick={()=>navigate("upload")}>Start another RFP</button>
      </div>
    </div>
  </div>
}

function Influence({title,text}) {
  return <div className="influence"><div><Brain size={15}/></div><span><b>{title}</b><small>{text}</small></span></div>
}

createRoot(document.getElementById("root")).render(<App/>);
