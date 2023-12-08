const resourceLoadPromises = {};

export function loadResource(url) {
  if (resourceLoadPromises[url]) return resourceLoadPromises[url];
  const loadPromise = new Promise((resolve, reject) => {
    const dataAttribute = `data-${url.split("/").pop().replace(/\./g, "-")}`;
    if (document.querySelector(`[${dataAttribute}]`)) {
      resolve();
      return;
    }
    let element;
    if (url.endsWith(".css")) {
      element = document.createElement("link");
      element.setAttribute("rel", "stylesheet");
      element.setAttribute("href", url);
    } else if (url.endsWith(".js")) {
      element = document.createElement("script");
      element.setAttribute("src", url);
    }
    element.setAttribute(dataAttribute, "");
    document.head.appendChild(element);
    element.onload = resolve;
    element.onerror = reject;
  });
  resourceLoadPromises[url] = loadPromise;
  return loadPromise;
}
