import imageio_ffmpeg
import matplotlib.pyplot as plt
import matplotlib.animation as mpl_animation
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.integrate import solve_ivp
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time

def derivatives(t, u_vec, l_1, l_2, m_1, m_2, g): # creating a footprint that's compatible with solve_ivp, i.e. the equations of motion
    u_1, u_2, u_3, u_4 = u_vec
    du1_dt = u_3
    du2_dt = u_4
    du3_dt = (g*m_1*np.sin(u_1) + g*m_2*np.sin(u_1)/2 + g*m_2*np.sin(u_1 - 2*u_2)/2 + l_1*m_2*u_3**2*np.sin(2*u_1 - 2*u_2)/2 + l_2*m_2*u_4**2*np.sin(u_1 - u_2))/(l_1*(-m_1 + m_2*np.cos(u_1 - u_2)**2 - m_2))
    du4_dt = (-g*m_1*np.sin(u_2) + g*m_1*np.sin(2*u_1 - u_2) - g*m_2*np.sin(u_2) + g*m_2*np.sin(2*u_1 - u_2) + 2*l_1*m_1*u_3**2*np.sin(u_1 - u_2) + 2*l_1*m_2*u_3**2*np.sin(u_1 - u_2) + l_2*m_2*u_4**2*np.sin(2*u_1 - 2*u_2))/(2*l_2*(m_1 - m_2*np.cos(u_1 - u_2)**2 + m_2))
    return np.array([du1_dt,du2_dt,du3_dt,du4_dt])

def find_solution(t_end, dt, theta1_0=0, theta2_0=0, l_1=1, l_2=1, m_1=1, m_2=1, g=9.8, error=10**(-13)):
    t_val = np.arange(0, t_end, dt)
    initial_state = [theta1_0, theta2_0, 0, 0] # [u_1, u_2, u_3, u_4] at t=0: I chose the starting velocities to be zero in all cases
    solution = solve_ivp(derivatives, [0, t_end], initial_state, t_eval=t_val, args=(l_1, l_2, m_1, m_2, g, ), rtol=error, atol=error)
    return [solution, dt, l_1, l_2, m_1, m_2]

def animation(sol, filename=None, root=None):
    solution, dt, l_1, l_2, m_1, m_2 = sol
    plot_max = l_1 + l_2 + 0.2
    
    # static properties of the plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), dpi=100)
    ax1.set_xlabel("x"), ax1.set_ylabel("y"), ax1.set_aspect("equal"), ax1.set_xlim(-plot_max, plot_max), ax1.set_ylim(-plot_max, plot_max), ax1.set_title("Simulation")
    ax2.set_xlabel("theta1"), ax2.set_ylabel("theta2"), ax2.set_aspect("equal"), ax2.set_xlim(-np.pi, np.pi), ax2.set_ylim(-np.pi, np.pi), ax2.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi]), ax2.set_yticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi]), ax2.set_xticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"]), ax2.set_yticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"]), ax2.set_title("Angular Phase Space")
    ax1.plot(0, 0, c="black", marker="o", markersize=3, zorder=2)
    
    # dynamic / animated properties
    time_text = ax1.text(0.05, 0.95, "", transform=ax1.transAxes, fontsize=12, verticalalignment="top", bbox=dict(boxstyle="round", facecolor="white", alpha=0.5))
    sim_trace, = ax1.plot([], [], c="red", alpha=0.4, markersize=3, zorder=1)
    sim_mass1, = ax1.plot([], [], c="blue", marker="o", markersize=3*m_1, zorder=2)
    sim_mass2, = ax1.plot([], [], c="red", marker="o", markersize=3*m_2, zorder=2)
    sim_lines, = ax1.plot([], [], c="black", linewidth=1, markevery=[0, 1, 2], zorder=1)
    aps_dot, = ax2.plot([], [], c="black", marker="o", markersize=3, zorder=2) # aps = APS = Angular Phase Space
    aps_trace, = ax2.plot([], [], c="black", alpha=0.4, markersize=3, zorder=1)
    
    theta1 = solution.y[0]
    theta2 = solution.y[1]
    x1 = l_1*np.sin(theta1)
    y1 = -l_1*np.cos(theta1)
    x2 = l_1*np.sin(theta1) + l_2*np.sin(theta2)
    y2 = -l_1*np.cos(theta1) - l_2*np.cos(theta2)
    
    trace_steps = int(3/dt) # limiting the trace to 3s and the fps to 24 for performance reasons
    target_fps = 24
    
    def update_data(index):
        start = max(0, index - trace_steps) # the start index for the tracing
        sim_trace.set_data(x2[start:index], y2[start:index])
        sim_lines.set_data([0, x1[index], x2[index]], [0, y1[index], y2[index]])
        sim_mass1.set_data([x1[index]], [y1[index]])
        sim_mass2.set_data([x2[index]], [y2[index]])
        aps_dot.set_data([(theta1[index] + np.pi) % (2*np.pi) - np.pi], [(theta2[index] + np.pi) % (2*np.pi) - np.pi])
        t1 = (theta1[start:index] + np.pi) % (2*np.pi) - np.pi
        t2 = (theta2[start:index] + np.pi) % (2*np.pi) - np.pi
        jump_indices = np.where((np.abs(np.diff(t1)) > np.pi) | (np.abs(np.diff(t2)) > np.pi))[0]
        t1_plot = np.insert(t1.astype(float), jump_indices + 1, np.nan)
        t2_plot = np.insert(t2.astype(float), jump_indices + 1, np.nan)
        aps_trace.set_data(t1_plot, t2_plot) # make sure the traces in the APS are mapped correctly
    
    if filename: # i.e. export / save mode
        popup = tk.Toplevel(root)
        popup.title("Saving...")
        popup.geometry("310x50")
        ttk.Label(popup, text="This may take a few moments...\nPlease note: Main window out of order until finished.").pack()
        popup.grab_set()
        root.update() # force the popup to be drawn before rendering the video file
        video_duration = solution.t[-1]
        total_frames = int(video_duration*target_fps)
        frame_indices = np.linspace(0, len(solution.t) - 1, total_frames).astype(int)
        
        def anim_export(frame):
            idx = frame
            if idx >= len(theta1):
                idx = len(theta1) - 1
            update_data(idx)
            time_text.set_text(f"Time: {solution.t[idx]:.2f}s")
            return sim_trace, sim_mass1, sim_mass2, sim_lines, aps_dot, aps_trace, time_text
        ani = FuncAnimation(fig, anim_export, frames=frame_indices, blit=True, cache_frame_data=False)
        
        try:
            if filename.lower().endswith(".mp4"):
                plt.rcParams["animation.ffmpeg_path"] = imageio_ffmpeg.get_ffmpeg_exe()
                if not mpl_animation.FFMpegWriter.isAvailable():
                    raise RuntimeError("FFmpeg-Writer is not available. Please install imageio-ffmpeg as listed in requirements.txt.")
                writer_to_use = "ffmpeg"
            elif filename.lower().endswith(".gif"):
                if not mpl_animation.PillowWriter.isAvailable():
                    raise RuntimeError("Pillow-Writer is not available. Please install pillow as listed in requirements.txt.")
                writer_to_use = "pillow"
            else:
                writer_to_use = None
            ani.save(filename, writer=writer_to_use, fps=target_fps)
            plt.close(fig)
            popup.destroy()
            messagebox.showinfo("Done!", f"The animation has been saved successfully!")
        except Exception as e:
            popup.destroy()
            messagebox.showerror("Error!", f"An error occurred when trying to save your animation: {e}")
    
    else: # i.e. live mode
        def anim_live(frame):
            global start_time
            if frame == 0:
                start_time = time.time()
            real_elapsed = time.time() - start_time
            if real_elapsed >= solution.t[-1]:
                start_time = time.time()
            idx = int(real_elapsed/dt) # downsampling in order to preserve "real" speed
            if idx >= len(theta1):
                idx = len(theta1) - 1
            update_data(idx)
            time_text.set_text(f"Time: {real_elapsed:.2f}s")
            return sim_trace, sim_mass1, sim_mass2, sim_lines, aps_dot, aps_trace, time_text
        ani = FuncAnimation(fig, anim_live, interval=10, blit=True, cache_frame_data=False)
        plt.tight_layout()
        plt.show()

