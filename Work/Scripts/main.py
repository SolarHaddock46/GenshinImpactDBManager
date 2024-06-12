import tkinter as tk
from tkinter import ttk
# import Work.Scripts.report_creator as report_creator
import report_creator
import graphics_display

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu Example")
        self.geometry("400x300")

        # Define styles
        self.style = ttk.Style(self)
        self.style.configure('TButton', font=('Helvetica', 12), padding=5)
        self.style.configure('TFrame', background='lightgrey')

        # Create a frame for the buttons
        button_frame = ttk.Frame(self, style='TFrame')
        button_frame.pack(pady=20)

        # Create the buttons
        view_data_button = ttk.Button(button_frame, text="View source data", command=self.view_data)
        view_data_button.grid(row=0, column=0, padx=5)

        text_reports_button = ttk.Button(button_frame, text="Text reports", command=self.show_text_reports)
        text_reports_button.grid(row=1, column=0, padx=5, pady=5)

        graphic_reports_button = ttk.Button(button_frame, text="Graphic reports", command=self.show_graphic_reports)
        graphic_reports_button.grid(row=2, column=0, padx=5)

        quit_button = ttk.Button(button_frame, text="Quit", command=self.destroy)
        quit_button.grid(row=3, column=0, padx=5, pady=5)

    def view_data(self):
        # Function to view source data
        print("Viewing source data")

        # Create a new window for the menu
        data_window = tk.Toplevel(self)
        data_window.title("Source Data")
        data_window.geometry("300x200")

        # Create a frame for the menu
        menu_frame = ttk.Frame(data_window, style='TFrame')
        menu_frame.pack(pady=20)

        # Create the menu buttons
        characters_button = ttk.Button(menu_frame, text="Characters", command=self.view_characters)
        characters_button.grid(row=0, column=0, padx=5, pady=5)

        artifacts_button = ttk.Button(menu_frame, text="Artifacts", command=self.view_artifacts)
        artifacts_button.grid(row=1, column=0, padx=5, pady=5)

        back_button = ttk.Button(menu_frame, text="Back", command=data_window.destroy)
        back_button.grid(row=2, column=0, padx=5, pady=5)

    def view_characters(self):
        # Function to view characters
        print("Viewing characters")

    def view_artifacts(self):
        # Function to view artifacts
        print("Viewing artifacts")

    def show_text_reports(self):
        # Function to show text reports menu
        text_reports_window = tk.Toplevel(self)
        text_reports_window.title("Text Reports")
        text_reports_window.geometry("300x200")

        text_reports_frame = ttk.Frame(text_reports_window, style='TFrame')
        text_reports_frame.pack(pady=20)

        report_a_button = ttk.Button(text_reports_frame, text="Report A", command=self.make_report_a)
        report_a_button.grid(row=0, column=0, padx=5)

        report_b_button = ttk.Button(text_reports_frame, text="Report B", command=self.make_report_b)
        report_b_button.grid(row=1, column=0, padx=5, pady=5)

        report_c_button = ttk.Button(text_reports_frame, text="Report C", command=self.make_report_c)
        report_c_button.grid(row=2, column=0, padx=5)

        report_d_button = ttk.Button(text_reports_frame, text="Report D", command=self.make_report_d)
        report_d_button.grid(row=3, column=0, padx=5, pady=5)

        report_e_button = ttk.Button(text_reports_frame, text="Report E", command=self.make_report_e)
        report_e_button.grid(row=4, column=0, padx=5)

        back_button = ttk.Button(text_reports_frame, text="Back", command=text_reports_window.destroy)
        back_button.grid(row=5, column=0, padx=5, pady=5)

    def make_report_a(self):
        # Function to make report A
        print("Making report A")

    def make_report_b(self):
        # Function to make report B
        print("Making report B")

    def make_report_c(self):
        # Function to make report C
        print("Making report C")

    def make_report_d(self):
        # Function to make report D
        print("Making report D")

    def make_report_e(self):
        # Function to make report E
        print("Making report E")

    def show_graphic_reports(self):
        # Function to show graphic reports menu
        graphic_reports_window = tk.Toplevel(self)
        graphic_reports_window.title("Graphic Reports")
        graphic_reports_window.geometry("300x200")

        graphic_reports_frame = ttk.Frame(graphic_reports_window, style='TFrame')
        graphic_reports_frame.pack(pady=20)

        scatter_button = ttk.Button(graphic_reports_frame, text="Scatter Plot", command=self.make_scatter_plot)
        scatter_button.grid(row=0, column=0, padx=5)

        boxplot_button = ttk.Button(graphic_reports_frame, text="Box Plot", command=self.make_box_plot)
        boxplot_button.grid(row=1, column=0, padx=5, pady=5)

        bar_button = ttk.Button(graphic_reports_frame, text="Bar Chart", command=self.make_bar_chart)
        bar_button.grid(row=2, column=0, padx=5)

        hist_button = ttk.Button(graphic_reports_frame, text="Histogram", command=self.make_histogram)
        hist_button.grid(row=3, column=0, padx=5, pady=5)

        back_button = ttk.Button(graphic_reports_frame, text="Back", command=graphic_reports_window.destroy)
        back_button.grid(row=4, column=0, padx=5, pady=5)

    def make_scatter_plot(self):
        # Function to make scatter plot
        data, characters, rarities = report_creator.load_data()
        report_creator.generate_graphical_report(data, 'scatter', 'Текущий уровень', 'Требуемый опыт', 'scatter_plot', title='Scatter Plot: Experience vs Level')
        print("Scatter plot generated")
        graphics_display.run_app("../Graphics/scatter_plot.png")
        

    def make_box_plot(self):
        # Function to make box plot
        data, characters, rarities = report_creator.load_data()
        report_creator.generate_graphical_report(data, 'boxplot', 'Редкость артефакта', 'Требуемый опыт', 'box_plot', title='Box Plot: Experience by Rarity')
        print("Box plot generated")
        graphics_display.run_app("../Graphics/box_plot.png")


    def make_bar_chart(self):
        # Function to make bar chart
        data, characters, rarities = report_creator.load_data()
        report_creator.generate_graphical_report(data, 'bar', 'Редкость артефакта', 'Требуемый опыт', 'bar_chart', title='Bar Chart: Experience by Rarity')
        print("Bar chart generated")
        graphics_display.run_app("../Graphics/bar_chart.png")


    def make_histogram(self):
        # Function to make histogram
        data, characters, rarities = report_creator.load_data()
        report_creator.generate_graphical_report(data, 'hist', 'Текущий уровень', 'histogram', title='Histogram: Current Level Distribution')
        print("Histogram generated")
        graphics_display.run_app("../Graphics/histogram.png")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
