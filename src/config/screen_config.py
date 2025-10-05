from dataclasses import dataclass, field
from rich.console import Console
from rich.layout import Layout
from rich.progress import Progress
from rich.table import Table


@dataclass
class ScreenConfig:
    name: str
    console: Console = field(default=None, init=False)
    layout: Layout = field(default=None, init=False)
    progress: Progress = field(default=None, init=False)
    config_table: Table = field(default=None, init=False)

    def __post_init__(self):
        self.console = Console()
        self.layout = Layout()

        self.config_table = Table(show_header=True, header_style="bold magenta", title="TransRomIA")
        self.config_table.add_column("Rom")
        self.config_table.add_column("Directory")
        self.config_table.add_column("Extencion")
        self.config_table.add_column("Size")
        self.config_table.add_column("Output Directory")
        self.config_table.add_column("Quality")

        self.generate_initial_layout()

    def generate_initial_layout(self):
        self.layout.split_column(
            Layout(name="Config"),
            Layout(name="Process"),
        )

        self.layout["lower"].split_row(
            Layout(name="Progress"),
        )

        self.layout['Config'].update(self.config_table)

    def set_progress_collumns(self, collumns):
        self.progress.columns = collumns
