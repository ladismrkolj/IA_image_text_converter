from PIL import Image
import os

def convert_and_scale(input_folder, output_folder, scale_factor, suffix):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each file in the input folder
    for filename in os.listdir(input_folder):
        filepath = os.path.join(input_folder, filename)
        output_filepath = os.path.join(output_folder, filename)

        # Process TIFF images
        if filename.lower().endswith((".tiff", ".tif")):
            with Image.open(filepath) as img:
                # Calculate new dimensions
                new_width = int(img.width / scale_factor)
                new_height = int(img.height / scale_factor)
                # Resize image
                resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                # Convert to RGB if necessary
                if resized_img.mode != 'RGB':
                    resized_img = resized_img.convert('RGB')
                # Save as JPG
                output_filename = os.path.splitext(filename)[0] + suffix + ".jpg"
                resized_img.save(os.path.join(output_folder, output_filename), quality=95)

        # Process text files
        elif filename.lower().endswith(".txt"):
            with open(filepath, 'r') as f:
                lines = f.readlines()

            # Scale numeric values
            scaled_lines = []
            first=True
            for i in range(len(lines)):

                if not lines[i].strip():
                    scaled_lines.append("")
                    continue

                if first:
                    scaled_lines.append(lines[i].strip())
                    first=False
                    continue

                current_scaled_line = []
                line = lines[i]
                split_line = line.split()
                current_scaled_line.extend(split_line[:4])
                current_scaled_line.extend([str(int(int(a) / scale_factor)) for a in split_line[4:]])
                scaled_lines.append(' '.join(current_scaled_line))
            
            output_filename = os.path.splitext(filename)[0] + suffix + ".txt"
            output_filepath = os.path.join(output_folder, output_filename)
            # Save the scaled values to a new file
            with open(output_filepath, 'w') as f:
                f.writelines(line + '\n' for line in scaled_lines)

# Example usage
input_folder = "."
output_folder = "."
scale_factor = 4  # Adjust as needed
suffix= "_s"

#input_folder = input("Enter the input folder path: ")
#output_folder = input("Enter the output folder path: ")
#scale_factor = int(input("Enter the downscale factor: "))
#suffix = input("Enter the suffix: ")


convert_and_scale(input_folder, output_folder, scale_factor, suffix)