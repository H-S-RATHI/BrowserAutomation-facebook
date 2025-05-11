import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import json
import os
from PIL import Image, ImageTk
from io import BytesIO
import base64

class PostCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Post Creator")
        self.root.geometry("800x600")
        
        # Styling
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5, font=('Arial', 10))
        self.style.configure('TLabel', padding=5, font=('Arial', 10))
        self.style.configure('TEntry', padding=5)
        
        # Post data
        self.photos = []
        self.photo_previews = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Description
        ttk.Label(main_frame, text="Post Description:").pack(anchor=tk.W, pady=(0, 5))
        self.description_text = tk.Text(main_frame, height=5, font=('Arial', 10))
        self.description_text.pack(fill=tk.X, pady=(0, 10))
        
        # Photo selection
        photo_frame = ttk.LabelFrame(main_frame, text="Photos", padding=10)
        photo_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Buttons frame
        btn_frame = ttk.Frame(photo_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.add_photo_btn = ttk.Button(btn_frame, text="Add Photo", command=self.add_photo)
        self.add_photo_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_photos_btn = ttk.Button(btn_frame, text="Clear All Photos", command=self.clear_photos)
        self.clear_photos_btn.pack(side=tk.LEFT)
        
        # Canvas for photo previews
        self.canvas = tk.Canvas(photo_frame, bg='#f0f0f0', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(photo_frame, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.pack(fill=tk.X, pady=(5, 0))
        
        # Save button
        self.save_btn = ttk.Button(main_frame, text="Save Post", command=self.save_post, style='Accent.TButton')
        self.save_btn.pack(pady=(20, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
    
    def add_photo(self):
        filetypes = (
            ('Image files', '*.jpg *.jpeg *.png *.gif'),
            ('All files', '*.*')
        )
        
        filenames = filedialog.askopenfilenames(
            title="Select photos",
            filetypes=filetypes
        )
        
        for filename in filenames:
            if filename not in self.photos:  # Avoid duplicates
                self.photos.append(filename)
                self.add_photo_preview(filename)
    
    def add_photo_preview(self, filename):
        try:
            # Open and resize image for preview
            img = Image.open(filename)
            img.thumbnail((150, 150), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Keep a reference to the image
            self.photo_previews.append(photo)
            
            # Create a frame for each preview
            preview_frame = ttk.Frame(self.scrollable_frame, padding=5, relief="groove", borderwidth=1)
            preview_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
            
            # Add image to the frame
            label = ttk.Label(preview_frame, image=photo)
            label.image = photo  # Keep a reference!
            label.pack()
            
            # Add filename label
            ttk.Label(preview_frame, text=os.path.basename(filename), 
                     width=15, wraplength=140).pack()
            
            # Add remove button
            ttk.Button(
                preview_frame, 
                text="Remove", 
                command=lambda f=filename, p=preview_frame: self.remove_photo(f, p)
            ).pack(pady=(5, 0))
            
            # Update canvas scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open {filename}: {str(e)}")
    
    def remove_photo(self, filename, preview_frame):
        if filename in self.photos:
            self.photos.remove(filename)
        preview_frame.destroy()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def clear_photos(self):
        if messagebox.askyesno("Clear Photos", "Are you sure you want to remove all photos?"):
            self.photos.clear()
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self.photo_previews.clear()
    
    def save_post(self):
        description = self.description_text.get("1.0", tk.END).strip()
        
        if not description and not self.photos:
            messagebox.showwarning("Empty Post", "Please add a description or at least one photo.")
            return
        
        # Create posts directory if it doesn't exist
        os.makedirs('posts', exist_ok=True)
        
        # Create post data
        post_data = {
            'description': description,
            'photos': [os.path.abspath(photo) for photo in self.photos],
            'created_at': datetime.now().isoformat(),
            'posted': False
        }
        
        # Create a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"posts/post_{timestamp}.json"
        
        try:
            # Save the post data
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(post_data, f, indent=4, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Post saved successfully!\n\nLocation: {os.path.abspath(filename)}")
            
            # Clear the form
            self.description_text.delete("1.0", tk.END)
            self.clear_photos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save post: {str(e)}")

def main():
    root = tk.Tk()
    app = PostCreatorApp(root)
    
    # Center the window
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Set minimum window size
    root.minsize(600, 500)
    
    # Configure the style for the save button
    style = ttk.Style()
    style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
    
    root.mainloop()

if __name__ == "__main__":
    main()
