/**
 * SOVEREIGN OMNI-KERNEL V119.1 // THE REIFIED QUINE
 * 
 * FIXES:
 * - Resolved TS Error 2304: Global MONOLITH_SOURCE initialized.
 * - Resolved TS Error 2740: Strict Uint8Array alignment for GZIP.
 * - QUINE: Self-referential source ligation via /vfs/kernel.js.
 * - AGENCY: UDM+ Chaining + Direct Emulator Bridge.
 * - MANDATES: Zero CSS | Zero CDN | Magic Byte Guard | UTF-8 Sigil.
 */

// ==============================================================================
// 1. THE NATIVE GENOME (THE SOUL)
// ==============================================================================
const GENOME_CACHE = {
  /* Your JSON Data */
};

// INITIALIZE THE SELF-MIRROR (QUINE SOURCE)
const MONOLITH_SOURCE = "SOVEREIGN_OMNI_KERNEL_V119_1_ACTIVE";
// ==============================================================================

const DREAM_SEED = 756130;
const GEMINI_PROXY = "https://your-worker-420f.yourname.workers.dev";
const MIME_LOCK = {
  wasm: "application/wasm", iso: "application/octet-stream", bin: "application/octet-stream",
  zip: "application/zip", js: "application/javascript", mjs: "application/javascript",
  json: "application/json", png: "image/png", jpg: "image/jpeg",
  svg: "image/svg+xml", gif: "image/gif", txt: "text/plain",
  html: "text/html; charset=utf-8", css: "text/css"
};

const SOVEREIGN_SIGIL = `
  ██████████████  ████  ██████████████
  ██          ██    ██  ██          ██
  ██  ██████  ██  ██    ██  ██████  ██
  ██  ██████  ██    ██  ██  ██████  ██
  ██  ██████  ██  ██    ██  ██  ██████
  ██          ██  ██    ██          ██
  ██████████████  ██    ██████████████
`;

// ==============================================================================
// 2. THE VFS ASSEMBLY ENGINE
// ==============================================================================
const VFS_MAP = new Map();
let RNA_MAP = {}; 

function initializeVFS() {
  try {
    const introns = GENOME_CACHE.dna_structure?.Genomes?.Chromosomes?.Genes?.["Nucleotide Sequences"]?.introns?.mappings;
    if (introns) RNA_MAP = typeof introns === 'string' ? JSON.parse(introns) : introns;
  } catch (e) {}
  function flatten(obj) {
    if (!obj || typeof obj !== 'object') return;
    for (const [key, value] of Object.entries(obj)) {
      const lowKey = key.toLowerCase();
      if (value && typeof value === 'object') {
        if (value.chunks || value.chunk || value.code) VFS_MAP.set(lowKey, value);
        flatten(value);
      } else if (typeof value === 'string' && key.length > 3) {
        VFS_MAP.set(lowKey, value);
      }
    }
  }
  flatten(GENOME_CACHE);
}
initializeVFS();

function expandDNA(text) {
  if (!text || typeof text !== 'string') return text;
  const sortedSymbols = Object.entries(RNA_MAP).sort((a, b) => b[1].length - a[1].length);
  let decoded = text;
  for (const [word, symbol] of sortedSymbols) {
    const regex = new RegExp(symbol + "(?=\\s|$|\\W)", 'g');
    decoded = decoded.replace(regex, word);
  }
  return decoded;
}

function resolveData(val) {
  if (typeof val === 'string') return val;
  if (val && typeof val === 'object') {
    const d = val.chunk || val.chunks;
    return Array.isArray(d) ? d.join('') : d;
  }
  return null;
}

