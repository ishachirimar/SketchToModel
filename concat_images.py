from PIL import Image
import os
import shutil
import splitfolders

# normal_directory = 'TrainingData_220425/NormalMap'
# sketch_directory = 'TrainingData_220425/Sketches'

# i = 0
# for (sketch_file, normal_file) in zip(sorted(os.listdir(sketch_directory)), sorted(os.listdir(normal_directory))):
#     sketch = Image.open(sketch_directory + "/" + sketch_file)
#     normal = Image.open(normal_directory + "/" + normal_file)
#     filename_concat = sketch_file[:sketch_file.find(
#         "_")] + "_CONCAT_" + sketch_file[sketch_file.find(".")-2:sketch_file.find(".")] + ".png"
#    # print(filename_concat)
#     new_image = Image.new('RGB', (512, 256))
#     new_image.paste(sketch, (0, 0))
#     new_image.paste(normal, (256, 0))
#     new_image.save("TrainingData_220425/train/" + filename_concat, "PNG")
#    # new_image.show()


splitfolders.ratio('TrainingData_220425/training',
                   output="TrainingData_220425", seed=1337, ratio=(.8, 0.1, 0.1))
