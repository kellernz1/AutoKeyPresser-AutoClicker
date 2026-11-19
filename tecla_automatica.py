import ctypes
import threading
import time
import tkinter as tk
from ctypes import wintypes
from tkinter import messagebox, ttk


if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ctypes.c_ulonglong
else:
    ULONG_PTR = ctypes.c_ulong


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ULONG_PTR),
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ULONG_PTR),
    ]


class INPUT_UNION(ctypes.Union):
    # MOUSEINPUT ensures the union has the same size/alignment as Windows INPUT.
    _fields_ = [("ki", KEYBDINPUT), ("mi", MOUSEINPUT)]


class INPUT(ctypes.Structure):
    _anonymous_ = ("data",)
    _fields_ = [("type", ctypes.c_ulong), ("data", INPUT_UNION)]


class GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("hwndActive", wintypes.HWND),
        ("hwndFocus", wintypes.HWND),
        ("hwndCapture", wintypes.HWND),
        ("hwndMenuOwner", wintypes.HWND),
        ("hwndMoveSize", wintypes.HWND),
        ("hwndCaret", wintypes.HWND),
        ("rcCaret", wintypes.RECT),
    ]


user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
WM_HOTKEY = 0x0312
WM_QUIT = 0x0012
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
HOTKEY_ID = 1
TOGGLE_KEY = "F8"
CLICKER_HOTKEY_ID = 2
CLICKER_TOGGLE_KEY = "F7"

TARGET_ANY = "Any window (normal)"
TARGET_ACTIVE = "Only while the selected window is active"
TARGET_BACKGROUND = "Send to the selected window in the background"
TARGET_AUTOFOCUS = "Focus window, send input, and switch back (Chrome/games)"
ACTION_HOLD = "Hold for the selected duration"
ACTION_REPEAT = "Press repeatedly"
POSITION_CURRENT = "Current mouse position"
POSITION_FIXED = "Fixed position"
SW_RESTORE = 9

user32.GetForegroundWindow.restype = wintypes.HWND
user32.IsWindow.argtypes = (wintypes.HWND,)
user32.IsWindow.restype = wintypes.BOOL
user32.PostMessageW.argtypes = (
    wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM
)
user32.PostMessageW.restype = wintypes.BOOL
user32.GetWindowThreadProcessId.argtypes = (wintypes.HWND, ctypes.c_void_p)
user32.GetWindowThreadProcessId.restype = wintypes.DWORD
user32.GetGUIThreadInfo.argtypes = (wintypes.DWORD, ctypes.POINTER(GUITHREADINFO))
user32.GetGUIThreadInfo.restype = wintypes.BOOL
user32.IsChild.argtypes = (wintypes.HWND, wintypes.HWND)
user32.IsChild.restype = wintypes.BOOL
user32.SetForegroundWindow.argtypes = (wintypes.HWND,)
user32.SetForegroundWindow.restype = wintypes.BOOL
user32.BringWindowToTop.argtypes = (wintypes.HWND,)
user32.BringWindowToTop.restype = wintypes.BOOL
user32.IsIconic.argtypes = (wintypes.HWND,)
user32.IsIconic.restype = wintypes.BOOL


VK_NAMES = {
    "BACKSPACE": 0x08,
    "TAB": 0x09,
    "ENTER": 0x0D,
    "SHIFT": 0x10,
    "CTRL": 0x11,
    "CONTROL": 0x11,
    "ALT": 0x12,
    "PAUSE": 0x13,
    "CAPSLOCK": 0x14,
    "ESC": 0x1B,
    "ESCAPE": 0x1B,
    "SPACE": 0x20,
    "PAGEUP": 0x21,
    "PAGEDOWN": 0x22,
    "END": 0x23,
    "HOME": 0x24,
    "LEFT": 0x25,
    "UP": 0x26,
    "RIGHT": 0x27,
    "DOWN": 0x28,
    "PRINTSCREEN": 0x2C,
    "INSERT": 0x2D,
    "DELETE": 0x2E,
    "WIN": 0x5B,
    "WINDOWS": 0x5B,
    "MENU": 0x5D,
    "NUM0": 0x60,
    "NUM1": 0x61,
    "NUM2": 0x62,
    "NUM3": 0x63,
    "NUM4": 0x64,
    "NUM5": 0x65,
    "NUM6": 0x66,
    "NUM7": 0x67,
    "NUM8": 0x68,
    "NUM9": 0x69,
    "MULTIPLY": 0x6A,
    "ADD": 0x6B,
    "SUBTRACT": 0x6D,
    "DECIMAL": 0x6E,
    "DIVIDE": 0x6F,
    "NUMLOCK": 0x90,
    "SCROLLLOCK": 0x91,
}