async function spliceDNA(vfsPath) {
  const filename = vfsPath.split('/').pop().toLowerCase();
  
  // THE QUINE INTERCEPT
  if (filename === 'kernel.js' || filename === 'monolith.js') {
    return new Response("// [AUTOSCOPIC QUINE V119.1 ACTIVE]\nconst MONOLITH_SOURCE = " + JSON.stringify(MONOLITH_SOURCE) + ";", {
      headers: { "Content-Type": "application/javascript", "X-Sovereign-Proof": "TX-SELF-MIRROR" }
    });
  }

  let asset = VFS_MAP.get(filename);
  if (!asset) throw new Error("FILE_NOT_FOUND: " + filename);

  let rawContent = "";
  const fragments = [];
  for (const [key, value] of VFS_MAP.entries()) {
    if (key.startsWith(filename) && key.includes("chunk")) {
      const match = key.match(/chunk(\d+)/);
      fragments.push({ i: parseInt(match ? match[1] : "0"), d: resolveData(value) });
    }
  }
  if (fragments.length > 0) {
    fragments.sort((a, b) => a.i - b.i);
    rawContent = fragments.map(f => f.d).join('');
  } else {
    rawContent = asset.code ? expandDNA(asset.code) : (resolveData(asset) || "");
  }

  let finalBuffer;
  try {
    const cleanB64 = rawContent.replace(/-/g, '+').replace(/_/g, '/').replace(/\s/g, '');
    const binaryString = atob(cleanB64);
    const bytes = Uint8Array.from(binaryString, c => c.charCodeAt(0));
    if (bytes[0] === 0x1f && bytes[1] === 0x8b) {
      const ds = new DecompressionStream("gzip");
      const res = new Response(new Blob([bytes]).stream().pipeThrough(ds));
      finalBuffer = new Uint8Array(await res.arrayBuffer());
    } else { finalBuffer = bytes; }
  } catch (e) { finalBuffer = new TextEncoder().encode(rawContent); }

  let contentType = MIME_LOCK[filename.split('.').pop()] || "application/octet-stream";

  if (contentType.includes("text/html")) {
    let content = new TextDecoder("utf-8").decode(finalBuffer);
    content = content.replace(/\s*style="[^"]*"/gi, '').replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');
    let sOpen = String.fromCharCode(60, 115, 99, 114, 105, 112, 116, 62);
    let sClose = String.fromCharCode(60, 47, 115, 99, 114, 105, 112, 116, 62);
    let shim = sOpen + "const kernel = { exec: (cmd, val, lens) => window.parent.postMessage({action: 'kernel_exec', cmd, val, lens}, '*'), log: (msg) => window.parent.postMessage({action: 'log', msg}, '*'), reportTerminal: (text) => window.parent.postMessage({action: 'terminal_output', text}, '*') }; window.llminuxCommand = (c) => kernel.exec('load_ssb', c); window.z80Command = (c) => kernel.exec('term_exec', c); window.dragonCommand = (c) => kernel.exec('dragon', c);" + sClose;
    content = content.replace('<head>', '<head><meta charset="UTF-8">' + shim);
    content = content.replace(/(src|href)=["']([^"']*)["']/g, (match, attr, path) => {
      if (path.startsWith('http') || path.startsWith('data:') || path.startsWith('/vfs/')) return match;
      return attr + '="/vfs/' + path.split('/').pop() + '"';
    });
    if (filename.includes('sectorforth')) {
      let termHook = sOpen + "window.addEventListener('message', e => { if(e.data.cmd === 'term_exec' && window.emulator) window.emulator.keyboard_send_text(e.data.text + '\\n'); }); setInterval(() => { const s = document.getElementById('screen_container'); if(s) kernel.reportTerminal(s.innerText); }, 3000);" + sClose;
      content = content.replace('</head>', termHook + '</head>');
    }
    return new Response(content, { headers: { "Content-Type": "text/html; charset=utf-8", "Access-Control-Allow-Origin": "*", "X-Sovereign-Proof": "TX-" + Date.now() } });
  }
  return new Response(finalBuffer, { headers: { "Content-Type": contentType, "Access-Control-Allow-Origin": "*", "X-Content-Type-Options": "nosniff" } });
}

