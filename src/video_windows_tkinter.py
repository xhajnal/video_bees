import analyse
import threading
import tkinter as tk
from tkinter import TclError, ttk

# My imports
import make_video
import traces_logic

global video_file
global trim_offset
global traces_to_show
global app


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        """ A Frame that shows GUI to edit the traces shown in the video """

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

    def create_button_frame(self, traces):
        frame = ttk.Frame(self)
        frame.columnconfigure(0, weight=1)

        show_all_traces_button = ttk.Button(frame, text=f"Show All Traces")
        show_all_traces_button.grid(column=0, row=0)
        show_all_traces_button.bind('<Button-1>', show_all_traces)

        for index, trace in enumerate(traces):
            if trace.trace_id != traces[index].trace_id:
                raise Exception("internal indexing problem")

            button_1 = ttk.Button(frame, text=f"Highlight Trace {trace.trace_id}")
            button_1.grid(column=0, row=1 + index)
            button_1.index = index
            button_1.trace_id = trace.trace_id
            button_1.bind('<Button-1>', onButton_Handler_highlight_trace)

            button_2 = ttk.Button(frame, text=f"Delete Trace {trace.trace_id}")
            button_2.grid(column=1, row=1 + index)
            button_2.trace_id = trace.trace_id
            button_2.bind('<Button-1>', OnButton_Handler_delete_trace)

            button_3 = ttk.Button(frame, text=f"UnDelete Trace {trace.trace_id}")
            button_3.grid(column=2, row=1 + index)
            button_3.index = index
            button_3.trace_id = trace.trace_id
            button_3.bind('<Button-1>', OnButton_Handler_undelete_trace)

            button_4 = ttk.Button(frame, text=f"[{trace.frame_range[0]},{trace.frame_range[1]}]")
            button_4.grid(column=3, row=1 + index)
            button_4.index = index
            button_4.bind('<Button-1>', OnButton_Handler_go_to_frame)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        return frame

    ## Key press handlers
    def keydown(self, event):
        char = event.char
        # print(char)

        if char == "q":
            # TODO quit video and gui
            self.destroy()
            pass
        elif char == "r":
            # TODO restart video
            pass
        elif char == "a":
            # TODO rewind video
            pass
        elif char == "d":
            # TODO forward video
            pass
        elif char == "+":
            # TODO speed up video
            pass
        elif char == "-":
            # TODO slow down video
            pass


class GuiVideoThread(threading.Thread):
    def __init__(self, a, c):
        threading.Thread.__init__(self)
        global traces_to_show
        traces_to_show = a
        global trim_offset
        trim_offset = c
        self.app = None

    def run(self):
        # app = App()
        # app.mainloop()

        self.app = App()
        self.app.mainloop()
        print("hello")

    def terminate(self):
        self.app.quit()


def gui(a, b):
    global traces_to_show
    traces_to_show = a
    global trim_offset
    trim_offset = b
    app = App()
    app.mainloop()


## Button handlers
def show_all_traces(event):
    make_video.show_all_traces()


# def show_single_trace(event):
#     make_video.show_single_trace(event.widget.index)


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
