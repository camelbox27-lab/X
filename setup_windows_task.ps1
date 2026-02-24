Param(
    [string]$TaskName = "AIKuponOtomasyon",
    [string]$ProjectPath = "$PSScriptRoot",
    [string]$RunAt = "10:00"
)

$batPath = Join-Path $ProjectPath "run_otomatik_kupon.bat"

if (-Not (Test-Path $batPath)) {
    Write-Error "run_otomatik_kupon.bat bulunamadi: $batPath"
    exit 1
}

$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c \"$batPath\""
$trigger = New-ScheduledTaskTrigger -Daily -At $RunAt
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Force | Out-Null

Write-Host "Gorev olusturuldu: $TaskName"
Write-Host "Calisma saati: $RunAt"
Write-Host "Komut: $batPath"
