# AutoKeyPresser and AutoClicker

A Windows program with two independent tabs: keyboard automation and AutoClicker.
No additional libraries are required.

## Keyboard tab

1. Double-click `AutoKeyPresser and AutoClicker.vbs`. It starts the program without opening a Command Prompt window.
2. Select a key from the list, or click **Capture key** and press it.
3. Select a target:
   - **Any window (normal)**: the program's original behavior.
   - **Only while the selected window is active**: input is sent only while that window is in the foreground. If you switch windows, the key is released immediately and the program waits.
   - **Send to the selected window in the background**: attempts to send input directly without bringing the window to the foreground.
   - **Focus window, send input, and switch back (Chrome/games)**: brings the selected window forward, sends the input, and then restores the previously active window.
4. If you choose a specific window, select it from the list. Click **Refresh windows** if it was opened after the program.
5. Select an action:
   - **Hold for the selected duration**: holds the key and releases it after the configured duration.
   - **Press repeatedly**: holds the key for the configured duration, releases it, waits for the interval, and repeats.
6. Click **ENABLE** or press **F8** from any window.
7. Press **F8** again to stop immediately.

`F8` is reserved as the keyboard automation hotkey and cannot be automated.

## AutoClicker tab

1. Select the **Left**, **Right**, or **Middle** mouse button.
2. Set the interval between clicks. The minimum is `0.01` second.
3. Select the click position:
   - **Current mouse position**: continuously clicks wherever the pointer is located.
   - **Fixed position**: enter X and Y, or click **Use current position**. The pointer returns to its previous location after each click.
4. Click **ENABLE AUTOCLICKER** or press **F7**.
5. Press **F7** again to stop immediately.

Keyboard automation (`F8`) and the AutoClicker (`F7`) can run at the same time.

## Notes

- Time values accept either a comma or a period (`1,5` or `1.5`).
- Closing the window releases any key or mouse button currently being held.
- Background mode uses Windows messages. Chrome, games, and protected applications usually ignore these messages. For those applications, use **Focus window, send input, and switch back (Chrome/games)**.
- In automatic focus mode, the selected window stays in the foreground for the entire **Hold duration**. Use `0.05` or `0.1` second for a quick tap.
- Some games running as administrator only accept input if this program is also run as administrator.
