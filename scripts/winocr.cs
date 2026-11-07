using System;
using System.IO;
using System.Threading.Tasks;
using Windows.Storage;
using Windows.Graphics.Imaging;
using Windows.Media.Ocr;

class Program {
    static void Main(string[] args) {
        if (args.Length == 0) {
            Console.WriteLine("Usage: winocr <image_path>");
            return;
        }
        try {
            string text = RunOcr(Path.GetFullPath(args[0])).GetAwaiter().GetResult();
            Console.WriteLine(text);
        } catch (Exception ex) {
            Console.Error.WriteLine("Error: " + ex.ToString());
        }
    }

    static async Task<string> RunOcr(string path) {
        var file = await WindowsRuntimeSystemExtensions.AsTask(StorageFile.GetFileFromPathAsync(path));
        using (var stream = await WindowsRuntimeSystemExtensions.AsTask(file.OpenAsync(FileAccessMode.Read))) {
            var decoder = await WindowsRuntimeSystemExtensions.AsTask(BitmapDecoder.CreateAsync(stream));
            var bitmap = await WindowsRuntimeSystemExtensions.AsTask(decoder.GetSoftwareBitmapAsync());
            var engine = OcrEngine.TryCreateFromUserProfileLanguages();
            if (engine == null) {
                throw new Exception("Could not create OCR engine for user profile language.");
            }
            var result = await WindowsRuntimeSystemExtensions.AsTask(engine.RecognizeAsync(bitmap));
            return result.Text;
        }
    }
}
