import os
import socket
import subprocess
import time
import sys
import shutil
import ctypes

# === CONFIGURATION ===
VNC_INSTALLER = "tightvnc-2.8.85-gpl-setup-64bit.msi"
VNC_REG_FILE = "vnc.reg"

# === FONCTIONS UTILITAIRES ===

def bring_console_to_front():
    """Met la console Windows au premier plan."""
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.SetForegroundWindow(hwnd)
    except Exception as e:
        print(f"⚠️ Impossible de mettre la console au premier plan : {e}")

def get_local_ip():
    """Retourne l'adresse IP locale."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"

# === TIGHTVNC ===

def stop_tightvnc_service():
    bring_console_to_front()
    print("🧱 Arrêt rapide du service TightVNC...")
    subprocess.run("taskkill /F /IM tvnserver.exe >nul 2>&1", shell=True)
    time.sleep(0.5)
    result = subprocess.run("sc query tvnserver", capture_output=True, text=True, shell=True)
    if "RUNNING" in result.stdout.upper():
        print("⏳ Service encore actif — tentative d’arrêt forcé...")
        subprocess.run("sc stop tvnserver >nul 2>&1", shell=True)
        time.sleep(1)
    for _ in range(3):
        result = subprocess.run("sc query tvnserver", capture_output=True, text=True, shell=True)
        if "STOPPED" in result.stdout.upper() or "FAILED" in result.stdout.upper():
            break
        time.sleep(0.5)
    print("✅ Service TightVNC arrêté ou inexistant.")

def uninstall_tightvnc():
    bring_console_to_front()
    print("🧹 Vérification de la présence de TightVNC...")
    subprocess.run("taskkill /F /IM tvnserver.exe >nul 2>&1", shell=True)
    subprocess.run("taskkill /F /IM tvnviewer.exe >nul 2>&1", shell=True)
    time.sleep(1)

    print("🔍 Recherche du code produit MSI de TightVNC...")
    result = subprocess.run(
        r'reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall /s /f TightVNC',
        shell=True, capture_output=True, text=True, errors="ignore"
    )
    product_code = None
    for line in result.stdout.splitlines():
        if line.strip().startswith("{") and line.strip().endswith("}"):
            product_code = line.strip()
            break

    if product_code:
        print(f"⚙️ Désinstallation silencieuse de TightVNC ({product_code})...")
        subprocess.run(["msiexec", "/x", product_code, "/quiet", "/norestart"], shell=True)
        time.sleep(3)
        print("✅ TightVNC désinstallé avec succès.")
    else:
        print("ℹ️ TightVNC n’est pas installé ou GUID introuvable.")

    subprocess.run("taskkill /F /IM tvnserver.exe >nul 2>&1", shell=True)
    subprocess.run("taskkill /F /IM tvnviewer.exe >nul 2>&1", shell=True)

def install_tightvnc():
    bring_console_to_front()
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    installer = os.path.join(base_path, VNC_INSTALLER)

    if not os.path.exists(installer):
        print(f"❌ Fichier d'installation {installer} introuvable.")
        return

    temp_installer = os.path.join(os.getcwd(), "tightvnc_temp.msi")
    shutil.copy(installer, temp_installer)

    print("📦 Installation silencieuse de TightVNC...")
    subprocess.run(["msiexec", "/i", temp_installer, "/quiet", "/norestart"], shell=True)
    time.sleep(10)
    print("✅ Installation terminée.")
    os.remove(temp_installer)

def merge_vnc_registry():
    bring_console_to_front()
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    reg_file_path = os.path.join(base_path, VNC_REG_FILE)

    if os.path.exists(reg_file_path):
        print("🧩 Fusion du fichier vnc.reg avec le registre Windows...")
        subprocess.run(["regedit", "/s", reg_file_path], shell=True)
        print("✅ Paramètres TightVNC importés.")
    else:
        print("⚠️ Fichier vnc.reg introuvable, fusion ignorée.")

def restart_vnc_service():
    bring_console_to_front()
    print("🔄 Préparation du redémarrage du service TightVNC...")

    result = subprocess.run("sc query tvnserver", shell=True, capture_output=True, text=True)
    if "FAILED" in result.stdout.upper() or "does not exist" in result.stdout.lower():
        print("⚠️ Service TightVNC non trouvé. Attente avant relance...")
        time.sleep(5)

    print("🧱 Étape 1/3 — Arrêt du service TightVNC...")
    subprocess.run("sc stop tvnserver >nul 2>&1", shell=True)
    subprocess.run("taskkill /F /IM tvnserver.exe >nul 2>&1", shell=True)
    time.sleep(3)

    print("🔎 Étape 2/3 — Vérification de l’arrêt complet...")
    for _ in range(5):
        result = subprocess.run("sc query tvnserver", shell=True, capture_output=True, text=True)
        if "STOPPED" in result.stdout.upper():
            break
        time.sleep(1)

    print("🚀 Étape 3/3 — Démarrage du service TightVNC...")
    subprocess.run("sc start tvnserver >nul 2>&1", shell=True)
    time.sleep(3)

    result = subprocess.run("sc query tvnserver", shell=True, capture_output=True, text=True)
    if "RUNNING" in result.stdout.upper():
        print("✅ Service TightVNC démarré avec succès.")
    else:
        print("⚠️ Impossible de confirmer le démarrage du service.")

# === PING LOOP ===

def ping_loop():
    local_ip = get_local_ip()
    bring_console_to_front()
    print(f"\n🖥️ Adresse IP locale : {local_ip}\n")
    while True:
        try:
            result = subprocess.run("ping -n 1 8.8.8.8", shell=True, capture_output=True, text=True)
            latency = "Aucune réponse"
            if "temps" in result.stdout or "time" in result.stdout:
                for line in result.stdout.splitlines():
                    if "temps" in line or "time" in line:
                        latency = line.strip()
                        break
            current_time = time.strftime("%H:%M:%S")
            print(f"[{current_time}] 📶 {latency} | IP locale : {local_ip}")
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Surveillance arrêtée par l'utilisateur.")
            break

# === PROGRAMME PRINCIPAL ===

if __name__ == "__main__":
    bring_console_to_front()
    print("🚀 Initialisation du script TightVNC + Ping Monitor...")

    stop_tightvnc_service()
    uninstall_tightvnc()
    install_tightvnc()
    merge_vnc_registry()
    restart_vnc_service()

    print("\n=== Surveillance Réseau Démarrée ===")
    ping_loop()
