# Double Pendulum Simulation

A sophisticated physics simulation of a double pendulum system with real-time visualization and export capabilities. Built with Python, this project integrates numerical integration, interactive GUI controls, and professional-grade animations.

## Overview

This simulation accurately models the chaotic motion of a double pendulum system by solving the equations of motion using numerical integration. The application provides both a live visualization and the ability to export animations in multiple formats.

### Key Features

- **Real-time Simulation**: Watch the double pendulum evolve with live phase space visualization
- **Customizable Parameters**: Adjust masses, lengths, initial angles, and gravitational acceleration via intuitive sliders
- **Dual Visualization**: 
  - **Spatial View**: Real-time animation of the pendulum motion with position traces
  - **Phase Space View**: Angular phase space (θ₁ vs θ₂) representation for chaos analysis
- **Export Capabilities**: Save animations as high-quality MP4 videos or GIF files
- **High-Precision Integration**: Configurable error tolerances for accurate numerical solutions
- **Performance Optimized**: Frame rate limiting and intelligent trace windowing for smooth playback

## Technical Details

### Physics Model

The simulation solves the coupled differential equations of motion for a two-link pendulum system using the `scipy.integrate.solve_ivp` method with user-configurable tolerance levels (default: 10⁻¹³).

**System Parameters:**
- θ₁, θ₂: Angular positions of pendulum links
- l₁, l₂: Lengths of pendulum links
- m₁, m₂: Masses of pendulum bobs
- g: Gravitational acceleration

### Visualization Features

- **Position Traces**: Configurable 3-second motion history in the spatial view
- **Phase Space Mapping**: Automatic handling of angular discontinuities (±π wrapping)
- **Real-time Rendering**: 24 FPS target for smooth animation
- **Dual-Panel Display**: Side-by-side spatial and phase space views

## Requirements

```
matplotlib
numpy
scipy
pillow
imageio-ffmpeg
```

Install via:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python double_pendulum_sourcecode.py
```

This launches the interactive GUI where you can:

1. **Configure Simulation Parameters** using the sliders:
   - Mass 1 & 2 (1-5 kg)
   - Length 1 & 2 (0.1-3 m)
   - Gravitational Acceleration (0.5-20 m/s²)
   - Initial Angles (0-360°)

2. **Simulate** - View the live animation in real time

3. **Save Animation** - Export as MP4 (requires FFmpeg) or GIF format

### Example: Chaotic Motion

Set initial angles to non-zero values (e.g., θ₁ = 90°, θ₂ = 45°) to observe chaotic behavior in the phase space diagram.
![pendel12](https://github.com/user-attachments/assets/a6d2ad67-5b53-4fba-ae60-504314b37148)

## Performance Considerations

- The simulation includes matplotlib overhead; some latency is expected on initial render
- Frame rate is capped at 24 FPS for performance optimization
- Motion traces are limited to 3 seconds for real-time responsiveness
- Video export may require several moments depending on system specifications

## File Structure

- `double_pendulum_sourcecode.py` - Main application with GUI, physics engine, and visualization

## How It Works

1. **Physics Integration**: The `find_solution()` function computes the system trajectory using high-precision numerical integration from numpy's `solve_ivp()` function
2. **Animation Core**: The `animation()` function manages both live playback and video export with synchronized spatial and phase space visualization
3. **GUI Interface**: The `interface()` function provides an intuitive control panel for all simulation parameters

## Mathematical Foundation

The simulation solves the Lagrangian-derived equations of motion for a coupled pendulum system. The phase space visualization reveals the system's chaotic characteristics—sensitive dependence on initial conditions is a hallmark feature of this non-linear dynamical system.

## Export Formats

- **MP4**: High-quality video export (requires FFmpeg)
- **GIF**: Animated GIF format

## Author

Leo Barth
