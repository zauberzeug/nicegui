export function recursive_has_dynamic(obj) {
  if (typeof obj !== "object" || obj === null) return false;
  if (Array.isArray(obj)) {
    return obj.some((v) => recursive_has_dynamic(v));
  }
  for (const [key, value] of Object.entries(obj)) {
    if (key.startsWith(":")) return true;
    if (recursive_has_dynamic(value)) {
      return true;
    }
  }
  return false;
}

export function recursive_convert_dynamic(obj) {
  if (!recursive_has_dynamic(obj)) return obj; // double-loop hierarchy is probably safer and uses less RAM if dynamic not used
  if (typeof obj !== "object" || obj === null) return obj;
  if (Array.isArray(obj)) {
    return obj.map((v) => recursive_convert_dynamic(v));
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
      targetObj[attr] = recursive_convert_dynamic(value);
    }
  }
  return targetObj;
}
