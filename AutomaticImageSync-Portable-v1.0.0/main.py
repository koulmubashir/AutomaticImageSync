try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
except ImportError:
    print("❌ Error: tkinter is not available on this system.")
    print("🔧 Please use the command-line version instead:")
    print("   python cli.py <folder1> <folder2> <output_folder>")
    print("   Example: python cli.py ./images1 ./images2 ./organized")
    print("   Use --help for more options")
    exit(1)

from pathlib import Path
import threading
from image_processor import ImageSynchronizer


class ImageSyncGUI:
    """GUI application for automatic image synchronization"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Automatic Image Sync - Advanced Image Organization")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.folder1_path = tk.StringVar()
        self.folder2_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        # Synchronizer
        self.synchronizer = None
        self.processing_thread = None
        
        self.setup_ui()
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Automatic Image Synchronizer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Folder selection section
        folder_frame = ttk.LabelFrame(main_frame, text="Folder Selection", padding="10")
        folder_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        folder_frame.columnconfigure(1, weight=1)
        
        # Folder 1
        ttk.Label(folder_frame, text="Folder 1:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(folder_frame, textvariable=self.folder1_path, width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=5)
        ttk.Button(folder_frame, text="Browse", 
                  command=lambda: self.browse_folder(self.folder1_path)).grid(
            row=0, column=2, pady=5)
        
        # Folder 2
        ttk.Label(folder_frame, text="Folder 2:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(folder_frame, textvariable=self.folder2_path, width=50).grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=5)
        ttk.Button(folder_frame, text="Browse", 
                  command=lambda: self.browse_folder(self.folder2_path)).grid(
            row=1, column=2, pady=5)
        
        # Output folder
        ttk.Label(folder_frame, text="Output Folder:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(folder_frame, textvariable=self.output_path, width=50).grid(
            row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=5)
        ttk.Button(folder_frame, text="Browse", 
                  command=lambda: self.browse_folder(self.output_path, is_output=True)).grid(
            row=2, column=2, pady=5)
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Similarity threshold
        ttk.Label(options_frame, text="Similarity Threshold:").grid(row=0, column=0, sticky=tk.W)
        self.similarity_var = tk.DoubleVar(value=0.85)
        similarity_scale = ttk.Scale(options_frame, from_=0.5, to=0.99, 
                                   variable=self.similarity_var, orient=tk.HORIZONTAL)
        similarity_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        self.similarity_label = ttk.Label(options_frame, text="0.85")
        self.similarity_label.grid(row=0, column=2)
        
        # Update similarity label
        def update_similarity_label(*args):
            self.similarity_label.config(text=f"{self.similarity_var.get():.2f}")
        
        self.similarity_var.trace_add('write', update_similarity_label)
        options_frame.columnconfigure(1, weight=1)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 20))
        
        self.start_button = ttk.Button(button_frame, text="Start Synchronization", 
                                     command=self.start_sync, style="Accent.TButton")
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="Stop", 
                                    command=self.stop_sync, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Clear All", 
                                     command=self.clear_all)
        self.clear_button.pack(side=tk.LEFT)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        progress_frame.columnconfigure(0, weight=1)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to start...")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Results text area
        self.results_text = tk.Text(results_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Initial message
        self.results_text.insert(tk.END, "Welcome to Automatic Image Synchronizer!\n\n")
        self.results_text.insert(tk.END, "Features:\n")
        self.results_text.insert(tk.END, "• Fast parallel image processing\n")
        self.results_text.insert(tk.END, "• Multiple hash algorithms for accurate similarity detection\n")
        self.results_text.insert(tk.END, "• Automatic folder organization based on image content\n")
        self.results_text.insert(tk.END, "• Handles exact duplicates and similar images\n")
        self.results_text.insert(tk.END, "• Safe file operations with conflict resolution\n\n")
        self.results_text.insert(tk.END, "Instructions:\n")
        self.results_text.insert(tk.END, "1. Select two folders containing images to compare\n")
        self.results_text.insert(tk.END, "2. Choose an output folder for organized images\n")
        self.results_text.insert(tk.END, "3. Adjust similarity threshold if needed (0.85 recommended)\n")
        self.results_text.insert(tk.END, "4. Click 'Start Synchronization' to begin\n\n")
        self.results_text.config(state=tk.DISABLED)
    
    def browse_folder(self, var, is_output=False):
        """Browse for folder selection"""
        if is_output:
            folder = filedialog.askdirectory(title="Select Output Folder")
        else:
            folder = filedialog.askdirectory(title="Select Image Folder")
        
        if folder:
            var.set(folder)
    
    def clear_all(self):
        """Clear all input fields"""
        self.folder1_path.set("")
        self.folder2_path.set("")
        self.output_path.set("")
        self.progress_var.set(0)
        self.status_var.set("Ready to start...")
        
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "All fields cleared. Ready for new synchronization.\n")
        self.results_text.config(state=tk.DISABLED)
    
    def update_progress(self, value, message=""):
        """Update progress bar and message"""
        self.progress_var.set(value)
        if message:
            self.status_var.set(message)
        self.root.update_idletasks()
    
    def update_status(self, message):
        """Update status message"""
        self.status_var.set(message)
        
        # Also add to results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, f"{message}\n")
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        self.root.update_idletasks()
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.folder1_path.get():
            messagebox.showerror("Error", "Please select Folder 1")
            return False
        
        if not self.folder2_path.get():
            messagebox.showerror("Error", "Please select Folder 2")
            return False
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select Output Folder")
            return False
        
        # Check if paths exist
        folder1 = Path(self.folder1_path.get())
        folder2 = Path(self.folder2_path.get())
        
        if not folder1.exists():
            messagebox.showerror("Error", "Folder 1 does not exist")
            return False
        
        if not folder2.exists():
            messagebox.showerror("Error", "Folder 2 does not exist")
            return False
        
        # Check if output folder is different from input folders
        output_path = Path(self.output_path.get())
        if output_path == folder1 or output_path == folder2:
            messagebox.showerror("Error", "Output folder must be different from input folders")
            return False
        
        return True
    
    def start_sync(self):
        """Start the synchronization process"""
        if not self.validate_inputs():
            return
        
        # Disable start button and enable stop button
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Clear results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        # Reset progress
        self.progress_var.set(0)
        
        # Create synchronizer
        self.synchronizer = ImageSynchronizer(
            progress_callback=self.update_progress,
            status_callback=self.update_status
        )
        
        # Start processing in separate thread
        self.processing_thread = threading.Thread(target=self.run_sync, daemon=True)
        self.processing_thread.start()
    
    def run_sync(self):
        """Run synchronization in background thread"""
        try:
            folder1 = Path(self.folder1_path.get())
            folder2 = Path(self.folder2_path.get())
            output = Path(self.output_path.get())
            
            # Run synchronization
            stats = self.synchronizer.organize_images(folder1, folder2, output)
            
            # Update UI with results
            self.root.after(0, self.sync_completed, stats)
            
        except Exception as e:
            error_msg = f"Error during synchronization: {str(e)}"
            self.root.after(0, self.sync_error, error_msg)
    
    def sync_completed(self, stats):
        """Handle synchronization completion"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        if "cancelled" in stats:
            self.status_var.set("Synchronization cancelled by user")
            return
        
        if "error" in stats:
            self.status_var.set("Error: " + stats.get("message", "Unknown error"))
            return
        
        # Display results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, "\n" + "="*50 + "\n")
        self.results_text.insert(tk.END, "SYNCHRONIZATION COMPLETED SUCCESSFULLY!\n")
        self.results_text.insert(tk.END, "="*50 + "\n\n")
        
        self.results_text.insert(tk.END, f"📊 Results Summary:\n")
        self.results_text.insert(tk.END, f"  • Similar image groups created: {stats.get('similar_groups', 0)}\n")
        self.results_text.insert(tk.END, f"  • Unique images moved: {stats.get('unique_images', 0)}\n")
        self.results_text.insert(tk.END, f"  • Total images processed: {stats.get('total_processed', 0)}\n")
        self.results_text.insert(tk.END, f"  • Errors encountered: {stats.get('errors', 0)}\n\n")
        
        self.results_text.insert(tk.END, f"📁 Output folder: {self.output_path.get()}\n")
        self.results_text.insert(tk.END, f"  • Similar images are in folders named 'similar_[context]'\n")
        self.results_text.insert(tk.END, f"  • Unique images are in 'unique_images' folder\n\n")
        
        if stats.get('errors', 0) > 0:
            self.results_text.insert(tk.END, "⚠️  Some errors occurred during processing. ")
            self.results_text.insert(tk.END, "Check console for details.\n")
        
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        self.status_var.set("Synchronization completed successfully!")
        
        # Show completion message
        messagebox.showinfo("Success", 
                          f"Image synchronization completed!\n\n"
                          f"Similar groups: {stats.get('similar_groups', 0)}\n"
                          f"Unique images: {stats.get('unique_images', 0)}\n"
                          f"Total processed: {stats.get('total_processed', 0)}")
    
    def sync_error(self, error_msg):
        """Handle synchronization error"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Error occurred during synchronization")
        
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, f"\n❌ ERROR: {error_msg}\n")
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        messagebox.showerror("Error", error_msg)
    
    def stop_sync(self):
        """Stop the synchronization process"""
        if self.synchronizer:
            self.synchronizer.stop()
            self.status_var.set("Stopping synchronization...")
            
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def run(self):
        """Run the GUI application"""
        try:
            # Try to set modern theme if available
            self.root.tk.call("source", "azure.tcl")
            self.root.tk.call("set_theme", "light")
        except:
            # Fall back to default theme
            pass
        
        self.root.mainloop()


def main():
    """Main entry point"""
    app = ImageSyncGUI()
    app.run()


if __name__ == "__main__":
    main()
