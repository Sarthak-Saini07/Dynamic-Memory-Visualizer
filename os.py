import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from collections import deque

class MemoryVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Visualizer")
        
        self.frame_label = tk.Label(root, text="Number of Frames:")
        self.frame_label.pack()
        
        self.frame_entry = tk.Entry(root)
        self.frame_entry.pack()
        
        self.ref_label = tk.Label(root, text="Reference String (comma-separated):")
        self.ref_label.pack()
        
        self.ref_entry = tk.Entry(root)
        self.ref_entry.pack()
        
        self.algo_label = tk.Label(root, text="Choose Algorithm:")
        self.algo_label.pack()
        
        self.algo_var = tk.StringVar(value="FIFO")
        self.fifo_radio = tk.Radiobutton(root, text="FIFO", variable=self.algo_var, value="FIFO")
        self.fifo_radio.pack()
        self.lru_radio = tk.Radiobutton(root, text="LRU", variable=self.algo_var, value="LRU")
        self.lru_radio.pack()
        
        self.run_button = tk.Button(root, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack()
        
    def run_simulation(self):
        try:
            num_frames = int(self.frame_entry.get())
            ref_string = list(map(int, self.ref_entry.get().split(',')))
            algo = self.algo_var.get()
            
            if algo == "FIFO":
                page_faults = self.fifo_algorithm(num_frames, ref_string)
            else:
                page_faults = self.lru_algorithm(num_frames, ref_string)
            
            messagebox.showinfo("Simulation Complete", f"Total Page Faults: {page_faults}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
    
    def fifo_algorithm(self, capacity, reference_string):
        frames = deque()
        page_faults = 0
        history = []
        
        for page in reference_string:
            if page not in frames:
                if len(frames) == capacity:
                    frames.popleft()
                frames.append(page)
                page_faults += 1
            history.append(list(frames))
        
        self.visualize(reference_string, history)
        return page_faults
    
    def lru_algorithm(self, capacity, reference_string):
        frames = []
        page_faults = 0
        history = []
        
        for page in reference_string:
            if page not in frames:
                if len(frames) == capacity:
                    frames.pop(0)
                frames.append(page)
                page_faults += 1
            else:
                frames.remove(page)
                frames.append(page)
            history.append(list(frames))
        
        self.visualize(reference_string, history)
        return page_faults
    
    def visualize(self, reference_string, history):
        plt.figure(figsize=(10, 5))
        
        for i, frame_state in enumerate(history):
            plt.scatter([i] * len(frame_state), frame_state, label=f"Step {i}" if i == 0 else "")
        
        plt.plot(range(len(reference_string)), reference_string, "ro--", label="Reference String")
        plt.xlabel("Time Steps")
        plt.ylabel("Page Numbers")
        plt.title("Memory Page Replacement Visualization")
        plt.legend()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryVisualizer(root)
    root.mainloop()