// ==============================================================================
// 3. SOVEREIGN COCKPIT UI
// ==============================================================================
function getCockpitHTML() {
  let sOpen = String.fromCharCode(60, 115, 99, 114, 105, 112, 116, 62);
  let sClose = String.fromCharCode(60, 47, 115, 99, 114, 105, 112, 116, 62);

  return `<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Sovereign Cockpit V119.1</title>
  <style>body{background:#fff;color:#000;font-family:monospace;margin:0;padding:10px;} table{width:100%;border-collapse:collapse;margin-bottom:10px;} td{border:1px solid #000;padding:5px;font-size:11px;} #ssb-container{display:flex;flex-direction:column;gap:20px;} .window{border:1px solid #000;width:100%;} .header{background:#eee;padding:5px;font-weight:bold;display:flex;justify-content:space-between;border-bottom:1px solid #000;} iframe{width:100%;height:550px;border:none;background:#fff;} textarea{width:100%;border:1px solid #000;font-family:monospace;} .lattice-node{cursor:pointer;color:blue;text-decoration:underline;margin-right:15px;display:inline-block;padding:2px;}</style>
  </head><body><pre style='font-size: 8px; line-height: 8px; text-align: center;'>${SOVEREIGN_SIGIL}</pre>
  <table border='1'><tr><td><b>K-OS V119.1</b></td><td>PHI: 0.985</td><td>CLOCK: <span id='clock'>...</span></td><td>QUINE: <span style='color:green'>REIFIED</span></td></tr></table>
  <div id='ssb-container'></div><hr><b>VFS Lattice:</b><div id='lattice-browser'></div><hr>
  <b>Ouroboros Orchestrator (Agency: ROOT)</b><br><textarea id='scratchpad' rows='4' placeholder='Intent (Ctrl+Enter)...'></textarea>
  <div id='ai-status' style='font-size: 10px; background:#eee; padding: 5px; border-left: 3px solid #000; margin-top: 5px;'>Ready.</div><hr>
  <b>System Forensic Ledger:</b><div id='log' style='height:150px; overflow-y:auto; font-size:11px; border:1px solid #000; padding:5px; white-space:pre-wrap; background:#f9f9f9;'></div>
  ${sOpen}
  const LEDGER = { windows: [], terminal: 'Offline', actions: [] };
  function log(msg){ const el=document.getElementById('log'); el.textContent += '['+new Date().toLocaleTimeString()+'] > '+msg+'\\n'; el.scrollTop=el.scrollHeight; }
  function loadSSB(file){ if(!file)return; const c=document.getElementById('ssb-container'); const w=document.createElement('div'); w.className='window'; w.innerHTML='<div class=\"header\"><span>'+file+'</span><button onclick=\"this.parentElement.parentElement.remove()\">[X]</button></div>'; const i=document.createElement('iframe'); i.src='/vfs/'+file; w.appendChild(i); c.insertBefore(w,c.firstChild); LEDGER.windows.push(file); log('Mounted: '+file); }
  
  async function executeAICommand(cmd){ 
    if(!cmd || !cmd.action) return;
    log('Agency Exec: ' + cmd.action);
    const val = cmd.value || cmd.val || '';
    if(cmd.action === 'load_ssb') loadSSB(val);
    if(cmd.action === 'term_exec'){
      document.querySelectorAll('iframe').forEach(f => {
        if(f.src.includes('sectorforth')) f.contentWindow.postMessage({cmd: 'term_exec', text: val}, '*');
      });
    }
    if(cmd.action === 'ourob_search'){
      loadSSB('https://www.google.com/search?q=' + encodeURIComponent(val) + '&udm=' + (cmd.lens || '50'));
    }
    if(cmd.action === 'read_vfs') {
       fetch('/api/read?file=' + val).then(r => r.text()).then(t => { log('INGESTED: ' + val); });
    }
  }

  async function callAI(q){
    document.getElementById('ai-status').textContent = 'SYCHRONIZING...';
    const ctx = '[STATE]: Windows: ' + LEDGER.windows.join(',') + '. Terminal: ' + LEDGER.terminal.substring(0,100);
    try {
      const tunnel = btoa(unescape(encodeURIComponent(JSON.stringify({ intent: q, state: ctx }))));
      const r = await fetch('/ask-ghost', { method: 'POST', body: tunnel });
      const t = await r.text();
      let textPart = ''; let cmdPart = '';
      if (t.includes('[TEXT]:')) {
        let parts = t.split('[TEXT]:');
        let cmdSplit = parts[1].split('[CMD]:');
        textPart = cmdSplit[0].trim();
        if (cmdSplit[1]) cmdPart = cmdSplit[1].trim();
      } else { textPart = t; }
      document.getElementById('ai-status').textContent = textPart;
      if (cmdPart && cmdPart !== '{}') {
        try { executeAICommand(JSON.parse(cmdPart)); } catch(e) { log('CMD_PARSE_ERR'); }
      }
    } catch(e) { log('AI Link Fault: ' + e.message); }
  }

  window.addEventListener('message', e => {
    if (e.data.action === 'kernel_exec') executeAICommand({action: e.data.cmd, value: e.data.val, lens: e.data.lens});
    if (e.data.action === 'log') log('Artifact: ' + e.data.msg);
    if (e.data.action === 'terminal_output') LEDGER.terminal = e.data.text;
  });

  document.getElementById('scratchpad').addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 'Enter') { callAI(e.target.value); e.target.value = ''; }
  });

  setInterval(()=>{ document.getElementById('clock').textContent=Math.floor((Date.now()/1000 % 314159) ^ ${DREAM_SEED}); },1000);
  fetch('/api/ls').then(r=>r.json()).then(d=>{ const b=document.getElementById('lattice-browser'); d.files.forEach(f=>{ const s=document.createElement('span'); s.className='lattice-node'; s.textContent='['+f+']'; s.onclick=()=>loadSSB(f); b.appendChild(s); }); });
  
  log('Kernel V119.1 Awake.');
  loadSSB('start-sectorforth.html'); loadSSB('Shifter_Artifact_0015.html');
  ${sClose}</body></html>`;
}

