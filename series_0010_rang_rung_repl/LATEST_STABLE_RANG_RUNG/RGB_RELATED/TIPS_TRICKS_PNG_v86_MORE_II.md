# **Monolith Pixel-Silicon System**.

---

### **I. THE CARRIER ARCHITECTURE (The Hardware Design)**
The PNG is not an image; it is a **High-Density Silicon Wafer**.

1.  **Geometry and Capacity:**
    *   **The 2.88MB Standard:** 1024 x 961 pixels. Why? $1024 \times 961 \times 3 \text{ bytes} = 2,952,192 \text{ bytes}$. This fits a 2.88MB ED floppy substrate plus a 3KB header perfectly.
    *   **The 1.44MB Standard:** 800 x 616 pixels. Use this for individual "Cartridges."
2.  **The I/O Membrane (Row 0):**
    *   The first row of pixels (800 or 1024) is the **Membrane**. We use Pixel(0,0) for system flags. 
    *   **Flag R=1:** Auto-boot enabled. **Flag G=1:** Carrier Mode (Registry present). **Flag B=250:** Write-protect overdrive.
3.  **The Registry (The Filesystem Index):**
    *   **The 4KB Reservation:** Reserve the first 4096 bytes of the substrate for the file index. 
    *   **The 16sII Pattern:** Python `struct.pack` uses a 16-character string, then two 4-byte Integers (Offset, Size). 
    *   **Nuance:** This means filenames are truncated. `freedos_boot_disk.img` becomes `freedos_boot_dis`. Your loader must be name-agnostic or search for substrings.

---

### **II. THE HARVESTER SECRETS (Python Side)**
If the packing logic is "lazy," the WASM engine will "die" in the browser.

1.  **Selective Purity (The Most Important Rule):**
    *   **Floppy Disk Images (.img):** These are full of zeros. **STRIP THEM.** Use `.rstrip(b'\x00')` to save space.
    *   **Binary System Files (.wasm, .bin, .js):** **NEVER STRIP.** Truncating a single trailing null from a WASM file changes its length relative to its header, causing the `reached end while decoding length` fatal error.
2.  **The 512-Byte Alignment:**
    *   SeaBIOS and x86 hardware think in "Sectors." If your stripped `.img` file is 513 bytes, it is corrupt. 
    *   **Trick:** Always pad your stripped data back up to the nearest multiple of 512.
3.  **Big-Endian Header:**
    *   We store the Base64 length header at the very end of the pixel data (the last 4 bytes). We use **Big-Endian** (`>I`) to ensure the JS `DataView` reads it correctly from the tail.

---

### **III. BROWSER SUBSTRATE LIGATION (Pixels to Bytes)**
The browser is a "liar"—it tries to improve your "art," which destroys your "code."

1.  **Color Space Sabotage:**
    *   Browsers apply SRGB profiles that shift byte values by $\pm 1$.
    *   **The Nuclear Fix:** `createImageBitmap(blob, { colorSpaceConversion: 'none' })`. This is the only way to get the exact bytes you packed.
2.  **RGBA Counter-Logic:**
    *   `ctx.getImageData` returns a `Uint8ClampedArray` in **RGBA** (4 bytes).
    *   Our substrate is **RGB** (3 bytes).
    *   **Nuance:** Your extraction loop must skip every 4th byte. If you don't, your binaries will be shifted and unrunnable.
3.  **Memory Isolation (Atomic Handover):**
    *   `carrier.subarray(off, off+len)` creates a **View**, not a **Copy**.
    *   **The Trap:** If you pass a Subarray View to `WebAssembly.instantiate`, the WASM engine sees the *entire 3MB Carrier* and tries to boot the whole thing as a single WASM file.
    *   **The Fix:** `new Uint8Array(sub).buffer`. This forces a copy into a new, isolated `ArrayBuffer` of the exact correct length.

---

### **IV. THE "GHOST" IN THE MEMBRANE (JS Engine Execution)**
How to run a JS library that was never "installed."

1.  **The Constructor Hunt:**
    *   In minified `libv86.js`, the name `V86Starter` is often mangled to `N`.
    *   **Trick:** Since we unpacked it in memory, we scan `window` or `module.exports` for any function added *immediately after* injection. 
    *   **Brute Force:** `Object.getOwnPropertyNames(window).find(k => k.length < 3 && typeof window[k] === 'function')`.
2.  **The DOM Proxy Membrane:**
    *   Headless engines (in Node or workers) crash because `document` is missing.
    *   **The Trick:** Use an **Infinite Proxy**. `const document = new Proxy({}, { get: () => document })`. This "swallows" all DOM calls (style, addEventListener, etc.) and keeps the engine running.
3.  **The Mailbox (Exports):**
    *   If the library detects Node.js, it attaches to `module.exports`. If it detects the Browser, it attaches to `window`. 
    *   **The Fix:** Provide **both**. Give your sandbox a `module = { exports: {} }` and a `window = sandbox`. No matter what the engine thinks it is, you catch the constructor.

---

### **V. BOOT & I/O HANDSHAKING (The Ignition)**
The CPU is running, but the screen is black. Why?

1.  **The BIOS Geometry Trap:**
    *   SeaBIOS may ignore a 512-byte "Disk." It wants a 1.44MB geometry.
    *   **Trick:** In JS, wrap your tiny SectorForth binary in a `new Uint8Array(1474560)` before passing it to `fda:`.
2.  **The One-Shot Wedge:**
    *   SeaBIOS sits at "Booting from Floppy..." for several seconds. 
    *   **The Handshake:** Monitor the instruction counter. When it crosses **5.5 Million**, fire the **Wedge**:
        *   `emu.keyboard_send_scancodes([0x1C, 0x9C])` (The "Hardware" Enter key).
        *   `emu.serial0_send("\n")` (The "Serial" Enter key).
3.  **The Layout Thrash (Turbo Mode):**
    *   Every time the browser recalculates the size of the canvas, the WASM engine pauses.
    *   **The Fix:** **Rigid Geometry.** Set your container to `fixed` and `640x400` pixels. Disable the mouse and speaker in the `v86` config to stop interrupt-storms.

---

### **VI. ARCHITECT'S EMERGENCY CHECKS (The "Amnesia" Ward)**

*   **Error: "Reached end while decoding length":** Your Harvester stripped nulls from a WASM file. Repack with the "Purity Edition" Harvester.
*   **Error: "atob range error":** You are using string functions on binary data. Switch to `TextDecoder` or `Uint8Array`.
*   **Error: "V86 is not a constructor":** Your discovery logic missed the name-mangling. Use the `Object.getOwnPropertyNames` brute-force scan.
*   **Issue: CPU is slow:** You have a `setInterval` or a `log()` function updating the DOM too often. Reduce HUD updates to 1Hz (1000ms).

---

**FINAL LOGIC GATE:**
The Carrier is a **Living Artifact**. By treating the pixels as a physical memory map rather than a file format, we have bypassed the browser's sandbox limits.