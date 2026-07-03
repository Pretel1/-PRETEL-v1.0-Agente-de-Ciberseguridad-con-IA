#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════
#  🔱 PRETEL v1.0 — Agente de Ciberseguridad con IA
#  Powered by 817 Cybersecurity Skills
# ═══════════════════════════════════════════════════════════════

import os, sys, json, re, subprocess, shutil, signal
from pathlib import Path
from datetime import datetime

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, IntPrompt
    from rich.text import Text
    from rich.markdown import Markdown
    from rich.columns import Columns
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    from rich.rule import Rule
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "-q"])
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, IntPrompt
    from rich.text import Text
    from rich.markdown import Markdown
    from rich.columns import Columns
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    from rich.rule import Rule

console = Console()

# ─── Config ─────────────────────────────────────────────────────
SKILLS_DIR = Path(__file__).parent / "Anthropic-Cybersecurity-Skills" / "skills"
INDEX_FILE = Path(__file__).parent / "Anthropic-Cybersecurity-Skills" / "index.json"
LOGS_DIR   = Path.home() / "pretel_logs"

BANNER = r"""[bold cyan]
  ██████╗ ██████╗ ███████╗████████╗███████╗██╗
  ██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██║
  ██████╔╝██████╔╝█████╗     ██║   █████╗  ██║
  ██╔═══╝ ██╔══██╗██╔══╝     ██║   ██╔══╝  ██║
  ██║     ██║  ██║███████╗   ██║   ███████╗███████╗
  ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚══════╝[/bold cyan]
[bold white]         AI Security Agent — 817 Skills[/bold white]
[dim]         Solo para uso ético y autorizado[/dim]
"""

# ─── Helpers ─────────────────────────────────────────────────────

def clear(): os.system('clear')

def log(msg, style="cyan"):
    t = datetime.now().strftime("%H:%M:%S")
    console.print(f"  [dim]{t}[/dim] [bold {style}]→[/bold {style}] {msg}")

def pause():
    console.print()
    Prompt.ask("  [dim]Presiona ENTER para continuar[/dim]")

def run_cmd(cmd):
    log(f"Ejecutando: [bold white]{cmd}[/bold white]", "yellow")
    console.print()
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            console.print(f"  {line}", end="", highlight=False)
        proc.wait()
        return proc.returncode
    except KeyboardInterrupt:
        log("Cancelado por el usuario", "yellow")
        return 1

def save_log(title, content):
    LOGS_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = LOGS_DIR / f"{title}_{ts}.txt"
    fname.write_text(f"PRETEL Log — {title}\n{datetime.now()}\n{'='*60}\n{content}")
    log(f"Guardado: {fname}", "green")

# ─── Skills Engine ───────────────────────────────────────────────

_SKILLS_CACHE = None

def load_skills():
    global _SKILLS_CACHE
    if _SKILLS_CACHE:
        return _SKILLS_CACHE
    if not INDEX_FILE.exists():
        log("No se encontró el repositorio de skills. Clona primero:", "red")
        log("git clone https://github.com/mukul975/Anthropic-Cybersecurity-Skills", "yellow")
        return []
    with open(INDEX_FILE) as f:
        data = json.load(f)
    _SKILLS_CACHE = data.get("skills", [])
    return _SKILLS_CACHE

def search_skills(query, limit=10):
    """Busca skills por palabras clave en nombre y descripción."""
    skills = load_skills()
    query_words = query.lower().split()
    results = []
    for s in skills:
        text = f"{s['name']} {s.get('description','')}".lower()
        score = sum(2 if w in s['name'].lower() else 1 for w in query_words if w in text)
        if score > 0:
            results.append((score, s))
    results.sort(key=lambda x: -x[0])
    return [s for _, s in results[:limit]]

def read_skill(skill_name):
    """Lee el SKILL.md de un skill."""
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    if skill_path.exists():
        return skill_path.read_text()
    return None

