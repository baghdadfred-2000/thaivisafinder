# preview.ps1 - zero-install local preview server for ThaiVisaFinder.
# Mirrors the live Netlify setup: serves /assets/* from the site root AND maps
# clean URLs like /about -> about.html, so the header + footer work exactly
# like production when you preview locally. No Node, no installs needed.

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$port = 8000
$prefix = "http://localhost:$port/"

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($prefix)
try {
    $listener.Start()
} catch {
    Write-Host "Could not start server on $prefix" -ForegroundColor Red
    Write-Host $_.Exception.Message
    Read-Host "Press Enter to close"
    exit 1
}

Write-Host ""
Write-Host "  ThaiVisaFinder preview server" -ForegroundColor Green
Write-Host "  Serving: $root"
Write-Host "  Open:    $prefix" -ForegroundColor Cyan
Write-Host "  Stop:    press Ctrl+C, then close this window"
Write-Host ""
Start-Process $prefix

$mime = @{
    ".html"="text/html; charset=utf-8";  ".htm"="text/html; charset=utf-8"
    ".js"="text/javascript; charset=utf-8"; ".mjs"="text/javascript; charset=utf-8"
    ".css"="text/css; charset=utf-8";    ".json"="application/json; charset=utf-8"
    ".svg"="image/svg+xml";              ".png"="image/png"
    ".jpg"="image/jpeg";                 ".jpeg"="image/jpeg"
    ".gif"="image/gif";                  ".webp"="image/webp"
    ".ico"="image/x-icon";               ".woff"="font/woff"
    ".woff2"="font/woff2";               ".ttf"="font/ttf"
    ".txt"="text/plain; charset=utf-8";  ".xml"="application/xml; charset=utf-8"
    ".map"="application/json; charset=utf-8"
}

while ($listener.IsListening) {
    try {
        $ctx = $listener.GetContext()
    } catch {
        break
    }
    $req = $ctx.Request
    $res = $ctx.Response
    try {
        $path = [System.Uri]::UnescapeDataString($req.Url.AbsolutePath)
        if ($path -eq "/") { $path = "/index.html" }
        $rel  = $path.TrimStart("/")
        $file = Join-Path $root $rel

        # Clean-URL resolution, like Netlify: /about -> about.html, /dir -> /dir/index.html
        if (-not (Test-Path -LiteralPath $file -PathType Leaf)) {
            $asHtml = Join-Path $root ($rel + ".html")
            $asIndex = Join-Path $file "index.html"
            if (Test-Path -LiteralPath $asHtml -PathType Leaf) {
                $file = $asHtml
            } elseif (Test-Path -LiteralPath $asIndex -PathType Leaf) {
                $file = $asIndex
            }
        }

        if (Test-Path -LiteralPath $file -PathType Leaf) {
            $ext = [System.IO.Path]::GetExtension($file).ToLower()
            $ct  = $mime[$ext]; if (-not $ct) { $ct = "application/octet-stream" }
            $bytes = [System.IO.File]::ReadAllBytes($file)
            $res.StatusCode  = 200
            $res.ContentType = $ct
            $res.OutputStream.Write($bytes, 0, $bytes.Length)
            Write-Host ("200  {0}" -f $path)
        } else {
            $nf = Join-Path $root "404.html"
            if (Test-Path -LiteralPath $nf -PathType Leaf) {
                $bytes = [System.IO.File]::ReadAllBytes($nf)
                $res.StatusCode  = 404
                $res.ContentType = "text/html; charset=utf-8"
                $res.OutputStream.Write($bytes, 0, $bytes.Length)
            } else {
                $b = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $path")
                $res.StatusCode = 404
                $res.OutputStream.Write($b, 0, $b.Length)
            }
            Write-Host ("404  {0}" -f $path) -ForegroundColor DarkYellow
        }
    } catch {
        Write-Host ("ERR  {0}" -f $_.Exception.Message) -ForegroundColor Red
    } finally {
        $res.OutputStream.Close()
    }
}
