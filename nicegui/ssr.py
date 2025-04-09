import json
from pathlib import Path
import subprocess
from nodejs_wheel import node, npm

import uuid

cwd = Path(__file__).parent

print("cwd", cwd)

package_json = cwd / 'package.json'

quasar_path = cwd / 'node_modules' / 'quasar' / 'dist' / 'quasar.server.prod.js'


def write_js_script(uuid: str, elements_string: str) -> None:
    """Write the JavaScript script to a file."""
    script = """
// this runs in Node.js on the server.
import { createSSRApp, withModifiers, withKeys, resolveComponent, h } from 'vue'
// Vue's server-rendering API is exposed under `vue/server-renderer`.
import { renderToString } from 'vue/server-renderer'
// Quasar is a Vue.js framework for building responsive web applications.
// @ts-ignore
import { Quasar } from 'quasar'

const True = true;
const False = false;
const None = undefined;

const loaded_libraries = new Set();
const loaded_components = new Set();

function parseElements(raw_elements) {
  return JSON.parse(
    raw_elements
      .replace(/&#36;/g, "$")
      .replace(/&#96;/g, "`")
      .replace(/&gt;/g, ">")
      .replace(/&lt;/g, "<")
      .replace(/&amp;/g, "&")
  );
}

function replaceUndefinedAttributes(element) {
  element.class ??= [];
  element.style ??= {};
  element.props ??= {};
  element.text ??= null;
  element.events ??= [];
  element.update_method ??= null;
  element.component ??= null;
  element.libraries ??= [];
  element.slots = {
    default: { ids: element.children || [] },
    ...(element.slots ?? {}),
  };
}

function renderRecursively(elements, id) {
  const element = elements[id];
  if (element === undefined) {
    return;
  }

  // @todo: Try avoid this with better handling of initial page load.
  if (element.component) loaded_components.add(element.component.name);
  element.libraries.forEach((library) => loaded_libraries.add(library.name));

  const props = {
    id: "c" + id,
    ref: "r" + id,
    key: id, // HACK: workaround for #600 and #898
    class: element.class.join(" ") || undefined,
    style: Object.entries(element.style).reduce((str, [p, val]) => `${str}${p}:${val};`, "") || undefined,
    ...element.props,
  };
  Object.entries(props).forEach(([key, value]) => {
    if (key.startsWith(":")) {
      try {
        try {
          props[key.substring(1)] = new Function(`return (${value})`)();
        } catch (e) {
          props[key.substring(1)] = eval(value);
        }
        delete props[key];
      } catch (e) {
        console.error(`Error while converting ${key} attribute to function:`, e);
      }
    }
  });
  element.events.forEach((event) => {
    let event_name = "on" + event.type[0].toLocaleUpperCase() + event.type.substring(1);
    event.specials.forEach((s) => (event_name += s[0].toLocaleUpperCase() + s.substring(1)));

    let handler;
    if (event.js_handler) {
      handler = eval(event.js_handler);
    } else {
      handler = (...args) => {
        const emitter = () =>
          window.socket?.emit("event", {
            id: id,
            client_id: window.clientId,
            listener_id: event.listener_id,
            args: stringifyEventArgs(args, event.args),
          });
        const delayed_emitter = () => {
          if (window.did_handshake) emitter();
          else setTimeout(emitter, 10);
        };
        throttle(delayed_emitter, event.throttle, event.leading_events, event.trailing_events, event.listener_id);
        if (element.props["loopback"] === False && event.type == "update:modelValue") {
          element.props["model-value"] = args;
        }
      };
    }

    handler = withModifiers(handler, event.modifiers);
    handler = event.keys.length ? withKeys(handler, event.keys) : handler;
    if (props[event_name]) {
      props[event_name].push(handler);
    } else {
      props[event_name] = [handler];
    }
  });
  const slots = {};
  const element_slots = {
    default: { ids: element.children || [] },
    ...element.slots,
  };
  Object.entries(element_slots).forEach(([name, data]) => {
    slots[name] = (props) => {
      const rendered = [];
      if (data.template) {
        rendered.push(
          h(
            {
              props: { props: { type: Object, default: {} } },
              template: data.template,
            },
            {
              props: props,
            }
          )
        );
      }
      const children = data.ids.map((id) => renderRecursively(elements, id));
      if (name === "default" && element.text !== null) {
        children.unshift(element.text);
      }
      return [...rendered, ...children];
    };
  });
  return h(resolveComponent(element.tag), props, slots);
}

const elements = parseElements(String.raw`ELEMENTS_GO_HERE`)

Object.entries(elements).forEach(([_, element]) => replaceUndefinedAttributes(element));

const app = createSSRApp({
  data() {
    return {
      elements,
    };
  },
  render() {
    return renderRecursively(elements, 0);
  },
});

app.use(Quasar, {});



renderToString(app).then((html) => {
  console.log(html)
})
"""
    script = script.replace('ELEMENTS_GO_HERE', elements_string, 1)
    with open(cwd / f'ssr_{uuid}.js', 'w') as file:
        file.write(script)


