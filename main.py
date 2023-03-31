import openai
import PyPDF2

# Set up OpenAI API credentials
openai.api_key = "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"

# Define function to generate text from ChatGPT
def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

# Define function to convert text to PDF
def convert_to_pdf(text):
    pdf_writer = PyPDF2.PdfFileWriter()
    pdf_writer.addPage(PyPDF2.pdf.PageObject.createFromString(text))
    with open('output.pdf', 'wb') as output:
        pdf_writer.write(output)

# Main function to interact with ChatGPT and generate PDF response
def main():
    # Get input from user
    prompt = input("Enter your prompt: ")

    # Generate response from ChatGPT
    response_text = generate_text(prompt)

    # Convert response to PDF
    convert_to_pdf(response_text)

    # Print success message
    print("PDF file generated successfully!")

if __name__ == '__main__':
    main()
