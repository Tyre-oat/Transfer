#!/usr/bin/env python3
# ============================================================
# FILE TRANSMISSION SHOWCASE (Competition Visual Edition)
# - Pure send-only visual simulation
# - Stable rich progress (no Live / no dashboard bug)
# - Focus on cool effects
# ============================================================

import os
import time
import random
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    SpinnerColumn,
    DownloadColumn,
)
from rich.text import Text

console = Console()


# =======================
# Startup Animation
# =======================
def startup():
    os.system("cls" if os.name == "nt" else "clear")
    console.print(
        """
[bold cyan]
███████╗██╗██╗     ███████╗    ████████╗██████╗  █████╗ ███╗   ██╗
██╔════╝██║██║     ██╔════╝    ╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║
█████╗  ██║██║     █████╗         ██║   ██████╔╝███████║██╔██╗ ██║
██╔══╝  ██║██║     ██╔══╝         ██║   ██╔══██╗██╔══██║██║╚██╗██║
██║     ██║███████╗███████╗       ██║   ██║  ██║██║  ██║██║ ╚████║
╚═╝     ╚═╝╚══════╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
[/bold cyan]
        """
    )
    console.print("[cyan]>>> Initializing transmission engine...[/cyan]")
    time.sleep(1.5)


# =======================
# Demo File Generator
# =======================
def prepare_files(path="demo_data"):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        for i in range(6):
            with open(f"{path}/sample_{i}.bin", "wb") as f:
                f.write(os.urandom(random.randint(80, 200) * 1024))

    files = []
    total = 0
    for f in os.listdir(path):
        size = os.path.getsize(os.path.join(path, f))
        files.append((f, size))
        total += size

    return files, total


# =======================
# Transmission Simulation
# =======================
def simulate(files, total_size):
    total_mb = total_size / 1024 / 1024
    start_time = datetime.now()

    console.print(
        Panel(
            f"[bold cyan]FILES[/bold cyan] : {len(files)}\n"
            f"[bold cyan]SIZE[/bold cyan]  : {total_mb:.1f} MB\n"
            f"[bold cyan]START[/bold cyan] : {start_time.strftime('%H:%M:%S')}\n"
            f"[bold green]STATUS[/bold green]: TRANSMITTING",
            title="[bold]TRANSMISSION OVERVIEW[/bold]",
            border_style="cyan",
        )
    )

    time.sleep(1)

    with Progress(
        SpinnerColumn("dots", style="bold cyan"),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=55, complete_style="bright_green"),
        DownloadColumn(binary_units=True),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
        refresh_per_second=30,
    ) as progress:

        task = progress.add_task(
            "Establishing virtual channel...", total=total_size
        )

        sent = 0
        file_idx = 0
        offset = 0

        while sent < total_size:
            fname, fsize = files[file_idx]

            chunk = random.randint(20_000, 60_000)
            remain = fsize - offset
            send = min(chunk, remain)

            time.sleep(0.02)
            progress.advance(task, send)

            sent += send
            offset += send

            percent = sent / total_size * 100

            if percent < 10:
                desc = "Performing handshake..."
            elif percent < 25:
                desc = "Negotiating channel parameters..."
            elif percent < 50:
                desc = f"Streaming: {fname}"
            elif percent < 75:
                desc = f"Transmitting payload: {fname}"
            elif percent < 95:
                desc = "Flushing buffers..."
            else:
                desc = "Finalizing transmission..."

            progress.update(task, description=desc)

            if offset >= fsize:
                offset = 0
                file_idx = (file_idx + 1) % len(files)

        progress.update(task, description="Transmission completed!")

    console.print(
        Panel(
            "[bold green]DATA TRANSMISSION COMPLETED SUCCESSFULLY[/bold green]\n\n"
            f"Files Transmitted : {len(files)}\n"
            f"Total Size        : {total_mb:.1f} MB\n"
            f"Finished At       : {datetime.now().strftime('%H:%M:%S')}",
            title="[bold green]RESULT[/bold green]",
            border_style="green",
        )
    )


# =======================
# Main
# =======================
if __name__ == "__main__":
    startup()
    files, total = prepare_files()
    simulate(files, total)
