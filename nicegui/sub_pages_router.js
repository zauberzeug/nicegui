window.addEventListener("popstate", (event) =>
  emitEvent("open", event.state?.page || window.location.pathname + window.location.search + window.location.hash)
);
window.addEventListener("pushstate", (event) =>
  emitEvent("open", event.state?.page || window.location.pathname + window.location.search + window.location.hash)
);
document.addEventListener("click", (e) => {
  const a = e.target.closest("a[href]");
  if (a && a.target !== "_blank" && !a.hasAttribute("download")) {
    const href = a.getAttribute("href");
    if (href.startsWith("/")) {
      e.preventDefault();

      const currentPath = window.location.pathname + window.location.search + window.location.hash;
      const targetUrl = new URL(href, window.location.origin);
      const targetPath = targetUrl.pathname + targetUrl.search;

      if (currentPath === targetPath && targetUrl.hash) {
        // Same page, different fragment - handle directly
        const fragmentName = targetUrl.hash.substring(1);
        let target = document.getElementById(fragmentName);
        if (!target) {
          target = document.querySelector(`a[name="${fragmentName}"]`);
        }
        if (target) {
          target.scrollIntoView({ behavior: "smooth" });
          // Update URL without triggering page reload
          history.pushState({ page: href }, "", (window.path_prefix || "") + href);
          return;
        }
      }

      emitEvent("navigate", href);
    }
  }
});
console.log("SubPagesRouter initialized");
