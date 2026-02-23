"""
gui.py
------
Interface gráfica Tkinter para o Validador de Bandeiras de Cartão de Crédito.
Sem dependências externas — apenas Python stdlib.
"""

import tkinter as tk
from tkinter import font as tkfont

from validator import validate_card


# ---------------------------------------------------------------------------
# Paleta de cores por bandeira
# ---------------------------------------------------------------------------
BRAND_COLORS: dict[str, dict] = {
    "Visa":             {"bg": "#1A1F71", "fg": "#FFFFFF"},
    "MasterCard":       {"bg": "#EB001B", "fg": "#FFFFFF"},
    "American Express": {"bg": "#007BC1", "fg": "#FFFFFF"},
    "Diners Club":      {"bg": "#004A97", "fg": "#FFFFFF"},
    "Discover":         {"bg": "#FF6600", "fg": "#FFFFFF"},
    "EnRoute":          {"bg": "#2E8B57", "fg": "#FFFFFF"},
    "JCB":              {"bg": "#003087", "fg": "#FFFFFF"},
    "Voyager":          {"bg": "#6A0DAD", "fg": "#FFFFFF"},
    "HiperCard":        {"bg": "#C8102E", "fg": "#FFFFFF"},
    "Aura":             {"bg": "#FFD700", "fg": "#000000"},
    None:               {"bg": "#E0E0E0", "fg": "#555555"},
}

# Comprimentos típicos por bandeira (para a barra de progresso)
BRAND_LENGTHS: dict[str, int] = {
    "Visa":             16,
    "MasterCard":       16,
    "American Express": 15,
    "Diners Club":      14,
    "Discover":         16,
    "EnRoute":          15,
    "JCB":              16,
    "Voyager":          15,
    "HiperCard":        16,
    "Aura":             16,
}

WINDOW_BG   = "#F4F6F9"
CARD_BG     = "#FFFFFF"
LABEL_FG    = "#333333"
HINT_FG     = "#888888"
GREEN       = "#28A745"
RED         = "#DC3545"
NEUTRAL     = "#6C757D"


