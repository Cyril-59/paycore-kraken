#!/usr/bin/env python3
"""
Script de vérification de sécurité PayCore MCP.
Détecte les violations de sécurité courantes.
"""

import re
import sys
from pathlib import Path

# Configurations
FORBIDDEN_SQL_WORDS = ["insert", "update", "delete", "drop", "alter", "create", "pragma"]
API_KEY_PATTERNS = [
    r"api_key\s*=\s*['\"]",  # api_key = "..."
    r"GEMINI_API_KEY\s*=\s*['\"]",  # GEMINI_API_KEY = "..."
    r"sk-[a-zA-Z0-9]{20,}",  # OpenAI format
]
SUSPICIOUS_DATA_PATTERNS = [
    r"\d{4}-\d{4}",  # Customer ID format
    r"[a-z]+@paycore\.com",  # Production email
    r"prod.*database",  # Production reference
]

def check_file(filepath: str) -> dict:
    """Vérifie un fichier pour les problèmes de sécurité."""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return {"file": filepath, "error": str(e), "issues": []}
    
    # Vérifier les clés API en dur
    for i, line in enumerate(lines, 1):
        for pattern in API_KEY_PATTERNS:
            if re.search(pattern, line):
                issues.append({
                    "line": i,
                    "type": "API_KEY_HARDCODED",
                    "message": f"Clé API détectée en dur : {line.strip()}",
                    "severity": "CRITICAL"
                })
    
    # Vérifier les données suspectes
    for i, line in enumerate(lines, 1):
        for pattern in SUSPICIOUS_DATA_PATTERNS:
            if re.search(pattern, line) and not "exemple" in line.lower() and not "fictif" in line.lower():
                issues.append({
                    "line": i,
                    "type": "SUSPICIOUS_DATA",
                    "message": f"Donnée potentiellement réelle : {line.strip()}",
                    "severity": "WARNING"
                })
    
    # Pour db_tools.py : vérifier validate_readonly_query
    if "db_tools.py" in filepath:
        if "from_incidents" not in content and "from incidents" not in content:
            issues.append({
                "line": 0,
                "type": "MISSING_INCIDENTS_CHECK",
                "message": "Pas de vérification 'from incidents' détectée",
                "severity": "HIGH"
            })
        
        if "LIMIT" not in content and "limit" not in content:
            issues.append({
                "line": 0,
                "type": "MISSING_LIMIT",
                "message": "Pas de vérification LIMIT 10 détectée",
                "severity": "HIGH"
            })
    
    # Pour agent_demo.py : vérifier os.getenv
    if "agent_demo.py" in filepath or "mcp_server.py" in filepath:
        if "os.getenv" not in content and "GEMINI_API_KEY" in content:
            issues.append({
                "line": 0,
                "type": "ENV_VAR_MISSING",
                "message": "GEMINI_API_KEY détecté mais os.getenv() non utilisé",
                "severity": "HIGH"
            })
    
    return {
        "file": filepath,
        "issues": issues,
        "total": len(issues)
    }

def main():
    """Scan tous les fichiers .py du projet."""
    project_root = Path(__file__).parent.parent.parent.parent  # Remonte à la racine
    py_files = list(project_root.glob("*.py"))
    
    print("🔍 Vérification de sécurité PayCore MCP\n")
    print("=" * 60)
    
    total_issues = 0
    critical_issues = 0
    
    for py_file in py_files:
        result = check_file(str(py_file))
        
        if result.get("error"):
            print(f"❌ {py_file.name} : {result['error']}")
            continue
        
        if result["total"] > 0:
            print(f"\n📄 {py_file.name}")
            for issue in result["issues"]:
                severity = issue["severity"]
                icon = "🔴" if severity == "CRITICAL" else "🟠" if severity == "HIGH" else "🟡"
                print(f"  {icon} [{severity}] L{issue['line']}: {issue['message']}")
                if severity == "CRITICAL":
                    critical_issues += 1
                total_issues += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Scan terminé : {total_issues} problème(s) détecté(s)")
    
    if critical_issues > 0:
        print(f"🚨 {critical_issues} CRITIQUE(S) : Action immédiate requise !")
        return 1
    elif total_issues > 0:
        print(f"⚠️  {total_issues - critical_issues} avertissement(s)")
        return 0
    else:
        print("✨ Aucun problème détecté !")
        return 0

if __name__ == "__main__":
    sys.exit(main())
