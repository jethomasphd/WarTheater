/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Consumer Impact Calculator
   "How much more are YOU paying?"
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Calculator = {
  // State gas price premiums (approximate cents above/below national avg)
  statePremiums: {
    'avg': 0,
    'CA': 0.85,
    'TX': -0.15,
    'FL': 0.05,
    'NY': 0.45,
    'PA': 0.10,
    'OH': -0.10,
    'IL': 0.20
  },

  init() {
    const miles = document.getElementById('calc-miles');
    const mpg = document.getElementById('calc-mpg');
    const state = document.getElementById('calc-state');

    if (!miles || !mpg || !state) return;

    const calc = () => this.calculate();
    miles.addEventListener('input', calc);
    mpg.addEventListener('input', calc);
    state.addEventListener('change', calc);

    // Initial calculation
    this.calculate();
  },

  calculate() {
    const milesPerWeek = parseFloat(document.getElementById('calc-miles').value) || 0;
    const mpg = parseFloat(document.getElementById('calc-mpg').value) || 28;
    const stateKey = document.getElementById('calc-state').value;

    // Gas price increase due to war
    const preWarBase = 3.05;
    const currentBase = 3.48;
    const statePremium = this.statePremiums[stateKey] || 0;

    const preWarPrice = preWarBase + statePremium;
    const currentPrice = currentBase + statePremium;
    const priceIncrease = currentPrice - preWarPrice;

    // Monthly gallons consumed
    const weeklyGallons = milesPerWeek / mpg;
    const monthlyGallons = weeklyGallons * 4.33;

    // Additional monthly cost
    const additionalMonthlyCost = monthlyGallons * priceIncrease;

    const output = document.getElementById('calc-output');
    if (output) {
      output.textContent = WarTheater.Utils.formatCurrency(additionalMonthlyCost);
    }
  }
};
