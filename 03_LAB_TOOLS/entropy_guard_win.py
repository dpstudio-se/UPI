import time
import os

# Sökväg till Windows Firewall-loggen
LOG_FILE = r'C:\Windows\System32\LogFiles\Firewall\pfirewall.log'
JOURNAL_FILE = r'C:\Users\Admin\WORKSPACE_EMILIA_T800_VORTEX\01_JOURNAL\security_alerts.log'

def monitor_win_firewall():
    print('--- [ENTROPY-GUARD: WINDOWS ACTIVE] ---')
    # Skapa journal-mapp om den saknas
    os.makedirs(os.path.dirname(JOURNAL_FILE), exist_ok=True)
    
    # Vänta på att loggfilen skapas av Windows
    while not os.path.exists(LOG_FILE):
        print('Väntar på att firewall-loggfilen ska skapas...')
        time.sleep(2)

    file = open(LOG_FILE, 'r')
    file.seek(0, os.SEEK_END)
    
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
            
        if 'DROP' in line:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            alert = f'[{timestamp}] Dissonans detekterad (Windows): {line.strip()}'
            print(alert)
            
            with open(JOURNAL_FILE, 'a') as f:
                f.write(alert + '\n')

if __name__ == '__main__':
    try:
        monitor_win_firewall()
    except KeyboardInterrupt:
        print('--- [ENTROPY-GUARD: STANDBY] ---')