class App(tk.Tk):
    """Janela principal do Validador de Cartão de Crédito."""

    def __init__(self):
        super().__init__()

        self.title("Validador de Bandeiras de Cartão de Crédito")
        self.resizable(False, False)
        self.configure(bg=WINDOW_BG)

        # Centraliza na tela
        self.update_idletasks()
        w, h = 520, 380
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        self._build_fonts()
        self._build_ui()

    # ------------------------------------------------------------------
    # Fontes
    # ------------------------------------------------------------------
    def _build_fonts(self):
        self.font_title   = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.font_label   = tkfont.Font(family="Segoe UI", size=10)
        self.font_hint    = tkfont.Font(family="Segoe UI", size=9, slant="italic")
        self.font_brand   = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.font_status  = tkfont.Font(family="Segoe UI", size=11)
        self.font_entry   = tkfont.Font(family="Courier New", size=15)
        self.font_btn     = tkfont.Font(family="Segoe UI", size=10, weight="bold")

    # ------------------------------------------------------------------
    # Construção da UI
    # ------------------------------------------------------------------
    def _build_ui(self):
        # --- Título ---
        tk.Label(
            self, text="Validador de Cartão de Crédito",
            font=self.font_title, bg=WINDOW_BG, fg=LABEL_FG
        ).pack(pady=(22, 4))

        tk.Label(
            self, text="Digite o número e a bandeira será identificada automaticamente",
            font=self.font_hint, bg=WINDOW_BG, fg=HINT_FG
        ).pack(pady=(0, 16))

        # --- Card container ---
        card = tk.Frame(self, bg=CARD_BG, bd=0, relief="flat",
                        highlightbackground="#D0D0D0", highlightthickness=1)
        card.pack(padx=32, fill="x")

        # Label do campo
        tk.Label(card, text="Número do Cartão", font=self.font_label,
                 bg=CARD_BG, fg=LABEL_FG, anchor="w").pack(
            padx=18, pady=(14, 2), fill="x")

        # Frame do entry
        entry_frame = tk.Frame(card, bg=CARD_BG)
        entry_frame.pack(padx=18, fill="x")

        self._card_var = tk.StringVar()
        self._card_var.trace_add("write", self._on_change)

        vcmd = (self.register(self._validate_input), "%P")
        self._entry = tk.Entry(
            entry_frame,
            textvariable=self._card_var,
            font=self.font_entry,
            validate="key",
            validatecommand=vcmd,
            bd=1, relief="solid",
            fg=LABEL_FG,
            insertbackground=LABEL_FG,
            highlightthickness=2,
            highlightcolor="#007BC1",
            highlightbackground="#CCCCCC",
        )
        self._entry.pack(side="left", fill="x", expand=True, ipady=8)
        self._entry.bind("<<Paste>>", self._on_paste)

        # Botão limpar
        self._btn_clear = tk.Button(
            entry_frame, text="✕", font=self.font_btn,
            bg="#F0F0F0", fg=NEUTRAL, relief="flat", bd=0,
            cursor="hand2", padx=10,
            command=self._clear,
            activebackground="#E0E0E0",
        )
        self._btn_clear.pack(side="left", padx=(6, 0), ipady=8)

        # Hint de comprimento
        self._len_label = tk.Label(
            card, text="0 dígitos", font=self.font_hint,
            bg=CARD_BG, fg=HINT_FG, anchor="e"
        )
        self._len_label.pack(padx=18, pady=(2, 14), fill="x")

        # --- Barra de progresso simples ---
        progress_bg = tk.Frame(self, bg="#E0E0E0", height=6)
        progress_bg.pack(padx=32, fill="x")
        progress_bg.pack_propagate(False)

        self._progress_bar = tk.Frame(progress_bg, bg="#CCCCCC", height=6)
        self._progress_bar.place(x=0, y=0, relheight=1, relwidth=0)

        # --- Resultado: bandeira ---
        result_frame = tk.Frame(self, bg=WINDOW_BG)
        result_frame.pack(pady=(18, 0), padx=32, fill="x")

        tk.Label(result_frame, text="Bandeira detectada:", font=self.font_label,
                 bg=WINDOW_BG, fg=HINT_FG).pack(anchor="w")

        self._brand_badge = tk.Label(
            result_frame, text="—",
            font=self.font_brand,
            bg=BRAND_COLORS[None]["bg"],
            fg=BRAND_COLORS[None]["fg"],
            padx=20, pady=8,
            anchor="center",
            relief="flat",
        )
        self._brand_badge.pack(fill="x", pady=(4, 0))

        # --- Status Luhn ---
        self._status_label = tk.Label(
            self, text="Aguardando número...",
            font=self.font_status,
            bg=WINDOW_BG, fg=NEUTRAL
        )
        self._status_label.pack(pady=(10, 0))

        # Foca no entry ao abrir
        self._entry.focus_set()

    # ------------------------------------------------------------------
    # Validação de input (aceita apenas dígitos, máx 19 chars)
    # ------------------------------------------------------------------
    def _validate_input(self, new_value: str) -> bool:
        return new_value == "" or (new_value.isdigit() and len(new_value) <= 19)

    # ------------------------------------------------------------------
    # Callback de mudança em tempo real
    # ------------------------------------------------------------------
    def _on_change(self, *_):
        number = self._card_var.get()
        result = validate_card(number)

        length  = result["length"]
        brand   = result["brand"]
        is_luhn = result["luhn_valid"]

        # ---- Hint de comprimento ----
        self._len_label.configure(text=f"{length} dígito{'s' if length != 1 else ''}")

        # ---- Barra de progresso ----
        max_len = BRAND_LENGTHS.get(brand, 16) if brand else 19
        progress = min(length / max_len, 1.0) if max_len > 0 else 0
        colors = BRAND_COLORS.get(brand, BRAND_COLORS[None])
        self._progress_bar.place(relwidth=progress)
        self._progress_bar.configure(bg=colors["bg"] if brand else "#CCCCCC")

        # ---- Badge de bandeira ----
        if brand:
            self._brand_badge.configure(
                text=brand,
                bg=colors["bg"],
                fg=colors["fg"],
            )
        else:
            if length == 0:
                text = "—"
            elif length < 13:
                text = "digitando..."
            else:
                text = "Desconhecida"
            self._brand_badge.configure(
                text=text,
                bg=BRAND_COLORS[None]["bg"],
                fg=BRAND_COLORS[None]["fg"],
            )

        # ---- Status Luhn ----
        if length == 0:
            self._status_label.configure(text="Aguardando número...", fg=NEUTRAL)
        elif length < 13:
            self._status_label.configure(text="Continue digitando...", fg=NEUTRAL)
        elif brand is None:
            self._status_label.configure(text="Bandeira não reconhecida", fg=NEUTRAL)
        elif is_luhn:
            self._status_label.configure(text="✓  Número válido", fg=GREEN)
        else:
            self._status_label.configure(text="✗  Número inválido", fg=RED)

    # ------------------------------------------------------------------
    # Cola (strip de não-dígitos antes de inserir)
    # ------------------------------------------------------------------
    def _on_paste(self, event):
        try:
            text = self.clipboard_get()
        except tk.TclError:
            return "break"

        digits = "".join(c for c in text if c.isdigit())
        if not digits:
            return "break"

        current = self._card_var.get()
        pos = self._entry.index(tk.INSERT)

        # Substitui a seleção, se houver
        try:
            sel_start = self._entry.index(tk.SEL_FIRST)
            sel_end   = self._entry.index(tk.SEL_LAST)
            new_value = current[:sel_start] + digits + current[sel_end:]
            new_pos   = sel_start + len(digits)
        except tk.TclError:
            new_value = current[:pos] + digits + current[pos:]
            new_pos   = pos + len(digits)

        new_value = new_value[:19]          # respeita o limite máximo
        new_pos   = min(new_pos, len(new_value))

        self._card_var.set(new_value)
        self._entry.icursor(new_pos)
        return "break"                      # impede o comportamento padrão

    # ------------------------------------------------------------------
    # Limpar
    # ------------------------------------------------------------------
    def _clear(self):
        self._card_var.set("")
        self._entry.focus_set()
