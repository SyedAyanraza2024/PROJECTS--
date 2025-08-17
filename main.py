import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from algorithms import fcfs, sstf, scan, look, cscan, clook

# Algorithm router
def run_algorithm(algorithm, requests, head):
    if algorithm == "FCFS":
        return fcfs(requests, head)
    elif algorithm == "SSTF":
        return sstf(requests, head)
    elif algorithm == "SCAN":
        return scan(requests, head)
    elif algorithm == "LOOK":
        return look(requests, head)
    elif algorithm == "C-SCAN":
        return cscan(requests, head)
    elif algorithm == "C-LOOK":
        return clook(requests, head)
    else:
        raise NotImplementedError(f"Algorithm {algorithm} not implemented")

def plot_sequence(sequence, algorithm_name):
    plt.plot(range(len(sequence)), sequence, marker='o', linestyle='-', label=algorithm_name)

def animate_sequence(sequences):
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['#4CAF50', '#2196F3', '#FF5722', '#9C27B0', '#FFC107', '#009688']
    lines = []
    labels = list(sequences.keys())

    for idx, (label, seq) in enumerate(sequences.items()):
        line, = ax.plot([], [], marker='o', linestyle='-', color=colors[idx % len(colors)], label=label)
        lines.append((line, seq))

    ax.set_xlim(0, max(len(seq) for _, seq in lines) - 1)
    all_y = [y for _, seq in lines for y in seq]
    ax.set_ylim(min(all_y) - 10, max(all_y) + 10)
    ax.set_title("Disk Scheduling Comparison", fontsize=14)
    ax.set_xlabel("Step", fontsize=12)
    ax.set_ylabel("Cylinder", fontsize=12)
    ax.grid(True)
    ax.legend()

    def update(frame):
        for line, seq in lines:
            if frame < len(seq):
                line.set_data(range(frame + 1), seq[:frame + 1])
        return [line for line, _ in lines]

    ani = animation.FuncAnimation(fig, update, frames=max(len(seq) for _, seq in lines), interval=500, repeat=False)
    plt.tight_layout()
    plt.show()

class DiskSchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scheduling Visualizer")
        self.root.geometry("500x380")
        self.root.configure(bg="#1e1e2f")  #background color
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#1e1e2f", foreground="white", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, background="#7289da", foreground="white")
        style.map("TButton", background=[('active', '#5b6eae')])
        style.configure("TCheckbutton", background="#1e1e2f", foreground="white")

        title = tk.Label(self.root, text="Disk Scheduling Visualization", font=("Segoe UI", 16, "bold"), bg="#1e1e2f", fg="white")
        title.pack(pady=10)

        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Disk Requests:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.requests_entry = ttk.Entry(frame, width=35)
        self.requests_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Head Position:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.head_entry = ttk.Entry(frame, width=35)
        self.head_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Algorithm:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.algorithm_var = tk.StringVar()
        self.algorithm_dropdown = ttk.Combobox(frame, textvariable=self.algorithm_var, state="readonly", width=33)
        self.algorithm_dropdown['values'] = ("FCFS", "SSTF", "SCAN", "LOOK", "C-SCAN", "C-LOOK")
        self.algorithm_dropdown.current(0)
        self.algorithm_dropdown.grid(row=2, column=1, padx=5, pady=5)

        # Combine checkbox and label in one frame
        check_frame = tk.Frame(self.root, bg="#1e1e2f")
        check_frame.pack(pady=5)

        self.compare_var = tk.BooleanVar()
        self.check_btn = tk.Checkbutton(check_frame, variable=self.compare_var, bg="#1e1e2f", activebackground="#1e1e2f")
        self.check_btn.pack(side="left")

        self.check_label = tk.Label(check_frame, text="Compare All Algorithms", bg="#1e1e2f", fg="white", font=("Segoe UI", 10))
        self.check_label.pack(side="left")

        self.check_label.bind("<Enter>", lambda e: self.check_label.config(fg="#00ffff"))
        self.check_label.bind("<Leave>", lambda e: self.check_label.config(fg="white"))
        self.check_label.bind("<Button-1>", lambda e: self.toggle_check())

        run_button = ttk.Button(self.root, text="Visualize", command=self.run_visualization)
        run_button.pack(pady=10)

    def toggle_check(self):
        self.compare_var.set(not self.compare_var.get())
        self.check_btn.select() if self.compare_var.get() else self.check_btn.deselect()

    def run_visualization(self):
        try:
            requests = list(map(int, self.requests_entry.get().split(',')))
            head = int(self.head_entry.get())

            if self.compare_var.get():
                algorithms = ["FCFS", "SSTF", "SCAN", "LOOK", "C-SCAN", "C-LOOK"]
                sequences = {}
                for algo in algorithms:
                    seq, _ = run_algorithm(algo, requests.copy(), head)
                    sequences[algo] = seq
                animate_sequence(sequences)
            else:
                algorithm = self.algorithm_var.get()
                sequence, seek_time = run_algorithm(algorithm, requests, head)
                plt.figure(figsize=(10, 5))
                plot_sequence(sequence, algorithm)
                plt.title(f"{algorithm} Disk Scheduling", fontsize=14)
                plt.xlabel("Operation Step", fontsize=12)
                plt.ylabel("Cylinder Number", fontsize=12)
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.tight_layout()
                plt.legend()
                plt.show()
                messagebox.showinfo("Result", f"Total Seek Time: {seek_time}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskSchedulingApp(root)
    root.mainloop()
