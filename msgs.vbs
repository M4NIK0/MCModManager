Set objShell = CreateObject("Wscript.Shell")

If MsgBox("Installer un nouveau modpack ?", vbYesNo, "") = vbYes Then
 If MsgBox("Telecharger une nouvelle instance forge ?", vbYesNo, "") = vbYes Then
  objShell.Run "Cmd /k start 'lib\forge_load.bat'"
  MsgBox "Appuye sur Ok lorsque forge est installe.", 0, ""
 End If
 objShell.Run "Cmd /k install.bat"
End If

If MsgBox("Enregistrer un pack deja installe ?", vbYesNo, "") = vbYes Then
 objShell.Run "Cmd /k backup.bat"
End If

If MsgBox("Charger une config de pack ?", vbYesNo, "") = vbYes Then
 objShell.Run "Cmd /k load.bat"
End If

If MsgBox("Mettre un pack a jour ? (en cas de changements manuels)", vbYesNo, "") = vbYes Then
 If MsgBox("Update des mods ?", vbYesNo, "") = vbYes Then
  objShell.Run "Cmd /k updater/mods_update.bat"
 End If
 If MsgBox("Update des parametres ?", vbYesNo, "") = vbYes Then
  objShell.Run "Cmd /k updater/options_update.bat"
 End If
End If