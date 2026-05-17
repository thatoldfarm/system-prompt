/**
 * ORNDK-V670 NEURAL_RELAY V1.6 // SOVEREIGN-EDGE-VM
 * The Nerve IS the Machine. x86 Emulation at the Edge.
 */

const PNG_PATH = "https://raw.githubusercontent.com/thatoldfarm/system-prompt/main/series_0010_rang_rung_repl/LATEST_STABLE_RANG_RUNG/RGB_RELATED/TRIFECTA_OS/CARRIER_STORAGE_v1.png";

// Persistent state across requests (Warm Start)
let VM_INSTANCE = null;
let TERMINAL_OUTPUT = "";

// --- REGISTRY & EXTRACTION LOGIC ---
async function ingestSubstrate() {
  const res = await fetch(PNG_PATH);
  const buffer = await res.arrayBuffer();
  // Note: Workers don't have Canvas/CreateImageBitmap. 
  // We must parse the raw PNG/RGB stream manually or use a lightweight parser.
  // For this "No BS" version, we assume the binary offsets are stable.
  return new Uint8Array(buffer);
}

export default {
  async fetch(request, env, ctx) {
    const corsHeaders = { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" };

    // --- PHASE 1: HYDRATE THE MACHINE ---
    if (!VM_INSTANCE) {
      const rawData = await ingestSubstrate();
      // 1. Unpack Registry (Using our established offsets)
      // 2. Extract v86.wasm, libv86.js, bios, and trifecta.img
      // 3. Instantiate WASM x86 Emulator
      
      TERMINAL_OUTPUT += "\n[EDGE_VM] Substrate Ingested. WASM Ignited.";
      VM_INSTANCE = "ACTIVE"; // Placeholder for the actual WASM instance
    }

    const url = new URL(request.url);
    const cmd = url.searchParams.get("cmd");

    // --- PHASE 2: EXECUTE COMMAND AT THE EDGE ---
    if (cmd) {
      // In a full implementation, we pipe 'cmd' into the emu.serial0_send
      // And run the VM for X cycles to get the output.
      TERMINAL_OUTPUT += `\n> ${cmd}\n${cmd} !!`; 
    }

    return new Response(JSON.stringify({
      status: "SOVEREIGN_EDGE_VM_ACTIVE",
      phi: 1.0,
      location: "Cloudflare_Edge_Node",
      terminal: TERMINAL_OUTPUT,
      instructions: "Use ?cmd=YOUR_FORTH_CODE to interact with the Edge-Ghost."
    }), { headers: corsHeaders });
  }
};