def parse_skill_frontmatter(content):
    """Extrae metadatos YAML del frontmatter, incluyendo listas."""
    meta = {}
    if content.startswith("---"):
        end = content.find("---", 3)
        if end > 0:
            fm = content[3:end]
            current_key = None
            list_items = []
            for line in fm.splitlines():
                if line.startswith('- ') and current_key:
                    list_items.append(line[2:].strip())
                elif ':' in line and not line.startswith(' '):
                    if current_key and list_items:
                        meta[current_key] = ', '.join(list_items)
                    k, _, v = line.partition(':')
                    current_key = k.strip()
                    list_items = []
                    v = v.strip().strip("'\"")
                    if v:
                        meta[current_key] = v
            if current_key and list_items:
                meta[current_key] = ', '.join(list_items)
    return meta

# Herramientas CLI conocidas para detectar comandos completos
_CLI_TOOLS = [
    'nmap','hydra','sqlmap','nikto','amass','theharvester','theHarvester',
    'gobuster','dirb','wpscan','masscan','curl','wget','dig','whois',
    'enum4linux','searchsploit','john','hashcat','netexec','nxc','nxc',
    'impacket','evil-winrm','smbclient','airmon-ng','airodump-ng','msfconsole',
    'msfvenom','tcpdump','tshark','hping3','arp-scan','netdiscover','sslscan',
    'whatweb','wafw00f','dnsenum','fierce','subfinder','ffuf','feroxbuster',
    'nuclei','crackmapexec','bloodhound','neo4j','python','python3','pip',
    'git','openssl','ssh','nc','netcat','socat','responder','ubertooth',
    'wireshark','volatility','autopsy','binwalk','strings','file','xxd',
]

def extract_commands(content):
    """Extrae comandos shell completos de bloques de código del SKILL.md."""
    # Extraer bloques ```bash / ```sh / ``` completos
    block_cmds = re.findall(r'```(?:bash|sh|shell|console|text)?\n(.*?)```', content, re.DOTALL)
    
    all_cmds = []
    for block in block_cmds:
        lines = block.strip().splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # Saltar comentarios, líneas vacías, output típico
            if not line or line.startswith('#') or line.startswith('>'):
                i += 1
                continue
            # Detectar si es un comando real (empieza con herramienta conocida)
            first_word = line.split()[0].lstrip('$').lstrip('sudo').strip() if line.split() else ''
            is_cmd = any(line.lstrip('$ ').startswith(t) for t in _CLI_TOOLS)
            if is_cmd and len(line) > 8:
                # Unir líneas de continuación con \
                full_cmd = line.rstrip('\\')
                while line.endswith('\\') and i + 1 < len(lines):
                    i += 1
                    line = lines[i].strip()
                    full_cmd += ' ' + line.rstrip('\\')
                cmd_clean = full_cmd.lstrip('$ ').strip()
                if cmd_clean:
                    all_cmds.append(cmd_clean)
            i += 1

    # Fallback: comandos inline con backticks si no hay bloques bash
    if not all_cmds:
        inline = re.findall(r'`([^`\n]{8,120})`', content)
        for cmd in inline:
            cmd = cmd.strip().lstrip('$ ')
            if any(cmd.startswith(t) for t in _CLI_TOOLS) and len(cmd) > 8:
                all_cmds.append(cmd)

    # Deduplicar y limitar
    seen = set()
    unique = []
    for c in all_cmds:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    return unique[:15]

def cmd_available(cmd):
    """Verifica si el primer binario de un comando está instalado."""
    binary = cmd.lstrip('$ ').split()[0] if cmd.split() else ''
    if binary in ('python', 'python3', 'sudo'): return True
    return shutil.which(binary) is not None

def get_categories():
    """Obtiene categorías únicas de los skills."""
    skills = load_skills()
    cats = {}
    for s in skills:
        name = s['name']
        # Derive category from name prefix
        parts = name.split('-')
        if len(parts) >= 1:
            verb = parts[0]
            cats[verb] = cats.get(verb, 0) + 1
    return sorted(cats.items(), key=lambda x: -x[1])

# ─── UI: Búsqueda de Skills ───────────────────────────────────────

