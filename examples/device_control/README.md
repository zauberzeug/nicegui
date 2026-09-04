# Device Control

Demonstrate how to control an IoT device like a lightbulb.
The dashboard UI is bound to the device's properties and events, allowing real-time interaction and logging.

![Screenshot](screenshot.webp)

## Key Concepts

- **Events**: Device emits `power_changed`, `brightness_changed`, and `log_message` events
- **Properties**: Pythonic read and write access, `lightbulb.power = True` and `lightbulb.brightness = 75`
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
lightbulb.power_changed.subscribe(handle_power_change)
lightbulb.log_message.subscribe(log.push)
```

## Running

```bash
python main.py
```

Turn on the lightbulb to see autonomous heartbeat logging.

## Use Cases

Ideal for IoT devices, smart home controls, industrial equipment, robotics, and hardware interfaces
where you need event-driven communication between device logic and UI.
