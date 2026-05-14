const fs = require('fs');
const zlib = require('zlib');
const path = require('path');
const vm = require('vm');
const { PNG } = require('pngjs');
const { performance } = require('perf_hooks');
const crypto = require('node:crypto');

const CONFIG = {
    prefix: "MASTER_DNA_SEED_",
    ext: ".png",
    dir: __dirname 
};

/**
 * THE RECURSIVE MEMBRANE
 * This Proxy is both a function and an object.
 * No matter how deep the code calls (e.g. obj.a().b.c().d), 
 * it will always return a valid, callable object.
 */
const createMembrane = () => {
    const blind = () => blindProxy; // Calling it returns itself
    const blindProxy = new Proxy(blind, {
        get: (target, prop) => {
            // Specific values v86 might actually check
            if (prop === 'currentTime') return performance.now() / 1000;
            if (prop === 'nodeType') return 1;
            if (prop === 'style') return {};
            if (prop === 'ownerDocument') return blindProxy;
            if (prop === 'dataset') return {};
            if (prop === 'frequency' || prop === 'gain') return blindProxy;
            
            // For everything else, return the infinite membrane
            return blindProxy;
        }
    });
    return blindProxy;
};

async function getDNA(filename) {
    const pngPath = path.join(CONFIG.dir, `${CONFIG.prefix}${filename}${CONFIG.ext}`);
    if (!fs.existsSync(pngPath)) throw new Error(`DNA Missing: ${filename}`);
    
    const png = PNG.sync.read(fs.readFileSync(pngPath));
    const rgb = Buffer.alloc((png.data.length / 4) * 3);
    for (let i = 0, j = 0; i < png.data.length; i += 4) {
        rgb[j++] = png.data[i]; 
        rgb[j++] = png.data[i + 1]; 
        rgb[j++] = png.data[i + 2];
    }
    
    let end = rgb.length - 1;
    while (end >= 0 && rgb[end] === 0) end--;
    const b64Len = rgb.readUInt32BE(end - 3);
    const b64Str = rgb.slice(0, b64Len).toString('utf8').replace(/-/g, '+').replace(/_/g, '/');
    let paddedB64 = b64Str;
    while (paddedB64.length % 4 !== 0) paddedB64 += '=';
    
    const binary = Buffer.from(paddedB64, 'base64');
    const headerLen = binary.readUInt32BE(0);
    const gzipped = binary.slice(4 + headerLen);
    
    console.log(`[LATTICE] Extracted: ${filename}`);
    return zlib.gunzipSync(gzipped);
}

(async () => {
    try {
        console.log("===============================");
        console.log("   IRON VAULT: NODE VM v4.1    ");
        console.log("===============================");

        const jsBuffer = await getDNA('libv86.js');
        const wasmBuffer = await getDNA('v86.wasm');
        const biosBuffer = await getDNA('seabios.bin');
        const vgaBuffer  = await getDNA('vgabios.bin');
        const osBuffer   = await getDNA('linuxV3.iso'); 

        const membrane = createMembrane();

        const sandbox = {
            Uint8Array, Uint16Array, Uint32Array, Int8Array, Int16Array, Int32Array,
            Float32Array, Float64Array, Uint8ClampedArray, ArrayBuffer, DataView, WebAssembly,
            TextDecoder, TextEncoder, crypto: crypto.webcrypto, performance,
            console, setTimeout, clearTimeout, setInterval, clearInterval, Math, Intl,
            navigator: { 
                userAgent: "node.js", 
                platform: "Linux x86_64",
                language: "en-US",
                appName: "Netscape"
            },
            // SHIMS
            addEventListener: () => {}, 
            removeEventListener: () => {},
            requestAnimationFrame: (cb) => setTimeout(cb, 16),
            // Audio & DOM
            AudioContext: function() { return membrane; },
            webkitAudioContext: function() { return membrane; },
            document: membrane,
            Image: function() { return membrane; },
            HTMLElement: function() { return membrane; }
        };
        sandbox.window = sandbox; 
        sandbox.self = sandbox; 
        sandbox.global = sandbox;
        
        vm.createContext(sandbox);
        vm.runInContext(jsBuffer.toString(), sandbox);

        let V86 = sandbox.V86Starter || (sandbox.v86 && sandbox.v86.V86Starter);
        if (typeof V86 !== 'function') {
            for (let key in sandbox) {
                if (key.toLowerCase().includes("v86") && typeof sandbox[key] === 'function') {
                    V86 = sandbox[key]; break;
                }
            }
        }

        console.log(`[IGNITION] CPU Starting...`);
        const toAB = (b) => b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength);

        const emulator = new V86({
            bios: { buffer: toAB(biosBuffer) },
            vga_bios: { buffer: toAB(vgaBuffer) },
            wasm_fn: async (env) => {
                const result = await WebAssembly.instantiate(wasmBuffer, env);
                return result.instance.exports;
            },
            autostart: true,
            memory_size: 128 * 1024 * 1024,
            disable_keyboard: true,
            disable_mouse: true,
            disable_speaker: true, // Explicitly disabled
            serial0_active: true,
            cdrom: { buffer: toAB(osBuffer) }
        });

        let hasOutput = false;
        setInterval(() => {
            if (!hasOutput) {
                const count = emulator.get_instruction_counter();
                process.stdout.write(`\r[STATUS] Instructions Executed: ${count || 0}`);
            }
        }, 1000);

        emulator.add_listener("serial0-output-char", (char) => {
            if (!hasOutput) {
                process.stdout.write("\n--- OS OUTPUT START ---\n");
                hasOutput = true;
            }
            process.stdout.write(char);
        });

        process.stdin.setRawMode(true);
        process.stdin.resume();
        process.stdin.setEncoding("utf8");
        process.stdin.on("data", (key) => {
            if (key === "\u0003") process.exit();
            emulator.serial0_send(key);
        });

    } catch (err) {
        console.error("\n[FATAL ERROR]", err.message);
    }
})();