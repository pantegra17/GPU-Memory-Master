import customtkinter as ctk
from tkinter import messagebox

# --- GLOBAL SETTINGS ---
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")
ctk.set_widget_scaling(1.1)

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
        self.title("GPU Memory Master v9.9")
        self.width = 540; self.height = 620 
        self.about_window = None
        self.var_cores = ctk.StringVar(); self.var_clock = ctk.StringVar()
        self.setup_ui()
        self.center_window(self, self.width, self.height)
        self.resizable(False, False)

    def center_window(self, window, width, height):
        sw = window.winfo_screenwidth(); sh = window.winfo_screenheight()
        x = (sw // 2) - (width // 2); y = (sh // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def copy_to_clipboard(self, entry_widget):
        val = entry_widget.get()
        if val: self.clipboard_clear(); self.clipboard_append(val)

    def create_clickable_combo(self, parent, values, prompt, command=None):
        combo = ctk.CTkComboBox(parent, values=values, state="readonly", cursor="arrow", command=command)
        combo.set(prompt); combo._entry.configure(cursor="arrow")
        combo._entry.bind("<Button-1>", lambda e: combo._canvas.event_generate("<Button-1>"))
        return combo

    def update_arch_list(self, brand):
        archs = list(ARCH_DATA[brand].keys())
        self.combo_arch.configure(values=archs); self.combo_arch.set("Select Architecture...")
        # Toggle Mirroring: Only for manufacturers with unified core counts
        if brand == "Intel":
            self.ent_cores.configure(textvariable=""); self.ent_ai_cores.configure(textvariable="")
            self.ent_clock.configure(textvariable=""); self.ent_ai_clock.configure(textvariable="")
        else:
            self.ent_cores.configure(textvariable=self.var_cores); self.ent_ai_cores.configure(textvariable=self.var_cores)
            self.ent_clock.configure(textvariable=self.var_clock); self.ent_ai_clock.configure(textvariable=self.var_clock)

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
        self.btn_about = ctk.CTkButton(self.nav_frame, text="?", width=35, command=self.show_about_window).pack(side="right")

        self.sel_frame = ctk.CTkFrame(self, fg_color="transparent"); self.sel_frame.pack(fill="x", padx=25, pady=5)
        self.combo_brand = self.create_clickable_combo(self.sel_frame, list(ARCH_DATA.keys()), "Select Brand...", command=self.update_arch_list)
        self.combo_brand.pack(fill="x", pady=2)
        self.combo_arch = self.create_clickable_combo(self.sel_frame, [], "Select Architecture...")
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
        if arch == "Select Architecture...": messagebox.showwarning("Warning", "Select Architecture!"); return
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
        if arch == "Select Architecture...": messagebox.showwarning("Warning", "Select Architecture!"); return
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
        ctk.CTkLabel(self.about_window, text="GPU Memory Master v9.9", font=("Arial", 20, "bold"), text_color="#1565C0").pack(pady=20)
        ctk.CTkLabel(self.about_window, text="Dev: Gökhan Can\nContact: pantegra@gmail.com", font=("Arial", 12)).pack(pady=10)

if __name__ == "__main__": App().mainloop()