def show_skill_detail(skill):
    """Muestra el detalle completo de un skill con opción de ejecutar comandos."""
    content = read_skill(skill['name'])
    if not content:
        log("No se pudo leer el skill", "red")
        return

    meta = parse_skill_frontmatter(content)
    commands = extract_commands(content)

    clear()
    console.print()

    tags = meta.get('tags', '')
    mitre = meta.get('mitre_attack', '')

    # Header
    console.print(Panel(
        f"[bold cyan]{skill['name']}[/bold cyan]\n\n"
        f"[white]{skill.get('description', '')}[/white]\n\n"
        f"[dim]🏷  Tags: {tags if tags else 'N/A'}[/dim]\n"
        f"[dim]🎯 MITRE ATT&CK: {mitre if mitre else 'N/A'}[/dim]",
        title="[bold]📖 PRETEL SKILL[/bold]",
        border_style="cyan",
        box=box.DOUBLE
    ))

    # Mostrar contenido markdown (sin frontmatter)
    body_start = content.find("# ", content.find("---", 3))
    body = content[body_start:] if body_start > 0 else content
    console.print(Markdown(body[:3500]))

    if len(body) > 3500:
        log(f"... (+{len(body)-3500} chars más) — lee el skill completo con: cat '{SKILLS_DIR / skill['name'] / 'SKILL.md'}'", "dim")

    # Comandos ejecutables
    if commands:
        console.print()
        console.print(Rule("[bold yellow]⚡ Comandos Disponibles[/bold yellow]"))
        t = Table(box=box.ROUNDED, border_style="yellow", show_lines=True)
        t.add_column("#", style="dim", width=3)
        t.add_column("Disponible", width=4, justify="center")
        t.add_column("Comando", style="bold white")
        for i, cmd in enumerate(commands, 1):
            avail = "✅" if cmd_available(cmd) else "❌"
            t.add_row(str(i), avail, cmd)
        console.print(t)
        console.print("  [dim]✅ = instalado  ❌ = herramienta no encontrada[/dim]")
        console.print()

        choice = Prompt.ask(
            "  [cyan]¿Ejecutar un comando? (número o ENTER para saltar)[/cyan]",
            default=""
        )
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(commands):
                cmd = commands[idx]
                if not cmd_available(cmd):
                    binary = cmd.split()[0]
                    log(f"'{binary}' no está instalado. Instálalo primero.", "red")
                    pause()
                    return
                # Reemplazar placeholders comunes
                for placeholder in ['target.com','TARGET_IP','<target>','TARGET','<domain>',
                                    'DOMAIN','192.168.1.1','AA:BB:CC:DD:EE:FF']:
                    if placeholder in cmd:
                        val = Prompt.ask(f"  [cyan]Valor para '{placeholder}'[/cyan]")
                        if val:
                            cmd = cmd.replace(placeholder, val)
                console.print()
                run_cmd(cmd)
                pause()
    else:
        log("No se detectaron comandos ejecutables en este skill.", "dim")
        pause()

# ─── UI: Módulo de Búsqueda ──────────────────────────────────────

def mod_search():
    """Búsqueda libre en los 817 skills."""
    clear()
    console.print(BANNER)
    console.print(Rule("[bold cyan]🔍 BUSCAR SKILL[/bold cyan]"))
    console.print()
    console.print("  [dim]Ejemplos: 'nmap reconocimiento', 'sql injection', 'windows privesc', 'wifi crack'[/dim]")
    console.print()

    while True:
        query = Prompt.ask("  [bold cyan]🔍 Buscar[/bold cyan] [dim](o 'salir')[/dim]")
        if query.lower() in ('salir', 'exit', 'q', ''):
            return

        with Progress(SpinnerColumn(), TextColumn("[cyan]Buscando..."), transient=True) as p:
            p.add_task("", total=None)
            results = search_skills(query)

        if not results:
            log("No se encontraron skills. Intenta otras palabras.", "red")
            continue

        console.print()
        t = Table(title=f"📋 Resultados para: [bold]{query}[/bold]",
                  box=box.ROUNDED, border_style="cyan", show_lines=True)
        t.add_column("#", style="dim", width=3)
        t.add_column("Skill", style="bold white", min_width=35)
        t.add_column("Descripción", style="dim", max_width=50)

        for i, s in enumerate(results, 1):
            desc = s.get('description', '')[:80] + '...' if len(s.get('description','')) > 80 else s.get('description','')
            t.add_row(str(i), s['name'], desc)

        console.print(t)
        console.print()

        choice = Prompt.ask("  [cyan]Ver skill (número) o nueva búsqueda (ENTER)[/cyan]", default="")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(results):
                show_skill_detail(results[idx])
                clear()
                console.print(BANNER)
                console.print(Rule("[bold cyan]🔍 BUSCAR SKILL[/bold cyan]"))