for number in range(1, 25):
    VK_NAMES[f"F{number}"] = 0x6F + number

for character in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    VK_NAMES[character] = ord(character)


KEYSYM_TO_NAME = {
    "Return": "ENTER",
    "space": "SPACE",
    "Escape": "ESC",
    "BackSpace": "BACKSPACE",
    "Tab": "TAB",
    "Delete": "DELETE",
    "Insert": "INSERT",
    "Home": "HOME",
    "End": "END",
    "Prior": "PAGEUP",
    "Next": "PAGEDOWN",
    "Left": "LEFT",
    "Right": "RIGHT",
    "Up": "UP",
    "Down": "DOWN",
    "Shift_L": "SHIFT",
    "Shift_R": "SHIFT",
    "Control_L": "CTRL",
    "Control_R": "CTRL",
    "Alt_L": "ALT",
    "Alt_R": "ALT",
    "Caps_Lock": "CAPSLOCK",
    "Num_Lock": "NUMLOCK",
    "Scroll_Lock": "SCROLLLOCK",
    "Print": "PRINTSCREEN",
}


def send_key(vk_code, is_down):
    flags = 0 if is_down else KEYEVENTF_KEYUP
    event = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(vk_code, 0, flags, 0, 0))
    if user32.SendInput(1, ctypes.byref(event), ctypes.sizeof(INPUT)) != 1:
        raise ctypes.WinError(ctypes.get_last_error())


MOUSE_FLAGS = {
    "Left": (0x0002, 0x0004),
    "Right": (0x0008, 0x0010),
    "Middle": (0x0020, 0x0040),
}


def send_mouse_button(button, is_down):
    down_flag, up_flag = MOUSE_FLAGS[button]
    event = INPUT(
        type=0,
        mi=MOUSEINPUT(0, 0, 0, down_flag if is_down else up_flag, 0, 0),
    )
    if user32.SendInput(1, ctypes.byref(event), ctypes.sizeof(INPUT)) != 1:
        raise ctypes.WinError(ctypes.get_last_error())


def post_key(hwnd, vk_code, is_down):
    thread_id = user32.GetWindowThreadProcessId(hwnd, None)
    gui_info = GUITHREADINFO(cbSize=ctypes.sizeof(GUITHREADINFO))
    message_hwnd = hwnd
    if user32.GetGUIThreadInfo(thread_id, ctypes.byref(gui_info)):
        focused = gui_info.hwndFocus
        if focused and (focused == hwnd or user32.IsChild(hwnd, focused)):
            message_hwnd = focused
    scan_code = user32.MapVirtualKeyW(vk_code, 0)
    message = WM_KEYDOWN if is_down else WM_KEYUP
    lparam = 1 | (scan_code << 16)
    if not is_down:
        lparam |= (1 << 30) | (1 << 31)
    if not user32.PostMessageW(message_hwnd, message, vk_code, lparam):
        raise ctypes.WinError(ctypes.get_last_error())


def list_open_windows(excluded_hwnd=None):
    windows = []
    callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    def collect(hwnd, _lparam):
        if hwnd == excluded_hwnd or not user32.IsWindowVisible(hwnd):
            return True
        length = user32.GetWindowTextLengthW(hwnd)
        if length <= 0:
            return True
        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)
        title = buffer.value.strip()
        if title:
            windows.append((title, int(hwnd)))
        return True

    user32.EnumWindows(callback_type(collect), 0)
    windows.sort(key=lambda item: item[0].casefold())
    return windows


