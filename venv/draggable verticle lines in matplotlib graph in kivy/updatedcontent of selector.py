class DrawPlot(BoxLayout):
    def __init__(self, x,y,dragrabble, **kwargs):
        super().__init__(**kwargs)
        self.signal = x
        self.plotting_area = y
        self.isdragabble = dragrabble
        self.draw_my_plot()
    def draw_my_plot(self):
        self.figure_1 = Figure(figsize=(2, 2))
        self.figure_1.subplots_adjust(left=0.13, right=0.93, bottom=0.25,
                                      top=0.98)  # to expand and occupy full area around imshow
        #self.panel_col = (1,0,0)
        self.x_vals = np.arange(0, 10, 0.01)
        self.y_vals = np.zeros(len(self.x_vals))
        #self.figure_1.set_facecolor(self.rgb_to_hex(self.panel_col))
        self.axes = self.figure_1.add_subplot(111)
        self.canvas_speech = FigureCanvasKivyAgg(self.figure_1)
        #self.axes.set_xlim(0, 10)
        #self.axes.set_ylim(-1, 1)
        print(len(self.signal))
        self.axes.plot(self.signal)
        self.max_y_lim,self.min_y_lim = self.axes.get_ylim()

        #self.axes.set_facecolor(self.rgb_to_hex(self.panel_col))
        self.axes.grid(True, color='lightgray')
        #self.axes.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        self.axes.set_xlabel('Time (s)', fontsize=10, labelpad=0)
        self.axes.set_ylabel('Signal (norm)', fontsize=10, labelpad=0)
        self.line11, = self.axes.plot(self.x_vals, self.y_vals, "b", linewidth=0.5)



        self.axes.plot(self.x_vals, self.y_vals, "b", linewidth=0.5)
        self.canvas_speech.draw_idle()
        self.plotting_area.clear_widgets()
        #self.canvas_speech.Refresh()
        if self.isdragabble == True:
            # Draw 2 line on speech graph
            self.line_a = lines.Line2D((self.axes.get_xlim()[1]/4,self.axes.get_xlim()[1]/4), (self.min_y_lim, self.max_y_lim), picker=5, color="r", linewidth=2)
            self.line_b = lines.Line2D((self.axes.get_xlim()[1]/2,self.axes.get_xlim()[1]/2), (self.min_y_lim, self.max_y_lim), picker=5, color="r", linewidth=2)
            self.a_point = 0.25
            self.b_point = 9.25
            self.draggable_line_a(self.line_a, self.axes)
            self.draggable_line_b(self.line_b, self.axes)

            self.axes.add_line(self.line_a)
            self.axes.add_line(self.line_b)


        self.plotting_area.add_widget(self.canvas_speech, 1) #<==== This adds a graph above the first row (index=1)

    def draggable_line_a(self, line_a, ax):
        self.line_a = line_a
        self.c_a = ax.get_figure().canvas
        self.sid_a = self.c_a.mpl_connect('pick_event', self.clickonline_a)

    def draggable_line_b(self, line_b, ax):
        self.line_b = line_b
        self.c_b = ax.get_figure().canvas
        self.sid_b = self.c_b.mpl_connect('pick_event', self.clickonline_b)
    def clickonline_a(self, event):
        # pub.sendMessage("SELECT_CHANGE", value=None)
        if event.artist == self.line_a:
            self.foll_a = self.c_a.mpl_connect("motion_notify_event", self.followmouse_a)
            self.rel_a = self.c_a.mpl_connect("button_release_event", self.releaseonclick_a)

    def clickonline_b(self, event):
        # pub.sendMessage("SELECT_CHANGE", value=None)
        if event.artist == self.line_b:
            self.foll_b = self.c_b.mpl_connect("motion_notify_event", self.followmouse_b)
            self.rel_b = self.c_b.mpl_connect("button_release_event", self.releaseonclick_b)

   
    def followmouse_a(self, event):
        if event.inaxes is None:
            return
        if event.button != 1:
            return

        if 1==1:
            self.line_a.set_xdata(event.xdata)
            self.c_a.draw_idle()



    def followmouse_b(self, event):
        if event.inaxes is None:
            return
        if event.button != 1:
            return

        if 1==1:

            self.line_b.set_xdata(event.xdata)
            self.c_b.draw_idle()

    def releaseonclick_a(self, event):
        self.a_point = self.line_a.get_xdata()
        if 1==1:
            if round(self.b_point, 2) - round(self.a_point, 2) < 0.16:
                b_minus_a = round(self.b_point, 2) - round(self.a_point, 2)
                minus_val = 0.20 - b_minus_a
                if round(self.b_point,2) - round(self.a_point,2) < 1700 or round(self.a_point,2) - round(self.b_point,2) <100:
                    self.line_a.set_xdata(self.a_point - 600)
                    self.line_b.set_xdata(self.b_point + 400)
                else:
                    self.line_a.set_xdata(self.a_point - minus_val)

                self.a_point = self.line_a.get_xdata()
                self.c_a.draw_idle()

            self.c_a.mpl_disconnect(self.rel_a)

            self.c_a.mpl_disconnect(self.foll_a)
            if round(self.b_point, 2) - round(self.a_point, 2) < 0:
                self.line_a.set_xdata(self.b_point)
                self.line_b.set_xdata(self.a_point)
            print('a')
            print(round(self.b_point,2) - round(self.a_point,2))

    def releaseonclick_b(self, event):

        self.b_point = self.line_b.get_xdata()
        if 1==1:
            if round(self.b_point, 2) - round(self.a_point, 2) < 0.16:
                b_minus_a = round(self.b_point, 2) - round(self.a_point, 2)
                minus_val = 0.20 - b_minus_a
                if round(self.b_point, 2) - round(self.a_point, 2) <1700 or round(self.a_point, 2) - round(self.b_point, 2) < 700:
                    self.line_b.set_xdata(self.b_point + 400)
                    self.line_a.set_xdata(self.a_point - 600)
                else:

                    self.line_b.set_xdata(self.b_point + minus_val)

                self.b_point = self.line_b.get_xdata()
                self.c_b.draw_idle()


            self.c_b.mpl_disconnect(self.rel_b)

            self.c_b.mpl_disconnect(self.foll_b)
            if round(self.b_point, 2) - round(self.a_point, 2) < 0:
                self.line_a.set_xdata(self.b_point)
                self.line_b.set_xdata(self.a_point)
            print('b')
            print(round(self.b_point,2) - round(self.a_point,2))
    def get_linea_value(self):
        try:
            return self.line_a.get_xdata()[0]
        except:
            return self.line_a.get_xdata()
    def get_lineb_value(self):
        try:
            return self.line_b.get_xdata()[0]
        except:
            return self.line_b.get_xdata()
