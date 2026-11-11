import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import urllib.request
import json
import threading
import queue
import os

# --- GLOBAL SETTINGS ---
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")
ctk.set_widget_scaling(1.1)

# GitHub Raw URL for online GPU database
GITHUB_GPU_URL = "https://raw.githubusercontent.com/pantegra17/GPU-Memory-Master/main/gpus.json"

PROMPT_BRAND = "Select Brand..."
PROMPT_SEARCH_MODEL = "Search Model (e.g. 5090, 4080)..."
PROMPT_SELECT_BRAND_FIRST = "Select Brand First..."
PROMPT_ARCH = "Select Architecture..."

def format_num(num):
    try:
        val = float(num)
        val = round(val, 1)
        if val == int(val): return str(int(val))
        return f"{val:.1f}"
    except: return str(num)

# --- DETAILED ARCHITECTURE HIERARCHY ---
ARCH_DATA = {
    "NVIDIA": {
        "Blackwell (2024-2026)": {"ai": 64, "tf": 2},
        "Ampere / Ada (2020-2024)": {"ai": 32, "tf": 2},
        "Turing (2018-2020)": {"ai": 16, "tf": 2},
        "Pascal (2016-2018)": {"ai": 0, "tf": 2},
        "Maxwell (2014-2016)": {"ai": 0, "tf": 2}
    },
    "AMD": {
        "RDNA 3 / 4 / 5+ (2022-2026)": {"ai": 128, "tf": 4},
        "RDNA 1 / 2 (2019-2022)": {"ai": 0, "tf": 2},
        "GCN 4 / 5 (Polaris/Vega) (2016-2019)": {"ai": 0, "tf": 2},
        "GCN 1 / 2 / 3 (HD 7000 to R9) (2012-2016)": {"ai": 0, "tf": 2}
    },
    "Intel": {
        "Arc B-Series (Battlemage) (2024+)": {"ai": 512, "tf": 2},
        "Arc A-Series (Alchemist) (2022-2024)": {"ai": 256, "tf": 2}
    }
}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GPU Memory Master v10.0")
        self.width = 540; self.height = 660 
        self.about_window = None
        self.var_cores = ctk.StringVar(); self.var_clock = ctk.StringVar()
        self.gpu_database = {}
        self.db_source = "loading"
        self.msg_queue = queue.Queue()
        
        # Set icon if available
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ikon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass

        self.setup_ui()
        self.setup_autocomplete_popup()
        self.center_window(self, self.width, self.height)
        self.resizable(False, False)

        # Thread-safe queue polling in main thread
        self.after(50, self.poll_queue)

        # Start asynchronous fetch of GPU database in background
        threading.Thread(target=self.fetch_database_thread, daemon=True).start()

    def center_window(self, window, width, height):
        sw = window.winfo_screenwidth(); sh = window.winfo_screenheight()
        x = (sw // 2) - (width // 2); y = (sh // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def fetch_database_thread(self):
        """Fetches the GPU database from GitHub; falls back to local gpus.json if available."""
        # 1. Try GitHub Online
        try:
            req = urllib.request.Request(GITHUB_GPU_URL, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=4) as response:
                data = json.loads(response.read().decode("utf-8"))
                self.msg_queue.put(("success", data, "online"))
                return
        except Exception:
            pass

        # 2. Local fallback
        script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
        local_path = os.path.join(script_dir, "gpus.json")
        if not os.path.exists(local_path):
            local_path = "gpus.json"

        if os.path.exists(local_path):
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.msg_queue.put(("success", data, "local"))
                    return
            except Exception:
                pass

        self.msg_queue.put(("failed", None, "error"))

    def poll_queue(self):
        """Processes background worker events safely in the Tkinter main thread."""
        try:
            while True:
                msg_type, data, source = self.msg_queue.get_nowait()
                if msg_type == "success":
                    self.gpu_database = data
                    self.db_source = source
                    count = sum(len(v) for v in self.gpu_database.values()) if isinstance(self.gpu_database, dict) else 0
                    tag = "🟢 Cloud DB" if source == "online" else "🟡 Local DB"
                    self.lbl_status.configure(
                        text=f"{tag} ({count} GPUs)", 
                        text_color="#2E7D32" if source == "online" else "#E65100"
                    )
                elif msg_type == "failed":
                    self.db_source = "error"
                    self.lbl_status.configure(text="🔴 Offline (No Data)", text_color="#C62828")
        except queue.Empty:
            pass
        self.after(100, self.poll_queue)

    def copy_to_clipboard(self, entry_widget):
        val = entry_widget.get()
        if val: self.clipboard_clear(); self.clipboard_append(val)

    def create_clickable_combo(self, parent, values, prompt, command=None):
        combo = ctk.CTkComboBox(parent, values=values, state="readonly", cursor="arrow", command=command)
        combo.set(prompt)
        combo._entry.configure(cursor="arrow")
        combo._entry.bind("<Button-1>", lambda e: combo._canvas.event_generate("<Button-1>"))
        return combo

    def update_arch_list(self, brand):
        archs = list(ARCH_DATA[brand].keys())
        self.combo_arch.configure(values=archs); self.combo_arch.set(PROMPT_ARCH)
        
        # Toggle Mirroring: Only for manufacturers with unified core counts
        if brand == "Intel":
            self.ent_cores.configure(textvariable=""); self.ent_ai_cores.configure(textvariable="")
            self.ent_clock.configure(textvariable=""); self.ent_ai_clock.configure(textvariable="")
        else:
            self.ent_cores.configure(textvariable=self.var_cores); self.ent_ai_cores.configure(textvariable=self.var_cores)
            self.ent_clock.configure(textvariable=self.var_clock); self.ent_ai_clock.configure(textvariable=self.var_clock)

        # Clear and enable model search entry
        self.ent_model.configure(state="normal", placeholder_text=PROMPT_SEARCH_MODEL)
        self.ent_model.delete(0, "end")
        self.hide_suggestions()

    # --- AUTOCOMPLETE DROPDOWN POPUP ---
    def setup_autocomplete_popup(self):
        self.popup = tk.Toplevel(self)
        self.popup.withdraw()
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)

        self.pop_frame = tk.Frame(self.popup, bg="#1E88E5", bd=1)
        self.pop_frame.pack(fill="both", expand=True)

        self.pop_scrollbar = tk.Scrollbar(self.pop_frame, orient="vertical")
        self.pop_listbox = tk.Listbox(
            self.pop_frame,
            font=("Segoe UI", 10),
            selectmode="browse",
            activestyle="none",
            bg="#FFFFFF",
            fg="#212121",
            selectbackground="#1565C0",
            selectforeground="#FFFFFF",
            relief="flat",
            bd=0,
            highlightthickness=0,
            yscrollcommand=self.pop_scrollbar.set
        )
        self.pop_scrollbar.config(command=self.pop_listbox.yview)
        self.pop_scrollbar.pack(side="right", fill="y")
        self.pop_listbox.pack(side="left", fill="both", expand=True)

        # Events for selection
        self.pop_listbox.bind("<ButtonRelease-1>", self.on_listbox_click)
        self.pop_listbox.bind("<Return>", self.on_listbox_enter)
        self.pop_listbox.bind("<Escape>", lambda e: self.hide_suggestions())

        # Dismiss popup on outside clicks or when main window moves
        self.bind_all("<Button-1>", self.on_global_click, add="+")
        self.bind("<Configure>", self.on_window_configure, add="+")

    def show_suggestions(self, matches):
        if not matches:
            self.hide_suggestions()
            return

        self.pop_listbox.delete(0, "end")
        for m in matches:
            self.pop_listbox.insert("end", f"  {m}")

        # Position right below the model search row
        self.update_idletasks()
        x = self.model_frame.winfo_rootx()
        y = self.model_frame.winfo_rooty() + self.model_frame.winfo_height() + 2
        w = self.model_frame.winfo_width()
        item_count = len(matches)
        h = min(200, item_count * 26 + 4)

        self.popup.geometry(f"{w}x{h}+{x}+{y}")
        self.popup.deiconify()
        self.popup.lift()

    def hide_suggestions(self):
        if hasattr(self, "popup") and self.popup.winfo_ismapped():
            self.popup.withdraw()

    def on_model_key_release(self, event):
        """Triggered on keystrokes in the search box; opens/updates dropdown."""
        if event.keysym in ("Return", "Escape", "Down", "Up"):
            return

        brand = self.combo_brand.get()
        if brand not in ARCH_DATA:
            self.hide_suggestions()
            return

        all_models = list(self.gpu_database.get(brand, {}).keys())
        query = self.ent_model.get().strip().lower()

        if not query:
            filtered = all_models
        else:
            filtered = [m for m in all_models if query in m.lower()]

        if filtered:
            self.show_suggestions(filtered)
        else:
            self.hide_suggestions()

    def on_model_key_down(self, event):
        """Allows down arrow key navigation from entry into suggestions listbox."""
        if self.popup.winfo_ismapped() and self.pop_listbox.size() > 0:
            self.pop_listbox.focus_set()
            self.pop_listbox.selection_clear(0, "end")
            self.pop_listbox.selection_set(0)
            self.pop_listbox.activate(0)
            return "break"

    def on_model_enter(self, event):
        """Enter key selects exact or top matching model."""
        brand = self.combo_brand.get()
        all_models = list(self.gpu_database.get(brand, {}).keys())
        query = self.ent_model.get().strip().lower()

        matches = [m for m in all_models if query in m.lower()] if query else all_models
        if matches:
            self.select_model(matches[0])
            self.hide_suggestions()

    def toggle_model_dropdown(self):
        """Toggles full model list dropdown when clicking the arrow button."""
        brand = self.combo_brand.get()
        if brand not in ARCH_DATA:
            messagebox.showwarning("Warning", "Please select a brand first!")
            return

        if self.popup.winfo_ismapped():
            self.hide_suggestions()
        else:
            all_models = list(self.gpu_database.get(brand, {}).keys())
            query = self.ent_model.get().strip().lower()
            matches = [m for m in all_models if query in m.lower()] if query else all_models
            self.show_suggestions(matches)

    def on_listbox_click(self, event):
        self.after(10, self._process_listbox_selection)

    def on_listbox_enter(self, event):
        self._process_listbox_selection()

    def _process_listbox_selection(self):
        sel = self.pop_listbox.curselection()
        if sel:
            selected_model = self.pop_listbox.get(sel[0]).strip()
            self.select_model(selected_model)
            self.hide_suggestions()

    def select_model(self, model_name):
        self.ent_model.delete(0, "end")
        self.ent_model.insert(0, model_name)
        self.apply_gpu_preset(model_name)
        self.ent_model.focus_set()

    def on_global_click(self, event):
        """Hides dropdown when clicking anywhere outside."""
        if not hasattr(self, "popup") or not self.popup.winfo_ismapped():
            return
        
        try:
            px, py = self.popup.winfo_rootx(), self.popup.winfo_rooty()
            pw, ph = self.popup.winfo_width(), self.popup.winfo_height()
            mx, my = self.model_frame.winfo_rootx(), self.model_frame.winfo_rooty()
            mw, mh = self.model_frame.winfo_width(), self.model_frame.winfo_height()
            cx, cy = event.x_root, event.y_root

            inside_popup = (px <= cx <= px + pw) and (py <= cy <= py + ph)
            inside_frame = (mx <= cx <= mx + mw) and (my <= cy <= my + mh)

            if not inside_popup and not inside_frame:
                self.hide_suggestions()
        except Exception:
            pass

    def on_window_configure(self, event):
        """Hides popup if main window is moved."""
        if hasattr(self, "popup") and self.popup.winfo_ismapped():
            self.hide_suggestions()

    def apply_gpu_preset(self, model_name):
        """Automatically fills all architecture, memory, compute, and AI inputs."""
        brand = self.combo_brand.get()
        if brand not in self.gpu_database or model_name not in self.gpu_database[brand]:
            return

        data = self.gpu_database[brand][model_name]

        # 1. Architecture
        arch = data.get("arch", "")
        if arch in ARCH_DATA.get(brand, {}):
            self.combo_arch.set(arch)

        # 2. Memory Analysis tab
        self.ent_bus.delete(0, "end"); self.ent_bus.insert(0, data.get("bus", ""))
        self.ent_speed.delete(0, "end"); self.ent_speed.insert(0, data.get("speed", ""))
        self.ent_bw.delete(0, "end")
        self.calc_memory()

        # 3. Compute tab
        cores = data.get("cores", "")
        clock = data.get("clock", "")
        self.var_cores.set(cores)
        self.var_clock.set(clock)

        if brand == "Intel":
            self.ent_cores.delete(0, "end"); self.ent_cores.insert(0, cores)
            self.ent_clock.delete(0, "end"); self.ent_clock.insert(0, clock)
            self.ent_ai_cores.delete(0, "end"); self.ent_ai_cores.insert(0, cores)
            self.ent_ai_clock.delete(0, "end"); self.ent_ai_clock.insert(0, clock)

        self.ent_tflops.delete(0, "end")
        self.calc_tflops()

        # 4. AI tab
        self.ent_tops.delete(0, "end")
        self.calc_ai_tops()

    def clear_logic(self, mode):
        if mode == "core":
            for w in [self.ent_cores, self.ent_ai_cores, self.ent_clock, self.ent_ai_clock, self.ent_tflops, self.ent_tops]: w.delete(0, "end")
        elif mode in ["boost", "result"]:
            for w in [self.ent_clock, self.ent_ai_clock, self.ent_tflops, self.ent_tops]: w.delete(0, "end")

    def create_input_row(self, parent, label_text, clear_mode=None, shared_var=None):
        ctk.CTkLabel(parent, text=label_text, font=("Arial", 11, "bold")).pack(anchor="w", padx=65)
        row = ctk.CTkFrame(parent, fg_color="transparent"); row.pack(fill="x", pady=1)
        btn_copy = ctk.CTkButton(row, text="COPY", width=50, height=30, font=("Arial", 10, "bold"), fg_color="#E0E0E0", text_color="#424242", hover_color="#BDBDBD")
        btn_copy.pack(side="left", padx=(15, 5))
        entry = ctk.CTkEntry(row, height=30, textvariable=shared_var); entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
        btn_copy.configure(command=lambda e=entry: self.copy_to_clipboard(e))
        if clear_mode: entry.bind("<Button-1>", lambda e, m=clear_mode: self.clear_logic(m))
        else: entry.bind("<Button-1>", lambda e, ent=entry: ent.delete(0, "end"))
        return entry

    def setup_ui(self):
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent"); self.nav_frame.pack(fill="x", padx=25, pady=(10, 0))
        ctk.CTkLabel(self.nav_frame, text="GPU Memory Master", font=("Arial", 20, "bold"), text_color="#1565C0").pack(side="left")
        
        self.top_right = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        self.top_right.pack(side="right")
        self.lbl_status = ctk.CTkLabel(self.top_right, text="Connecting...", font=("Arial", 10, "italic"), text_color="#757575")
        self.lbl_status.pack(side="left", padx=8)
        self.btn_about = ctk.CTkButton(self.top_right, text="?", width=35, command=self.show_about_window).pack(side="right")

        self.sel_frame = ctk.CTkFrame(self, fg_color="transparent"); self.sel_frame.pack(fill="x", padx=25, pady=5)
        
        # 1. Brand selection
        self.combo_brand = self.create_clickable_combo(self.sel_frame, list(ARCH_DATA.keys()), PROMPT_BRAND, command=self.update_arch_list)
        self.combo_brand.pack(fill="x", pady=2)

        # 2. Model search row (Search entry + dropdown button)
        self.model_frame = ctk.CTkFrame(self.sel_frame, fg_color="transparent")
        self.model_frame.pack(fill="x", pady=2)

        self.ent_model = ctk.CTkEntry(
            self.model_frame, 
            placeholder_text=PROMPT_SELECT_BRAND_FIRST,
            height=32,
            font=("Arial", 12)
        )
        self.ent_model.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.ent_model.bind("<KeyRelease>", self.on_model_key_release)
        self.ent_model.bind("<Down>", self.on_model_key_down)
        self.ent_model.bind("<Return>", self.on_model_enter)

        self.btn_drop = ctk.CTkButton(
            self.model_frame, 
            text="▼", 
            width=36, 
            height=32, 
            font=("Arial", 11, "bold"), 
            fg_color="#E0E0E0", 
            text_color="#424242", 
            hover_color="#BDBDBD",
            command=self.toggle_model_dropdown
        )
        self.btn_drop.pack(side="right")

        # 3. Architecture selection
        self.combo_arch = self.create_clickable_combo(self.sel_frame, [], PROMPT_ARCH)
        self.combo_arch.pack(fill="x", pady=2)

        self.tabview = ctk.CTkTabview(self, height=380); self.tabview.pack(fill="both", expand=True, padx=20, pady=5)
        self.tab_mem = self.tabview.add("Memory Analysis"); self.tab_comp = self.tabview.add("Compute (TFLOPS)"); self.tab_ai = self.tabview.add("AI (TOPS)")

        self.ent_bus = self.create_input_row(self.tab_mem, "Memory Bus (Bit):")
        self.ent_bw = self.create_input_row(self.tab_mem, "Bandwidth (GB/s):")
        self.ent_speed = self.create_input_row(self.tab_mem, "Effective Speed (Gbps):")
        ctk.CTkButton(self.tab_mem, text="CALCULATE", command=self.calc_memory, font=("Arial", 13, "bold"), height=40).pack(fill="x", pady=10, padx=15)
        self.lbl_res_val = ctk.CTkLabel(self.tab_mem, text="", font=("Arial", 16, "bold"), text_color="#1565C0"); self.lbl_res_val.pack()

        self.ent_cores = self.create_input_row(self.tab_comp, "Shading Units (Cuda/SP/ALU):", "core", self.var_cores)
        self.ent_clock = self.create_input_row(self.tab_comp, "Boost Clock (MHz):", "boost", self.var_clock)
        self.ent_tflops = self.create_input_row(self.tab_comp, "Compute Power (TFLOPS):", "result")
        ctk.CTkButton(self.tab_comp, text="CALCULATE", command=self.calc_tflops, font=("Arial", 13, "bold"), height=40, fg_color="#C62828").pack(fill="x", pady=15, padx=15)
        self.lbl_res_tflops = ctk.CTkLabel(self.tab_comp, text="", font=("Arial", 22, "bold"), text_color="#C62828"); self.lbl_res_tflops.pack()

        self.ent_ai_cores = self.create_input_row(self.tab_ai, "AI Core Count (Cuda/SP/XMX):", "core", self.var_cores)
        self.ent_ai_clock = self.create_input_row(self.tab_ai, "Boost Clock (MHz):", "boost", self.var_clock)
        self.ent_tops = self.create_input_row(self.tab_ai, "AI Performance (TOPS):", "result")
        ctk.CTkButton(self.tab_ai, text="CALCULATE", command=self.calc_ai_tops, font=("Arial", 13, "bold"), height=40, fg_color="#6A1B9A").pack(fill="x", pady=15, padx=15)
        self.lbl_res_tops = ctk.CTkLabel(self.tab_ai, text="", font=("Arial", 22, "bold"), text_color="#6A1B9A"); self.lbl_res_tops.pack()

        self.check_topmost = ctk.CTkCheckBox(self, text="Always on Top", font=("Arial", 11), command=self.toggle_topmost); self.check_topmost.pack(pady=(0, 10))

    def calc_memory(self):
        try:
            sp, bt, bw = self.ent_speed.get().replace(",", "."), self.ent_bus.get().replace(",", "."), self.ent_bw.get().replace(",", ".")
            if sp and bt and not bw:
                res = (float(bt) * float(sp)) / 8; self.ent_bw.delete(0, "end"); self.ent_bw.insert(0, format_num(res))
            elif bw and bt and not sp:
                res = (float(bw) * 8) / float(bt); self.ent_speed.delete(0, "end"); self.ent_speed.insert(0, format_num(res))
            elif bw and sp and not bt:
                res = (float(bw) * 8) / float(sp); self.ent_bus.delete(0, "end"); self.ent_bus.insert(0, format_num(res))
            self.lbl_res_val.configure(text=f"Result: {self.ent_speed.get()} Gbps")
        except: messagebox.showerror("Error", "Check input values!")

    def calc_tflops(self):
        brand = self.combo_brand.get(); arch = self.combo_arch.get()
        if arch in (PROMPT_ARCH, ""): messagebox.showwarning("Warning", "Select Architecture!"); return
        try:
            mult = ARCH_DATA[brand][arch]["tf"]; c, clk, tf = self.ent_cores.get(), self.ent_clock.get(), self.ent_tflops.get()
            if c and clk and not tf:
                res = (float(c) * float(clk) * mult) / 1000000; self.ent_tflops.delete(0, "end"); self.ent_tflops.insert(0, format_num(res))
            elif tf and c and not clk:
                res_clk = (float(tf) * 1000000) / (float(c) * mult); self.ent_clock.delete(0, "end"); self.ent_clock.insert(0, format_num(res_clk))
            elif tf and clk and not c:
                res_c = (float(tf) * 1000000) / (float(clk) * mult); self.ent_cores.delete(0, "end"); self.ent_cores.insert(0, format_num(int(res_c)))
            self.lbl_res_tflops.configure(text=f"{self.ent_tflops.get()} TFLOPS")
        except: messagebox.showerror("Error", "Check inputs!")

    def calc_ai_tops(self):
        brand = self.combo_brand.get(); arch = self.combo_arch.get()
        if arch in (PROMPT_ARCH, ""): messagebox.showwarning("Warning", "Select Architecture!"); return
        try:
            mult = ARCH_DATA[brand][arch]["ai"]
            if mult == 0: messagebox.showinfo("Info", "Legacy architectures do not have dedicated AI TOPS."); return
            c, clk, tops = self.ent_ai_cores.get(), self.ent_ai_clock.get(), self.ent_tops.get()
            if c and clk and not tops:
                res = (float(c) * float(clk) * mult) / 1000000; self.ent_tops.delete(0, "end"); self.ent_tops.insert(0, format_num(res))
            elif tops and c and not clk:
                res_clk = (float(tops) * 1000000) / (float(c) * mult); self.ent_ai_clock.delete(0, "end"); self.ent_ai_clock.insert(0, format_num(res_clk))
            elif tops and clk and not c:
                res_c = (float(tops) * 1000000) / (float(clk) * mult); self.ent_ai_cores.delete(0, "end"); self.ent_ai_cores.insert(0, format_num(int(res_c)))
            self.lbl_res_tops.configure(text=f"{self.ent_tops.get()} TOPS")
        except: messagebox.showerror("Error", "Check inputs!")

    def toggle_topmost(self): self.attributes("-topmost", self.check_topmost.get())
    def show_about_window(self):
        if self.about_window and self.about_window.winfo_exists(): self.about_window.lift(); return
        self.about_window = ctk.CTkToplevel(self); self.about_window.title("About"); self.about_window.geometry("400x250"); self.about_window.attributes("-topmost", True); self.about_window.grab_set()
        ctk.CTkLabel(self.about_window, text="GPU Memory Master v10.0", font=("Arial", 20, "bold"), text_color="#1565C0").pack(pady=20)
        ctk.CTkLabel(self.about_window, text="Dev: Gökhan Can\nContact: pantegra@gmail.com", font=("Arial", 12)).pack(pady=10)

if __name__ == "__main__": App().mainloop()
