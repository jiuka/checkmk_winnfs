Write-Host '<<<winnfsserverconfiguration:sep(0)>>>'
try {
    $cfg = Get-NfsServerConfiguration
    $cfg | Format-List
    Write-Host "Clients : $(@(Get-NFSMountedClient).Length)"
    Write-Host "Sessions : $(@(Get-NFSSession).Length)"
} catch {
    Break
}

Write-Host '<<<winnfsshare:sep(124)>>>'
write-host "Name|Online|Clustered|Authentication|AnonymousAccess|UnmappedUserAccess"
try {
    Get-NFSShare | ForEach {
        Write-Host "$($_.Name)|$($_.IsOnline)|$($_.IsClustered)|$($_.Authentication -join ',')|$($_.AnonymousAccess)|$($_.UnmappedUserAccess)"
    }
} catch {
    Break
}
