tell application "iTerm"
  if current window is equal to missing value then
    create window with default profile
  end if
end tell
