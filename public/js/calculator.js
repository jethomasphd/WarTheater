/* ═══════════════════════════════════════════════════════════════
   THE WAR THEATER — Consumer Impact Calculator
   "How much more are YOU paying?"
   This is the viral engine. Personal relevance drives sharing.
   ═══════════════════════════════════════════════════════════════ */

WarTheater.Calculator = {
  // State gas price premiums (cents above/below national average)
  // Source: AAA state averages, approximate differentials
  statePremiums: {
    'avg': 0,
    'CA': 1.15,
    'TX': -0.12,
    'FL': 0.08,
    'NY': 0.52,
    'PA': 0.10,
    'OH': -0.08,
    'IL': 0.28,
    'AZ': -0.02,
    'GA': -0.05,
    'WA': 0.65,
    'MI': 0.05,
    'NJ': 0.12,
    'VA': -0.03,
    'CO': 0.05,
    'NC': -0.05
  },

  // Gas price data
  preWarBase: 2.98,
  currentBase: 3.95,
  warIncrease: 0.97, // currentBase - preWarBase

  init() {
    var miles = document.getElementById('calc-miles');
    var mpg = document.getElementById('calc-mpg');
    var state = document.getElementById('calc-state');

    if (!miles || !mpg || !state) return;

    // Populate states dynamically
    this.populateStates(state);

    var self = this;
    var calc = function() { self.calculate(); };
    miles.addEventListener('input', calc);
    mpg.addEventListener('input', calc);
    state.addEventListener('change', calc);

    this.calculate();
  },

  populateStates(select) {
    var states = [
      { val: 'avg', label: 'National Average' },
      { val: 'CA', label: 'California' },
      { val: 'TX', label: 'Texas' },
      { val: 'FL', label: 'Florida' },
      { val: 'NY', label: 'New York' },
      { val: 'PA', label: 'Pennsylvania' },
      { val: 'OH', label: 'Ohio' },
      { val: 'IL', label: 'Illinois' },
      { val: 'AZ', label: 'Arizona' },
      { val: 'GA', label: 'Georgia' },
      { val: 'WA', label: 'Washington' },
      { val: 'MI', label: 'Michigan' },
      { val: 'NJ', label: 'New Jersey' },
      { val: 'VA', label: 'Virginia' },
      { val: 'CO', label: 'Colorado' },
      { val: 'NC', label: 'North Carolina' }
    ];

    select.innerHTML = states.map(function(s) {
      return '<option value="' + s.val + '"' + (s.val === 'TX' ? ' selected' : '') + '>' + s.label + '</option>';
    }).join('');
  },

  calculate() {
    var milesPerWeek = parseFloat(document.getElementById('calc-miles').value) || 0;
    var mpg = parseFloat(document.getElementById('calc-mpg').value) || 28;
    var stateKey = document.getElementById('calc-state').value;

    var statePremium = this.statePremiums[stateKey] || 0;
    var preWarPrice = this.preWarBase + statePremium;
    var currentPrice = this.currentBase + statePremium;
    var priceIncrease = currentPrice - preWarPrice;

    // Weekly gallons
    var weeklyGallons = milesPerWeek / mpg;
    var monthlyGallons = weeklyGallons * 4.33;
    var yearlyGallons = weeklyGallons * 52;

    // Additional costs due to war
    var additionalMonthlyCost = monthlyGallons * priceIncrease;
    var additionalYearlyCost = yearlyGallons * priceIncrease;
    var additionalWeeklyCost = weeklyGallons * priceIncrease;

    // Number of fill-ups per month (assume 14 gallon tank)
    var fillUpsPerMonth = monthlyGallons / 14;
    var extraPerFillUp = 14 * priceIncrease;

    // Update output
    var output = document.getElementById('calc-output');
    if (output) {
      output.textContent = WarTheater.Utils.formatCurrency(additionalMonthlyCost);
    }

    // Update or create the extended results
    var resultContainer = document.getElementById('calc-result');
    if (!resultContainer) return;

    // Check if extended container exists
    var extended = document.getElementById('calc-extended');
    if (!extended) {
      extended = document.createElement('div');
      extended.id = 'calc-extended';
      extended.style.cssText = 'margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border);';
      resultContainer.appendChild(extended);
    }

    extended.innerHTML =
      '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; text-align: center;">' +

        '<div style="background: var(--bg-card); padding: 10px; border: 1px solid var(--border);">' +
          '<div style="font-family: \'JetBrains Mono\', monospace; font-size: var(--text-lg); color: var(--financial-up);">' +
            WarTheater.Utils.formatCurrency(additionalWeeklyCost) +
          '</div>' +
          '<div style="font-size: 10px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.06em; margin-top: 4px;">Extra Per Week</div>' +
        '</div>' +

        '<div style="background: var(--bg-card); padding: 10px; border: 1px solid var(--border);">' +
          '<div style="font-family: \'JetBrains Mono\', monospace; font-size: var(--text-lg); color: var(--financial-up);">' +
            WarTheater.Utils.formatCurrency(additionalYearlyCost) +
          '</div>' +
          '<div style="font-size: 10px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.06em; margin-top: 4px;">Projected Annual Cost</div>' +
        '</div>' +

      '</div>' +

      '<div style="margin-top: 12px; font-size: var(--text-xs); color: var(--text-secondary); line-height: 1.6;">' +
        '<div style="margin-bottom: 6px;">' +
          '<strong style="color: var(--text-accent);">Your state price:</strong> ' +
          '$' + currentPrice.toFixed(2) + '/gal (was $' + preWarPrice.toFixed(2) + ' pre-war)' +
        '</div>' +
        '<div style="margin-bottom: 6px;">' +
          '<strong style="color: var(--text-accent);">Per fill-up:</strong> ' +
          'Extra $' + extraPerFillUp.toFixed(2) + ' each time you fill a 14-gallon tank' +
        '</div>' +
        '<div>' +
          '<strong style="color: var(--text-accent);">In context:</strong> ' +
          this.getContextComparison(additionalYearlyCost) +
        '</div>' +
      '</div>' +

      '<div style="margin-top: 10px; font-size: 9px; color: var(--text-dim); font-family: \'JetBrains Mono\', monospace;">' +
        'Based on war-driven increase of $' + priceIncrease.toFixed(2) + '/gal. ' +
        'Pre-war national avg: $' + this.preWarBase.toFixed(2) + '. Current: $' + this.currentBase.toFixed(2) + '. ' +
        'Source: AAA.' +
      '</div>';
  },

  // Put the annual cost in relatable context
  getContextComparison(yearlyCost) {
    if (yearlyCost < 50) {
      return 'About ' + Math.round(yearlyCost / 5) + ' cups of coffee per year.';
    } else if (yearlyCost < 150) {
      return 'That\'s a month of streaming subscriptions — paid to the war.';
    } else if (yearlyCost < 300) {
      return 'That\'s roughly a family\'s monthly grocery increase.';
    } else if (yearlyCost < 600) {
      return 'That\'s a car payment — just in extra gas.';
    } else {
      return 'That\'s $' + WarTheater.Utils.formatNumber(Math.round(yearlyCost)) + ' — enough for ' + Math.round(yearlyCost / 200) + ' months of a family\'s electric bill.';
    }
  }
};