def interface(): # Tkinter mainloop
    root = tk.Tk()
    ttk.Style().configure("TLabelframe.Label", font=("Helvetica", 10, "bold"))
    root.title("Double Pendulum Simulation")
    root.geometry("500x580")
    settings = ttk.LabelFrame(root, padding=10, text="Settings")
    settings.pack(fill=tk.X)
    
    def create_labeled_slider(parent, label_text, from_val, to_val, start_val):
        labelframe = ttk.LabelFrame(parent, text=label_text)
        labelframe.pack(side=tk.TOP, fill=tk.X, pady=2, expand=False)
        var = tk.DoubleVar(value=start_val)
        slider = ttk.LabeledScale(labelframe, from_=from_val, to=to_val, variable=var)
        slider.scale.configure(command=lambda value: slider.label.configure(text=round(float(value), 1)))
        var.set(start_val)
        slider.pack(padx=7, pady=0, fill=tk.X, expand=False)
        return slider
    m1_slider = create_labeled_slider(settings, "Mass 1 (kg)", 1, 5, 1)
    m2_slider = create_labeled_slider(settings, "Mass 2 (kg)", 1, 5, 1)
    l1_slider = create_labeled_slider(settings, "Length 1 (m)", 0.1, 3, 1)
    l2_slider = create_labeled_slider(settings, "Length 2 (m)", 0.1, 3, 1)
    g_slider  = create_labeled_slider(settings, "Gravitational Acceleration (m*s^-2)", 0.5, 20, 9.8)
    t1_slider = create_labeled_slider(settings, "Initial Angle 1 (deg)", 0, 360, 0)
    t2_slider = create_labeled_slider(settings, "Initial Angle 2 (deg)", 0, 360, 0)
    
    # button logic with helper function
    button_simulate = ttk.Button(settings, text="Simulate", command=lambda: animation(find_solution(15, 0.01, t1_slider.value/180*np.pi, t2_slider.value/180*np.pi, l1_slider.value, l2_slider.value, m1_slider.value, m2_slider.value, g_slider.value, 10**(-10))))
    button_simulate.pack()
    def save_to_file():
        path = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF-Animation", "*.gif"), ("Video-Datei", "*.mp4")])
        if path:
            animation(find_solution(15, 0.01, t1_slider.value/180*np.pi, t2_slider.value/180*np.pi, l1_slider.value, l2_slider.value, m1_slider.value, m2_slider.value, g_slider.value, 10**(-10)), filename=path, root=root)
    button_save = ttk.Button(settings, text="Save Animation", command=save_to_file)
    button_save.pack()
    
    def on_closing():
        plt.close("all")
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing) # ensuring correct termination upon closing
    root.mainloop()

interface() # starting the interface mainloop

# When running the simulation, it has a little bit of latency, at least on my PC. This can, for the most part, be attributed to matplotlib's overhead in drawing. In an effort to reduce this latency, I have implemented blitting in the FuncAnimation function, and am reducing the amount of points being plotted for the traces, as well as downsampling the drawn steps in accordance to python's real-time clock. When saving the simulation as a video (either mp4- or GIF-formatted), it seemed to have no serious measurable latency.