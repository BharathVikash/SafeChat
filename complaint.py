from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_complaint_document(name, mobile_number, message, time, output_directory="  Complains"):
    # Create the specified output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Construct the file path with the specified directory
    file_path = os.path.join(
        output_directory, f"{name}_cyberbullying_complaint.pdf")

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    complaint_title = Paragraph(
        "Complaint Against Cyberbullying", styles['Title'])
    story.append(complaint_title)

    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Name of the Bully: {name}", normal_style))
    story.append(
        Paragraph(f"Mobile Number of the Bully: {mobile_number}", normal_style))
    story.append(Paragraph(f"Message by the Bully: {message}", normal_style))
    story.append(Paragraph(f"Time of the Message: {time}", normal_style))

    complaint_text = (
        "I, the undersigned, hereby lodge this complaint against the above-named individual for engaging in cyberbullying activities against me. "
        "The offensive message(s) as described above were sent to me on the mentioned date and time, causing emotional distress and harassment. "
        "I request immediate action against the offender to prevent further harassment."
    )

    story.append(Spacer(1, 12))
    story.append(Paragraph("Complaint Details:", styles['Heading2']))
    story.append(Paragraph(complaint_text, normal_style))

    story.append(Spacer(1, 12))

    story.append(Paragraph("Signature: ________________", normal_style))
    story.append(Paragraph("Date: ________________", normal_style))

    doc.build(story)
    print(
        f"Complaint document generated in the '{output_directory}' directory as '{file_path}'.")


if __name__ == "__main__":
    name = input("Enter the name of the bully: ")
    mobile_number = input("Enter the mobile number of the bully: ")
    message = input("Enter the message sent by the bully: ")
    time = input("Enter the time the message was written: ")

    generate_complaint_document(name, mobile_number, message, time)
