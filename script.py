import obspython as obs
import csv


#Camera Source Settings  
device_id_str = "/dev/video0"
input_int = 0
pixelformat_int = 1196444237
settings = obs.obs_data_create()
obs.obs_data_set_string(settings, "device_id", device_id_str)
obs.obs_data_set_int(settings, "input", input_int)
obs.obs_data_set_int(settings, "pixelformat", pixelformat_int)
camera_source = obs.obs_source_create("v4l2_input", "Camera", settings, None)
obs.obs_data_release(settings)

#Slides Source Settings
slides_source = obs.obs_source_create("xcomposite_input", "Presentation", None, None)

with open("scene.csv", mode="r") as file:  #have to update the correct path
    reader= csv.DictReader(file)
    print("------")
    print(typereader)
    print("------")
    for row in reader:
        # print(f"{row['scene_name']} {row['scene_type']}  {row['png_file']}")
        scene_name = row['scene_name']
        scene_type = row['scene_type']
        png_file = row['png_file']
        print(scene_name, scene_type, png_file)


        scene = obs.obs_scene_create(scene_name) 

        if scene_type == "static":
            if png_file:
                settings = obs.obs_data_create()
                obs.obs_data_set_string(settings, "file", png_file)

                static_image=obs.obs_source_create("image_source", f"Img_{scene_name}", settings, None)
                obs.obs_scene_add(scene, static_image)
                obs.obs_source_release(static_image)
                obs.obs_data_release(settings)

        elif scene_type == "speakeronly":
            obs.obs_scene_add(scene, camera_source)
            if png_file:
                settings = obs.obs_data_create()
                obs.obs_data_set_string(settings, "file", png_file)
                overlay = obs.obs_source_create("image_source", f"Overlay_{scene_name}", settings, None)
                obs.obs_scene_add(scene, overlay)
                obs.obs_source_release(overlay)
                obs.obs_data_release(settings)

        elif scene_type == "sidebyside":
            obs.obs_scene_add(scene, camera_source)
            obs.obs_scene_add(scene, slides_source)
            
            if png_file:
                settings = obs.obs_data_create()
                obs.obs_data_set_string(settings, "file", png_file)
                overlay = obs.obs_source_create("image_source", f"Overlay_{scene_name}", settings, None)
                obs.obs_scene_add(scene, overlay)
                obs.obs_source_release(overlay)
                obs.obs_data_release(settings)

        obs.obs_scene_release(scene)



obs.obs_source_release(camera_source)
obs.obs_source_release(slides_source)