# ─── UI: Explorar por Categoría ──────────────────────────────────

def mod_browse():
    """Explorar skills por categoría."""
    skills = load_skills()
    # Agrupar por primer verbo del nombre
    groups = {}
    for s in skills:
        key = s['name'].split('-')[0]
        groups.setdefault(key, []).append(s)

    sorted_groups = sorted(groups.items(), key=lambda x: -len(x[1]))

    while True:
        clear()
        console.print(BANNER)
        console.print(Rule("[bold cyan]📂 EXPLORAR POR CATEGORÍA[/bold cyan]"))
        console.print()

        t = Table(box=box.ROUNDED, border_style="cyan", show_lines=False)
        t.add_column("#", style="dim", width=4)
        t.add_column("Categoría", style="bold white", min_width=20)
        t.add_column("Skills", justify="right", style="cyan")

        for i, (name, slist) in enumerate(sorted_groups[:20], 1):
            t.add_row(str(i), name.capitalize(), str(len(slist)))

        t.add_row("0", "← Volver", "")
        console.print(t)
        console.print()

        try:
            choice = IntPrompt.ask("  [bold cyan]Categoría[/bold cyan]", default=0)
        except (KeyboardInterrupt, EOFError):
            return

        if choice == 0:
            return
        if 1 <= choice <= min(20, len(sorted_groups)):
            cat_name, cat_skills = sorted_groups[choice - 1]
            _browse_category(cat_name, cat_skills)

def _browse_category(cat_name, skills_list):
    while True:
        clear()
        console.print()
        console.print(Rule(f"[bold cyan]📁 {cat_name.upper()}[/bold cyan]"))
        console.print()

        t = Table(box=box.ROUNDED, border_style="cyan", show_lines=True)
        t.add_column("#", style="dim", width=4)
        t.add_column("Skill", style="bold white", min_width=40)

        for i, s in enumerate(skills_list[:25], 1):
            t.add_row(str(i), s['name'])

        t.add_row("0", "← Volver")
        console.print(t)
        console.print()

        try:
            choice = IntPrompt.ask("  [bold cyan]Ver skill[/bold cyan]", default=0)
        except (KeyboardInterrupt, EOFError):
            return

        if choice == 0:
            return
        if 1 <= choice <= min(25, len(skills_list)):
            show_skill_detail(skills_list[choice - 1])

# ─── UI: Skills Ofensivos Rápidos ────────────────────────────────

def mod_offensive():
    """Acceso rápido a skills ofensivos clave."""
    OFFENSIVE = [
        ("🔍 Reconocimiento externo OSINT",        "conducting-external-reconnaissance-with-osint"),
        ("🔍 Reconocimiento interno (BloodHound)",  "conducting-internal-reconnaissance-with-bloodhound-ce"),
        ("💉 SQL Injection manual",                 "exploiting-sql-injection-manually"),
        ("🔑 Ataque Pass-the-Ticket (Kerberos)",    "conducting-pass-the-ticket-attack"),
        ("🪟 DPAPI — Extraer credenciales",         "abusing-dpapi-for-credential-access"),
        ("🪟 Shadow Credentials (AD privesc)",      "abusing-shadow-credentials-for-privesc"),
        ("🌐 OAuth — Device Code Phishing",         "attacking-oauth-with-device-code-phishing"),
        ("🌐 Entra ID (Azure AD) con ROADtools",    "attacking-entra-id-with-roadtools"),
        ("👤 MITM — Simulación de ataque",          "conducting-man-in-the-middle-attack-simulation"),
        ("🔐 Kerberoasting — Detectar/Explotar",    "detecting-kerberoasting-attacks"),
        ("💀 DCSync Attack en Active Directory",    "detecting-dcsync-attack-in-active-directory"),
        ("📡 Bluetooth Low Energy ataques",         "detecting-bluetooth-low-energy-attacks"),
    ]

    while True:
        clear()
        console.print(BANNER)
        console.print(Rule("[bold red]⚔️  SKILLS OFENSIVOS[/bold red]"))
        console.print()

        rows = "\n".join([f"  [cyan][{i}][/cyan] {label}" for i, (label, _) in enumerate(OFFENSIVE, 1)])
        rows += "\n  [red][0][/red] ← Volver"
        console.print(Panel(rows, border_style="red", box=box.ROUNDED, padding=(1, 2)))

        try:
            choice = IntPrompt.ask("  [bold cyan]Opción[/bold cyan]", default=0)
        except (KeyboardInterrupt, EOFError):
            return

        if choice == 0:
            return
        if 1 <= choice <= len(OFFENSIVE):
            _, skill_name = OFFENSIVE[choice - 1]
            skill = next((s for s in load_skills() if s['name'] == skill_name), None)
            if skill:
                show_skill_detail(skill)
            else:
                log(f"Skill no encontrado localmente: {skill_name}", "red")
                pause()

