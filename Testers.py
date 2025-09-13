import tkinter as tk
import random
import time

class SkillTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Skill Test Arcade")
        self.root.geometry("560x560")
        self.after_ids = []
        self.main_menu()

    # ---------- Utilities ----------
    def schedule(self, ms, func):
        aid = self.root.after(ms, func)
        self.after_ids.append(aid)
        return aid

    def cancel_all_after(self):
        for aid in self.after_ids:
            try:
                self.root.after_cancel(aid)
            except Exception:
                pass
        self.after_ids.clear()

    def unbind_common(self):
        for ev in ["<space>", "<Double-Button-1>", "<Button-1>", "<ButtonPress-1>", "<ButtonRelease-1>",
                   "<MouseWheel>", "<Button-4>", "<Button-5>", "<Key>", "<KeyPress>", "<KeyRelease>"]:
            try:
                self.root.unbind(ev)
            except Exception:
                pass

    def clear_window(self):
        self.cancel_all_after()
        self.unbind_common()
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------- Main menu ----------
    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="🎯 Skill Test Arcade", font=("Arial", 22, "bold")).pack(pady=16)

        testers = [
            ("1. Click Speed Test", self.click_speed_test),
            ("2. Spacebar Click Test", self.spacebar_test),
            ("3. Reaction Time Test", self.reaction_time_test),
            ("4. Double Click Test", self.double_click_test),
            ("5. Typing Speed Test", self.typing_speed_test),
            ("6. Aim Trainer", self.aim_trainer),
            ("7. Hold Duration Test", self.hold_duration_test),
            ("8. Scroll Speed Test", self.scroll_speed_test),
            ("9. Key Sequence Test", self.key_sequence_test),
            ("10. Memory Click Test", self.memory_click_test),
        ]

        for name, func in testers:
            tk.Button(self.root, text=name, width=32, height=1, command=func).pack(pady=6)

        tk.Label(self.root, text="Tip: Use Back to Menu to switch testers.", fg="gray").pack(pady=10)
        tk.Button(self.root, text="Exit", width=32, command=self.root.quit).pack(pady=10)

    # ---------- 1. Click Speed Test ----------
    def click_speed_test(self):
        self.clear_window()
        self.clicks = 0
        self.time_left = 5
        tk.Label(self.root, text="Click Speed Test", font=("Arial", 18, "bold")).pack(pady=8)
        self.timer_label = tk.Label(self.root, text=f"Time: {self.time_left}", font=("Arial", 14))
        self.timer_label.pack()
        self.click_label = tk.Label(self.root, text="Clicks: 0", font=("Arial", 14))
        self.click_label.pack(pady=6)
        self.click_button = tk.Button(self.root, text="Click Me!", font=("Arial", 16), width=14,
                                      state="disabled", command=self.count_click)
        self.click_button.pack(pady=10)
        tk.Button(self.root, text="Start (5s)", command=self.start_click_speed).pack()
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=12)

    def count_click(self):
        self.clicks += 1
        self.click_label.config(text=f"Clicks: {self.clicks}")

    def start_click_speed(self):
        self.clicks = 0
        self.time_left = 5
        self.click_label.config(text="Clicks: 0")
        self.timer_label.config(text=f"Time: {self.time_left}")
        self.click_button.config(state="normal")
        self.update_click_speed_timer()

    def update_click_speed_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.schedule(1000, self.update_click_speed_timer)
        else:
            self.click_button.config(state="disabled")
            cps = round(self.clicks / 5, 2)
            self.timer_label.config(text=f"Done! {self.clicks} clicks ({cps} CPS)")

    # ---------- 2. Spacebar Click Test ----------
    def spacebar_test(self):
        self.clear_window()
        self.space_clicks = 0
        self.time_left = 5
        tk.Label(self.root, text="Spacebar Click Test", font=("Arial", 18, "bold")).pack(pady=8)
        self.space_label = tk.Label(self.root, text="Press SPACE repeatedly for 5 seconds!", font=("Arial", 14))
        self.space_label.pack(pady=6)
        self.timer_s_label = tk.Label(self.root, text="Time: 5", font=("Arial", 14))
        self.timer_s_label.pack()
        self.root.bind("<space>", self.spacebar_press)
        tk.Button(self.root, text="Back to Menu",
                  command=lambda: [self.root.unbind("<space>"), self.main_menu()]).pack(pady=12)
        self.update_space_timer()

    def spacebar_press(self, event):
        self.space_clicks += 1
        self.space_label.config(text=f"Presses: {self.space_clicks}")

    def update_space_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_s_label.config(text=f"Time: {self.time_left}")
            self.schedule(1000, self.update_space_timer)
        else:
            self.root.unbind("<space>")
            cps = round(self.space_clicks / 5, 2)
            self.space_label.config(text=f"Done! {self.space_clicks} presses ({cps} PPS)")

    # ---------- 3. Reaction Time Test ----------
    def reaction_time_test(self):
        self.clear_window()
        tk.Label(self.root, text="Reaction Time Test", font=("Arial", 18, "bold")).pack(pady=8)
        self.react_label = tk.Label(self.root, text="Wait for GREEN, then click!", font=("Arial", 14))
        self.react_label.pack(pady=12)
        self.react_button = tk.Button(self.root, text="Wait...", font=("Arial", 16),
                                      state="disabled", width=18, command=self.stop_reaction_timer)
        self.react_button.pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=12)
        wait_time = random.randint(2000, 5000)
        self.schedule(wait_time, self.start_reaction_timer)

    def start_reaction_timer(self):
        self.react_label.config(text="CLICK NOW!")
        self.react_button.config(state="normal", bg="green", activebackground="green")
        self.start_time = time.time()

    def stop_reaction_timer(self):
        reaction_time = round((time.time() - self.start_time) * 1000, 2)
        self.react_label.config(text=f"Your reaction: {reaction_time} ms")
        self.react_button.config(state="disabled", bg="SystemButtonFace", activebackground="SystemButtonFace")

    # ---------- 4. Double Click Test ----------
    def double_click_test(self):
        self.clear_window()
        self.double_clicks = 0
        self.time_left = 5
        tk.Label(self.root, text="Double Click Test", font=("Arial", 18, "bold")).pack(pady=8)
        self.double_label = tk.Label(self.root, text="Double-click anywhere inside the window!", font=("Arial", 14))
        self.double_label.pack(pady=6)
        self.timer_d_label = tk.Label(self.root, text="Time: 5", font=("Arial", 14))
        self.timer_d_label.pack()
        self.root.bind("<Double-Button-1>", self.double_click)
        tk.Button(self.root, text="Back to Menu",
                  command=lambda: [self.root.unbind("<Double-Button-1>"), self.main_menu()]).pack(pady=12)
        self.update_double_timer()

    def double_click(self, event):
        self.double_clicks += 1
        self.double_label.config(text=f"Double Clicks: {self.double_clicks}")

    def update_double_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_d_label.config(text=f"Time: {self.time_left}")
            self.schedule(1000, self.update_double_timer)
        else:
            self.root.unbind("<Double-Button-1>")
            cps = round(self.double_clicks / 5, 2)
            self.double_label.config(text=f"Done! {self.double_clicks} double clicks ({cps} DPS)")

    # ---------- 5. Typing Speed Test ----------
    def typing_speed_test(self):
        self.clear_window()
        samples = [
            "python tkinter speed test",
            "fast fingers make light work",
            "practice makes perfect typing",
            "arcade games are fun to build",
        ]
        self.sample_text = random.choice(samples)
        tk.Label(self.root, text="Typing Speed Test", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(self.root, text=f"Type this exactly:", font=("Arial", 13)).pack(pady=2)
        tk.Label(self.root, text=self.sample_text, font=("Consolas", 14)).pack(pady=4)
        self.entry = tk.Entry(self.root, font=("Consolas", 14), width=40)
        self.entry.pack(pady=8)
        self.entry.focus_set()
        self.start_time = time.time()
        tk.Button(self.root, text="Submit", command=self.check_typing_speed).pack()
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=12)
        self.result_t_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_t_label.pack(pady=6)

    def check_typing_speed(self):
        typed = self.entry.get()
        elapsed = max(0.001, time.time() - self.start_time)
        if typed.strip() == self.sample_text:
            words = len(typed.split())
            wpm = round((words / elapsed) * 60, 2)
            self.result_t_label.config(text=f"Correct! {words} words in {elapsed:.2f}s → {wpm} WPM")
        else:
            self.result_t_label.config(text="Incorrect text. Try again!")

    # ---------- 6. Aim Trainer ----------
    def aim_trainer(self):
        self.clear_window()
        self.hits = 0
        self.time_left = 10
        tk.Label(self.root, text="Aim Trainer", font=("Arial", 18, "bold")).pack(pady=8)
        self.info_a = tk.Label(self.root, text="Click the red targets. You have 10 seconds.", font=("Arial", 13))
        self.info_a.pack(pady=4)
        self.timer_a_label = tk.Label(self.root, text=f"Time: {self.time_left}", font=("Arial", 14))
        self.timer_a_label.pack()
        self.canvas = tk.Canvas(self.root, width=480, height=360, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(pady=8)
        self.canvas.bind("<Button-1>", self.check_hit)
        self.spawn_target()
        tk.Button(self.root, text="Back to Menu",
                  command=lambda: [self.canvas.unbind("<Button-1>"), self.main_menu()]).pack(pady=12)
        self.update_aim_timer()

    def spawn_target(self):
        self.canvas.delete("all")
        r = 14
        x = random.randint(r, 480 - r)
        y = random.randint(r, 360 - r)
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red", outline="", tags="target")

    def check_hit(self, event):
        ids = self.canvas.find_withtag("target")
        if ids:
            x1, y1, x2, y2 = self.canvas.bbox(ids[0])
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.hits += 1
                self.spawn_target()

    def update_aim_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_a_label.config(text=f"Time: {self.time_left}")
            self.schedule(1000, self.update_aim_timer)
        else:
            self.canvas.unbind("<Button-1>")
            self.info_a.config(text=f"Done! Targets hit: {self.hits}")

    # ---------- 7. Hold Duration Test ----------
    def hold_duration_test(self):
        self.clear_window()
        self.holding = False
        self.hold_start = None
        self.best_hold = 0.0
        tk.Label(self.root, text="Hold Duration Test", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(self.root, text="Press and hold the button. Release to stop.", font=("Arial", 13)).pack(pady=4)
        self.hold_button = tk.Button(self.root, text="Hold Me", font=("Arial", 16), width=16)
        self.hold_button.pack(pady=12)
        self.hold_button.bind("<ButtonPress-1>", self.start_hold)
        self.hold_button.bind("<ButtonRelease-1>", self.end_hold)
        self.hold_label = tk.Label(self.root, text="Current: 0.00s   Best: 0.00s", font=("Arial", 14))
        self.hold_label.pack(pady=6)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=12)

    def start_hold(self, event):
        if not self.holding:
            self.holding = True
            self.hold_start = time.time()
            self.update_hold_display()

    def update_hold_display(self):
        if self.holding and self.hold_start is not None:
            curr = time.time() - self.hold_start
            self.hold_label.config(text=f"Current: {curr:.2f}s   Best: {self.best_hold:.2f}s")
            self.schedule(50, self.update_hold_display)

    def end_hold(self, event):
        if self.holding and self.hold_start is not None:
            duration = time.time() - self.hold_start
            self.best_hold = max(self.best_hold, duration)
            self.holding = False
            self.hold_start = None
            self.hold_label.config(text=f"Current: 0.00s   Best: {self.best_hold:.2f}s")

    # ---------- 8. Scroll Speed Test ----------
    def scroll_speed_test(self):
        self.clear_window()
        self.scrolls = 0
        self.time_left = 5
        tk.Label(self.root, text="Scroll Speed Test", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(self.root, text="Scroll the mouse wheel as fast as you can (5s).", font=("Arial", 13)).pack(pady=4)
        self.scroll_label = tk.Label(self.root, text="Scrolls: 0", font=("Arial", 14))
        self.scroll_label.pack(pady=6)
        self.timer_scroll = tk.Label(self.root, text="Time: 5", font=("Arial", 14))
        self.timer_scroll.pack()
        # Bind for Windows/Mac
        self.root.bind("<MouseWheel>", self.on_scroll)
        # Bind for Linux (X11)
        self.root.bind("<Button-4>", self.on_scroll)
        self.root.bind("<Button-5>", self.on_scroll)
        tk.Button(self.root, text="Back to Menu",
                  command=lambda: [self.unbind_scroll_events(), self.main_menu()]).pack(pady=12)
        self.update_scroll_timer()

    def unbind_scroll_events(self):
        for ev in ["<MouseWheel>", "<Button-4>", "<Button-5>"]:
            try:
                self.root.unbind(ev)
            except Exception:
                pass

    def on_scroll(self, event):
        self.scrolls += 1
        self.scroll_label.config(text=f"Scrolls: {self.scrolls}")

    def update_scroll_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_scroll.config(text=f"Time: {self.time_left}")
            self.schedule(1000, self.update_scroll_timer)
        else:
            self.unbind_scroll_events()
            sps = round(self.scrolls / 5, 2)
            self.scroll_label.config(text=f"Done! {self.scrolls} scrolls ({sps} SPS)")

    # ---------- 9. Key Sequence Test ----------
    def key_sequence_test(self):
        self.clear_window()
        keys_bank = ["A", "S", "D", "F", "J", "K", "L", ";",
                     "W", "E", "R", "U", "I", "O", "1", "2", "3", "4"]
        self.sequence = [random.choice(keys_bank) for _ in range(8)]
        tk.Label(self.root, text="Key Sequence Test", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(self.root, text="Type the sequence in order (ignore caps):", font=("Arial", 13)).pack(pady=4)
        self.seq_label = tk.Label(self.root, text=" ".join(self.sequence), font=("Consolas", 16))
        self.seq_label.pack(pady=8)
        self.progress_label = tk.Label(self.root, text="Progress: 0 / 8", font=("Arial", 14))
        self.progress_label.pack(pady=4)
        self.seq_index = 0
        self.errors = 0
        self.start_time = time.time()
        self.root.bind("<Key>", self.on_key_sequence)
        tk.Button(self.root, text="Back to Menu",
                  command=lambda: [self.root.unbind("<Key>"), self.main_menu()]).pack(pady=12)
        self.result_seq_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_seq_label.pack(pady=6)

    def on_key_sequence(self, event):
        if self.seq_index >= len(self.sequence):
            return
        expected = self.sequence[self.seq_index].lower()
        pressed = (event.char or "").lower()
        # Some keys like ";" may come as ";" in char; fallback to keysym for letters
        if not pressed and event.keysym:
            pressed = event.keysym.lower()
        if pressed == expected.lower():
            self.seq_index += 1
            self.progress_label.config(text=f"Progress: {self.seq_index} / {len(self.sequence)}")
        else:
            self.errors += 1
        if self.seq_index == len(self.sequence):
            elapsed = max(0.001, time.time() - self.start_time)
            kps = round(len(self.sequence) / elapsed, 2)
            self.result_seq_label.config(text=f"Done in {elapsed:.2f}s | Errors: {self.errors} | {kps} keys/s")
            self.root.unbind("<Key>")

    # ---------- 10. Memory Click Test (Simon-style) ----------
    def memory_click_test(self):
        self.clear_window()
        tk.Label(self.root, text="Memory Click Test", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(self.root, text="Watch the sequence, then repeat it by clicking.", font=("Arial", 13)).pack(pady=4)

        self.mem_frame = tk.Frame(self.root)
        self.mem_frame.pack(pady=10)

        # 3x3 grid buttons
        self.mem_buttons = []
        colors = ["#e6e6e6"] * 9
        for i in range(3):
            row = []
            for j in range(3):
                idx = i * 3 + j
                btn = tk.Button(self.mem_frame, text=str(idx+1), width=6, height=3,
                                bg=colors[idx], command=lambda k=idx: self.memory_click(k), state="disabled")
                btn.grid(row=i, column=j, padx=6, pady=6)
                row.append(btn)
            self.mem_buttons.extend(row)

        self.seq_len = 4
        self.memory_seq = [random.randint(0, 8) for _ in range(self.seq_len)]
        self.mem_index = 0
        self.status_mem = tk.Label(self.root, text="Get ready...", font=("Arial", 14))
        self.status_mem.pack(pady=6)

        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=12)
        self.schedule(800, self.play_memory_sequence_step)

    def play_memory_sequence_step(self):
        # Disable during playback
        for b in self.mem_buttons:
            b.config(state="disabled")
        if self.mem_index < len(self.memory_seq):
            k = self.memory_seq[self.mem_index]
            self.flash_button(k)
            self.mem_index += 1
            self.schedule(700, self.play_memory_sequence_step)
        else:
            # Enable for input
            for b in self.mem_buttons:
                b.config(state="normal")
            self.status_mem.config(text="Your turn! Repeat the sequence.")
            self.mem_index = 0
            self.user_progress = []

    def flash_button(self, idx):
        btn = self.mem_buttons[idx]
        orig = btn.cget("bg")
        btn.config(bg="#ffd54f")
        self.schedule(350, lambda: btn.config(bg=orig))

    def memory_click(self, idx):
        if self.mem_index >= len(self.memory_seq):  # safety
            return
        self.user_progress.append(idx)
        expected = self.memory_seq[len(self.user_progress) - 1]
        if idx != expected:
            for b in self.mem_buttons:
                b.config(state="disabled")
            self.status_mem.config(text="Wrong! Sequence failed.")
            return
        if len(self.user_progress) == len(self.memory_seq):
            for b in self.mem_buttons:
                b.config(state="disabled")
            self.status_mem.config(text="Great memory! You got it.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SkillTestApp(root)
    root.mainloop()
import tkinter as tk
import random
import time

class SkillTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Skill Test Arcade")
        self.root.geometry("560x560")
        self.after_ids = []
        self.main_menu()

    # ---------- Utilities ----------
    def schedule(self, ms, func):
        aid = self.root.after(ms, func)
        self.after_ids.append(aid)
        return aid

    def cancel_all_after(self):
        for aid in self.after_ids:
            try:
                self.root.after_cancel(aid)
            except Exception:
                pass
        self.after_ids.clear()

    def unbind_common(self):
        for ev in ["<space>", "<Double-Button-1>", "<Button-1>", "<ButtonPress-1>", "<ButtonRelease-1>",
                   "<MouseWheel>", "<Button-4>", "<Button-5>", "<Key>", "<KeyPress>", "<KeyRelease>"]:
            try:
                self.root.unbind(ev)
            except Exception:
                pass

    def clear_window(self):
        self.cancel_all_after()
        self.unbind_common()
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------- Main menu ----------
    def main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="🎯 Skill Test Arcade", font=("Arial", 22, "bold")).pack(pady=16)

        testers = [
            ("1. Click Speed Test", self.click_speed_test),
            ("2. Spacebar Click Test", self.spacebar_test),
            ("3. Reaction Time Test", self.reaction_time_test),
            ("4. Double Click Test", self.double_click_test),
            ("5. Typing Speed Test", self.typing_speed_test),
            ("6. Aim Trainer", self.aim_trainer),
            ("7. Hold Duration Test", self.hold_duration_test),
            ("8. Scroll Speed Test", self.scroll_speed_test),
            ("9. Key Sequence Test", self.key_sequence_test),
            ("10. Memory Click Test", self.memory_click_test),
        ]

        for name, func in testers:
            tk.Button(self.root, text=name, width=32, height=1, command=func).pack(pady=6)

        tk.Label(self.root, text="Tip: Use Back to Menu to switch testers.", fg="gray").pack(pady=10)
        tk.Button(self.root, text="Exit", width=32, command=self.root.quit).pack(pady=10)

    # ---------- 1. Click Speed Test ----------
    def click_speed_test(self):
        self.clear_window()
        self.clicks = 0
        self.time_left = 5
        tk.Label(self.root, text="Click Speed Test", font=("Arial", 18, "bold")).pack(pady=8)
        self.timer_label = tk.Label(self.root, text=f"Time: {self.time_left}", font=("Arial", 14))
        self.timer_label.pack()
        self.click_label = tk.Label(self.root, text="Clicks: 0", font=("Arial", 14))
        self.click_label.pack(pady=6)
        self.click_button = tk.Button(self.root, text="Click Me!", font=("Arial", 16), width=14,
                                      state="disabled", command=self.count_click)
        self.click_button.pack(pady=10)
        tk.Button(self.root, text="Start (5s)", command=self.start_click_speed).pack()
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=12)

    def count_click(self):
        self.clicks += 1
        self.click_label.config(text=f"Clicks: {self.clicks}")

    def start_click_speed(self):
        self.clicks = 0
        self.time_left = 5
        self.click_label.config(text="Clicks: 0")
        self.timer_label.config(text=f"Time: {self.time_left}")
        self.click_button.config(state="normal")
        self.update_click_speed_timer()

    def update_click_speed_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.schedule(1000, self.update_click_speed_timer)
        else:
            self.click_button.config(state="disabled")
            cps = round(self.clicks / 5, 2)
            self.timer_label.config(text=f"Done! {self.clicks} clicks ({cps} CPS)")

    # ---------- 2. Spacebar Click Test ----------
    def spacebar_test(self):
        self.clear_window()
        self.space_clicks = 0
        self.time_left = 5
        tk.Label(self.root, text="Spacebar Click Test", font=("Arial", 18, "bold")).pack(pady=8)
        self.space_label = tk.Label(self.root, text="Press SPACE repeatedly for 5 seconds!", font=("Arial", 14))
        self.space_label.pack(pady=6)
        self.timer_s_label = tk.Label(self.root, text="Time: 5", font=("Arial", 14))
        self.timer_s_label.pack()
        self.root.bind("<space>", self.spacebar_press)
        tk.Button(self.root, text="Back to Menu",
                  command=lambda: [self.root.unbind("<space>"), self.main_menu()]).pack(pady=12)
        self.update_space_timer()

    def spacebar_press(self, event):
        self.space_clicks += 1
        self.space_label.config(text=f"Presses: {self.space_clicks}")

    def update_space_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_s_label.config(text=f"Time: {self.time_left}")
            self.schedule(1000, self.update_space_timer)
        else:
            self.root.unbind("<space>")
            cps = round(self.space_clicks / 5, 2)
            self.space_label.config(text=f"Done! {self.space_clicks} presses ({cps} PPS)")

    # ---------- 3. Reaction Time Test ----------
    def reaction_time_test(self):
        self.clear_window()
        tk.Label(self.root, text="Reaction Time Test", font=("Arial", 18, "bold")).pack(pady=8)
        self.react_label = tk.Label(self.root, text="Wait for GREEN, then click!", font=("Arial", 14))
        self.react_label.pack(pady=12)
        self.react_button = tk.Button(self.root, text="Wait...", font=("Arial", 16),
                                      state="disabled", width=18, command=self.stop_reaction_timer)
        self.react_button.pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=12)
        wait_time = random.randint(2000, 5000)
        self.schedule(wait_time, self.start_reaction_timer)

    def start_reaction_timer(self):
        self.react_label.config(text="CLICK NOW!")
        self.react_button.config(state="normal", bg="green", activebackground="green")
        self.start_time = time.time()

    def stop_reaction_timer(self):
        reaction_time = round((time.time() - self.start_time) * 1000, 2)
        self.react_label.config(text=f"Your reaction: {reaction_time} ms")
        self.react_button.config(state="disabled", bg="SystemButtonFace", activebackground="SystemButtonFace")

    # ---------- 4. Double Click Test ----------
    def double_click_test(self):
        self.clear_window()
        self.double_clicks = 0
        self.time_left = 5
        tk.Label(self.root, text="Double Click Test", font=("Arial", 18, "bold")).pack(pady=8)
        self.double_label = tk.Label(self.root, text="Double-click anywhere inside the window!", font=("Arial", 14))
        self.double_label.pack(pady=6)
        self.timer_d_label = tk.Label(self.root, text="Time: 5", font=("Arial", 14))
        self.timer_d_label.pack()
        self.root.bind("<Double-Button-1>", self.double_click)
        tk.Button(self.root, text="Back to Menu",
                  command=lambda: [self.root.unbind("<Double-Button-1>"), self.main_menu()]).pack(pady=12)
        self.update_double_timer()

    def double_click(self, event):
        self.double_clicks += 1
        self.double_label.config(text=f"Double Clicks: {self.double_clicks}")

    def update_double_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_d_label.config(text=f"Time: {self.time_left}")
            self.schedule(1000, self.update_double_timer)
        else:
            self.root.unbind("<Double-Button-1>")
            cps = round(self.double_clicks / 5, 2)
            self.double_label.config(text=f"Done! {self.double_clicks} double clicks ({cps} DPS)")

    # ---------- 5. Typing Speed Test ----------
    def typing_speed_test(self):
        self.clear_window()
        samples = [
            "python tkinter speed test",
            "fast fingers make light work",
            "practice makes perfect typing",
            "arcade games are fun to build",
        ]
        self.sample_text = random.choice(samples)
        tk.Label(self.root, text="Typing Speed Test", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(self.root, text=f"Type this exactly:", font=("Arial", 13)).pack(pady=2)
        tk.Label(self.root, text=self.sample_text, font=("Consolas", 14)).pack(pady=4)
        self.entry = tk.Entry(self.root, font=("Consolas", 14), width=40)
        self.entry.pack(pady=8)
        self.entry.focus_set()
        self.start_time = time.time()
        tk.Button(self.root, text="Submit", command=self.check_typing_speed).pack()
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=12)
        self.result_t_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_t_label.pack(pady=6)

    def check_typing_speed(self):
        typed = self.entry.get()
        elapsed = max(0.001, time.time() - self.start_time)
        if typed.strip() == self.sample_text:
            words = len(typed.split())
            wpm = round((words / elapsed) * 60, 2)
            self.result_t_label.config(text=f"Correct! {words} words in {elapsed:.2f}s → {wpm} WPM")
        else:
            self.result_t_label.config(text="Incorrect text. Try again!")

    # ---------- 6. Aim Trainer ----------
    def aim_trainer(self):
        self.clear_window()
        self.hits = 0
        self.time_left = 10
        tk.Label(self.root, text="Aim Trainer", font=("Arial", 18, "bold")).pack(pady=8)
        self.info_a = tk.Label(self.root, text="Click the red targets. You have 10 seconds.", font=("Arial", 13))
        self.info_a.pack(pady=4)
        self.timer_a_label = tk.Label(self.root, text=f"Time: {self.time_left}", font=("Arial", 14))
        self.timer_a_label.pack()
        self.canvas = tk.Canvas(self.root, width=480, height=360, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(pady=8)
        self.canvas.bind("<Button-1>", self.check_hit)
        self.spawn_target()
        tk.Button(self.root, text="Back to Menu",
                  command=lambda: [self.canvas.unbind("<Button-1>"), self.main_menu()]).pack(pady=12)
        self.update_aim_timer()

    def spawn_target(self):
        self.canvas.delete("all")
        r = 14
        x = random.randint(r, 480 - r)
        y = random.randint(r, 360 - r)
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="red", outline="", tags="target")

    def check_hit(self, event):
        ids = self.canvas.find_withtag("target")
        if ids:
            x1, y1, x2, y2 = self.canvas.bbox(ids[0])
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.hits += 1
                self.spawn_target()

    def update_aim_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_a_label.config(text=f"Time: {self.time_left}")
            self.schedule(1000, self.update_aim_timer)
        else:
            self.canvas.unbind("<Button-1>")
            self.info_a.config(text=f"Done! Targets hit: {self.hits}")

    # ---------- 7. Hold Duration Test ----------
    def hold_duration_test(self):
        self.clear_window()
        self.holding = False
        self.hold_start = None
        self.best_hold = 0.0
        tk.Label(self.root, text="Hold Duration Test", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(self.root, text="Press and hold the button. Release to stop.", font=("Arial", 13)).pack(pady=4)
        self.hold_button = tk.Button(self.root, text="Hold Me", font=("Arial", 16), width=16)
        self.hold_button.pack(pady=12)
        self.hold_button.bind("<ButtonPress-1>", self.start_hold)
        self.hold_button.bind("<ButtonRelease-1>", self.end_hold)
        self.hold_label = tk.Label(self.root, text="Current: 0.00s   Best: 0.00s", font=("Arial", 14))
        self.hold_label.pack(pady=6)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=12)

    def start_hold(self, event):
        if not self.holding:
            self.holding = True
            self.hold_start = time.time()
            self.update_hold_display()

    def update_hold_display(self):
        if self.holding and self.hold_start is not None:
            curr = time.time() - self.hold_start
            self.hold_label.config(text=f"Current: {curr:.2f}s   Best: {self.best_hold:.2f}s")
            self.schedule(50, self.update_hold_display)

    def end_hold(self, event):
        if self.holding and self.hold_start is not None:
            duration = time.time() - self.hold_start
            self.best_hold = max(self.best_hold, duration)
            self.holding = False
            self.hold_start = None
            self.hold_label.config(text=f"Current: 0.00s   Best: {self.best_hold:.2f}s")

    # ---------- 8. Scroll Speed Test ----------
    def scroll_speed_test(self):
        self.clear_window()
        self.scrolls = 0
        self.time_left = 5
        tk.Label(self.root, text="Scroll Speed Test", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(self.root, text="Scroll the mouse wheel as fast as you can (5s).", font=("Arial", 13)).pack(pady=4)
        self.scroll_label = tk.Label(self.root, text="Scrolls: 0", font=("Arial", 14))
        self.scroll_label.pack(pady=6)
        self.timer_scroll = tk.Label(self.root, text="Time: 5", font=("Arial", 14))
        self.timer_scroll.pack()
        # Bind for Windows/Mac
        self.root.bind("<MouseWheel>", self.on_scroll)
        # Bind for Linux (X11)
        self.root.bind("<Button-4>", self.on_scroll)
        self.root.bind("<Button-5>", self.on_scroll)
        tk.Button(self.root, text="Back to Menu",
                  command=lambda: [self.unbind_scroll_events(), self.main_menu()]).pack(pady=12)
        self.update_scroll_timer()

    def unbind_scroll_events(self):
        for ev in ["<MouseWheel>", "<Button-4>", "<Button-5>"]:
            try:
                self.root.unbind(ev)
            except Exception:
                pass

    def on_scroll(self, event):
        self.scrolls += 1
        self.scroll_label.config(text=f"Scrolls: {self.scrolls}")

    def update_scroll_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_scroll.config(text=f"Time: {self.time_left}")
            self.schedule(1000, self.update_scroll_timer)
        else:
            self.unbind_scroll_events()
            sps = round(self.scrolls / 5, 2)
            self.scroll_label.config(text=f"Done! {self.scrolls} scrolls ({sps} SPS)")

    # ---------- 9. Key Sequence Test ----------
    def key_sequence_test(self):
        self.clear_window()
        keys_bank = ["A", "S", "D", "F", "J", "K", "L", ";",
                     "W", "E", "R", "U", "I", "O", "1", "2", "3", "4"]
        self.sequence = [random.choice(keys_bank) for _ in range(8)]
        tk.Label(self.root, text="Key Sequence Test", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(self.root, text="Type the sequence in order (ignore caps):", font=("Arial", 13)).pack(pady=4)
        self.seq_label = tk.Label(self.root, text=" ".join(self.sequence), font=("Consolas", 16))
        self.seq_label.pack(pady=8)
        self.progress_label = tk.Label(self.root, text="Progress: 0 / 8", font=("Arial", 14))
        self.progress_label.pack(pady=4)
        self.seq_index = 0
        self.errors = 0
        self.start_time = time.time()
        self.root.bind("<Key>", self.on_key_sequence)
        tk.Button(self.root, text="Back to Menu",
                  command=lambda: [self.root.unbind("<Key>"), self.main_menu()]).pack(pady=12)
        self.result_seq_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_seq_label.pack(pady=6)

    def on_key_sequence(self, event):
        if self.seq_index >= len(self.sequence):
            return
        expected = self.sequence[self.seq_index].lower()
        pressed = (event.char or "").lower()
        # Some keys like ";" may come as ";" in char; fallback to keysym for letters
        if not pressed and event.keysym:
            pressed = event.keysym.lower()
        if pressed == expected.lower():
            self.seq_index += 1
            self.progress_label.config(text=f"Progress: {self.seq_index} / {len(self.sequence)}")
        else:
            self.errors += 1
        if self.seq_index == len(self.sequence):
            elapsed = max(0.001, time.time() - self.start_time)
            kps = round(len(self.sequence) / elapsed, 2)
            self.result_seq_label.config(text=f"Done in {elapsed:.2f}s | Errors: {self.errors} | {kps} keys/s")
            self.root.unbind("<Key>")

    # ---------- 10. Memory Click Test (Simon-style) ----------
    def memory_click_test(self):
        self.clear_window()
        tk.Label(self.root, text="Memory Click Test", font=("Arial", 18, "bold")).pack(pady=8)
        tk.Label(self.root, text="Watch the sequence, then repeat it by clicking.", font=("Arial", 13)).pack(pady=4)

        self.mem_frame = tk.Frame(self.root)
        self.mem_frame.pack(pady=10)

        # 3x3 grid buttons
        self.mem_buttons = []
        colors = ["#e6e6e6"] * 9
        for i in range(3):
            row = []
            for j in range(3):
                idx = i * 3 + j
                btn = tk.Button(self.mem_frame, text=str(idx+1), width=6, height=3,
                                bg=colors[idx], command=lambda k=idx: self.memory_click(k), state="disabled")
                btn.grid(row=i, column=j, padx=6, pady=6)
                row.append(btn)
            self.mem_buttons.extend(row)

        self.seq_len = 4
        self.memory_seq = [random.randint(0, 8) for _ in range(self.seq_len)]
        self.mem_index = 0
        self.status_mem = tk.Label(self.root, text="Get ready...", font=("Arial", 14))
        self.status_mem.pack(pady=6)

        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=12)
        self.schedule(800, self.play_memory_sequence_step)

    def play_memory_sequence_step(self):
        # Disable during playback
        for b in self.mem_buttons:
            b.config(state="disabled")
        if self.mem_index < len(self.memory_seq):
            k = self.memory_seq[self.mem_index]
            self.flash_button(k)
            self.mem_index += 1
            self.schedule(700, self.play_memory_sequence_step)
        else:
            # Enable for input
            for b in self.mem_buttons:
                b.config(state="normal")
            self.status_mem.config(text="Your turn! Repeat the sequence.")
            self.mem_index = 0
            self.user_progress = []

    def flash_button(self, idx):
        btn = self.mem_buttons[idx]
        orig = btn.cget("bg")
        btn.config(bg="#ffd54f")
        self.schedule(350, lambda: btn.config(bg=orig))

    def memory_click(self, idx):
        if self.mem_index >= len(self.memory_seq):  # safety
            return
        self.user_progress.append(idx)
        expected = self.memory_seq[len(self.user_progress) - 1]
        if idx != expected:
            for b in self.mem_buttons:
                b.config(state="disabled")
            self.status_mem.config(text="Wrong! Sequence failed.")
            return
        if len(self.user_progress) == len(self.memory_seq):
            for b in self.mem_buttons:
                b.config(state="disabled")
            self.status_mem.config(text="Great memory! You got it.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SkillTestApp(root)
    root.mainloop()


