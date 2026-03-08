# Task 1: Relax Your Eyes

## Overview
This application monitors eye fatigue by tracking user activity (keyboard and mouse input) and enforces break times by locking the screen. It is designed to help users maintain healthy computer usage habits by ensuring they take regular breaks.

## Features
- **Input Monitoring**: continuously tracks keyboard and mouse usage to calculate active time.
- **Smart Warnings**: Displays a countdown warning modal when usage limits are reached.
- **Screen Locking**: Automatically triggers the operating system's built-in lock screen to force a break.
- **Configuration**: Fully customizable settings via `config.yaml`.

## Configuration
Before running the application, you can customize the behavior by editing the `config.yaml` file located in the project root.

### Key Settings
The `usage_monitor` section controls the core logic:

- **`max_continuous_usage_seconds`**: The maximum amount of time (in seconds) you can work continuously before a break is enforced. 
  - *Example*: `1200` (20 minutes).
- **`idle_threshold_seconds`**: The duration of inactivity (in seconds) required to consider it a "break". If you stop using the computer for this long, the usage timer resets.
  - *Example*: `60` (1 minute).
- **`warning_duration_seconds`**: How long the warning countdown lasts before the screen locks.
  - *Example*: `10` (10 seconds).

### Example `config.yaml`
```yaml
usage_monitor:
  max_continuous_usage_seconds: 1200 # 20 minutes working time
  idle_threshold_seconds: 60        # 1 minute break resets the timer
  warning_duration_seconds: 10      # 10s countdown before lock
```

## How It Works
1.  **Monitoring**: The application runs in the background and listens for any keyboard or mouse events.
2.  **Tracking**: It calculates the duration of "continuous usage". If you stop typing or moving the mouse for longer than the `idle_threshold_seconds`, the timer resets, acknowledging that you took a break.
3.  **Warning**: Once your continuous usage exceeds the `max_continuous_usage_seconds`, a modal window pops up at the top of your screen.
4.  **Locking**: The modal displays a countdown. When it reaches zero, the application triggers the **operating system's built-in lock screen** (e.g., Windows Lock or macOS Login Screen). We do not use a custom lock screen implementation; we rely on the secure, native OS capability to ensure privacy and security.

## Usage
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the application from the project root:
    ```bash
    python3 T1-RelaxYourEyes/main.py
    ```

## Future Roadmap
We are planning to introduce a gamified credit system to encourage better habits:

1.  **Personalized Strategy**
    *   **Goal**: Ensure users actually take a break after the screen locks.
    *   **Mechanism**: If a user immediately unlocks the computer and resumes work without taking the required break, the system will detect this "cheating" behavior and deduct credits.

2.  **Daily Credit System**
    *   **Concept**: Users start each day with **100 credits**.
    *   **Rules**:
        *   **Keep Credits**: Work continuously for the set duration (e.g., 30 mins) and then take a valid break (e.g., 5 mins).
        *   **Lose Credits**: Immediately log back in after a forced lock, ignoring the break time. This "hurts your eyes" and reduces your daily score.

3.  **Progress Visualization**
    *   **Feature**: Visual charts and marks to track performance over time.
    *   **Insight**: Users will be able to see their daily credit trends, highlighting how often they obeyed the rules versus how often they skipped breaks.
