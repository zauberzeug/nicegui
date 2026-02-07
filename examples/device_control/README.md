# Device Control Example

Demonstrates how to control a device (lightbulb) using a class with events and UI bindings.
Shows patterns for connecting hardware or IoT devices to NiceGUI with real-time logging and autonomous behavior.

## Key Concepts

- **Events**: Device emits `power_changed`, `brightness_changed`, and `log_message` events
- **Property Setters**: Pythonic `lightbulb.power = True` and `lightbulb.brightness = 75`
- **Reactive UI**: UI subscribes to events and updates automatically
- **Autonomous Behavior**: Device logs heartbeat every 10 seconds when powered on
- **Clean Separation**: Device logic independent from UI code

## Usage

```python
# Create device
lightbulb = Lightbulb()

# Control via properties
lightbulb.power = True
lightbulb.brightness = 75

# Subscribe to events
lightbulb.power_changed.subscribe(on_power_changed)
lightbulb.log_message.subscribe(log.push)
```

## Running

```bash
python main.py
```

Turn on the lightbulb to see autonomous heartbeat logging.

## Use Cases

Ideal for IoT devices, smart home controls, industrial equipment, robotics, and hardware interfaces where you need event-driven communication between device logic and UI.
