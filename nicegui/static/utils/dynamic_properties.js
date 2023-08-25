export function hasDynamicProperties(obj) {
  if (typeof obj !== "object" || obj === null) return false;
  if (Array.isArray(obj)) {
    return obj.some((v) => hasDynamicProperties(v));
  }
  for (const [key, value] of Object.entries(obj)) {
    if (key.startsWith(":")) {
      return true;
    }
    if (hasDynamicProperties(value)) {
      return true;
    }
  }
  return false;
}

export function convertDynamicProperties(obj) {
  if (!hasDynamicProperties(obj)) {
    // double-loop hierarchy is probably safer and uses less RAM if dynamic not used
    return obj;
  }
  if (typeof obj !== "object" || obj === null) {
    return obj;
  }
  if (Array.isArray(obj)) {
    return obj.map((v) => convertDynamicProperties(v));
  }
  const targetObj = {};
  for (const [attr, value] of Object.entries(obj)) {
    if (attr.startsWith(":")) {
      try {
        targetObj[attr.slice(1)] = new Function("return " + value)();
      } catch (e) {
        console.error(`Error while converting ${attr} attribute to function:`, e);
      }
    } else {
      targetObj[attr] = convertDynamicProperties(value);
    }
  }
  return targetObj;
}
