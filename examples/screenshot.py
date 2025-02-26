import os
import signal
import subprocess
import time
from pathlib import Path

from selenium import webdriver


running_processes = []


def find_main_py_files():
    """Find all `main.py` files in subdirectories."""
    return [str(path) for path in Path('.').rglob('*/main.py')]

def take_screenshot(url, save_path):
    """Capture a screenshot of the web page."""
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        time.sleep(2)  # Ensure the page is fully loaded
        driver.save_screenshot(save_path)
        print(f"Screenshot saved to {save_path}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

def run_example_and_capture_screenshot(main_py_path):
    """Run the NiceGUI app, take a screenshot, and stop the process."""
    example_dir = os.path.dirname(main_py_path)
    print(f"Processing: {example_dir}")

    # Start NiceGUI application
    process = subprocess.Popen(
        ["poetry", "run", "python", "main.py"],
        cwd=example_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    running_processes.append(process)

    # Wait for the web page to be available
    time.sleep(5)

    # Capture screenshot
    take_screenshot("http://0.0.0.0:8080", os.path.join(example_dir, "screenshot.png"))

    # Terminate the process
    process.terminate()
    process.wait()
    running_processes.remove(process)
    print(f"Finished processing: {example_dir}\n")

def cleanup(signum, frame):
    """Ensure all running processes are terminated on interruption."""
    print("Interrupt received, terminating running processes...")
    for process in running_processes:
        process.terminate()
        process.wait()
    exit(0)

def main():
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    main_py_files = find_main_py_files()
    if not main_py_files:
        print("No examples found!")
        return

    for main_py in main_py_files:
        run_example_and_capture_screenshot(main_py)

if __name__ == "__main__":
    main()