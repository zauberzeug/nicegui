export function convertDynamicProperties(obj, recursive) {
  if (typeof obj !== "object" || obj === null) {
    return;
  }
  if (Array.isArray(obj)) {
    if (recursive) {
      obj.forEach((v) => convertDynamicProperties(v, true));
    }
    return;
  }
  for (const [attr, value] of Object.entries(obj)) {
    if (attr.startsWith(":")) {
      try {
        try {
          obj[attr.slice(1)] = new Function(`return (${value})`)();
        } catch (e) {
          obj[attr.slice(1)] = eval(value);
        }
        delete obj[attr];
      } catch (e) {
        console.error(`Error while converting ${attr} attribute to function:`, e);
      }
    } else {
      if (recursive) {
        convertDynamicProperties(value, true);
      }
    }
  }
}
