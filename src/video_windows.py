import tkinter as tk
from tkinter import TclError, ttk

# My imports
import analyse
import make_video
import traces_logic

global trim_offset
global traces_to_show
global app


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        """ A Frame that shows GUI to edit the traces shown in the video """

        newWindow = None

        self.title('Traces Editor')
        self.resizable(0, 0)
        try:
            # windows only (remove the minimize/maximize button)
            self.attributes('-toolwindow', True)
        except TclError:
            print('Not supported on your platform')

        # layout on the root window
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        button_frame = self.create_button_frame(traces_to_show)
        button_frame.grid(column=1, row=0)

        self.bind("<KeyPress>", self.keydown)

        self.check_to_quit()

    def create_button_frame(self, traces):
        frame = ttk.Frame(self)
        frame.columnconfigure(0, weight=1)

        show_all_traces_button = ttk.Button(frame, text=f"Show All Traces")
        show_all_traces_button.grid(column=0, row=0)
        show_all_traces_button.bind('<Button-1>', show_all_traces)

        for index, trace in enumerate(traces):
            if trace is None:
                continue
            if trace.trace_id != traces[index].trace_id:
                raise Exception("internal indexing problem")

            button_1 = ttk.Button(frame, text=f"Highlight Trace {trace.trace_id}")
            button_1.grid(column=0, row=1 + index)
            button_1.index = index
            button_1.trace_id = trace.trace_id
            button_1.bind('<Button-1>', onButton_Handler_highlight_trace)

            button_2 = ttk.Button(frame, text=f"Trim Trace {trace.trace_id}")
            button_2.grid(column=1, row=1 + index)
            button_2.trace_id = trace.trace_id
            button_2.bind('<Button-1>', self.OnButton_Handler_trim_trace)

            button_3 = ttk.Button(frame, text=f"Delete Trace {trace.trace_id}")
            button_3.grid(column=2, row=1 + index)
            button_3.trace_id = trace.trace_id
            button_3.bind('<Button-1>', OnButton_Handler_delete_trace)

            button_4 = ttk.Button(frame, text=f"UnDelete Trace {trace.trace_id}")
            button_4.grid(column=3, row=1 + index)
            button_4.index = index
            button_4.trace_id = trace.trace_id
            button_4.bind('<Button-1>', OnButton_Handler_undelete_trace)

            button_5 = ttk.Button(frame, text=f"[{trace.frame_range[0]},{trace.frame_range[1]}]")
            button_5.grid(column=4, row=1 + index)
            button_5.index = index
            button_5.bind('<Button-1>', OnButton_Handler_go_to_frame)
            button_5.bind('<Button-3>', OnButton_Handler_go_to_frame2)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame

    def check_to_quit(self):
        # print("kill gui rn")
        if analyse.gonna_run is False:
            try:
                self.destroy()
            except Exception as err:
                pass
        self.after(1, self.check_to_quit)
        # print("killed gui rn")

    def OnButton_Handler_trim_trace(self, event):
        self.newWindow = tk.Toplevel(self)

        self.newWindow.title("New Window")
        self.newWindow.geometry("260x180")

        frame_range = [0, 0]
        for trace in analyse.traces:
            if trace is None:
                continue

            if trace.trace_id == event.widget.trace_id:
                frame_range = trace.frame_range

        tk.Label(self.newWindow, text=f"Trimming a trace with id {event.widget.trace_id}").pack()
        tk.Label(self.newWindow, text=f"Select a part of the trace to be trimmed out.").pack()

        tk.Label(self.newWindow, text=f"Starting frame of trimming (including)").pack()
        self.start_entry = tk.Entry(self.newWindow, width=10)
        self.start_entry.pack()
        self.start_entry.insert(0, str(frame_range[0]))

        tk.Label(self.newWindow, text=f"End frame of trimming (including)").pack()
        self.end_entry = tk.Entry(self.newWindow, width=10)
        self.end_entry.pack()
        self.end_entry.insert(0, str(frame_range[1]))

        self.current_id = event.widget.trace_id

        btn = ttk.Button(self.newWindow, text="Trim")
        btn.bind('<Button-1>', self.OnButton_Handler_trim_trace2)
        btn.pack(pady=10)

    def OnButton_Handler_trim_trace2(self, event):
        traces_logic.trim_trace_with_id(self.current_id, int(self.start_entry.get()), int(self.end_entry.get()))
        self.newWindow.destroy()


    ## Key press handlers
    def keydown(self, event):
        char = event.char
        # print(char)

        if char == "q":
            self.destroy()
            pass
        elif char == '':
            pass
        else:
            print("We are sorry that the buttons do not work here any more, please click on the video windows to operate with it this way.")
        # elif char == "r":
        #     # TODO restart video
        #     pass
        # elif char == "a":
        #     # TODO rewind video
        #     pass
        # elif char == "d":
        #     # TODO forward video
        #     pass
        # elif char == "+":
        #     # TODO speed up video
        #     pass
        # elif char == "-":
        #     # TODO slow down video
        #     pass


# class GuiVideoThread(threading.Thread):
#     def __init__(self, a, c):
#         threading.Thread.__init__(self)
#         global traces_to_show
#         traces_to_show = a
#         global trim_offset
#         trim_offset = c
#         self.app = None
#
#     def run(self):
#         # app = App()
#         # app.mainloop()
#
#         self.app = App()
#         self.app.mainloop()
#         print("hello")
#
#     def terminate(self):
#         self.app.quit()
#
#
# def gui(a, b):
#     global traces_to_show
#     traces_to_show = a
#     global trim_offset
#     trim_offset = b
#     app = App()
#     app.mainloop()


## Button handlers
def show_all_traces(event):
    make_video.show_all_traces()


def onButton_Handler_highlight_trace(event):
    make_video.show_single_trace(event.widget.index)


def OnButton_Handler_delete_trace(event):
    traces_logic.delete_trace_with_id(event.widget.trace_id)


def OnButton_Handler_undelete_trace(event):
    traces_logic.undelete_trace_with_id(event.widget.trace_id, event.widget.index)


def OnButton_Handler_go_to_frame(event):
    global traces_to_show
    global trim_offset
    make_video.goto = (event.widget.index, traces_to_show, trim_offset)
    make_video.go_outside = False


def OnButton_Handler_go_to_frame2(event):
    global traces_to_show
    global trim_offset
    make_video.goto = (event.widget.index, traces_to_show, trim_offset)
    make_video.go_outside = True
