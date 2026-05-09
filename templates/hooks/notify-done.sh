#!/bin/bash
# notify-done.sh — Send a desktop notification when Claude finishes
# Usage: Add to .claude/settings.json Stop hooks
#
# Configuration:
# {
#   "hooks": {
#     "Stop": [{
#       "matcher": "",
#       "hooks": ["./scripts/notify-done.sh"]
#     }]
#   }
# }

TITLE="Claude Code"
MESSAGE="Task completed!"

# macOS
if command -v osascript &>/dev/null; then
    osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\"" 2>/dev/null
    exit 0
fi

# Linux (notify-send)
if command -v notify-send &>/dev/null; then
    notify-send "$TITLE" "$MESSAGE" 2>/dev/null
    exit 0
fi

# Windows (WSL) — PowerShell toast notification
if command -v powershell.exe &>/dev/null; then
    powershell.exe -Command "
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom, ContentType = WindowsRuntime] | Out-Null
        \$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        \$xml.LoadXml('<toast><visual><binding template=\"ToastText02\"><text id=\"1\">$TITLE</text><text id=\"2\">$MESSAGE</text></binding></visual></toast>')
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Claude Code').Show(\$xml)
    " 2>/dev/null
    exit 0
fi

# Fallback: terminal bell
echo -e '\a'
exit 0