def delete_js_script(uuid: str) -> None:
    """Delete the JavaScript script file."""
    script_path = cwd / f'ssr_{uuid}.js'
    if script_path.exists():
        script_path.unlink()
        print(f'Deleted {script_path}')
    else:
        print(f'{script_path} does not exist')


def ensure_npm_init() -> None:
    """Check if npm is initialized in the current directory."""
    if package_json.exists():
        print('npm already initialized')
    else:
        print('npm not initialized')
        npm(['init', '-y'], cwd=cwd)


def check_npm_install() -> None:
    """Check if npm packages are installed in the current directory."""
    ensure_npm_init()  # make a call to the lower-level check

    def npm_install() -> None:
        npm(['install', 'vue@3.4.38', 'quasar@2.16.9'], cwd=cwd)

    with open(package_json, 'r') as file:
        package_data = json.load(file)
    for package in ['vue', 'quasar']:
        if package in package_data.get('dependencies', {}):
            print(f'{package} already installed')
        else:
            print("Did not install the required packages")
            npm_install()
            break

    if not quasar_path.exists():
        print('quasar.server.prod.js does not exist. This is strange but we will try again.')
        npm_install()

        if not quasar_path.exists():
            print('quasar.server.prod.js still does not exist. This is a critical error.')
            raise FileNotFoundError(f'{quasar_path} does not exist. Please check your installation.')


def ensure_type_module() -> None:
    """Check if the type module is set in package.json."""
    check_npm_install()  # make a call to the lower-level check

    with open(package_json, 'r') as file:
        package_data = json.load(file)
    if 'type' in package_data:
        print('Type module already set')
    else:
        print('Setting type module')
        package_data['type'] = 'module'
        with open(package_json, 'w') as file:
            json.dump(package_data, file, indent=4)


def ensure_patch_quasar() -> None:
    """Check if quasar is patched."""
    ensure_type_module()  # make a call to the lower-level check

    with open(quasar_path, 'r') as file:
        quasar_data = file.read()
    if '// modified by ssr.py' in quasar_data:
        print('quasar.server.prod.js already patched')
    else:
        print('Patching quasar.server.prod.js')
        quasar_data = quasar_data.replace(
            'e.req.headers["user-agent"]||e.req.headers["User-Agent"]', 'e.req?.headers["user-agent"]||e.req?.headers["User-Agent"]')
        quasar_data = quasar_data.replace('e,t={},o', 'e,t={},o={}')
        quasar_data += '\n// modified by ssr.py'
        with open(quasar_path, 'w') as file:
            file.write(quasar_data)


def get_ssr_output(elements_string: str) -> str:
    """Get the SSR output."""
    unique_id = str(uuid.uuid4())  # Generate a random UUID
    write_js_script(unique_id, elements_string)
    result = node([f'ssr_{unique_id}.js'], cwd=cwd, return_completed_process=True,
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        print("Error:", result.stderr.decode('utf-8').strip())
    print(result)
    output = result.stdout.decode('utf-8').strip()
    delete_js_script(unique_id)
    return output


ensure_patch_quasar()

if __name__ == '__main__':
    elements_input = input('Enter elements string: ')
    print(get_ssr_output(elements_input))
