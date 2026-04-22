import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).parent / '.env')

# ── lazy imports so GUI opens instantly ──────────────────────────────────────
pdf_loader   = None
embedder     = None
search_mod   = None
callAPI_mod  = None

def lazy_import():
    global pdf_loader, embedder, search_mod, callAPI_mod
    from pdf_loader import text_extracter_into_chunks
    from embedder   import embed_sentences
    from search     import create_faiss_index
    from callAPI    import format_LLM
    pdf_loader  = text_extracter_into_chunks
    embedder    = embed_sentences
    search_mod  = create_faiss_index
    callAPI_mod = format_LLM

# ── state ─────────────────────────────────────────────────────────────────────
chunks        = []
pdf_embeddings = None

# ── helpers ───────────────────────────────────────────────────────────────────
def append_output(text, tag=None):
    output_box.config(state="normal")
    output_box.insert("end", text + "\n", tag or "")
    output_box.see("end")
    output_box.config(state="disabled")

def set_status(msg, color="#a0c4ff"):
    status_var.set(msg)
    status_label.config(fg=color)

def set_ui_busy(busy: bool):
    state = "disabled" if busy else "normal"
    load_btn.config(state=state)
    ask_btn.config(state=state)
    question_entry.config(state=state)

# ── load PDF ──────────────────────────────────────────────────────────────────
def load_pdf():
    path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not path:
        return
    file_label.config(text=Path(path).name)
    set_status("Loading & embedding PDF…", "#ffd166")
    set_ui_busy(True)
    output_box.config(state="normal")
    output_box.delete("1.0", "end")
    output_box.config(state="disabled")

    def worker():
        global chunks, pdf_embeddings
        try:
            lazy_import()
            chunks         = pdf_loader(path)
            pdf_embeddings = embedder(chunks)
            root.after(0, lambda: set_status(f"✓ Ready — {len(chunks)} chunks loaded", "#06d6a0"))
        except Exception as e:
            root.after(0, lambda: set_status(f"Error: {e}", "#ef476f"))
        finally:
            root.after(0, lambda: set_ui_busy(False))

    threading.Thread(target=worker, daemon=True).start()

# ── ask question ──────────────────────────────────────────────────────────────
def ask_question():
    if pdf_embeddings is None:
        messagebox.showwarning("No PDF", "Please load a PDF first.")
        return
    question = question_entry.get().strip()
    if not question:
        messagebox.showwarning("Empty", "Please enter a question.")
        return

    append_output(f"Q: {question}", "question")
    set_status("Thinking…", "#ffd166")
    set_ui_busy(True)

    def worker():
        try:
            I           = search_mod(pdf_embeddings, question, pdf_embeddings.shape[1])
            top_matches = [chunks[i] for i in I[0]]
            answer      = callAPI_mod(question, top_matches)
            root.after(0, lambda: append_output(f"A: {answer}\n", "answer"))
            root.after(0, lambda: set_status("✓ Done", "#06d6a0"))
        except Exception as e:
            root.after(0, lambda: append_output(f"Error: {e}", "error"))
            root.after(0, lambda: set_status("Error", "#ef476f"))
        finally:
            root.after(0, lambda: set_ui_busy(False))

    threading.Thread(target=worker, daemon=True).start()

def on_enter(event):
    ask_question()

# ── build UI ──────────────────────────────────────────────────────────────────
BG      = "#0d1117"
SURFACE = "#161b22"
BORDER  = "#30363d"
ACCENT  = "#58a6ff"
GREEN   = "#06d6a0"
TEXT    = "#e6edf3"
MUTED   = "#8b949e"

root = tk.Tk()
root.title("PDF Q&A")
root.configure(bg=BG)
root.geometry("780x620")
root.resizable(True, True)

# fonts
import tkinter.font as tkfont
title_font   = tkfont.Font(family="Georgia", size=15, weight="bold")
label_font   = tkfont.Font(family="Courier", size=9)
mono_font    = tkfont.Font(family="Courier", size=10)
button_font  = tkfont.Font(family="Courier", size=10, weight="bold")

# ── header ────────────────────────────────────────────────────────────────────
header = tk.Frame(root, bg=SURFACE, pady=14)
header.pack(fill="x")
tk.Label(header, text="PDF Q&A", font=title_font,
         bg=SURFACE, fg=ACCENT).pack()
tk.Label(header, text="ask questions about any PDF",
         font=label_font, bg=SURFACE, fg=MUTED).pack()

# ── file row ──────────────────────────────────────────────────────────────────
file_row = tk.Frame(root, bg=BG, pady=12, padx=20)
file_row.pack(fill="x")

load_btn = tk.Button(file_row, text="[ load pdf ]", font=button_font,
                     bg=SURFACE, fg=ACCENT, activebackground=BORDER,
                     activeforeground=ACCENT, relief="flat", cursor="hand2",
                     bd=0, padx=12, pady=6, command=load_pdf)
load_btn.pack(side="left")

file_label = tk.Label(file_row, text="no file selected", font=label_font,
                      bg=BG, fg=MUTED)
file_label.pack(side="left", padx=14)

# ── output box ────────────────────────────────────────────────────────────────
out_frame = tk.Frame(root, bg=BORDER, padx=1, pady=1)
out_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

output_box = scrolledtext.ScrolledText(
    out_frame, font=mono_font, bg=SURFACE, fg=TEXT,
    insertbackground=ACCENT, relief="flat", state="disabled",
    wrap="word", padx=14, pady=12,
    selectbackground=ACCENT, selectforeground=BG
)
output_box.pack(fill="both", expand=True)
output_box.tag_config("question", foreground=ACCENT)
output_box.tag_config("answer",   foreground=GREEN)
output_box.tag_config("error",    foreground="#ef476f")

# ── question row ─────────────────────────────────────────────────────────────
q_frame = tk.Frame(root, bg=BG, padx=20, pady=6)
q_frame.pack(fill="x")

question_entry = tk.Entry(q_frame, font=mono_font, bg=SURFACE, fg=TEXT,
                          insertbackground=ACCENT, relief="flat",
                          bd=0, highlightthickness=1,
                          highlightbackground=BORDER,
                          highlightcolor=ACCENT)
question_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
question_entry.bind("<Return>", on_enter)

ask_btn = tk.Button(q_frame, text="[ ask ]", font=button_font,
                    bg=ACCENT, fg=BG, activebackground="#79b8ff",
                    activeforeground=BG, relief="flat", cursor="hand2",
                    bd=0, padx=14, pady=8, command=ask_question)
ask_btn.pack(side="right")

# ── status bar ────────────────────────────────────────────────────────────────
status_var = tk.StringVar(value="load a PDF to get started")
status_label = tk.Label(root, textvariable=status_var, font=label_font,
                        bg=SURFACE, fg=MUTED, anchor="w", padx=20, pady=6)
status_label.pack(fill="x", side="bottom")

root.mainloop()
