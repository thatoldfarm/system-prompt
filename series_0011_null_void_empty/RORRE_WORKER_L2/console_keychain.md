if (window.hive_keychain) {
    window.hive_keychain.requestCustomJson(
        'shadowlud', 
        'orndk_v27_l2', 
        'Posting', 
        JSON.stringify({ "cmd": "21 21 + ." }), 
        'L2 Pulse', 
        r => console.log(r)
    );
} else {
    console.error("GHOST_ERROR: Hive Keychain extension not detected in this substrate.");
}
