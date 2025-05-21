// Remove keysToRemove, functions, and circular references from obj
export function cleanObject(obj, keysToRemove = [], seen = new WeakSet()) {
  if (obj === null || typeof obj !== "object") {
    return obj;
  }

  if (typeof value === "function") {
    return undefined;
  }

  if (seen.has(obj)) {
    return undefined;
  }

  seen.add(obj);

  if (Array.isArray(obj)) {
    return obj.map((item) => cleanObject(item, keysToRemove, seen));
  }

  return Object.fromEntries(
    Object.entries(obj)
      .filter(([key, value]) => !keysToRemove.includes(key) && typeof value !== "function" && !seen.has(value))
      .map(([key, value]) => [key, cleanObject(value, keysToRemove, seen)])
  );
}
