function getPathPrefix() {
  return window.path_prefix || "";
}

function getCurrentPath() {
  return window.location.pathname + window.location.search + window.location.hash;
}

function stripPathPrefix(path) {
  const prefix = getPathPrefix();
  return prefix && path.startsWith(prefix) ? path.substring(prefix.length) : path;
}

function getCleanCurrentPath() {
  return stripPathPrefix(getCurrentPath());
}

function buildFullPath(cleanPath) {
  return getPathPrefix() + cleanPath;
}

function handleStateEvent(event) {
  const cleanPath = event.state?.page || getCleanCurrentPath();
  emitEvent("sub_pages_open", cleanPath);
}

function handleFragmentNavigation(href, targetUrl) {
  const fragmentName = targetUrl.hash.substring(1);
  const target = document.getElementById(fragmentName) || document.querySelector(`a[name="${fragmentName}"]`);
  if (!target) return false;

  target.scrollIntoView({ behavior: "smooth" });
  const cleanHref = stripPathPrefix(href);
  history.pushState({ page: cleanHref }, "", buildFullPath(cleanHref));
  return true;
}

window.addEventListener("popstate", handleStateEvent);
window.addEventListener("pushstate", handleStateEvent);

document.addEventListener("click", (e) => {
  const a = e.target.closest("a[href]");
  if (a && a.target !== "_blank" && !a.hasAttribute("download")) {
    const href = a.getAttribute("href");
    if (href.startsWith("/")) {
      e.preventDefault();

      const currentPath = getCleanCurrentPath();
      const targetUrl = new URL(href, window.location.origin);
      const targetPath = stripPathPrefix(targetUrl.pathname + targetUrl.search);

      // Handle same-page fragment navigation
      if (currentPath === targetPath && targetUrl.hash) {
        if (handleFragmentNavigation(href, targetUrl)) {
          return;
        }
      }

      // Regular page navigation
      emitEvent("sub_pages_navigate", stripPathPrefix(href));
    }
  }
});

export default {
  template: `<div><slot></slot></div>`,
};
