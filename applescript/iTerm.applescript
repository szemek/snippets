tell application "iTerm"
  if current window is equal to missing value then
    create window with default profile
  end if
  tell current window
    tell (create tab with default profile)
      tell current session
        write text "uptime"
      end tell
    end tell
  end tell
end tell