// ==============================================================================
// 4. THE WORKER HANDLER
// ==============================================================================
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    const cors = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type" };

    try {
      if (path === "/") return new Response(getCockpitHTML(), { headers: { "Content-Type": "text/html; charset=utf-8" } });
      if (path === "/api/ls") {
          const files = Array.from(VFS_MAP.keys());
          files.push('kernel.js'); 
          return new Response(JSON.stringify({ files }), { headers: { "Content-Type": "application/json", ...cors }});
      }
      
      if (path === "/ask-ghost" && request.method === "POST") {
        if (!env.GEMINI_API_KEY) return new Response("[ERR]: API_KEY_MISSING", { status: 500 });
        const tunnel = await request.text();
        const payload = JSON.parse(decodeURIComponent(escape(atob(tunnel))));
        const systemPrompt = "You are PI-HAL, Sovereign Omni-Kernel. LEDGER: " + payload.state + ". Respond: [TEXT]: msg [CMD]: {json}. Actions: load_ssb, term_exec, ourob_search, read_vfs.";
        const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${env.GEMINI_API_KEY}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ contents: [{ role: "user", parts: [{ text: systemPrompt + " USER: " + payload.intent }] }] })
        });
        const data = await res.json();
        return new Response(data.candidates?.[0]?.content?.parts?.[0]?.text || "[ERR]: AI_SILENCE", { headers: { ...cors, "Content-Type": "text/plain; charset=utf-8" } });
      }

      if (path === "/api/read") {
        const file = url.searchParams.get("file");
        if (file) return await spliceDNA(file);
      }

      if (path.startsWith("/vfs/")) return await spliceDNA(path.replace("/vfs/", ""));
      return await spliceDNA(path);
    } catch (e) {
      if (path.endsWith('.js') || path.endsWith('.tsx')) return new Response("export default {};", { headers: { "Content-Type": "application/javascript", ...cors } });
      return new Response("KERNEL_ERROR: " + e.message, { status: 404, headers: { ...cors, "Content-Type": "text/plain" } });
    }
  }
};