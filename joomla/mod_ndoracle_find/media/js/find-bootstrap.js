/* ND ORACLE. Browser-local discovery reuses the unchanged, reviewed
 * v1.1 Find evaluator. Only the static index and evaluator JS are fetched,
 * never a query, answer, personal input or search history.
 */
(() => {
  "use strict";
  const initialise = async () => {
    const input = document.getElementById("find-input");
    const button = document.getElementById("find-button");
    const output = document.getElementById("find-results");
    if (!input || !button || !output) return;
    button.disabled = true;
    output.textContent = "Preparing browser-local discovery…";
    try {
      const response = await fetch("/media/ndoracle/find-index.json", {
        method:"GET", credentials:"same-origin", cache:"force-cache"
      });
      if (!response.ok) throw new Error("Discovery catalogue unavailable");
      const data = await response.json();
      if (data?.policy?.version !== "1.1" || !Array.isArray(data.index) ||
          data.index.length !== 363) {
        throw new Error("Unexpected discovery catalogue");
      }
      const template = document.createElement("template");
      template.id = "search-index";
      template.content.textContent = JSON.stringify(data);
      document.body.appendChild(template);
      const script = document.createElement("script");
      script.src = "/media/ndoracle/find.js";
      script.onload = () => {
        output.textContent = "Results will appear here. Relevance is not a personal recommendation.";
        button.disabled = false;
      };
      script.onerror = () => {
        output.textContent = "Browser-local discovery could not start. You can still browse Questions or A–Z.";
      };
      document.head.appendChild(script);
    } catch (error) {
      output.textContent = "Browser-local discovery could not start. Use Questions, Browse by need, or the A–Z.";
    }
  };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialise, {once:true});
  } else {
    initialise();
  }
})();
