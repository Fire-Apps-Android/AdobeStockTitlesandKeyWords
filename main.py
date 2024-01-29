import os

import PIL.Image
import google.generativeai as genai


def get_image_names(folder_path):
    files = os.listdir(folder_path)
    image_files = [file for file in files if file.lower().endswith(('.jpg', '.jpeg'))]
    return image_files


global _prompt


def main(prompt):
    if prompt == "null":
        _prompt = ("Give a seo optimized title for this picture and give 60 seo optimized trending keywords for this "
                   "picture to upload adobe stock, Important result must not add extra titles only need title and "
                   "keywords without use numbers and use comma separator for keywords separation and all only in "
                   "english")
    else:
        _prompt = prompt
    directory = 'Output'
    if not os.path.exists(directory):
        os.makedirs(directory)
    folder_path = 'Images'
    image_names = get_image_names(folder_path)

    GOOGLE_API_KEY = "AIzaSyBqchj9ztlb8wcdjHYeGIFmRAIIxTyj5eg"

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro-vision')

    for i in range(0, len(image_names)):
        img = PIL.Image.open(f'Images/{image_names[i]}')

        response = model.generate_content([
            _prompt,
            img], stream=True)
        response.resolve()
        print(f'Image {i + 1}:{image_names[i]}')
        print(response.text.replace("**", ''))

        try:
            file_path = "Output/output.txt"
            with open(file_path, 'a') as file:
                file.write(f'\nImage {i + 1}:{image_names[i]}\n')
                file.write(response.text.replace("**", '').replace(' Title', 'Title') + '\n')
            print(f"File '{file_path}' has been created with the specified content.")
        except Exception as e:
            print(f"Error: {e}")


prompt = input("Prompt is ''Give a seo optimized title for this picture and give 60 seo optimized trending keywords "
               "for this picture to upload adobe stock, Important result must not add extra titles only need title "
               "and keywords without use numbers and use comma separator for keywords separation and all only in "
               "english''\n Do you want to"
               "edit prompt: ")
if os.path.exists("Output/output.txt"):
    clear = input("Do you want to clear output.txt: ")
    if clear in ['y', 'Yes', 'yes', 'Y', 'YES', 'YeS', 'yeS']:
        file_path = "Output/output.txt"
        with open(file_path, 'w') as file:
            file.write('')

if prompt in ['n', 'N', 'NO', 'No', 'no', 'nO']:
    main("null")

else:
    _prompt_ = input("What is your prompt: ")
    main(_prompt_)
