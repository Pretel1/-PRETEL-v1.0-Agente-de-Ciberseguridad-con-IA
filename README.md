# 🔱 PRETEL — AI Security Agent

<div align="center">

```
  ██████╗ ██████╗ ███████╗████████╗███████╗██╗
  ██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝██║
  ██████╔╝██████╔╝█████╗     ██║   █████╗  ██║
  ██╔═══╝ ██╔══██╗██╔══╝     ██║   ██╔══╝  ██║
  ██║     ██║  ██║███████╗   ██║   ███████╗███████╗
  ╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚══════╝
```

**Terminal-based AI Security Agent powered by 817 Cybersecurity Skills**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-red?style=flat-square&logo=linux)
![Skills](https://img.shields.io/badge/Skills-817-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

</div>

---

## ¿Qué es PRETEL?

**PRETEL** es un agente de ciberseguridad por terminal para Kali Linux que integra una librería de **817 skills de seguridad** con guías paso a paso, comandos reales y mapeos MITRE ATT&CK. Permite buscar, explorar y ejecutar técnicas de pentesting directamente desde la terminal.

## Características

- 🔍 **Búsqueda inteligente** — encuentra el skill correcto por palabras clave en español o inglés
- 📂 **Explorador por categorías** — navega 66 categorías: Exploiting, Detecting, Analyzing, Hunting...
- ⚔️ **Skills ofensivos rápidos** — acceso directo a OSINT, Kerberoasting, MITM, Pass-the-Ticket, DPAPI
- ⚡ **Ejecución directa** — detecta y ejecuta los comandos del skill con un número
- ✅ **Verificación de herramientas** — indica qué herramientas están instaladas antes de ejecutar
- 🎯 **MITRE ATT&CK** — cada skill mapeado a técnicas y tácticas reales
- 📊 **817 skills** cubriendo 29 dominios de seguridad

## Instalación

```bash
# 1. Clonar este repositorio
git clone https://github.com/TU_USUARIO/PRETEL.git
cd PRETEL

# 2. Clonar la librería de skills
git clone https://github.com/mukul975/Anthropic-Cybersecurity-Skills

# 3. Instalar dependencias
pip install rich

# 4. Ejecutar
python3 pretel.py
```

## Uso

```bash
python3 pretel.py
# o con root para herramientas que lo requieren:
sudo python3 pretel.py
```

### Menú Principal

```
╔══════════════════════ 🔱 PRETEL (817 skills cargados) ══════════════════╗
║  [1]  🔍 Buscar skill por palabras clave                               ║
║  [2]  📂 Explorar por categoría                                         ║
║  [3]  ⚔️  Skills ofensivos rápidos                                       ║
║  [4]  📊 Estadísticas del repositorio                                   ║
║  [0]  ❌ Salir                                                          ║
╚═════════════════════════════════════════════════════════════════════════╝
```

### Ejemplos de búsqueda

```
> nmap reconocimiento
> sql injection
> windows privesc
> kerberoasting
> osint dominio
> wifi bluetooth
```

## Dominios cubiertos

| Dominio | Skills |
|---|---|
| Performing (pentesting activo) | 172 |
| Implementing (configuración segura) | 168 |
| Detecting (detección de ataques) | 96 |
| Analyzing (análisis forense/logs) | 76 |
| Hunting (threat hunting) | 37 |
| Building (herramientas/pipelines) | 36 |
| Exploiting (explotación) | 34 |

## Frameworks mapeados

- **MITRE ATT&CK** v19.1 — 15 tácticas, 286 técnicas
- **NIST CSF 2.0** — 6 funciones
- **MITRE D3FEND** v1.3 — contramedidas defensivas
- **MITRE ATLAS** v5.4 — amenazas AI/ML

## Requisitos

- Python 3.10+
- Kali Linux (recomendado) o cualquier Linux con herramientas de seguridad
- `pip install rich`
- Repositorio de skills clonado en `./Anthropic-Cybersecurity-Skills/`

## ⚠️ Aviso Legal

Este tool es para **uso ético y autorizado únicamente**. Solo úsalo en sistemas que te pertenecen o en los que tienes permiso explícito por escrito. El autor no se responsabiliza del mal uso.

## Licencia

MIT License — ver [LICENSE](LICENSE)
