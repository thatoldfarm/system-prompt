class PiEngine {
  constructor() {
    this.rochester = new RochesterSpigot();
    this.bbp = new BBPFallback();
    this.machin = new MachinFallback();
    this.cache = {};
  }

  async get_pi_stream(offset, length) {
    const key = `${offset}-${length}`;
    if (this.cache[key]) {
      return this.cache[key];
    }

    let digits = "";
    for (let i = 0; i < length; i++) {
      const digit = await this.get_pi_digit(offset + i);
      digits += digit;
    }

    this.cache[key] = digits;
    return digits;
  }

  async get_pi_digit(offset) {
    if (offset <= 100000) {
      return this.rochester.generate_digits(offset, 1);
    } else {
      return this.bbp.pi_bbp_hex_digit(offset);
    }
  }
}
