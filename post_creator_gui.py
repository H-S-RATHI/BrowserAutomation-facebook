import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import json
import os
from PIL import Image, ImageTk
from io import BytesIO
import base64
import threading
from gemini_utils import enhance_description

class PostCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Post Creator with AI Enhancement")
        self.root.geometry("900x650")
        
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
        
        # Description frame
        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Description label and enhance button
        desc_header = ttk.Frame(desc_frame)
        desc_header.pack(fill=tk.X)
        
        ttk.Label(desc_header, text="Post Description:").pack(side=tk.LEFT)
        
        # Add Enhance button
        self.enhance_btn = ttk.Button(
            desc_header, 
            text="✨ Enhance with AI", 
            command=self.enhance_description,
            style='Accent.TButton'
        )
        self.enhance_btn.pack(side=tk.RIGHT, padx=5)
        
        # Description text area with scrollbar
        desc_container = ttk.Frame(desc_frame)
        desc_container.pack(fill=tk.BOTH, expand=True)
        
        self.description_text = scrolledtext.ScrolledText(
            desc_container, 
            height=10, 
            font=('Arial', 10),
            wrap=tk.WORD
        )
        self.description_text.pack(fill=tk.BOTH, expand=True)
        
        # Loading indicator
        self.loading_label = ttk.Label(desc_frame, text="Enhancing description...")
        self.loading_label.pack_forget()
        
        # Photo selection
        photo_frame = ttk.LabelFrame(main_frame, text="Photos", padding=10)
        # only stretch horizontally, not vertically:
        photo_frame.pack(fill=tk.X, expand=False, pady=(10, 0))
        
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
        
        self.canvas.config(height=190)
        self.canvas.pack(fill=tk.X, expand=False)
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
            img.thumbnail((75, 75), Image.Resampling.LANCZOS)
            
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
    
    def enhance_description(self):
        """Enhance the description using Gemini AI"""
        description = self.description_text.get("1.0", tk.END).strip()
        
        if not description:
            messagebox.showinfo("Empty Description", "Please enter a description to enhance.")
            return
            
        # Disable buttons during processing
        self.enhance_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.loading_label.pack(pady=5)
        
        # Run enhancement in a separate thread to keep the UI responsive
        def enhance_thread():
            try:
                enhanced = enhance_description(description)
                if enhanced:
                    self.root.after(0, self._update_description, enhanced)
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Failed to enhance description. Please try again."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}\n\nMake sure you've set up your Gemini API key in gemini_config.py"))
            finally:
                self.root.after(0, self._enable_enhance_ui)
        
        threading.Thread(target=enhance_thread, daemon=True).start()
    
    def _update_description(self, text):
        """Update the description text area with enhanced text"""
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert("1.0", text)
    
    def _enable_enhance_ui(self):
        """Re-enable UI elements after enhancement"""
        self.enhance_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)
        self.loading_label.pack_forget()
    
    def save_post(self):
        description = self.description_text.get("1.0", tk.END).strip()
        
        if not description and not self.photos:
            messagebox.showwarning("Empty Post", "Please add a description or at least one photo.")
            return
        
        # Create posts directory if it doesn't exist
        os.makedirs('posts', exist_ok=True)
        
        # Save post data to JSON file
        post_data = {
            'description': self.description_text.get('1.0', tk.END).strip(),
            'photos': [],
            'photos_data': [],  # Store base64 encoded image data
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add photo data as base64
        for photo_path in self.photos:
            try:
                with open(photo_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    post_data['photos_data'].append({
                        'filename': os.path.basename(photo_path),
                        'data': img_data
                    })
            except Exception as e:
                print(f"Error reading photo {photo_path}: {str(e)}")
        
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
