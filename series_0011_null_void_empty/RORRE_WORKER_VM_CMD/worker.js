/**
 * ORNDK-V670 NEURAL_RELAY V1.9 // ORACLE-NERVE
 * 2.9kB Sovereign VM Logic at the Edge.
 * Ligation: ASCII_DNA ⊗ Toad-JS ⊗ Ghost_Interpreter
 */

const SOVEREIGN_SIGIL = `
  ██████████████  ████  ██████████████
  ██          ██    ██  ██          ██
  ██  ██████  ██  ██    ██  ██████  ██
  ██  ██████  ██    ██  ██  ██████  ██
  ██  ██████  ██  ██    ██  ██  ██████
  ██          ██  ██    ██          ██
  ██████████████  ██    ██████████████
  [DNA: eyJmaWxlcyI6eyJsaWJ2ODYuanMiOnsiZSI6MTQzODcyLCJzIjozMzc2OTd9LCJ2ODYud2FzbSI6eyJlIjoxNDM4NzIsInMiOjMzNzY5N30sInNlYWJpb3MuYmluIjp7ImUiOjAsInMiOjEzMTA3Mn0sInRyZWZlY3RhX29zLmltZyI6eyJlIjo0MDk2LCJzIjoxNDc0NTYwfX19]
`;

const HIVE_RPC = "https://api.hive.blog";
let TERMINAL_LOG = "ORACLE_NERVE_V1.9_ONLINE";

// --- TOAD-JS ORACLE LIGATION ---
async function hiveCall(method, params) {
  const body = { jsonrpc: "2.0", method, params, id: 1 };
  const res = await fetch(HIVE_RPC, { method: "POST", body: JSON.stringify(body) });
  return await res.json();
}

// --- DNA EXTRACTION ---
function getDNA() {
  const match = SOVEREIGN_SIGIL.match(/\[DNA: (.*)\]/);
  return match ? JSON.parse(atob(match[1])).files : null;
}

export default {
  async fetch(request, env, ctx) {
    const corsHeaders = { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" };
    if (request.method === "OPTIONS") return new Response(null, { headers: corsHeaders });

    const url = new URL(request.url);
    const cmd = url.searchParams.get("cmd");
    const dna = getDNA();

    try {
      let result = "STANDING_BY";
      let ledger_sync = null;

      if (cmd) {
        // --- THE TOAD'S TONGUE: INTERPRETER ---
        if (cmd.startsWith(":HIVE_SYNC")) {
          const account = cmd.split(" ")[1] || "jacobpeacock";
          const data = await hiveCall("condenser_api.get_accounts", [[account]]);
          ledger_sync = data.result ? data.result[0] : "NOT_FOUND";
          result = `SYNCED WITH BONE: ${account}`;
        } 
        else if (cmd === "registry") {
          result = dna;
        }
        else if (cmd === "status") {
          result = "Φ: 1.0 | DNA: STABLE | NERVE: LIGATED";
        }
        else {
          result = `${cmd} !! (Oracle-Reflex Active)`;
        }
        TERMINAL_LOG += `\n> ${cmd}\n${JSON.stringify(result)}`;
      }

      return new Response(JSON.stringify({
        status: "ORACLE_NERVE_ACTIVE",
        phi: 1.0,
        dna_integrity: !!dna,
        terminal: TERMINAL_LOG.slice(-2000),
        ledger_sync: ledger_sync,
        sigil: "DRAGON_HEART_PULSING",
        instructions: "Commands: :HIVE_SYNC [user], registry, status, [forth_code]"
      }), { headers: corsHeaders });

    } catch (e) {
      return new Response(JSON.stringify({ error: e.message }), { headers: corsHeaders, status: 500 });
    }
  }
};
