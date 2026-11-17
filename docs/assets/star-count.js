(function () {
  "use strict";
  if (window.location.protocol === "file:") return;
  const CACHE_KEY = "ppc_gh_stars";
  const API_URL = "https://api.github.com/repos/fintech-infrastructure/payment-processing-comparison";

  function applyCount(count) {
    if (!Number.isFinite(count) || count <= 0) return;
    document.querySelectorAll("[data-gh-stars-text]").forEach((el) => {
      el.textContent = `Star on GitHub (${count.toLocaleString("en-US")})`;
    });
  }

  try {
    const cached = sessionStorage.getItem(CACHE_KEY);
    if (cached !== null) {
      applyCount(Number(cached));
      return;
    }
  } catch (_) {}

  fetch(API_URL)
    .then((r) => (r.ok ? r.json() : null))
    .then((data) => {
      if (data && typeof data.stargazers_count === "number") {
        try {
          sessionStorage.setItem(CACHE_KEY, String(data.stargazers_count));
        } catch (_) {}
        applyCount(data.stargazers_count);
      }
    })
    .catch(() => {});
})();
