import obspython as obs
import csv

FullScreen_Pos = {'x': 0, 'y': 0}
FullScreen_Scale = {'x': 1.5, 'y': 1.5}

Sidebyside_Camera_Pos = {'x': 1258, 'y': 229}
Sidebyside_Camera_Scale = {'x': 0.67890626192092896, 'y': 0.67916667461395264}

Sidebyside_Slides_Pos = {'x': 38, 'y': 122}
Sidebyside_Slides_Scale = {'x': 0.75208336114883423, 'y': 0.75185185670852661}


def set_transform(scene_item, pos, scale):
    vec = obs.vec2()
    vec.x, vec.y = pos['x'], pos['y']
    obs.obs_sceneitem_set_pos(scene_item, vec)
    vec.x, vec.y = scale['x'], scale['y']
    obs.obs_sceneitem_set_scale(scene_item, vec)


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

with open("/home/mohdyasir/Desktop/IndiaFoss_Live_Streaming/obsscripting/scene.csv", mode="r") as file:
    reader= csv.DictReader(file)
    all_rows = list(reader)
    all_rows.reverse()

    for row in all_rows:
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
            camera_item = obs.obs_scene_add(scene, camera_source)
            set_transform(camera_item, FullScreen_Pos, FullScreen_Scale)

            if png_file:
                settings = obs.obs_data_create()
                obs.obs_data_set_string(settings, "file", png_file)
                overlay = obs.obs_source_create("image_source", f"Overlay_{scene_name}", settings, None)
                obs.obs_scene_add(scene, overlay)
                obs.obs_source_release(overlay)
                obs.obs_data_release(settings)

        elif scene_type == "sidebyside":
            camera_item = obs.obs_scene_add(scene, camera_source)
            set_transform(camera_item, Sidebyside_Camera_Pos, Sidebyside_Camera_Scale)

            slides_item = obs.obs_scene_add(scene, slides_source)
            set_transform(slides_item, Sidebyside_Slides_Pos, Sidebyside_Slides_Scale)
            
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