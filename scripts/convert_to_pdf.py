import os
import win32com.client

def pptx_to_pdf(input_pptx, output_pdf):
    input_pptx = os.path.abspath(input_pptx)
    output_pdf = os.path.abspath(output_pdf)
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    
    print(f"Converting: {input_pptx} -> {output_pdf}")
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    # ppSaveAsPDF format code is 32
    try:
        deck = powerpoint.Presentations.Open(input_pptx, WithWindow=False)
        deck.SaveAs(output_pdf, 32)
        deck.Close()
        print("Successfully exported to PDF!")
    finally:
        powerpoint.Quit()

if __name__ == "__main__":
    pptx_to_pdf(r"E:\Airtel\submission\Halo_Thapar.pptx", r"E:\Airtel\submission\Halo_Thapar.pdf")
