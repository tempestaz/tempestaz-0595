# How It All Fits Together

## Idle events:

When idle, Klipper runs IDLE_SLEEP.

On wake (restart or reconnect), Moonraker watcher triggers WAKE_UP.

## System events:
* "ready" → WAKE_UP
* "shutdown" → PRINTER_SHUTDOWN
* "error" → PRINTER_ERROR
* "startup" → PRINTER_STARTUP
* "disconnected" → PRINTER_DISCONNECTED

This gives you a full sleep/wake cycle plus graceful handling of failures.



1. Create the Watcher Script

Let’s say the script is stored at /home/pi/klipper-watcher.py.

2. Create the systemd Service File

Create a new systemd service file to run the script as a background service:

sudo nano /etc/systemd/system/klipper-watcher.service

3. Reload systemd and Enable the Service

To reload systemd, enable the service to start on boot, and then start it:

# Reload systemd to register the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable klipper-watcher.service

# Start the service right now
sudo systemctl start klipper-watcher.service

4. Check the Service Status

To make sure the service is running properly, check its status with:

sudo systemctl status klipper-watcher.service

This should show that the service is active and running.

5. View Logs (If Needed)

You can also view the logs of the service by running:

sudo journalctl -u klipper-watcher.service -f