param(
    [Parameter(Mandatory=$true)]
    [string]$ImagePath
)

try {
    [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
    [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime] | Out-Null
    [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime] | Out-Null

    $absPath = (Resolve-Path $ImagePath).Path
    $file = [Windows.Storage.StorageFile]::GetFileFromPathAsync($absPath).GetAwaiter().GetResult()
    $stream = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read).GetAwaiter().GetResult()
    $decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
    $bitmap = $decoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
    $ocrResult = $engine.RecognizeAsync($bitmap).GetAwaiter().GetResult()
    Write-Output $ocrResult.Text
} catch {
    Write-Error $_.Exception.Message
}