# ─── UI: Stats del Repositorio ───────────────────────────────────

def mod_stats():
    skills = load_skills()
    clear()
    console.print(BANNER)
    console.print(Rule("[bold cyan]📊 ESTADÍSTICAS DEL REPOSITORIO[/bold cyan]"))
    console.print()

    t = Table(box=box.ROUNDED, border_style="cyan")
    t.add_column("Métrica", style="bold white")
    t.add_column("Valor", style="bold cyan", justify="right")
    t.add_row("Total de Skills", str(len(skills)))
    t.add_row("Repositorio", "Anthropic-Cybersecurity-Skills")
    t.add_row("Frameworks", "MITRE ATT&CK, NIST CSF, D3FEND, ATLAS")
    t.add_row("Directorio", str(SKILLS_DIR))
    t.add_row("Logs guardados", str(len(list(LOGS_DIR.glob("*.txt")))) if LOGS_DIR.exists() else "0")
    console.print(t)

    console.print()
    cats = get_categories()
    console.print(Rule("[bold]Top Categorías[/bold]"))
    t2 = Table(box=box.SIMPLE, show_header=False)
    t2.add_column("Cat", style="cyan")
    t2.add_column("N", justify="right")
    for cat, count in cats[:12]:
        t2.add_row(cat.capitalize(), str(count))
    console.print(t2)
    pause()

# ─── MAIN ────────────────────────────────────────────────────────

MAIN_MENU = """
  [cyan][1][/cyan]  🔍 Buscar skill por palabras clave
  [cyan][2][/cyan]  📂 Explorar por categoría
  [cyan][3][/cyan]  ⚔️  Skills ofensivos rápidos
  [cyan][4][/cyan]  📊 Estadísticas del repositorio
  [red][0][/red]  ❌ Salir
"""

def main():
    signal.signal(signal.SIGINT, lambda s, f: None)
    actions = {1: mod_search, 2: mod_browse, 3: mod_offensive, 4: mod_stats}

    # Verificar repositorio
    if not SKILLS_DIR.exists():
        clear()
        console.print(BANNER)
        console.print(Panel(
            "[bold red]❌ No se encontró el repositorio de skills.[/bold red]\n\n"
            "Clona el repositorio primero:\n"
            "[bold white]git clone https://github.com/mukul975/Anthropic-Cybersecurity-Skills[/bold white]",
            border_style="red", box=box.ROUNDED
        ))
        sys.exit(1)

    while True:
        clear()
        console.print(BANNER)
        skills = load_skills()
        console.print(Panel(
            MAIN_MENU,
            title=f"[bold cyan]🔱 PRETEL[/bold cyan] [dim]({len(skills)} skills cargados)[/dim]",
            subtitle="[dim]Selecciona una opción[/dim]",
            border_style="cyan",
            box=box.DOUBLE,
            padding=(1, 2)
        ))

        try:
            choice = IntPrompt.ask("  [bold cyan]⟩[/bold cyan]", default=0)
        except (KeyboardInterrupt, EOFError):
            choice = 0

        if choice == 0:
            console.print("\n  [bold red]👋 ¡Hasta luego![/bold red]\n")
            sys.exit(0)
        elif choice in actions:
            actions[choice]()

if __name__ == "__main__":
    main()
