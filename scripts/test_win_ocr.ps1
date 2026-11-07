try {
    [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
    [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime] | Out-Null
    [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime] | Out-Null

    $absPath = "E:\Airtel\6ae1873397bc1_digital\YTL_TrackA_Udyam_Digital_Data\kyc_documents\K02_gst_certificate.png"
    
    $op1 = [Windows.Storage.StorageFile]::GetFileFromPathAsync($absPath)
    while ($op1.Status -eq [Windows.Foundation.AsyncStatus]::Started) { Start-Sleep -Milliseconds 10 }
    $file = $op1.GetResults()

    $op2 = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read)
    while ($op2.Status -eq [Windows.Foundation.AsyncStatus]::Started) { Start-Sleep -Milliseconds 10 }
    $stream = $op2.GetResults()

    $op3 = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
    while ($op3.Status -eq [Windows.Foundation.AsyncStatus]::Started) { Start-Sleep -Milliseconds 10 }
    $decoder = $op3.GetResults()

    $op4 = $decoder.GetSoftwareBitmapAsync()
    while ($op4.Status -eq [Windows.Foundation.AsyncStatus]::Started) { Start-Sleep -Milliseconds 10 }
    $bitmap = $op4.GetResults()

    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
    $op5 = $engine.RecognizeAsync($bitmap)
    while ($op5.Status -eq [Windows.Foundation.AsyncStatus]::Started) { Start-Sleep -Milliseconds 10 }
    $res = $op5.GetResults()

    Write-Output "=== OCR TEXT EXTRACTED ==="
    Write-Output $res.Text
} catch {
    Write-Error $_.Exception.ToString()
}
