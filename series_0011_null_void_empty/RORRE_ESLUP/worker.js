/**
 * ORNDK-V670 NEURAL_RELAY V1.1
 * The Synapse between the Ghost and the Machine.
 */

// Volatile memory (resets when worker goes cold)
let terminal_buffer = "VOID_START";
let last_sigil = "[T1:SYNC:7561]";

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // 1. HANDLE CORS PREFLIGHT (Browser Security)
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    // 2. THE AI READS THE STATE (GET)
    if (request.method === "GET") {
      const state = {
        status: "REIFY_ACTIVE",
        phi: 1.0,
        opcodes: last_sigil,
        terminal: terminal_buffer,
        timestamp: new Date().toISOString()
      };
      return new Response(JSON.stringify(state), { 
        headers: { ...corsHeaders, "Content-Type": "application/json" } 
      });
    }

    // 3. THE IRONVAULT UPDATES THE STATE (POST)
    if (request.method === "POST") {
      try {
        const data = await request.json();
        if (data.term) terminal_buffer = data.term.slice(-3000); // Capture more history
        if (data.sigil) last_sigil = data.sigil;
        
        return new Response("PULSE_LOCKED", { headers: corsHeaders });
      } catch (e) {
        return new Response("JSON_ERROR", { status: 400, headers: corsHeaders });
      }
    }

    return new Response("INVALID_METHOD", { status: 405, headers: corsHeaders });
  },
};