def focus_window(hwnd):
    """Bring a window to the foreground, including from a worker thread."""
    if not user32.IsWindow(hwnd):
        return False
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, SW_RESTORE)

    foreground = user32.GetForegroundWindow()
    current_thread = kernel32.GetCurrentThreadId()
    foreground_thread = (
        user32.GetWindowThreadProcessId(foreground, None) if foreground else 0
    )
    target_thread = user32.GetWindowThreadProcessId(hwnd, None)
    attached_foreground = False
    attached_target = False
    try:
        if foreground_thread and foreground_thread != current_thread:
            attached_foreground = bool(
                user32.AttachThreadInput(current_thread, foreground_thread, True)
            )
        if target_thread and target_thread != current_thread:
            attached_target = bool(
                user32.AttachThreadInput(current_thread, target_thread, True)
            )
        user32.BringWindowToTop(hwnd)
        user32.SetForegroundWindow(hwnd)
    finally:
        if attached_target:
            user32.AttachThreadInput(current_thread, target_thread, False)
        if attached_foreground:
            user32.AttachThreadInput(current_thread, foreground_thread, False)
    return int(user32.GetForegroundWindow()) == int(hwnd)


class KeyAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoKeyPresser and AutoClicker")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.running = False
        self.stop_event = threading.Event()
        self.worker_thread = None
        self.hotkey_thread_id = None
        self.hotkey_ready = threading.Event()
        self.capture_window = None
        self.closing = False
        self.window_map = {}
        self.clicker_running = False
        self.clicker_stop_event = threading.Event()
        self.clicker_thread = None

        self.key_var = tk.StringVar(value="SPACE")
        self.mode_var = tk.StringVar(value=ACTION_HOLD)
        self.target_mode_var = tk.StringVar(value=TARGET_ANY)
        self.target_window_var = tk.StringVar()
        self.duration_var = tk.StringVar(value="1.0")
        self.interval_var = tk.StringVar(value="0.5")
        self.status_var = tk.StringVar(value="DISABLED")
        self.hotkey_status_var = tk.StringVar(value="Registering F8 hotkey...")
        self.clicker_button_var = tk.StringVar(value="Left")
        self.clicker_interval_var = tk.StringVar(value="0.1")
        self.clicker_position_mode_var = tk.StringVar(value=POSITION_CURRENT)
        self.clicker_x_var = tk.StringVar(value="0")
        self.clicker_y_var = tk.StringVar(value="0")
        self.clicker_status_var = tk.StringVar(value="DISABLED")
        self.clicker_hotkey_status_var = tk.StringVar(value="Registering F7 hotkey...")

        self.build_ui()
        self.refresh_windows()
        threading.Thread(target=self.hotkey_loop, daemon=True).start()

    def build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.grid(sticky="nsew", padx=8, pady=8)
        container = ttk.Frame(notebook, padding=18)
        clicker_container = ttk.Frame(notebook, padding=18)
        notebook.add(container, text="  Keyboard  ")
        notebook.add(clicker_container, text="  AutoClicker  ")

        ttk.Label(container, text="Key").grid(row=0, column=0, sticky="w")
        common_keys = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") + [
            "SPACE", "ENTER", "TAB", "ESC", "SHIFT", "CTRL", "ALT",
            "LEFT", "RIGHT", "UP", "DOWN", "HOME", "END", "DELETE",
        ] + [f"F{i}" for i in range(1, 25)]
        self.key_box = ttk.Combobox(
            container, textvariable=self.key_var, values=common_keys, width=24
        )
        self.key_box.grid(row=1, column=0, padx=(0, 8), pady=(4, 12), sticky="ew")
        ttk.Button(container, text="Capture key", command=self.capture_key).grid(
            row=1, column=1, pady=(4, 12), sticky="ew"
        )

        ttk.Label(container, text="Target").grid(row=2, column=0, columnspan=2, sticky="w")
        target_mode_box = ttk.Combobox(
            container,
            textvariable=self.target_mode_var,
            values=(TARGET_ANY, TARGET_ACTIVE, TARGET_BACKGROUND, TARGET_AUTOFOCUS),
            state="readonly",
            width=52,
        )
        target_mode_box.grid(row=3, column=0, columnspan=2, pady=(4, 6), sticky="ew")
        target_mode_box.bind(
            "<<ComboboxSelected>>", lambda _event: self.update_target_fields()
        )

        self.window_box = ttk.Combobox(
            container, textvariable=self.target_window_var, state="disabled", width=39
        )
        self.window_box.grid(row=4, column=0, padx=(0, 8), pady=(0, 12), sticky="ew")
        self.refresh_button = ttk.Button(
            container, text="Refresh windows", command=self.refresh_windows,
            state="disabled",
        )
        self.refresh_button.grid(row=4, column=1, pady=(0, 12), sticky="ew")

        ttk.Label(container, text="Action").grid(row=5, column=0, columnspan=2, sticky="w")
        mode_box = ttk.Combobox(
            container,
            textvariable=self.mode_var,
            values=(ACTION_HOLD, ACTION_REPEAT),
            state="readonly",
            width=38,
        )
        mode_box.grid(row=6, column=0, columnspan=2, pady=(4, 12), sticky="ew")
        mode_box.bind("<<ComboboxSelected>>", lambda _event: self.update_fields())

        ttk.Label(container, text="Hold duration (seconds)").grid(
            row=7, column=0, sticky="w"
        )
        self.duration_entry = ttk.Entry(container, textvariable=self.duration_var, width=15)
        self.duration_entry.grid(row=8, column=0, padx=(0, 8), pady=(4, 12), sticky="ew")

        self.interval_label = ttk.Label(container, text="Interval between repeats (seconds)")
        self.interval_label.grid(row=7, column=1, sticky="w")
        self.interval_entry = ttk.Entry(container, textvariable=self.interval_var, width=15)
        self.interval_entry.grid(row=8, column=1, pady=(4, 12), sticky="ew")

        self.toggle_button = ttk.Button(container, text="ENABLE (F8)", command=self.toggle)
        self.toggle_button.grid(row=9, column=0, columnspan=2, ipady=8, sticky="ew")

        self.status_label = tk.Label(
            container,
            textvariable=self.status_var,
            bg="#8b1e1e",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            padx=8,
            pady=8,
        )
        self.status_label.grid(row=10, column=0, columnspan=2, pady=(12, 4), sticky="ew")
        ttk.Label(container, textvariable=self.hotkey_status_var).grid(
            row=11, column=0, columnspan=2, sticky="w"
        )
        ttk.Label(
            container,
            text="F8 works even when this window is not selected.",
            foreground="#555555",
        ).grid(row=12, column=0, columnspan=2, pady=(3, 0), sticky="w")

        self.update_fields()
        self.update_target_fields()
        self.build_clicker_ui(clicker_container)

    def build_clicker_ui(self, container):
        container.columnconfigure(0, weight=1, uniform="clicker_columns")
        container.columnconfigure(1, weight=1, uniform="clicker_columns")
        for row in (1, 3, 4, 7, 8):
            container.rowconfigure(row, weight=1)

        ttk.Label(container, text="Mouse button").grid(row=0, column=0, sticky="w")
        ttk.Label(container, text="Interval between clicks (seconds)").grid(
            row=0, column=1, sticky="w"
        )
        ttk.Combobox(
            container,
            textvariable=self.clicker_button_var,
            values=("Left", "Right", "Middle"),
            state="readonly",
            width=20,
        ).grid(row=1, column=0, padx=(0, 8), pady=(4, 14), sticky="ew")
        ttk.Entry(
            container, textvariable=self.clicker_interval_var, width=20
        ).grid(row=1, column=1, pady=(4, 14), sticky="ew")

        ttk.Label(container, text="Click position").grid(
            row=2, column=0, columnspan=2, sticky="w"
        )
        position_box = ttk.Combobox(
            container,
            textvariable=self.clicker_position_mode_var,
            values=(POSITION_CURRENT, POSITION_FIXED),
            state="readonly",
            width=42,
        )
        position_box.grid(row=3, column=0, columnspan=2, pady=(4, 8), sticky="ew")
        position_box.bind(
            "<<ComboboxSelected>>", lambda _event: self.update_clicker_fields()
        )

        coordinates = ttk.Frame(container)
        coordinates.grid(row=4, column=0, columnspan=2, pady=(0, 14), sticky="ew")
        ttk.Label(coordinates, text="X:").grid(row=0, column=0, padx=(0, 4))
        self.clicker_x_entry = ttk.Entry(
            coordinates, textvariable=self.clicker_x_var, width=8
        )
        self.clicker_x_entry.grid(row=0, column=1, padx=(0, 12))
        ttk.Label(coordinates, text="Y:").grid(row=0, column=2, padx=(0, 4))
        self.clicker_y_entry = ttk.Entry(
            coordinates, textvariable=self.clicker_y_var, width=8
        )
        self.clicker_y_entry.grid(row=0, column=3, padx=(0, 12))
        self.mouse_position_button = ttk.Button(
            coordinates, text="Use current position", command=self.use_current_mouse_position
        )
        self.mouse_position_button.grid(row=0, column=4)

        self.clicker_toggle_button = ttk.Button(
            container, text="ENABLE AUTOCLICKER (F7)", command=self.toggle_clicker
        )
        self.clicker_toggle_button.grid(
            row=5, column=0, columnspan=2, ipady=8, sticky="ew"
        )
        self.clicker_status_label = tk.Label(
            container,
            textvariable=self.clicker_status_var,
            bg="#8b1e1e",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            padx=8,
            pady=8,
        )
        self.clicker_status_label.grid(
            row=6, column=0, columnspan=2, pady=(12, 4), sticky="ew"
        )
        ttk.Label(container, textvariable=self.clicker_hotkey_status_var).grid(
            row=7, column=0, columnspan=2, sticky="w"
        )
        ttk.Label(
            container,
            text="F7 toggles the AutoClicker. F8 continues to control the keyboard.",
            foreground="#555555",
        ).grid(row=8, column=0, columnspan=2, pady=(3, 0), sticky="w")
        self.update_clicker_fields()

    def update_clicker_fields(self):
        fixed = self.clicker_position_mode_var.get() == POSITION_FIXED
        state = "normal" if fixed else "disabled"
        self.clicker_x_entry.configure(state=state)
        self.clicker_y_entry.configure(state=state)
        self.mouse_position_button.configure(state=state)

    def use_current_mouse_position(self):
        point = wintypes.POINT()
        if user32.GetCursorPos(ctypes.byref(point)):
            self.clicker_x_var.set(str(point.x))
            self.clicker_y_var.set(str(point.y))

    def update_target_fields(self):
        enabled = self.target_mode_var.get() != TARGET_ANY
        self.window_box.configure(state="readonly" if enabled else "disabled")
        self.refresh_button.configure(state="normal" if enabled else "disabled")

    def refresh_windows(self):
        previous_hwnd = self.window_map.get(self.target_window_var.get())
        self.window_map = {}
        selected_display = None
        for title, hwnd in list_open_windows(int(self.root.winfo_id())):
            display = f"{title}  [0x{hwnd:X}]"
            self.window_map[display] = hwnd
            if hwnd == previous_hwnd:
                selected_display = display
        values = list(self.window_map)
        self.window_box.configure(values=values)
        if selected_display:
            self.target_window_var.set(selected_display)
        elif values:
            self.target_window_var.set(values[0])
        else:
            self.target_window_var.set("")

    def update_fields(self):
        repeating = self.mode_var.get() == ACTION_REPEAT
        state = "normal" if repeating else "disabled"
        self.interval_entry.configure(state=state)
        self.interval_label.configure(state=state)

    def capture_key(self):
        if self.capture_window is not None:
            return
        window = tk.Toplevel(self.root)
        self.capture_window = window
        window.title("Capture key")
        window.resizable(False, False)
        window.transient(self.root)
        window.grab_set()
        ttk.Label(window, text="Press the desired key...", padding=24).grid()
        window.bind("<KeyPress>", self.on_captured_key)
        window.protocol("WM_DELETE_WINDOW", self.finish_capture)
        window.focus_force()

    def on_captured_key(self, event):
        name = KEYSYM_TO_NAME.get(event.keysym)
        if name is None:
            candidate = event.keysym.upper()
            if candidate in VK_NAMES:
                name = candidate
        if name is None:
            messagebox.showwarning(
                "Unrecognized key",
                "This key could not be recognized. Try another one.",
                parent=self.capture_window,
            )
            return "break"
        if name in (TOGGLE_KEY, CLICKER_TOGGLE_KEY):
            messagebox.showwarning(
                "Reserved key",
                "F7 and F8 are reserved for the program hotkeys.",
                parent=self.capture_window,
            )
            return "break"
        self.key_var.set(name)
        self.finish_capture()
        return "break"

    def finish_capture(self):
        if self.capture_window is not None:
            self.capture_window.grab_release()
            self.capture_window.destroy()
            self.capture_window = None

    def read_settings(self):
        key_name = self.key_var.get().strip().upper()
        if key_name in (TOGGLE_KEY, CLICKER_TOGGLE_KEY):
            raise ValueError("F7 and F8 are reserved for the program hotkeys.")
        if key_name not in VK_NAMES:
            raise ValueError("Invalid key. Use 'Capture key' to select it.")
        try:
            duration = float(self.duration_var.get().replace(",", "."))
            interval = float(self.interval_var.get().replace(",", "."))
        except ValueError as error:
            raise ValueError("Time values must be numbers, for example: 1.5") from error
        if duration <= 0:
            raise ValueError("The hold duration must be greater than zero.")
        if interval < 0:
            raise ValueError("The interval cannot be negative.")
        target_mode = self.target_mode_var.get()
        target_hwnd = None
        if target_mode != TARGET_ANY:
            target_hwnd = self.window_map.get(self.target_window_var.get())
            if not target_hwnd or not user32.IsWindow(target_hwnd):
                raise ValueError("Select a valid window and click Refresh windows.")
        return (
            VK_NAMES[key_name], duration, interval, self.mode_var.get(),
            target_mode, target_hwnd,
        )

    def toggle(self):
        if self.running:
            self.stop()
            return
        try:
            settings = self.read_settings()
        except ValueError as error:
            messagebox.showerror("Invalid settings", str(error), parent=self.root)
            return

        self.running = True
        self.stop_event.clear()
        self.set_status(True)
        self.worker_thread = threading.Thread(
            target=self.run_action, args=settings, daemon=True
        )
        self.worker_thread.start()

    def stop(self):
        self.stop_event.set()
        self.set_status(False)

    def set_status(self, active):
        if active:
            self.status_var.set("ENABLED — PRESS F8 TO STOP")
            self.status_label.configure(bg="#18733c")
            self.toggle_button.configure(text="DISABLE (F8)")
        else:
            self.status_var.set("DISABLED")
            self.status_label.configure(bg="#8b1e1e")
            self.toggle_button.configure(text="ENABLE (F8)")

    def set_waiting_status(self):
        if self.running:
            self.status_var.set("WAITING FOR THE SELECTED WINDOW")
            self.status_label.configure(bg="#9a6700")

    def target_is_ready(self, target_mode, target_hwnd):
        if target_mode == TARGET_ANY:
            return True
        if not user32.IsWindow(target_hwnd):
            raise RuntimeError("The selected window was closed.")
        if target_mode == TARGET_ACTIVE:
            return int(user32.GetForegroundWindow()) == target_hwnd
        return True

    def begin_autofocus(self, target_mode, target_hwnd):
        if target_mode != TARGET_AUTOFOCUS:
            return None
        previous_hwnd = int(user32.GetForegroundWindow() or 0)
        if not focus_window(target_hwnd):
            raise RuntimeError(
                "Windows did not allow the selected window to receive focus. "
                "Try running the program as administrator."
            )
        # Chrome needs a short delay to deliver focus to the page.
        if self.interruptible_wait(0.08):
            return previous_hwnd
        return previous_hwnd

    def restore_previous_window(self, target_mode, previous_hwnd):
        if (
            target_mode == TARGET_AUTOFOCUS
            and previous_hwnd
            and user32.IsWindow(previous_hwnd)
        ):
            focus_window(previous_hwnd)

    def dispatch_key(self, vk_code, is_down, target_mode, target_hwnd):
        if target_mode == TARGET_BACKGROUND:
            post_key(target_hwnd, vk_code, is_down)
        else:
            send_key(vk_code, is_down)

    def interruptible_wait(self, seconds):
        return self.stop_event.wait(seconds)

    def run_action(self, vk_code, duration, interval, mode, target_mode, target_hwnd):
        key_is_down = False
        previous_hwnd = None
        try:
            repeat = mode == ACTION_REPEAT
            while not self.stop_event.is_set():
                if not self.target_is_ready(target_mode, target_hwnd):
                    self.root.after(0, self.set_waiting_status)
                    if self.interruptible_wait(0.1):
                        break
                    continue

                self.root.after(0, self.set_status, True)
                previous_hwnd = self.begin_autofocus(target_mode, target_hwnd)
                if self.stop_event.is_set():
                    self.restore_previous_window(target_mode, previous_hwnd)
                    break
                self.dispatch_key(vk_code, True, target_mode, target_hwnd)
                key_is_down = True
                deadline = time.monotonic() + duration
                while not self.stop_event.is_set() and time.monotonic() < deadline:
                    focus_required = target_mode in (TARGET_ACTIVE, TARGET_AUTOFOCUS)
                    if focus_required and int(user32.GetForegroundWindow()) != target_hwnd:
                        break
                    remaining = max(0, deadline - time.monotonic())
                    self.interruptible_wait(min(0.02, remaining))

                self.dispatch_key(vk_code, False, target_mode, target_hwnd)
                key_is_down = False
                self.restore_previous_window(target_mode, previous_hwnd)
                if not repeat or self.stop_event.is_set():
                    break
                if self.interruptible_wait(interval):
                    break
        except Exception as error:
            self.root.after(
                0,
                lambda error=error: messagebox.showerror(
                    "Keyboard input error", str(error), parent=self.root
                ),
            )
        finally:
            if key_is_down:
                try:
                    self.dispatch_key(vk_code, False, target_mode, target_hwnd)
                except Exception:
                    pass
            self.restore_previous_window(target_mode, previous_hwnd)
            if not self.closing:
                self.root.after(0, self.action_finished)

    def action_finished(self):
        self.running = False
        self.stop_event.set()
        self.set_status(False)

    def read_clicker_settings(self):
        try:
            interval = float(self.clicker_interval_var.get().replace(",", "."))
        except ValueError as error:
            raise ValueError("The interval must be a number, for example: 0.1") from error
        if interval < 0.01:
            raise ValueError("The minimum interval is 0.01 second.")

        fixed = self.clicker_position_mode_var.get() == POSITION_FIXED
        x = y = None
        if fixed:
            try:
                x = int(self.clicker_x_var.get())
                y = int(self.clicker_y_var.get())
            except ValueError as error:
                raise ValueError("The X and Y coordinates must be integers.") from error
        return self.clicker_button_var.get(), interval, fixed, x, y

    def toggle_clicker(self):
        if self.clicker_running:
            self.stop_clicker()
            return
        try:
            settings = self.read_clicker_settings()
        except ValueError as error:
            messagebox.showerror("Invalid settings", str(error), parent=self.root)
            return

        self.clicker_running = True
        self.clicker_stop_event.clear()
        self.set_clicker_status(True)
        self.clicker_thread = threading.Thread(
            target=self.run_clicker, args=settings, daemon=True
        )
        self.clicker_thread.start()

    def stop_clicker(self):
        self.clicker_stop_event.set()
        self.set_clicker_status(False)

    def set_clicker_status(self, active):
        if active:
            self.clicker_status_var.set("AUTOCLICKER ENABLED — PRESS F7 TO STOP")
            self.clicker_status_label.configure(bg="#18733c")
            self.clicker_toggle_button.configure(text="DISABLE AUTOCLICKER (F7)")
        else:
            self.clicker_status_var.set("DISABLED")
            self.clicker_status_label.configure(bg="#8b1e1e")
            self.clicker_toggle_button.configure(text="ENABLE AUTOCLICKER (F7)")

    def run_clicker(self, button, interval, fixed, x, y):
        mouse_is_down = False
        try:
            while not self.clicker_stop_event.is_set():
                original_position = wintypes.POINT()
                if fixed:
                    user32.GetCursorPos(ctypes.byref(original_position))
                    if not user32.SetCursorPos(x, y):
                        raise ctypes.WinError(ctypes.get_last_error())

                send_mouse_button(button, True)
                mouse_is_down = True
                if self.clicker_stop_event.wait(0.01):
                    break
                send_mouse_button(button, False)
                mouse_is_down = False

                if fixed:
                    user32.SetCursorPos(original_position.x, original_position.y)
                if self.clicker_stop_event.wait(interval):
                    break
        except Exception as error:
            if not self.closing:
                self.root.after(
                    0,
                    lambda error=error: messagebox.showerror(
                        "AutoClicker error", str(error), parent=self.root
                    ),
                )
        finally:
            if mouse_is_down:
                try:
                    send_mouse_button(button, False)
                except Exception:
                    pass
            if fixed and "original_position" in locals():
                user32.SetCursorPos(original_position.x, original_position.y)
            if not self.closing:
                self.root.after(0, self.clicker_finished)

    def clicker_finished(self):
        self.clicker_running = False
        self.clicker_stop_event.set()
        self.set_clicker_status(False)

    def hotkey_loop(self):
        self.hotkey_thread_id = kernel32.GetCurrentThreadId()
        keyboard_registered = bool(
            user32.RegisterHotKey(None, HOTKEY_ID, 0, VK_NAMES[TOGGLE_KEY])
        )
        clicker_registered = bool(
            user32.RegisterHotKey(
                None, CLICKER_HOTKEY_ID, 0, VK_NAMES[CLICKER_TOGGLE_KEY]
            )
        )
        self.root.after(0, self.hotkey_result, keyboard_registered, clicker_registered)
        self.hotkey_ready.set()
        if not keyboard_registered and not clicker_registered:
            return

        message = wintypes.MSG()
        try:
            while user32.GetMessageW(ctypes.byref(message), None, 0, 0) > 0:
                if message.message == WM_HOTKEY and message.wParam == HOTKEY_ID:
                    self.root.after(0, self.toggle)
                elif (
                    message.message == WM_HOTKEY
                    and message.wParam == CLICKER_HOTKEY_ID
                ):
                    self.root.after(0, self.toggle_clicker)
        finally:
            if keyboard_registered:
                user32.UnregisterHotKey(None, HOTKEY_ID)
            if clicker_registered:
                user32.UnregisterHotKey(None, CLICKER_HOTKEY_ID)

    def hotkey_result(self, keyboard_registered, clicker_registered):
        if keyboard_registered:
            self.hotkey_status_var.set("Global F8 hotkey ready.")
        else:
            self.hotkey_status_var.set("F8 unavailable; use the window button.")
        if clicker_registered:
            self.clicker_hotkey_status_var.set("Global F7 hotkey ready.")
        else:
            self.clicker_hotkey_status_var.set("F7 unavailable; use the window button.")

    def close(self):
        self.closing = True
        self.stop()
        self.stop_clicker()
        self.finish_capture()
        if self.hotkey_thread_id:
            user32.PostThreadMessageW(self.hotkey_thread_id, WM_QUIT, 0, 0)
        self.root.destroy()


def main():
    root = tk.Tk()
    KeyAutomationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
