import os

opj = os.path.join
ol = os.listdir

source_root = "/Dataset/ScanNet/posed_images"
save_root = "/Dataset/ScanNet/color_images_cluster"
frame_step = 5
COPY = False

os.makedirs(save_root, exist_ok=True)

for scene_id in ol(source_root):
    scene_dir = opj(source_root, scene_id)
    if not os.path.isdir(scene_dir):
        continue

    save_scene_dir = opj(save_root, scene_id)
    os.makedirs(save_scene_dir, exist_ok=True)

    frame_files = []
    for name in ol(scene_dir):
        stem, ext = os.path.splitext(name)
        if ext.lower() != '.jpg':
            continue
        if not stem.isdigit():
            continue
        frame_files.append((int(stem), name))

    frame_files.sort(key=lambda x: x[0])

    for frame_idx, filename in frame_files:
        if frame_idx % frame_step != 0:
            continue
        src = opj(scene_dir, filename)
        
        # zero pad and rename file
        width = len(os.path.splitext(filename)[0])
        new_idx = frame_idx // frame_step
        new_name = f"{new_idx:0{width}d}.jpg"
        dst = opj(save_scene_dir, new_name)
        
        # if os.path.exists(dst):
        #     continue
        if COPY:
            import shutil
            shutil.copyfile(src, dst)
        else:
            rel_src = os.path.relpath(src, start=save_scene_dir)
            os.symlink(rel_src, dst)

