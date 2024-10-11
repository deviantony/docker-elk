# VHS - terminal recorder
# https://github.com/charmbracelet/vhs

Output demo.gif

Require docker

Set Shell bash
Set FontSize 24
Set Width 1500
Set Height 1200
Set WindowBar Rings
Set TypingSpeed 75ms
Set Theme "iTerm2 Light Background"
#Set Theme "iTerm2 Dark Background"

Hide

# BEGIN - Reset to clean state
Type "docker compose down setup"
Enter
Sleep 2s
Type "docker compose down -v"
Enter
Sleep 6s
Type "docker compose up elasticsearch -d"
Enter
Sleep 20s
Type "docker compose down"
Enter
Sleep 6s
Ctrl+L
# END - Reset to clean state

Show

Type "docker compose up setup"
Sleep 3s
Enter
Sleep 20s

Enter 2
Type "docker compose up -d"
Sleep 3s
Enter
Sleep 6s

Enter 2
Type "curl -s http://localhost:9200 -u elastic:changeme"
Sleep 3s
Enter
Sleep 12s

Enter 2
Type "👉 Open your web browser at http://localhost:5601 🚀📈"
Sleep 15s
