import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

# Load the catalog CSV
CSV_PATH = "music_catalog.csv"
df = pd.read_csv(CSV_PATH)

# Clean column names for display and logic
df.columns = [col.strip() for col in df.columns]

# Build main viewer app
class TrackstarViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Trackstar Viewer")
        self.frame = ttk.Frame(master)
        self.frame.pack(fill="both", expand=True)

        # Search bar
        self.search_var = tk.StringVar()
        search_box = ttk.Entry(self.frame, textvariable=self.search_var)
        search_box.pack(fill="x")
        search_box.bind("<KeyRelease>", self.filter_table)

        # Table
        self.tree = ttk.Treeview(self.frame, columns=list(df.columns), show="headings")
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=24)
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="w")
        self.tree.pack(fill="both", expand=True)

        # Buttons
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Save", command=self.save_csv).pack(side="left")
        ttk.Button(btn_frame, text="Sync", command=self.sync_metadata).pack(side="left")

        self.refresh_table(df)

    def refresh_table(self, data):
        self.tree.delete(*self.tree.get_children())
        for _, row in data.iterrows():
            values = [str(row[col]) if pd.notna(row[col]) else '' for col in df.columns]
            tag = self.get_color_tag(row)
            self.tree.insert("", "end", values=values, tags=(tag,))

        # Define color tags
        self.tree.tag_configure("low", background="#e6f7ff")
        self.tree.tag_configure("medium", background="#fff7e6")
        self.tree.tag_configure("high", background="#ffe6e6")

    def get_color_tag(self, row):
        try:
            level = str(row.get("Energy Level", "")).strip().lower()
            if level in ["low", "1"]:
                return "low"
            elif level in ["medium", "2"]:
                return "medium"
            elif level in ["high", "3"]:
                return "high"
        except:
            pass
        return ""

    def filter_table(self, event=None):
        query = self.search_var.get().lower()
        filtered = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)]
        self.refresh_table(filtered)

    def save_csv(self):
        df.to_csv(CSV_PATH, index=False)
        messagebox.showinfo("Saved", f"Catalog saved to {CSV_PATH}")

    def sync_metadata(self):
        # Placeholder sync logic (actual diffing will come in future version)
        messagebox.showinfo("Sync", "Sync logic will compare Mixxx + CSV and prioritize intelligently.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TrackstarViewer(root)
    root.mainloop()
