export function convertDynamicProperties(obj) {
  if (typeof obj !== "object" || obj === null) {
    return;
  }
  if (Array.isArray(obj)) {
    obj.forEach((v) => convertDynamicProperties(v));
    return;
  }
  for (const [attr, value] of Object.entries(obj)) {
    if (attr.startsWith(":")) {
      try {
        obj[attr.slice(1)] = new Function("return " + value)();
        delete obj[attr];
      } catch (e) {
        console.error(`Error while converting ${attr} attribute to function:`, e);
      }
    } else {
      convertDynamicProperties(value);
    }
  }
}
