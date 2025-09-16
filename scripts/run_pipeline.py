import os
import argparse
import subprocess
import yaml
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from scripts.utils.pipeline_context import init_run

# ========= Project Root Resolver =========
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
console = Console()


def run_pipeline(cfg_path, step=None, list_only=False):
    # Resolve config path relative to ROOT_DIR
    cfg_path = os.path.join(ROOT_DIR, cfg_path) if not os.path.isabs(cfg_path) else cfg_path
    if not os.path.exists(cfg_path):
        console.print(f"[red]❌ Config file not found: {cfg_path}[/red]")
        raise FileNotFoundError(f"Config file not found: {cfg_path}")

    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    scripts = cfg.get("scripts", [])
    if step:
        scripts = [s for s in scripts if s["script"].endswith(step)]

    if list_only:
        table = Table(title="📜 Pipeline Steps", header_style="bold cyan")
        table.add_column("Order", style="bold green")
        table.add_column("Script")
        table.add_column("Args", style="yellow")

        for i, s in enumerate(scripts, 1):
            args_str = " ".join(s.get("args", []))
            table.add_row(str(i), s["script"], args_str)

        console.print(table)
        return

    console.print(Panel.fit("🚀 Starting Pipeline", style="bold blue"))

    for s in track(scripts, description="Running pipeline..."):
        module_name = s["script"].replace("/", ".").replace("\\", ".").replace(".py", "")

    # Always pass --config <cfg_path>
        cmd = ["python", "-m", module_name, "--config", cfg_path]

    # Add any extra args from YAML (safe default)
        if "args" in s and s["args"]:
            cmd.extend(map(str, s["args"]))

        console.print(f"[cyan]▶ Running:[/cyan] [bold]{module_name}[/bold] {' '.join(cmd[2:])}")
        try:
            subprocess.run(cmd, check=True, cwd=ROOT_DIR)
            console.print(f"[green]✔ Success:[/green] {module_name}")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]❌ Failed:[/red] {module_name}")
            console.print(f"[red]Command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit Code:[/red] {e.returncode}")
            raise


        console.print(Panel.fit("✅ Pipeline Complete", style="bold green"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline Runner with UI")
    parser.add_argument("--config", default="configs/pipeline_v1.yaml", help="Path to pipeline config YAML")
    parser.add_argument("--step", help="Run only this script (filename match)")
    parser.add_argument("--list", action="store_true", help="List available steps instead of running")
    args = parser.parse_args()

    run_id = init_run(args.config)
    console.print(f"[bold blue]🚀 Starting pipeline run: {run_id}[/bold blue]")

    run_pipeline(args.config, args.step, args.list)




# python scripts/run_pipeline.py --config configs/pipeline_v0.yaml
# python -m scripts.run_pipeline --config configs/pipeline_v2.yaml



