import os
import subprocess
import json
import tkinter as tk
from tkinter import messagebox

# --- Setup Paths ---
# Saves data in Local AppData to ensure you have write permission
DATA_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "MyRobloxLauncher")
THEMES_PATH = os.path.join(DATA_PATH, "themes")
FAVS_PATH = os.path.join(DATA_PATH, "favorites")

for path in [DATA_PATH, THEMES_PATH, FAVS_PATH]:
    if not os.path.exists(path): os.makedirs(path)

# --- Workshop Catalog ---
WORKSHOP_CATALOG = {
    "Neon_Vibe": {"bg": "#000000", "btn_bg": "#39ff14", "btn_fg": "#000000"},
    "Ice_Blue": {"bg": "#e1f5fe", "btn_bg": "#03a9f4", "btn_fg": "#ffffff"},
    "Crimson_Dark": {"bg": "#210000", "btn_bg": "#ff0000", "btn_fg": "#ffffff"},
    "Midnight": {"bg": "#0b0c10", "btn_bg": "#45a29e", "btn_fg": "#0b0c10"},
    "Lava_Flow": {"bg": "#2b0000", "btn_bg": "#ff4500", "btn_fg": "#ffffff"},
    "Royal_Gold": {"bg": "#1c1c1c", "btn_bg": "#d4af37", "btn_fg": "#1c1c1c"}
}

# --- Core Functions ---
def launch_game(place_id):
    url = f"roblox://placeId={place_id}"
    subprocess.Popen(["cmd", "/c", f"start {url}"])

def apply_theme(data):
    # Dynamically updates UI colors based on selected theme
    root_bg = data["bg"]
    main_canvas.configure(bg=root_bg)
    scrollable_content.configure(bg=root_bg)
    play_button.configure(bg=data["btn_bg"], fg=data["btn_fg"])
    workshop_btn.configure(bg=data["btn_bg"], fg=data["btn_fg"])
    lib_label.configure(bg=root_bg, fg=data["btn_fg"])
    fav_label.configure(bg=root_bg, fg=data["btn_fg"])
    search_label.configure(bg=root_bg, fg="gray")
    theme_frame.configure(bg=root_bg)
    fav_container.configure(bg=root_bg)
    disclaimer.configure(bg=root_bg)

def download_theme(name, data):
    file_path = os.path.join(THEMES_PATH, f"{name}.json")
    with open(file_path, "w") as f: json.dump(data, f)
    refresh_all()
    messagebox.showinfo("Workshop", f"Installed {name}!")

def open_workshop():
    shop = tk.Toplevel(root)
    shop.title("Workshop Shop")
    shop.geometry("350x400")
    # Scrollable Shop setup
    c = tk.Canvas(shop); s = tk.Scrollbar(shop, command=c.yview); f = tk.Frame(c)
    f.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
    c.create_window((0, 0), window=f, anchor="nw"); c.configure(yscrollcommand=s.set)
    s.pack(side="right", fill="y"); c.pack(side="left", fill="both", expand=True)
    for name, data in WORKSHOP_CATALOG.items():
        row = tk.Frame(f); row.pack(fill="x", padx=10, pady=5)
        tk.Label(row, text=name, width=15).pack(side="left")
        tk.Button(row, text="Download", command=lambda n=name, d=data: download_theme(n, d)).pack(side="right")

def refresh_all(event=None):
    query = search_entry.get().lower()
    # Update Themes
    for w in theme_frame.winfo_children(): w.destroy()
    if os.path.exists(THEMES_PATH):
        for file in os.listdir(THEMES_PATH):
            if file.endswith(".json") and query in file.lower():
                with open(os.path.join(THEMES_PATH, file), "r") as f:
                    d = json.load(f)
                    row = tk.Frame(theme_frame, bg=scrollable_content["bg"])
                    row.pack(fill="x", pady=1)
                    tk.Button(row, text=file.replace(".json", ""), command=lambda data=d: apply_theme(data)).pack(side="left", expand=True, fill="x")
                    tk.Button(row, text="🗑️", fg="red", command=lambda f=file: [os.remove(os.path.join(THEMES_PATH, f)), refresh_all()]).pack(side="right")
    # Update Favorites
    for w in fav_container.winfo_children(): w.destroy()
    if os.path.exists(FAVS_PATH):
        for file in os.listdir(FAVS_PATH):
            if file.endswith(".json"):
                with open(os.path.join(FAVS_PATH, file), "r") as f:
                    data = json.load(f)
                    tk.Button(fav_container, text=f"⭐ {data['name']}", command=lambda i=data['id']: launch_game(i), bg="#FFD700", fg="black", font=("Arial", 9, "bold")).pack(fill="x", pady=2)
    # Force scrollable region update
    scrollable_content.update_idletasks()
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

# --- GUI Setup ---
root = tk.Tk()
root.title("Roblox Ultimate Launcher")
root.geometry("480x700")

# Setup Main Scrollable View
main_canvas = tk.Canvas(root, bg="#1a1a1a", highlightthickness=0)
main_scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_content = tk.Frame(main_canvas, bg="#1a1a1a")

scrollable_content.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
main_canvas.create_window((0, 0), window=scrollable_content, anchor="nw", width=460)
main_canvas.configure(yscrollcommand=main_scrollbar.set)

main_scrollbar.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)

# Main Launch Button
play_button = tk.Button(scrollable_content, text="OPEN ROBLOX APP", command=lambda: subprocess.Popen(["cmd", "/c", "start roblox://"]), font=("Arial Black", 18), bg="#00E676", fg="white")
play_button.pack(pady=20, fill="x", padx=20)

# Workshop & Search
workshop_btn = tk.Button(scrollable_content, text="🛒 OPEN WORKSHOP", command=open_workshop, font=("Arial", 10, "bold"))
workshop_btn.pack()

search_label = tk.Label(scrollable_content, text="Search Themes:", bg="#1a1a1a", fg="gray")
search_label.pack(pady=5)
search_entry = tk.Entry(scrollable_content, font=("Arial", 11)); search_entry.pack(padx=50, fill="x"); search_entry.bind("<KeyRelease>", refresh_all)

# Themes & Favorites Containers
lib_label = tk.Label(scrollable_content, text="MY THEMES", bg="#1a1a1a", fg="white", font=("Arial", 10, "bold"))
lib_label.pack(pady=10)
theme_frame = tk.Frame(scrollable_content, bg="#1a1a1a"); theme_frame.pack(fill="x", padx=20)

fav_label = tk.Label(scrollable_content, text="MANUAL FAVORITES", bg="#1a1a1a", fg="#FFD700", font=("Arial", 10, "bold"))
fav_label.pack(pady=10)
tk.Button(scrollable_content, text="📂 OPEN FAVS FOLDER", command=lambda: os.startfile(FAVS_PATH), font=("Arial", 8)).pack()
fav_container = tk.Frame(scrollable_content, bg="#1a1a1a"); fav_container.pack(fill="x", padx=20, pady=5)

# --- DISCLAIMER SIGN ---
disclaimer = tk.Label(root, text="⚠️ NOTICE: This is not official and not affiliated with Roblox.", fg="red", bg="#1a1a1a", font=("Arial", 8, "italic"), pady=10)
disclaimer.pack(side=tk.BOTTOM, fill="x")

# Mousewheel and Initial Scan
root.bind_all("<MouseWheel>", lambda e: main_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
refresh_all()
root.mainloop()
