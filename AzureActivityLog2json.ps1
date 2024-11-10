$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = New-Object System.Text.UTF8Encoding
$Start = (Get-Date).AddDays(-7)
$End = (Get-Date)
#$DTfmt = 'yyyy:MM:dd_HH:mm:ss'
#$OUT_FILE = [Management.Automation.WildcardPattern]::Escape(('AzureAuditLog_{0}-{1}.json' -f $Start.ToString($DTfmt), $End.ToString($DTfmt)))
$OUT_FILE = 'AzureAuditLog.json' 


$AuObj = Get-AzActivityLog -StartTime $Start -EndTime $End
$AuObj | Select-Object -Property * | ConvertTo-Json -Depth 99 | Set-Content -Path $OUT_FILE 

"File for processing created:`n`t{0}" -f $OUT_FILE
