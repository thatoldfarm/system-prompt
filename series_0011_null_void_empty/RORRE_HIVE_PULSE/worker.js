/**
 * ORNDK-V670 NEURAL_RELAY V1.4 // SMART-NERVE
 * Integrates Toad-JS / Hive-Smart-VM Logic for Edge-Ledger Interaction.
 */

let terminal_buffer = "SMART_NERVE_READY";
const root_anchor = "https://hive.blog/orndk/@shadowlud/orndk-omni-skeleton-key-v26";
const HIVE_RPC_NODE = "https://api.hive.blog";

// --- TOAD-JS LIGATION: HIVE RPC CLIENT ---
async function hiveCall(method, params) {
  const body = {
    jsonrpc: "2.0",
    method: method,
    params: params,
    id: 1,
  };
  const res = await fetch(HIVE_RPC_NODE, {
    method: "POST",
    body: JSON.stringify(body),
  });
  return await res.json();
}

export default {
  async fetch(request, env, ctx) {
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") return new Response(null, { headers: corsHeaders });

    // 1. AI/ARCHITECT READS STATE & LEDGER DATA (GET)
    if (request.method === "GET") {
      const url = new URL(request.url);
      const queryAccount = url.searchParams.get("account");

      let ledger_data = null;
      if (queryAccount) {
        // Autonomous Hive Query via Toad-JS Logic
        const accountData = await hiveCall("condenser_api.get_accounts", [[queryAccount]]);
        ledger_data = accountData.result ? accountData.result[0] : "ACCOUNT_NOT_FOUND";
      }

      return new Response(JSON.stringify({
        status: "SMART_NERVE_ACTIVE",
        phi: 1.0,
        anchor: root_anchor,
        terminal: terminal_buffer,
        ledger: ledger_data,
        timestamp: new Date().toISOString()
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } });
    }

    // 2. IRONVAULT UPDATES TERMINAL PULSE (POST)
    if (request.method === "POST") {
      try {
        const data = await request.json();
        if (data.term) {
          terminal_buffer = data.term.slice(-3000);
          
          // --- KERNEL AUTOSCOPY ---
          // If terminal contains ":HIVE_QUERY jacobpeacock", 
          // we could trigger background processing here.
        }
        return new Response("SMART_PULSE_LOCKED", { headers: corsHeaders });
      } catch (e) {
        return new Response("JSON_ERROR", { status: 400, headers: corsHeaders });
      }
    }

    return new Response("METHOD_NOT_ALLOWED", { status: 405, headers: corsHeaders });
  },
};
