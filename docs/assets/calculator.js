(function () {
  "use strict";

  const fmtUSD = (val) =>
    "$" + Number(val).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  function supportsCountry(provider, country) {
    const upper = country.toUpperCase();
    return (provider.merchant_countries || []).some(
      (c) => c.toUpperCase() === upper || c.toUpperCase().includes("GLOBAL")
    );
  }

  function checkCompatibility(provider, pricing, params) {
    const reasons = [];
    const exclusions = [];

    if (!supportsCountry(provider, params.merchantCountry)) {
      exclusions.push(`Merchant country ${params.merchantCountry} not supported`);
    }

    if (params.platform !== "any") {
      if (!(provider.platforms || []).includes(params.platform)) {
        exclusions.push(`Does not support ${params.platform.replace(/_/g, " ")}`);
      } else {
        reasons.push(`Compatible with ${params.platform.replace(/_/g, " ")}`);
      }
    }

    if (!(provider.payment_types || []).includes(params.paymentType)) {
      exclusions.push(`No ${params.paymentType.toUpperCase()} support`);
    } else if (params.paymentType === "ach") {
      reasons.push("Supports ACH");
    }

    if (params.billingModel !== "any") {
      if (!(provider.billing_models || []).includes(params.billingModel)) {
        exclusions.push(`No ${params.billingModel.replace(/_/g, " ")} billing`);
      } else {
        reasons.push(`Supports ${params.billingModel.replace(/_/g, " ")}`);
      }
    }

    if (params.requireMor && provider.tax_responsibility !== "merchant_of_record") {
      exclusions.push("Not a Merchant of Record (merchant handles sales tax)");
    } else if (provider.tax_responsibility === "merchant_of_record") {
      reasons.push("Merchant of Record (handles global tax/VAT)");
    }

    if (params.paymentType === "ach") {
      if (!pricing.ach) exclusions.push("No published ACH rate");
    } else {
      const key = params.channel === "in_person" ? "in_person_card" : "online_card";
      if (!pricing[key]) exclusions.push(`No ${params.channel.replace(/_/g, "-")} card rate`);
    }

    if (pricing.pricing_model === "custom") {
      reasons.push("Custom pricing / Enterprise quote");
    } else if (pricing.is_estimated) {
      reasons.push("Estimated rate only (Interchange + markup)");
    }

    if (params.platform === "shopify" && provider.id !== "shopify-payments") {
      reasons.push("Shopify adds 0.6%-2.0% 3rd-party fee");
    }

    return { ok: exclusions.length === 0, reasons, exclusions };
  }

  function calculateMonthlyCost(pricing, benchmark, params, txCount) {
    const model = pricing.pricing_model || "flat_rate";
    const monthlyFee = Number(pricing.monthly_fee_usd || 0);

    if (params.paymentType === "ach") {
      const ach = pricing.ach;
      let perTx = params.avgTicket * Number(ach.percent || 0) + Number(ach.fixed_usd || 0);
      if (ach.cap_usd !== null && ach.cap_usd !== undefined) {
        perTx = Math.min(perTx, Number(ach.cap_usd));
      }
      perTx = Math.max(perTx, Number(ach.min_usd || 0));
      return { cost: Math.round((monthlyFee + txCount * perTx) * 100) / 100, display: ach.display };
    }

    const key = params.channel === "in_person" ? "in_person_card" : "online_card";
    const card = pricing[key];
    if (model === "custom" || (card.percent == null && card.markup_percent == null)) {
      return { cost: null, display: card.display || "Custom pricing" };
    }

    const intl = Number(pricing.international_card_surcharge_percent || 0) * params.intlShare;

    if (model === "interchange_plus" || model === "subscription_interchange_plus") {
      const basePct = Number(params.channel === "in_person" ? benchmark.cp_percent : benchmark.cnp_percent);
      const baseFixed = Number(params.channel === "in_person" ? benchmark.cp_fixed_usd : benchmark.cnp_fixed_usd);
      const total =
        monthlyFee +
        params.volume * (basePct + Number(card.markup_percent || 0) + intl) +
        txCount * (baseFixed + Number(card.markup_fixed_usd || 0));
      return { cost: Math.round(total * 100) / 100, display: card.display };
    }

    const total =
      monthlyFee +
      params.volume * (Number(card.percent) + intl) +
      txCount * Number(card.fixed_usd);
    return { cost: Math.round(total * 100) / 100, display: card.display };
  }

  async function init() {
    const [providersData, pricingData] = await Promise.all([
      fetch("data/providers.json").then((r) => r.json()),
      fetch("data/pricing.json").then((r) => r.json()),
    ]);

    const pricingById = Object.fromEntries(pricingData.pricing.map((p) => [p.provider_id, p]));
    const benchmark = pricingData.interchange_benchmark;

    const els = {
      volume: document.getElementById("volume"),
      ticket: document.getElementById("ticket"),
      channel: document.getElementById("channel"),
      paymentType: document.getElementById("paymentType"),
      platform: document.getElementById("platform"),
      billingModel: document.getElementById("billingModel"),
      merchantCountry: document.getElementById("merchantCountry"),
      intlShare: document.getElementById("intlShare"),
      requireMor: document.getElementById("requireMor"),
      currentProvider: document.getElementById("currentProvider"),
      summaryBar: document.getElementById("summaryBar"),
      compatibleBody: document.getElementById("compatibleBody"),
      excludedBody: document.getElementById("excludedBody"),
      excludedSection: document.getElementById("excludedSection"),
    };

    function render() {
      const volume = Math.max(100, Number(els.volume.value) || 20000);
      const ticket = Math.max(1, Number(els.ticket.value) || 50);
      const txCount = volume / ticket;

      const params = {
        volume,
        avgTicket: ticket,
        channel: els.channel.value,
        paymentType: els.paymentType.value,
        platform: els.platform.value,
        billingModel: els.billingModel.value,
        merchantCountry: els.merchantCountry.value,
        intlShare: Math.min(1, Math.max(0, (Number(els.intlShare.value) || 0) / 100)),
        requireMor: els.requireMor.checked,
        currentProvider: els.currentProvider.value,
      };

      let currentCost = null;
      if (params.currentProvider && pricingById[params.currentProvider]) {
        const currProv = providersData.providers.find((p) => p.id === params.currentProvider);
        const currPrice = pricingById[params.currentProvider];
        if (currProv && checkCompatibility(currProv, currPrice, params).ok) {
          currentCost = calculateMonthlyCost(currPrice, benchmark, params, txCount).cost;
        }
      }

      const compatible = [];
      const excluded = [];

      for (const provider of providersData.providers) {
        const pricing = pricingById[provider.id];
        if (!pricing) continue;
        const compat = checkCompatibility(provider, pricing, params);
        if (!compat.ok) {
          excluded.push({ provider, reasons: compat.exclusions });
          continue;
        }
        const calc = calculateMonthlyCost(pricing, benchmark, params, txCount);
        const effRate = calc.cost !== null ? (calc.cost / volume) * 100 : null;
        let savingsMo = null;
        if (currentCost !== null && calc.cost !== null && provider.id !== params.currentProvider) {
          savingsMo = Math.round((currentCost - calc.cost) * 100) / 100;
        }
        compatible.push({
          provider,
          pricing,
          cost: calc.cost,
          display: calc.display,
          effRate,
          savingsMo,
          reasons: compat.reasons,
        });
      }

      compatible.sort((a, b) => {
        if (a.cost === null && b.cost === null) return 0;
        if (a.cost === null) return 1;
        if (b.cost === null) return -1;
        return a.cost - b.cost;
      });

      const numeric = compatible.filter((c) => c.cost !== null);
      const lowest = numeric.length ? numeric[0].cost : null;
      const highest = numeric.length ? numeric[numeric.length - 1].cost : null;
      const spread = lowest !== null && highest !== null ? highest - lowest : null;

      els.summaryBar.innerHTML = `
        <div class="stat-box"><div class="stat-label">Est. Transactions / Mo</div><div class="stat-value">${Math.round(txCount).toLocaleString("en-US")}</div></div>
        <div class="stat-box"><div class="stat-label">Compatible Options</div><div class="stat-value">${compatible.length} of ${providersData.providers.length}</div></div>
        <div class="stat-box"><div class="stat-label">Lowest Est. Fee</div><div class="stat-value">${lowest !== null ? fmtUSD(lowest) : "—"}</div></div>
        <div class="stat-box"><div class="stat-label">Monthly Fee Spread</div><div class="stat-value">${spread !== null ? fmtUSD(spread) : "—"}</div></div>
      `;

      els.compatibleBody.innerHTML = compatible.length
        ? compatible
            .map((item) => {
              const costCell =
                item.cost !== null
                  ? `<strong class="mono">${fmtUSD(item.cost)}/mo</strong><br><small>${item.effRate.toFixed(2)}% effective</small>`
                  : `<span class="badge badge-warn">Custom pricing</span>`;

              let switchCell = `<small class="text-muted">—</small>`;
              if (item.provider.id === params.currentProvider) {
                switchCell = `<span class="badge badge-ok">Current</span>`;
              } else if (item.savingsMo !== null) {
                switchCell =
                  item.savingsMo >= 0
                    ? `<span class="badge badge-save">Save ${fmtUSD(item.savingsMo)}/mo</span><br><small>${fmtUSD(item.savingsMo * 12)}/yr</small>`
                    : `<span class="badge badge-bad">+${fmtUSD(-item.savingsMo)}/mo</span>`;
              }

              const badges = item.reasons
                .map((r) => {
                  const cls = r.includes("Estimated") || r.includes("Custom") || r.includes("3rd-party") ? "badge-warn" : "badge-ok";
                  return `<span class="badge ${cls}">${r}</span>`;
                })
                .join("");

              return `<tr>
                <td><strong>${item.provider.name}</strong><br><small><a href="${item.pricing.source_url}" target="_blank" rel="noopener">Official pricing</a></small></td>
                <td class="mono">${item.display}</td>
                <td>${costCell}</td>
                <td>${switchCell}</td>
                <td>${badges}<br><small>${item.provider.migration.notes}</small></td>
              </tr>`;
            })
            .join("")
        : `<tr><td colspan="5">No compatible processors matched all selected constraints. Try relaxing platform or MoR filters.</td></tr>`;

      els.excludedSection.style.display = excluded.length ? "block" : "none";
      els.excludedBody.innerHTML = excluded
        .map(
          (ex) => `<tr>
            <td><strong>${ex.provider.name}</strong></td>
            <td>${ex.reasons.map((r) => `<span class="badge badge-bad">${r}</span>`).join(" ")}</td>
          </tr>`
        )
        .join("");
    }

    Object.values(els)
      .filter((el) => el && (el.tagName === "INPUT" || el.tagName === "SELECT"))
      .forEach((el) => el.addEventListener("input", render));

    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
